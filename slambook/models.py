from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from _datetime import datetime


# Create your models here.
class Friends(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=50)
    dateUpdated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('slambook:slambook_friend_detail', args=[self.id])


class Questions(models.Model):
    question = models.TextField()
    dateUpdated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('slambook:slambook_question_detail', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friends, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# hard-coded user accounts
regular_user = {"username": "valerie", "password": "pass12345"}
admin_user = {"username": "admin123", "password": "admin456"}
