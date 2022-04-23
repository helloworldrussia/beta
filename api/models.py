from django.db import models


class Worker(models.Model):
    name = models.TextField(unique=True)
    jobs = models.IntegerField()
    coins = models.IntegerField()
    status = models.CharField(max_length=255, default='null')