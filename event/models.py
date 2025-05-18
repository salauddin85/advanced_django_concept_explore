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

from django_currentuser.db.models import CurrentUserField
# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user
# )

class Order(models.Model):
    created_by = CurrentUserField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
