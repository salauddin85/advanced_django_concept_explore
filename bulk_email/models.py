# models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailCompose(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="HTML content for the email")
   
    def __str__(self):
        return self.subject
