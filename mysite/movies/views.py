# from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
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

# Should become a listview handling both post and get requests
@login_required
def favorite(request):
    WATCH_LIST = 'watch_list'
    context = {}
    
    watch_list = request.session.get(WATCH_LIST, [])
    
    if request.method == 'POST':
        # API request is now made twice, should look into it later to cache or something.
        id = request.POST['id']
        movie = get_movie(search_text=id, query_search_param='i').json()
        watch_list.append(movie)

        request.session[WATCH_LIST] = watch_list
        return HttpResponseRedirect(reverse('movies:favorite'))

    context[WATCH_LIST] = watch_list

    return render(request, 'movies/favorite.html', context=context)
