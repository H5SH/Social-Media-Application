from django.contrib.auth.models import AbstractUser
from django.db import models

class Follow(models.Model):
    user = models.CharField(max_length=150, default=None)
    following = models.CharField(max_length=150, default=None)

    def __str__(self):
        return f'{self.following.username}'
    
    def follower(self):
        return {
            'follower': [user.username for user in self.following]
        }


class Post(models.Model):
    body = models.TextField(blank=True, default=None)
    likes = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True, null=True)
    username = models.CharField(max_length=150, default=None)
    liked_by = models.ManyToManyField('User', default=None, related_name='liker')

    def serialize(self):
        return {
            'id': self.id,
            'body': self.body,
            'likes': self.likes,
            'time': self.time.strftime('%b %d %Y, %I:%M %p'),
            'username': self.username
        }
    
    def likers(self):
        return {
            'liked_by': [user.id for user in self.liked_by.all()]
        }
    


class User(AbstractUser):
    pass

    
