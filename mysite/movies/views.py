# from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pathlib import Path

import json
import os
import requests


class OmdbApi:
    ENDPOINT = 'http://www.omdbapi.com/'
    KEY = os.getenv('OMDB_KEY')


def index(request):
    return render(request, 'movies/index.html')

def search(request):
    if request.method == 'POST':
        request_handler = post_search
    else:
        request_handler = get_search

    return request_handler(request)
    
def post_search(request):
    title = request.POST.get('title')
    response = search_by_title(title)
    context = get_appropriate_context(response, title)

    return render(request, 'movies/search.html', context)

def search_by_title(search_title):
    if settings.DEBUG:
        response = get_mock_response()
    else:
        response = get_movie(search_title)

    return response

def get_mock_response():
    path = Path(__file__)
    parent_dir = path.parent
    path_to_mock_response_file = 'mock_responses/movie.json'

    with open(f'{parent_dir}/{path_to_mock_response_file}') as f:
        return json.load(f)

def get_movie(search_title):
    url = OmdbApi.ENDPOINT

    return requests.get(
        url,
        params={
            't': search_title,
            'apikey': OmdbApi.KEY
        },
    )

def get_appropriate_context(response, search_title):
    context = {}
    json_content = {}

    if settings.DEBUG:
        json_content = response
    else:
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

def get_search(request):
    return render(request, 'movies/search.html', context={})

def favorite(request):
    WATCH_LIST = 'watch_list'
    context = {}
    
    if WATCH_LIST not in request.session:
        request.session[WATCH_LIST] = []
    
    if request.method == 'POST':
        # could obtain the movie from the API or from a caching service
        # id = request.POST['id']
        request.session[WATCH_LIST].append(get_mock_response())

    context[WATCH_LIST] = request.session[WATCH_LIST]

    return render(request, 'movies/favorite.html', context=context)
