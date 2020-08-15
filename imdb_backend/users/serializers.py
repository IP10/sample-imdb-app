import base64

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from imdb_backend.users.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email','is_admin')


class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True)
	
	def validate(self, attrs):
		try:
			username = attrs.get('username')
			password = base64.b64decode(attrs.get('password')).decode('ascii')
			
			user = authenticate(request=self.context.get('request'), username=username, password=password)
			if not user or user.is_deleted:
				msg = 'Unable to login with required credentials'
				raise ValidationError(msg)
			return user
		except Exception as e:
			print(e)
			msg = 'Unable to login with required credentials'
			raise ValidationError(msg)
	
	class Meta:
		model = User
		fields = ('username', 'password')


class CreateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email')
	
	def validate(self, data):
		
		if len(data.get('first_name', '').strip()) <= 3:
			raise serializers.ValidationError({'first_name': "should consists of 4 characters"})
		if len(data.get('last_name', '').strip()) <= 3:
			raise serializers.ValidationError({'last_name': "should consists of 4 characters"})
		if len(data.get('username', '').strip()) <= 3:
			raise serializers.ValidationError({'username': "should consists of 4 characters"})
		if len(data.get('email', '').strip()) <= 3:
			raise serializers.ValidationError({'username': "should consists of 4 characters"})
		if len(data.get('email', '').strip()) <= 3:
			raise serializers.ValidationError({'username': "should consists of 4 characters"})
		if self.check_user_name_exists(data.get('username')):
			raise serializers.ValidationError({'username': "should be unique"})
		if self.check_email_exists(data.get('email')):
			raise serializers.ValidationError({'email': "should be unique"})
		return data
	
	def check_user_name_exists(self, username):
		
		return User.objects.filter(username__iexact=username).exists()
	
	def check_email_exists(self, username):
		
		return User.objects.filter(email__iexact=username).exists()
