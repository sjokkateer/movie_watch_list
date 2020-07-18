from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesHomeView.as_view(), name='index'),
    path('search', views.search, name='search'),
    path('favorite', views.WatchListView.as_view(), name='favorite'),
    path('remove', views.RemoveRedirectView.as_view(), name='remove'),
]