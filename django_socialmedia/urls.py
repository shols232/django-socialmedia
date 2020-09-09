"""django_socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from account import views as user_view
from post import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.content_list, name = "content"),
    #path('', user_view.home, name = 'home'),
    path('chat/', include('chatapp.urls', namespace='chatapp')),
    path('account/', include('account.urls')),
    path('post/', include('post.urls')),
    path('emoji/', include('emoji.urls')),
   # path('google/', include('allauth.urls'))
    path('social-auth/',include('social_django.urls', namespace='social')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

