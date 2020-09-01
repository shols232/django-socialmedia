from . import views as user_views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth login and register
    path('register/', user_views.register, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout"),

     path('activation_mail/', user_views.send_mail, name = "mail_sent"),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
   
    # Password Reset
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name='reset_password'),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_change.html"),name='password_reset_confirm'),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_success.html"),
    name='password_reset_complete'),

    # Profile
    path('profile/<int:id>', user_views.profile, name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/follow_unfollow/', user_views.follow_action)
]