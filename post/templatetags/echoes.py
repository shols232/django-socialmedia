from django import template
from post.models import Content

register = template.Library()

@register.filter
def post_echoes(value):
    return Content.objects.filter(parent=value).count()