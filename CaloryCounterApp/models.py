from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):

    def __str__(self):
        return self.username


class ProfileModel(models.Model):
    GENDER =[
        ('male','Male'),
        ('female','Female')
    ]

    user =models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name =models.CharField(max_length=200, blank=True, null=True)
    age =models.FloatField(blank=True, null=True)
    gender =models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
    height =models.FloatField(verbose_name="Height (in cm)", blank=True, null=True)
    weight =models.FloatField(verbose_name="Weight (in kg)", blank=True, null=True)
    bmr =models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class ConsumeCaloryModel(models.Model):
    user =models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item_name =models.CharField(max_length=200, blank=True, null=True)
    calory =models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.item_name