from django.contrib import admin
from .models import User, Game, Action

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Action)