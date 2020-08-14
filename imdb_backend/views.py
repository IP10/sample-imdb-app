from rest_framework import views
from rest_framework.permissions import AllowAny

from imdb_backend.utils import Utils
from imdb_backend.validators.ErrorMessage import ErrorMessage


class HealthCheckView(views.APIView):
	permission_classes = (AllowAny,)
	
	def get(self, request):
		try:
			print("Success")
			return Utils.dispatch_success(request, {})
		except Exception as e:
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
