# Create your views here.
import base64

from django.contrib.auth import logout
from django.core.paginator import Paginator
from rest_framework import views
from rest_framework.permissions import AllowAny

from imdb_backend.constant import DEFAULT_PAGE_SIZE, DEFAULT_PAGE_NUMBER
from imdb_backend.permissions import IsAdmin, IsAuthenticated
from imdb_backend.users import serializers
from imdb_backend.users.models import User
from imdb_backend.utils import Utils
from imdb_backend.validators.ErrorMessage import ErrorMessage


class UsersListView(views.APIView):
	permission_classes = (IsAdmin,)
	
	def post(self, request):
		try:
			data = request.data
			user = request.user
			if not user.is_admin:
				return Utils.dispatch_failure(request, ErrorMessage.UNAUTHORIZED_ACCESS)
			if len(data.get('password', '')) <= 4:
				return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
			try:
				password_decoded = base64.b64decode(data.get('password')).decode('ascii')
			except:
				return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
			
			serializer = serializers.CreateUserSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				user = User.objects.get(email=data['email'].strip())
				user.set_password(password_decoded)
				return Utils.dispatch_success(request, {'user': serializer.validated_data})
			else:
				return Utils.dispatch_failure(request, ErrorMessage.VALIDATION_ERROR, serializer.errors)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def get(self, request):
		try:
			users = User.objects.filter(is_deleted=False).order_by('username')
			page_size = int(request.GET.get('page_size', DEFAULT_PAGE_SIZE))
			page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))
			if isinstance(page_size, str):
				page_size = int(page_size)
			paginator = Paginator(users, per_page=page_size)
			page_queryset = paginator.page(page if page <= paginator.num_pages else DEFAULT_PAGE_NUMBER)
			user_serializer = serializers.UserSerializer(page_queryset, many=True)
			result = {'users': user_serializer.data, 'page': {'current': page, 'total': paginator.num_pages}}
			
			return Utils.dispatch_success(request, result)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class UserDetailView(views.APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request, id):
		try:
			user = User.objects.get(id=id)
			user_serializer = serializers.UserSerializer(user)
			result = {'user': user_serializer.data}
			return Utils.dispatch_success(request, result)
		except User.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def delete(self, request, id):
		try:
			user = User.objects.get(id=id)
			user.is_deleted = True
			user.save()
			return Utils.dispatch_success(request, {})
		except User.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
	
	def put(self, request, id):
		try:
			user = User.objects.get(id=id)
			user_data = request.data.get('user', None)
			if user_data is None:
				return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
			user_serializer = serializers.UpdateUserSerializer(user, data=user_data, partial=True)
			if user_serializer.is_valid():
				user_serializer.save()
				result = {'user': user_serializer.data}
				return Utils.dispatch_success(request, result)
			else:
				return Utils.dispatch_failure(request, ErrorMessage.VALIDATION_ERROR, user_serializer.errors)
		
		except User.DoesNotExist:
			return Utils.dispatch_failure(request, ErrorMessage.INVALID_PARAMETERS)
		
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class LoginView(views.APIView):
	permission_classes = (AllowAny,)
	
	def post(self, request):
		try:
			serializer = serializers.LoginSerializer(data=request.data)
			if serializer.is_valid():
				data = {}
				user = serializer.validated_data
				user_data = serializers.UserSerializer(user).data
				token = Utils.create_access(user)
				data['token'] = token
				data['user'] = user_data
				return Utils.dispatch_success(request, data)
			else:
				return Utils.dispatch_failure(request, ErrorMessage.INVALID_CREDENTIALS)
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)


class LogOutView(views.APIView):
	def delete(self, request):
		try:
			logout(request)
			return Utils.dispatch_success(request,{})
		except Exception as e:
			print(e)
			return Utils.dispatch_failure(request, ErrorMessage.INTERNAL_SERVER_ERROR)
