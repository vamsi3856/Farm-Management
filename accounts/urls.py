from django.contrib import admin
from .views import *
from django.urls import path

urlpatterns = [

    path('login/' , login_attempt , name="login"),
    path('register/' , register , name="register"),
    path('login-otp/', login_otp , name="login_otp"),
    path('register-otp/', register_otp , name="register_otp"),
    path('logout/',logout,name='logout'),
    
]