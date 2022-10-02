from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    email = models.EmailField(unique=True,blank=False,null=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    following = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    followers = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True)
    description = models.CharField(max_length=1000,blank=True)
    timestamp =  models.DateTimeField(auto_now_add=True)
    likes = ArrayField(ArrayField(models.IntegerField()),blank=True, null=True)
    comment = ArrayField(models.CharField(max_length=200),blank=True, null=True)


    
