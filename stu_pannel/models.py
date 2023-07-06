from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_name = models.CharField(max_length=100)
    Last_name= models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Phone_number = models.CharField(max_length=100)
    WhatsApp  = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pincode =  models.IntegerField()


class Product(models.Model):
    product_id = models.CharField(max_length=600)
    product_img = models.ImageField(upload_to="Product_Img/")
    product_name = models.CharField(max_length=200)
    Product_building_year = models.DateTimeField()
    Product_programingi_language = models.CharField(max_length=300)
    Product_Addition_Programing_language = models.CharField(max_length=600)
    product_summery = models.CharField(max_length=10000)
    product_price = models.IntegerField()
    dicount_product_price = models.IntegerField()





