from django.db import models
from .story import Story
from .individual import Individual


class IndividualStory(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name='individual_storys')
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='individual_related_storys')
