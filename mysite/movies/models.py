from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    # imdb_id example: tt4281724
    imdb_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    favorite_by = models.ManyToManyField(User, related_name='favorite_movies')

    def __str__(self):
        return f'({self.imdb_id}) {self.title}'
