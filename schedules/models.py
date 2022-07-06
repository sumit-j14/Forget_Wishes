from django.db import models


class Schedule(models.Model):
    user = models.CharField(max_length=100)
    birth_date = models.IntegerField()
    birth_month = models.IntegerField()
    wish_who = models.CharField(max_length=100, default='NoName')
    custom_wish = models.CharField(max_length=200, default='Best Wishes!')
    recipient_email = models.EmailField(max_length=254, default=None)
