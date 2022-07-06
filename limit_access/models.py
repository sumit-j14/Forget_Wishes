from django.db import models

# this table stores number of entries per user
class UsagePerUser(models.Model):
    user_name = models.CharField(max_length=50)
    times_used = models.IntegerField()
