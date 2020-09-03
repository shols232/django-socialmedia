from django.contrib import admin
from .models import Messages, Chat, Contact

admin.site.register(Messages)

admin.site.register(Contact)

class ChatAdmin(admin.ModelAdmin):
    list_display = ['user_one', 'user_two', 'updated']

admin.site.register(Chat, ChatAdmin)
