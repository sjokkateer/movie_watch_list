# from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import os
import requests

class OmdbApi:
    ENDPOINT = 'http://www.omdbapi.com/'
    KEY = os.getenv('OMDB_KEY')


def index(request):
    return render(request, 'movies/index.html')


def search(request):
    context = {}

    if request.method == 'POST':
        context['movie'] = mock_response()

        # search_title = request.POST.get('title')
        # url = OmdbApi.ENDPOINT

        # response = requests.get(
        #     url,
        #     params={
        #         't': search_title,
        #         'apikey': OmdbApi.KEY
        #     },
        # )

        # # 200 == OK
        # if response.status_code == 200:
        #     context['movie'] = response.json()
        # # So in case this will be made asynchronously json responses should be returned.
        # else:
        #     context['search_title'] = search_title
    
    return render(request, 'movies/search.html', context=context)

    # on post (which will be asynchronous)
    # we will return a json response
    # containing all the found movies and images

def mock_response():
    return {
    "Title": "Terrifier",
    "Year": "2016",
    "Rated": "Unrated",
    "Released": "15 Mar 2018",
    "Runtime": "82 min",
    "Genre": "Horror, Thriller",
    "Director": "Damien Leone",
    "Writer": "Damien Leone",
    "Actors": "Jenna Kanell, Samantha Scaffidi, David Howard Thornton, Catherine Corcoran",
    "Plot": "On Halloween night, Tara Heyes finds herself as the obsession of a sadistic murderer known as Art the Clown.",
    "Language": "English",
    "Country": "USA",
    "Awards": "1 win & 5 nominations.",
    "Poster": "https://m.media-amazon.com/images/M/MV5BYmMxNzA0OTUtOTJiOS00NTc4LWJmNTItMGM3OWE0N2Y0NjhjXkEyXkFqcGdeQXVyMTg5NjU4NjE@._V1_SX300.jpg",
    "Ratings": [
        {
            "Source": "Internet Movie Database",
            "Value": "5.6/10"
        },
        {
            "Source": "Rotten Tomatoes",
            "Value": "64%"
        }
    ],
    "Metascore": "N/A",
    "imdbRating": "5.6",
    "imdbVotes": "12,389",
    "imdbID": "tt4281724",
    "Type": "movie",
    "DVD": "27 Mar 2018",
    "BoxOffice": "N/A",
    "Production": "Epic Pictures",
    "Website": "N/A",
    "Response": "True"
}
