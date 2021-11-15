from .models import User, Game, Action
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'date_joined', 'photo']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'emulator', 'date_added']

class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = ['user', 'game', 'date_time', 'used_coins']

