from django.contrib import admin
from .models import  Product, ExtendedUser

# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display =  [
        "product_id", "product_img", "product_name",
        "Product_building_year", "Product_programingi_language",
        "product_summery"
    ]
admin.site.register(Product, AdminProduct)


class AdminUser(admin.ModelAdmin):
    list_display = [
        "user", "First_name", "Last_name", "Gender",
        "Phone_number", "WhatsApp", "email", "address",
        "pincode"
    ]
admin.site.register(ExtendedUser, AdminUser)
