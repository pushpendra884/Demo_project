from django.db import models

# Create your models here.

class Payment(models.Model):
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=50)
    price=models.CharField(max_length=10)
    info=models.CharField(max_length=50)

class Order(models.Model):
	orderid=models.AutoField(primary_key=True)
	pid=models.IntegerField()
	uid=models.CharField(max_length=50)
	qty=models.IntegerField()
	pprice=models.CharField(max_length=10)
	amount=models.CharField(max_length=10)
	info=models.CharField(max_length=50)


