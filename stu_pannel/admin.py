from django.contrib import admin
from .models import  Product, ExtendedUser, CartItem, Order,wislist,SupportUser,Careers, Contact, CareersSaveData, About

# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display =  [
        "product_id", "product_img", "product_name",
        "Product_building_year", "Product_programingi_language",
        "product_summery", "product_file"
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

class AdminSupportuser(admin.ModelAdmin):
    list_display = [
        'user_name', 'support_uname', 'support_umno',
        'support_uemail', 'support_proid', 'support_uprodate',
        'support_uupid', 'support_totalpayment'
    ]
admin.site.register(SupportUser, AdminSupportuser)

class CareerAdmin(admin.ModelAdmin):
    list_display = [
        'job_title', 'job_location', 'job_post_date',
        'skills_set'
    ]
admin.site.register(Careers, CareerAdmin)

class CareersSaveDataAdmin(admin.ModelAdmin):
    list_display = [
        'job_tile', 'resume_upload'
    ]
admin.site.register(CareersSaveData, CareersSaveDataAdmin)

class ContactAdmin(admin.ModelAdmin):
    meta = Careers
    list_display =[
        'person_name', 'person_email', 'person_message'
    ]
admin.site.register(Contact, ContactAdmin)


class AboutAdmin(admin.ModelAdmin):
    list_display = [
        'about_message'

    ]
admin.site.register(About, AboutAdmin)

