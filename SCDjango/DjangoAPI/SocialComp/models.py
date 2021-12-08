from django.db import models

# Create your models here.
class PostModel(models.Model):
    PostId = models.AutoField(primary_key=True)
    QueryId = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=5000)
    thumbnail = models.CharField(max_length=300)
    channel = models.CharField(max_length=300)
    date = models.CharField(max_length=100)
    views = models.CharField(max_length=100)
    comments = models.CharField(max_length=100)
    likes = models.CharField(max_length=100)


class QueryModel(models.Model):
    QueryId = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=30)
    brand1 = models.CharField(max_length=100)
    brand2 = models.CharField(max_length=100)
    brand3 = models.CharField(max_length=100)
    startDate = models.CharField(max_length=100)
    endDate = models.CharField(max_length=100)

