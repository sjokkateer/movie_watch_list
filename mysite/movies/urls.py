from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('favorite', views.favorite, name='favorite'),
    path('remove', views.remove, name='remove'),
]