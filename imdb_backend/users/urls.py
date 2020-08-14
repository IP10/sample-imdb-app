from django.urls import path

from imdb_backend.users import views

urlpatterns = [
	path('', views.UsersListView.as_view(), name='users-list'),
	path('<int:id>/', views.UserDetailView.as_view(), name='users-detail'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogOutView.as_view(), name='logout')
]
