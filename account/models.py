from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=350)
    image = models.ImageField(default='default/default.jpg')

    # def get_absolute_url(self):
    #     return reverse('profile', args=[self.user.id])

    def __str__(self):
        return self.user.username



class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.following_user_id.username} follows {self.user_id.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Notifications(models.Model):
    to_user = models.ForeignKey(User, related_name="my_notifications", on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.to_user.username

    @property
    def active_count(self):
        return self.objects.filter(read=False).count()
