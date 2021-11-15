from django.db import models
import os

def get_image_path(instance, filename):
    return os.path.join('users_photos', str(instance.username) + '.jpg')

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    date_joined = models.DateField(auto_now=True)
    photo = models.ImageField(upload_to=get_image_path)
    class Meta:
        app_label = 'arcadeAPI'

class Game(models.Model):
    name = models.CharField(max_length=255)
    emulator = models.CharField(max_length=255)
    date_added = models.DateField(auto_now=True)
    # photo = models.ImageField(upload_to=get_image_path)
    class Meta:
        app_label = 'arcadeAPI'

class Action(models.Model):
    user = models.CharField(max_length=255)
    game = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now=True)
    used_coins = models.IntegerField()
    class Meta:
        app_label = 'arcadeAPI'