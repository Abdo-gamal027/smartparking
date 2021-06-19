from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=200, null=True)
    password1 = models.CharField(max_length=20000, null=True)
    email = models.CharField(max_length=200, null=True)
    cardnumber = models.CharField(max_length=200, null=True)
    codenumber = models.CharField(max_length=4, null=True)
    objects = models.manager


