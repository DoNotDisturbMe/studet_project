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
        "user_id", "user_name", "Phone_number",
        "email", "address", "pincode",
        'district','photo_user'
    ]
admin.site.register(ExtendedUser, AdminUser)
