from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    name = models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=10,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
   



    def __str__(self):
        return self.mobile


    