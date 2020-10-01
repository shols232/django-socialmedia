from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Profile

# Create your models here.


class Content(models.Model):
    parent = models.ForeignKey('self', related_name='echoes', null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User, related_name="content", on_delete=models.CASCADE)
    posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='my_likes')
    loves = models.ManyToManyField(User, related_name="my_loves")
    image_content = models.ImageField(upload_to='content/', blank=True, null=True, default = None)


    @property
    def is_echo(self):
        return self.parent != None

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

    
# Comment threading model

class Comment(models.Model):
    post = models.ForeignKey(Content,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True,related_name='replies',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True,null=True)
    image_content = models.ImageField(upload_to='comment/', blank=True, null=True, default = None)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.content[:6]

