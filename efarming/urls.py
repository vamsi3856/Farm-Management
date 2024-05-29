from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/',include('accounts.urls')),
    path('orders/',include('orders.urls')),
]
