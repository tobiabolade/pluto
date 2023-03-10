from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

shift = (
    ("Late", "late"),
    ("Early", "early"),
    ("Long", "long"),
    ("Night", "night"),
)


# Create your models here.
class Week(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    week_end = models.DateField()

    def __str__(self):
        return str(self.week_start) + ' - ' + str(self.week_end)


class Timesheet(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    day = models.CharField(max_length=200)
    shift = models.CharField(max_length=20, choices=shift)
    client = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    start = models.DateTimeField()
    finish = models.DateTimeField()

    def __str__(self):
        return self.day + ' - ' + self.shift + ' - ' + self.address

