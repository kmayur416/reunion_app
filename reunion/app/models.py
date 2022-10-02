from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
    
class Profile(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    following = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    followers = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000,blank=True)
    timestamp =  models.DateTimeField(auto_now_add=True)
    likes = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    unlikes = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    comment = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)


    
