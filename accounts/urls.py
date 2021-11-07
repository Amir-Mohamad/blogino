from django.urls import path
from . import views

app_name = 'accounts'




urlpatterns = [
	path('', views.Profile.as_view(), name='profile'),
	path('register/', views.UserRegister, name='register'),
	path('verify/', views.VerifyCode, name='verify'),
	path('login/', views.UserLogin.as_view(), name='login'),
	path('logout/', views.UserLogout.as_view(), name='logout'),
	path('password_change/', views.PasswordChange.as_view(), name='password_change'),
]
