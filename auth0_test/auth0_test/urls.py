"""auth0_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from smauth import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('api_test/', views.api_test),
    path('token/', views.create_token),
    path('smbot/', views.smbot_api),
    path('admin/', admin.site.urls)
]
