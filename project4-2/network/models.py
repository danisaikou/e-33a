from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return self.username

class Post(models.Model):
    user_id = models.ForeignKey(User, verbose_name="user_id", on_delete=models.CASCADE)
    content = models.CharField("content", max_length=260)
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


    def __str__(self) -> str:
        return f"{self.id}posted by {self.user_id.name} on {self.datetime} - {self.user_id}"
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, default=0, related_name="followed")
    following = models.ManyToManyField(User, blank = True, default=0, related_name="following")

    def serialize(self):
        return {
            "profile": self.user.id,
            "username": self.user.username,
            "followers": self.followers.count(),
            "following": self.following.all(),
        }
    def __str__(self):
        return self.user.username 