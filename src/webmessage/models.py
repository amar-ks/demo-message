from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class EmailBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    sender_name = models.CharField(max_length=250)
    subject = models.CharField(max_length=500)
    description = models.TextField(default='', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.subject
