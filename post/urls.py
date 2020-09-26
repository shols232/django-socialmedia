from . import views as user_views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
   # path('test', user_views.ContentCreateListView.as_view(), name = "list"),
   # path('create/', user_views.ContentCreateView.as_view(), name = "create"),
    path('comment/<int:content_id>', user_views.comment_post, name = "comment"),
    path('react', user_views.like_post, name='react')
]