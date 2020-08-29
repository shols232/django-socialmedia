from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:id>', views.profile, name='profile'),
    path('follow_unfollow/', views.follow_action)
]
