from django.contrib import admin
from .models import  Product, ExtendedUser, CartItem, Order,wislist

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

class AdminOrder(admin.ModelAdmin):
    list_display = [
        'product', 'quantity', 'user','date_added'
    ]
admin.site.register(CartItem, AdminOrder)

class AdminWislist(admin.ModelAdmin):
    list_display = [
        'product', 'user','date_added'
    ]
admin.site.register(wislist, AdminWislist)

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user','order_date','total_amount', 'payment_id',
        'order_id', 'payment_signaure', 'shipping_address',
        'mobile_no'
    ]
# 'product_name', 'product_id'
admin.site.register(Order, OrderAdmin)
