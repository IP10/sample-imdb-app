from django.contrib import admin

# Register your models here.
from imdb_backend.movies.models import Movie, Genre


class MovieAdmin(admin.ModelAdmin):
	model = Movie
	list_display = ('name', 'director', 'popularity', 'imdb_score')


class GenreAdmin(admin.ModelAdmin):
	model = Genre
	list_display = ('name',)
	
	
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
