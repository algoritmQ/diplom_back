from rest_framework import serializers
from .models import Profile, Message, Notification
from .models import Ad
from .models import Chat
from .models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
        depth = 2


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'city']
