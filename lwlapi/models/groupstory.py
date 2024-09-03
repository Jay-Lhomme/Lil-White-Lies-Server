from django.db import models
from .group import Group
from .story import Story


class GroupStory(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='group_storys')
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='group_related_storys')
