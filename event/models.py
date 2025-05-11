from django.db import models

# Create your models here.
from test_app.models import *

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    management = models.ForeignKey(Management, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(User, related_name='events')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name