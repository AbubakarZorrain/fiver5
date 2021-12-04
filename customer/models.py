from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):

    phone = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    user = models.CharField(max_length=90, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    password = models.CharField(max_length=80,null=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.user

