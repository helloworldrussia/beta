from django.db import models


class Deal(models.Model):
    begin = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Worker(models.Model):
    name = models.TextField(unique=True)
    jobs = models.IntegerField()
    coins = models.IntegerField()
    status = models.CharField(max_length=255, default='null')
    deals = models.ManyToManyField(Deal)