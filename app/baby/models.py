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
    def format_log_str(self):
        time_format = '%H:%M'
        if self.change_type in ['1','Daiper1']:
            change_type='小便'
        elif self.change_type in ['2','Daiper2']:
            change_type='大便'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{change_type}\n"


class Feed(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    volume = models.FloatField()
    image = models.CharField(max_length=200)
    def format_log_str(self):
        time_format = '%H:%M'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{int(self.volume)} ml\n"
class Weight(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    weight = models.FloatField()
    image = models.CharField(max_length=200)

    def format_log_str(self):
        time_format = '%H:%M'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{int(self.weight)} g\n"
class Height(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    height = models.FloatField()
    image = models.CharField(max_length=200)

    def format_log_str(self):
        time_format = '%H:%M'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{int(self.height)} cm\n"
class HeadLength(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    head_length = models.FloatField()
    image = models.CharField(max_length=200)

    def format_log_str(self):
        time_format = '%H:%M'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{int(self.head_length)} cm\n"

class Temperature(models.Model):
    baby = models.ForeignKey(BabyInfo, on_delete=models.CASCADE)
    sitter = models.ForeignKey(BabySitterInfo, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()
    temperature = models.FloatField()
    image = models.CharField(max_length=200)

    def format_log_str(self):
        time_format = '%H:%M'
        return f"{datetime.datetime.fromtimestamp(self.time_stamp).strftime(time_format)} :{self.temperature}度\n"