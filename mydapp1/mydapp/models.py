from django.db import models

#create your models here.
class Register(models.Model):
    regid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    username=models.CharField(unique=True,max_length=50)
    password=models.CharField(max_length=10)
    address=models.CharField(max_length=1000)
    mobile=models.CharField(max_length=10)
    city=models.CharField(max_length=10)
    gender=models.CharField(max_length=20)
    status=models.IntegerField()
    role=models.CharField(max_length=20)	
    dt=models.CharField(max_length=1000)
