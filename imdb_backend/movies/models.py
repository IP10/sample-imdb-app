from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Genre(BaseModel):
	name = models.CharField(null=False, blank=False, max_length=20)
	
	def __str__(self):
		return self.name
	
	@staticmethod
	def check_exists_or_create(new_genres):
		genres = []
		for item in new_genres:
			genre = item.strip()
			genre_exits = Genre.objects.only('name').filter(name=genre).exists()
			if not genre_exits:
				new_genre = Genre(name=genre)
				new_genre.save()
				genres.append(new_genre)
			else:
				old_genre = Genre.objects.get(name=genre)
				genres.append(old_genre)
				
		return genres


class Movie(BaseModel):
	name = models.CharField(null=False, blank=False, max_length=100)
	popularity = models.FloatField(default=0.0)
	imdb_score = models.FloatField(default=0.0)
	director = models.CharField(max_length=100)
	genres = models.ManyToManyField(Genre)
	
	def __str__(self):
		return self.name


