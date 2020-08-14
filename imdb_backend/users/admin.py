from django.contrib import admin

# Register your models here.
from imdb_backend.users.models import User


class UserAdmin(admin.ModelAdmin):
	model = User
	list_display = ('username', 'email', 'is_admin', 'is_deleted')

	
admin.site.register(User, UserAdmin)
