# from django.core.mail import send_mail
from . import models
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from pathlib import Path

import json
import os
import requests


class OmdbApi:
    ENDPOINT = 'http://www.omdbapi.com/'
    KEY = os.getenv('OMDB_KEY')


class MoviesHomeView(ListView):
    template_name = 'movies/index.html'
    context_object_name = 'watch_listed_movies'
    
    def get_queryset(self):
        watch_listed_movies = models.Movie.objects \
                .annotate(total_times_listed=Count('favorite_by')) \
                .values('imdb_id', 'total_times_listed') \
                .filter(total_times_listed__gt=0) \
                .order_by('-total_times_listed', 'imdb_id')

        movies = []
        
        for watch_listed_movie in watch_listed_movies:
            movie = get_movie(watch_listed_movie['imdb_id'], 'i').json()
            movie['total_times_listed'] = watch_listed_movie['total_times_listed']
            movies.append(movie)

        return movies


# Can become generic template view
def index(request):
    return render(request, 'movies/index.html')

def search(request):
    context = {}
    title = request.GET.get('title', '')
    
    if title != '':
        response = get_movie(title)
        context = get_appropriate_context(response, title)

    return render(request, 'movies/search.html', context)

def get_movie(search_text, query_search_param='t'):
    url = OmdbApi.ENDPOINT

    return requests.get(
        url,
        params={
            query_search_param: search_text,
            'apikey': OmdbApi.KEY
        },
    )

def get_appropriate_context(response, search_title):
    context = {}
    OK = 200

    if response.status_code == OK:
        # Can still return an error in the json body, for ex if title not found.
        json_content = response.json()

    # if json_content is empty dictionary it evaluates to false
    if json_content and 'Error' not in json_content:
        context['movie'] = json_content
    else:
        # Maybe log the issue in the near future
        context['search_title'] = search_title

    return context

# Should become a more customized list view to handle pagination etc.
@login_required
def favorite(request):
    # List view would also remove this level of indentation
    if request.method == 'POST':
        imdb_id = request.POST.get('id', False)
        title = request.POST.get('title', False)

        if (imdb_id and imdb_id != '') and (title and title != ''):
            # Should ensure title is not an empty string
            movie = models.Movie.objects.get_or_create(imdb_id=imdb_id, title=title)[0]
            user = request.user
            user.favorite_movies.add(movie.id)

        return HttpResponseRedirect(reverse('movies:favorite'))

    # In case of a get, we should obtain all movies from the API.
    # Could've cached it in the session as one first step for efficiency.
    # Otherwise with a few movies, refreshing this page will exceed our 1000 daily requests.
    # But preferably later on I'll look into for ex a caching DB like Redis.
    context = {'watch_list': get_movies(request.user)}

    return render(request, 'movies/favorite.html', context=context)

def get_movies(user):
    movies = []
    
    for favorite_movie in user.favorite_movies.all():
        movies.append(get_movie(favorite_movie.imdb_id, query_search_param='i').json())

    return movies

def remove(request):
    id = request.POST.get('id', False)

    if request.method == 'POST' and id and id != '':
        try:
            movie = models.Movie.objects.get(imdb_id=id)
            request.user.favorite_movies.remove(movie.id)
        except ObjectDoesNotExist:
            # Log error
            pass
    
    return HttpResponseRedirect(reverse('movies:favorite'))
