from django.db import models
from .user import User


class Story(models.Model):
    name = models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
