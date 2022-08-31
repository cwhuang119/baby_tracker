from sqlite3 import Timestamp
from django.db import models

# Create your models here.

class BabyInfo(models.Model):
    name = models.CharField(max_length=200)

class BabySitterInfo(models.Model):
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    baby = models.ForeignKey(BabyInfo, on_delete = models.CASCADE)


class Daiper(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    image = models.CharField(max_length=200)
    change_type = models.CharField(max_length=200)


class Feed(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    volume = models.FloatField()
    image = models.CharField(max_length=200)

class Weight(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    weight = models.FloatField()
    image = models.CharField(max_length=200)


class Temperature(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    temperature = models.FloatField()
    image = models.CharField(max_length=200)
