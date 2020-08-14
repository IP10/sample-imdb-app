from datetime import datetime, timedelta

from oauth2_provider.admin import Application, AccessToken, RefreshToken
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from requests import request as req
from rest_framework import status
from rest_framework.response import Response
from imdb_backend.validators.ErrorMessage import ErrorMessage


class Utils:
	@staticmethod
	def dispatch_success(request, response, code=status.HTTP_200_OK, **kwargs):
		"""
		This method for dispatch the success response
		:param request:
		:param response:
		:param code:
		:return:
		"""
		if isinstance(response, list) or isinstance(response, dict):
			data = {'status': 'success', 'result': response, **kwargs}
		else:
			data = []
		return Response(data=data, status=code)
	
	@staticmethod
	def dispatch_failure(request, identifier, response=None, code=status.HTTP_400_BAD_REQUEST):
		"""
		This method for dispatch the failure response
		:param request:
		:param identifier:
		:param response:
		:param code:
		:return:
		"""
		error_code = identifier['code']
		error_message = identifier['message']
		
		errors = {}
		if response is None:
			errors['status'] = 'failure'
			errors['code'] = error_code
			errors['message'] = error_message
		else:
			errors['status'] = 'failure'
			errors['code'] = error_code
			errors['message'] = error_message
			errors['errors'] = response
		
		return Response(data=errors, status=code)
	
	@staticmethod
	def create_access(user):
		"""
			:param user: user object
			:return: json object
		"""
		expire_seconds = 36000
		scopes = 'read write'
		
		application = Application.objects.get(name="Application")
		expires = datetime.now() + timedelta(seconds=expire_seconds)
		access_token = AccessToken.objects.create(
			user=user,
			application=application,
			token=random_token_generator(req),
			expires=expires,
			scope=scopes)
		
		refresh_token = RefreshToken.objects.create(
			user=user,
			token=random_token_generator(req),
			access_token=access_token,
			application=application)
		token = {
			'access_token': access_token.token,
			'token_type': 'Bearer',
			'expires_in': expire_seconds,
			'refresh_token': refresh_token.token,
			'scope': scopes}
		return token
