from django.db import models

# Create your models here.

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catnm=models.CharField(unique=True,max_length=50)
    caticonnm=models.CharField(max_length=100)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=50)
    subcatnm=models.CharField(unique=True,max_length=50)
    subcaticonnm=models.CharField(max_length=100)

class Product(models.Model):
	pid=models.AutoField(primary_key=True)
	ptitle=models.CharField(max_length=50)
	pcategory=models.CharField(max_length=50)
	psubcategory=models.CharField(max_length=50)
	pdescription=models.CharField(max_length=500)
	pprice=models.IntegerField()
	uid=models.CharField(max_length=50)
	info=models.CharField(max_length=100)