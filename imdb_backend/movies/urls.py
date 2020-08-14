from django.urls import path

from imdb_backend.movies import views

urlpatterns = [
	path('', views.MoviesView.as_view(), name='movies-list'),
	path('<int:id>/', views.MovieDetailView.as_view(), name='movie-detail'),
	path('genres/', views.GenreListView.as_view(), name='genre-list'),
	path('directors/', views.DirectorListView.as_view(), name='director-list'),
    ]