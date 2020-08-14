import json
import os

from django.core.management.base import BaseCommand
from oauth2_provider.admin import Application

from imdb_backend.movies.models import Genre, Movie
from imdb_backend.settings import BASE_DIR
from imdb_backend.users.models import User


class Command(BaseCommand):
	base_path = BASE_DIR
	setup_path = os.path.abspath(os.path.dirname(__file__)) + '/setup/'
	help = 'Builds the IMDB pre-defined data\n' \
	       'Process List:\n\r' \
	       '1 - setup_profile_images\n\r' \
	       '2 - setup_admin_user\n\r' \
	       '3 - self.setup_oauth_application'
	
	def setup_movies(self):
		filename = self.setup_path + 'imdb.json'
		with open(filename) as f:
			data = json.load(f)
		for movie in data:
			genres = movie['genre']
			genre_ids = []
			for genre in genres:
				genre = genre.strip()
				genre_exits = Genre.objects.only('name').filter(name=genre).exists()
				if not genre_exits:
					new_genre = Genre(name=genre)
					new_genre.save()
					genre_ids.append(new_genre)
				else:
					old_genre = Genre.objects.get(name=genre)
					genre_ids.append(old_genre)
			new_movie = Movie(
				name=movie['name'],
				director=movie['director'],
				imdb_score=movie['imdb_score'],
				popularity=movie['99popularity']
			)
			
			new_movie.save()
			new_movie.genres.set(genre_ids)
			new_movie.save()
	
	def setup_admin_user(self):
		user = User(username="admin",
		            first_name="admin",
		            last_name="123",
		            email="admin@gmail.com",
		            is_admin=True,
		            is_superuser=True,
		            is_staff=True)
		user.save()
		user.set_password('admin')
		user.save()
	
	def setup_oauth_application(self):
		CLIENT_CONFIDENTIAL = "confidential"
		GRANT_PASSWORD = "password"
		
		Application(
			client_id=os.getenv('CLIENT_ID'),
			client_type=CLIENT_CONFIDENTIAL,
			client_secret=os.getenv('CLIENT_SECRET'),
			authorization_grant_type=GRANT_PASSWORD,
			name='Application'
		).save()
	
	def add_arguments(self, parser):
		parser.add_argument('-o', '--only', nargs='+', type=int, help="Only run the particular process")
		parser.add_argument('-n', '--not', nargs="+", type=int, help="Not include the the particular process")
	
	def handle(self, *args, **options):
		BUILD_DATA = {
			1: self.setup_movies,
			2: self.setup_admin_user,
			3: self.setup_oauth_application
		}
		
		if options['only']:
			print("Running for only {} \n".format(options['only']))
			for process_id in options['only']:
				print("Started '{} - {}' process".format(process_id, BUILD_DATA[process_id].__name__))
				try:
					BUILD_DATA[process_id]()
					print("Completed '{} - {}' process".format(process_id, BUILD_DATA[process_id].__name__))
				except Exception as e:
					print(
						"Error Occurred in '{} - {}' process - {}".format(process_id, BUILD_DATA[process_id].__name__,
						                                                  e))
				print("\n")
		else:
			for key, process in BUILD_DATA.items():
				
				print("Started '{} - {}' process....".format(key, process.__name__))
				try:
					process()
					print("Completed '{} - {}' process.".format(key, process.__name__))
				except Exception as e:
					print("Error Occurred in '{} - {}' process - {}".format(key, process.__name__, str(e)))
				print('\n')
		print('Completed Backend Setup')
