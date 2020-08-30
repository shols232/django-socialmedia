from . import views as user_views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_views.register, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout"),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='reset_complete'),
    path('profile/<int:id>', user_views.profile, name='profile'),
    path('follow_unfollow/', user_views.follow_action)
]