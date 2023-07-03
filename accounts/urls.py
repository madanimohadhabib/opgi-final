from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
	path('login/', views.loginPage, name="login"),  

	path('', views.abcd, name="abcd"),  
	path('logout/', views.logoutUser, name="logout"),
	path('profile/', views.profile, name="profile"),
  


]