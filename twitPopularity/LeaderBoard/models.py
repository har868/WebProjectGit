from django.db import models

# Create your models here.
class Person(models.Model):
    Username = models.CharField(max_length=250)
    ScreenName = models.CharField(max_length=250)
    following = models.IntegerField()
    followers = models.IntegerField()
    image = models.FileField(null=True, blank=True)


