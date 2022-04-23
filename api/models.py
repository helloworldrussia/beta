from django.db import models


class Deal(models.Model):
    begin = models.CharField(max_length=255)
    end = models.CharField(max_length=255)


class Worker(models.Model):
    name = models.TextField(unique=True)
    jobs = models.IntegerField()
    coins = models.IntegerField()
    status = models.CharField(max_length=255, default='null')
    deals = models.ManyToManyField(Deal)