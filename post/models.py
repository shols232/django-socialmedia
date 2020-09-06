from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Profile
# Create your models here.


class Content(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    image_content = models.ImageField(upload_to='content/', blank=True, null=True, default = None)

    # @property
    # def format_time(self):
    #     time = Content.posted
       
    #     now = timezone.now
    #     posting = now - time
    #     print(time,now)
    #     print(posting)
    #     return posting

    def __str__(self):
        return self.content[:10]