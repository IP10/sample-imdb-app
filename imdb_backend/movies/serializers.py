from rest_framework import serializers

from imdb_backend.movies.models import Movie, Genre


class GenreListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
	
	def to_representation(self, obj):
		return obj.name


class MoviesListSerializer(serializers.ModelSerializer):
	genres = serializers.SerializerMethodField()
	
	class Meta:
		model = Movie
		fields = ('id', 'name', 'popularity', 'imdb_score', 'genres', 'director')
	
	def get_genres(self, obj):
		return GenreListSerializer(obj.genres.all(), many=True).data


class GetMovieDetailSerializer(serializers.ModelSerializer):
	genres = serializers.SerializerMethodField()
	
	class Meta:
		model = Movie
		fields = ('id', 'name', 'popularity', 'imdb_score', 'genres', 'director')
	
	def get_genres(self, obj):
		return GenreListSerializer(obj.genres.all(), many=True).data


class UpdateMovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('name', 'popularity', 'imdb_score')


class CreateMovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('name', 'popularity', 'imdb_score', 'director')
	
	def validate(self, data):
		if len(data.get('name', '').strip()) <= 1:
			raise serializers.ValidationError({'name': "should not be empty"})
		if len(data.get('director', '').strip()) == 0:
			raise serializers.ValidationError({'director': "should not be empty"})
		return data
