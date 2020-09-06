from django.contrib import admin
from .models import Profile, UserFollowing, Notifications



admin.site.register(Profile)
admin.site.register(UserFollowing)
admin.site.register(Notifications)
# Register your models here.
