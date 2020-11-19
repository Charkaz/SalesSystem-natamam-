from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class userProfile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    kassa = models.FloatField(null=True)
    sirket = models.CharField(null=True,max_length=50)
    telefon = models.CharField(null = True , max_length=50)
    adress = models.CharField(null = True,max_length = 200)
    profilsekli = models.ImageField(null = True)
    dogumtarixi = models.DateField(null = True)

    def __str__(self):
        return self.user.username


def post_model_save(sender,instance,created,*args,**kwargs):
    print("after save")

post_save.connect(post_model_save,sender = User)


class Bos(models.Model):
    ad  = models.CharField(max_length=150)


class meat(models.Model):
    ad  = models.CharField(max_length=150)
