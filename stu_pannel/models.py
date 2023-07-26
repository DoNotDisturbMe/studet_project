from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ExtendedUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, default="default")
    Phone_number = models.CharField(max_length=100 ,default="default")
    email = models.CharField(max_length=100,default="default")
    address = models.CharField(max_length=200,default="default")
    pincode =  models.IntegerField(default="default")
    district = models.CharField(max_length=30,default="default")
    photo_user = models.ImageField(upload_to="user_img")

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

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If you have user authentication
    date_added = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=300)
    order_id = models.CharField(max_length=300)
    payment_signaure = models.CharField(max_length=3000)
    shipping_address = models.CharField(max_length=300)
    mobile_no = models.CharField(max_length=15)

   # # # product_download = models.FileField(upload_to="User Product")

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

class wislist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If you have user authentication
    date_added = models.DateTimeField(auto_now_add=True)

#
# class support(models.Model):
#     user_details = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
#     product_details = models.ForeignKey(Product, on_delete=models.CASCADE)
#     payment =
#





