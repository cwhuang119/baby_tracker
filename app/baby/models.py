from django.db import models
import datetime
import django
# Create your models here.

class BabyInfo(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateField(default=django.utils.timezone.now().date(), blank=True)
    gender = models.CharField(max_length=10,default="")


class BabyCustoms(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    feed_frequency = models.IntegerField(blank=True,null=True,default=None)
    feed_interval = models.IntegerField(blank=True,null=True,default=None)



class BabySitterInfo(models.Model):
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    baby = models.ForeignKey(BabyInfo, on_delete = models.CASCADE)

class BabySitterCustoms(models.Model):
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    extract_milk_interval = models.IntegerField()
    extract_volumn = models.IntegerField()


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

class Height(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    height = models.FloatField()
    image = models.CharField(max_length=200)

class HeadLength(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    head_length = models.FloatField()
    image = models.CharField(max_length=200)



class Temperature(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    temperature = models.FloatField()
    image = models.CharField(max_length=200)
