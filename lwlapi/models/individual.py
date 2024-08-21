from django.db import models


class Individual(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=500)
