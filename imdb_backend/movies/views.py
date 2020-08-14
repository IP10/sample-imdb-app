# Create your views here.
from django.core.paginator import Paginator
from rest_framework import views
from rest_framework.permissions import AllowAny

from imdb_backend.constant import DEFAULT_PAGE_SIZE, DEFAULT_PAGE_NUMBER
from imdb_backend.movies import serializers
from imdb_backend.movies.models import Movie, Genre
from imdb_backend.permissions import IsAuthenticated
from imdb_backend.utils import Utils
from imdb_backend.validators.ErrorMessage import ErrorMessage


class MoviesView(views.APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request):
		try:
			movies = Movie.objects.all()
			sort_key = request.GET.get('sort_key', None)
			sort_by = request.GET.get('sort_by', 'asc')
			filter_by = request.GET.get('filter_by', None)
			filter_by_key = request.GET.get('filter_key', None)
			search_key = request.GET.get('search_key', None)
			if search_key:
				movies = movies.filter(name__istartswith=search_key).all()
			if filter_by and filter_by_key:
				if filter_by == 'genre':
					movies = movies.filter(genres__name__in=[filter_by_key]).all()
				elif filter_by == 'director':
					movies = movies.filter(director=filter_by_key).all()
				else:
					movies = movies
			if sort_key is not None:
				if sort_key == "POPULARITY":
					sort_column = "popularity" if sort_by == 'asc' else "-popularity"
					movies = movies.order_by(sort_column)
				elif sort_key == "IMDB_SCORE":
					sort_column = "imdb_score" if sort_by == 'asc' else "-imdb_score"
					movies = movies.order_by(sort_column)
				else:
					sort_column = "name" if sort_by == 'asc' else "-name"
					movies = movies.order_by(sort_column)
			else:
				sort_column = "name" if sort_by == 'asc' else "-name"
				movies = movies.order_by(sort_column)
			page_size = int(request.GET.get('page_size', DEFAULT_PAGE_SIZE))
			page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))
			if isinstance(page_size, str):
				page_size = int(page_size)
			
			paginator = Paginator(movies, per_page=page_size)
			page_queryset = paginator.page(page if page <= paginator.num_pages else DEFAULT_PAGE_NUMBER)
			movie_serializer = serializers.MoviesListSerializer(page_queryset, many=True)
			result = {'movies': movie_serializer.data, 'page': {'current': page, 'total': paginator.num_pages}}
			return Utils.dispatch_success(request, result)
		except Exception as e:
			print(e, ErrorMessage.INTERNAL_SERVER_ERROR)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def post(self, request):
		try:
			data = request.data
			user = request.user
			if not user.is_admin:
				return Utils.dispatch_failure(request, ErrorMessage.UNAUTHORIZED_ACCESS)
			req_genres = data.get('genres', [])
			genres = Genre.check_exists_or_create(req_genres)
			serializer = serializers.CreateMovieSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				movie = Movie.objects.get(name=data['name'].strip())
				movie.genres.set(genres)
				movie.save()
				return Utils.dispatch_success(request, {'movie': serializer.validated_data})
			else:
				return Utils.dispatch_failure(request, ErrorMessage.VALIDATION_ERROR, serializer.errors)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class MovieDetailView(views.APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request, id):
		try:
			movie = Movie.objects.get(id=id)
			movie_serializer = serializers.GetMovieDetailSerializer(movie)
			result = {'movie': movie_serializer.data}
			return Utils.dispatch_success(request, result)
		except Movie.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def delete(self, request, id):
		try:
			user = request.user
			if not user.is_admin:
				return Utils.dispatch_failure(request, ErrorMessage.UNAUTHORIZED_ACCESS)
			movie = Movie.objects.get(id=id)
			movie.delete()
			return Utils.dispatch_success(request, {})
		except Movie.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def put(self, request, id):
		try:
			user = request.user
			if not user.is_admin:
				return Utils.dispatch_failure(request, ErrorMessage.UNAUTHORIZED_ACCESS)
			movie = Movie.objects.get(id=id)
			movie_data = request.data.get('movie', None)
			if movie_data is None:
				return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
			movie_serializer = serializers.UpdateMovieSerializer(movie, data=movie_data, partial=True)
			if movie_serializer.is_valid():
				movie_serializer.save()
				result = {'movie': movie_serializer.data}
				return Utils.dispatch_success(request, result)
			else:
				return Utils.dispatch_failure(request, ErrorMessage.VALIDATION_ERROR, movie_serializer.errors)
		
		except Movie.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class GenreListView(views.APIView):
	permission_classes = (AllowAny,)
	
	def get(self, request):
		try:
			genres = Genre.objects.all()
			genre_serializer = serializers.GenreListSerializer(genres, many=True)
			result = {'genres': genre_serializer.data}
			return Utils.dispatch_success(request, result)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class DirectorListView(views.APIView):
	permission_classes = (AllowAny,)
	
	def get(self, request):
		try:
			directors = Movie.objects.values_list("director", flat=True).distinct().order_by('director').all()
			result = {'directors': list(directors)}
			return Utils.dispatch_success(request, result)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
