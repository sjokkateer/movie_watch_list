import os 
import requests


class MoviesDAO:
    class OmdbApi:
        ENDPOINT = 'http://www.omdbapi.com/'
        KEY = os.getenv('OMDB_KEY')

    @classmethod
    def get_movies(cls, user):
        movies = []
        
        for favorite_movie in user.favorite_movies.all():
            movies.append(cls.get_movie(favorite_movie.imdb_id, query_search_param='i').json())

        return movies

    @classmethod
    def get_movie(cls, search_text: str, query_search_param: str = 't'):
        url = cls.OmdbApi.ENDPOINT

        return requests.get(
            url,
            params={
                query_search_param: search_text,
                'apikey': cls.OmdbApi.KEY
            },
        )

    @classmethod
    def get_appropriate_context(cls, response, search_title: str) -> dict:
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
