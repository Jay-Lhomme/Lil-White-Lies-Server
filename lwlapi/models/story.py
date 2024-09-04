from django.db import models
from .user import User


class Story(models.Model):
    name = models.CharField(max_length=100)
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stories')
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
