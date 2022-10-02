from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from app.models import *

@receiver(post_save, sender=User)
def save_user_profile(sender, instance,**kwargs):
    instance.Profile.save()



