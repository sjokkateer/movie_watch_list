# from django.core.mail import send_mail
from . import models
from .daos import MoviesDAO
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.base import RedirectView, TemplateView


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
            movie = MoviesDAO.get_movie(watch_listed_movie['imdb_id'], 'i').json()
            movie['total_times_listed'] = watch_listed_movie['total_times_listed']
            movies.append(movie)

        return movies


class SearchView(TemplateView):
    template_name = 'movies/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        title = self.request.GET.get('title', '')
        response = MoviesDAO.get_movie(title)
        return {**context, **MoviesDAO.get_appropriate_context(response, title)}


@method_decorator(login_required, name='dispatch')
class WatchListView(ListView):
    template_name = 'movies/favorite.html'
    context_object_name = 'watch_listed'

    def post(self, request, *args, **kwargs):
        imdb_id = request.POST.get('id', False)
        title = request.POST.get('title', False)

        if (imdb_id and imdb_id != '') and (title and title != ''):
            movie = models.Movie.objects.get_or_create(imdb_id=imdb_id, title=title)[0]
            user = request.user
            user.favorite_movies.add(movie.id)

        return redirect('movies:favorite')

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), id=self.request.user.id)
        
        return MoviesDAO.get_movies(user)


@method_decorator(login_required, name='dispatch')
class RemoveRedirectView(RedirectView):
    pattern_name = 'movies:favorite'

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', False)
        
        if id and id != '':
            movie = get_object_or_404(models.Movie, imdb_id=id)
            request.user.favorite_movies.remove(movie.id)

        return redirect(self.pattern_name)
