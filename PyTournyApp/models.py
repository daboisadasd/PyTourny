from django.db import models


class OfflineUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class OfflineWinner(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200)
    win_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class OfflineUserQueue(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username
