from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    city = models.CharField(max_length=25)


class Category(models.Model):
    title = models.CharField(max_length=100)


class Ad(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('S', 'Sold'),
    )

    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    full_description = models.TextField(max_length=1000, null=True, blank=True)
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    user_id = models.ForeignKey(Profile, models.CASCADE)


class Chat(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('F', 'Finished'),
    )

    user_1 = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name='buyer')
    user_2 = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name='seller')
    creator = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name='creator')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, models.CASCADE)
    user_id = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True)
    message_text = models.CharField(max_length=255)
    message_time = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    message_id = models.ForeignKey(Message, models.CASCADE)
