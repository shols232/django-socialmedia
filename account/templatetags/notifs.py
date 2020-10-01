from django import template
from account.models import Notifications

register = template.Library()

@register.filter
def unread_notifs(value):
    return Notifications.objects.filter(to_user=value).filter(read=False).count()