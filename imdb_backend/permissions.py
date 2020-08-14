from rest_framework import permissions, status
from rest_framework.exceptions import APIException

from imdb_backend.validators.ErrorMessage import ErrorMessage


class UnauthorizedAccess(APIException):
	status_code = status.HTTP_401_UNAUTHORIZED
	error = ErrorMessage.UNAUTHORIZED_ACCESS
	default_detail = {"message": error['message'], "status": "failed",
	                  "code": error['code']}


class IsAdmin(permissions.IsAuthenticated):
	
	def has_permission(self, request, view):
		if not request.user.is_authenticated or not request.user.is_admin:
			raise UnauthorizedAccess
		return True


class IsAuthenticated(permissions.IsAuthenticated):
	
	def has_permission(self, request, view):
		if not request.user.is_authenticated:
			raise UnauthorizedAccess
		return True
