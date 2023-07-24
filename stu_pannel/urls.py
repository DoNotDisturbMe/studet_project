from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views import View
from . import views

urlpatterns = [
    path('',views.home, name = "home"),
    path('about',views.about, name = "about"),
    path('career', views.career, name = "career"),
    path('contact', views.contact, name = "contact"),
    path('productdetails/<id>', views.productdetails, name = "pdetails"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cartItem, name = "cart"),
    path('remove/<int:id>', views.remove_cart_item, name = "remove"),
    path('wislist/<int:id>', views.add_to_wishlist, name = "wislist"),
    path('showwislist', views.show_wislist, name = "showwislist"),
    #payment
    # path('checkout/', views.checkout, name='checkout'),

#     login
    path('login', views.LoginPage, name= "login"),
    path('signup', views.RegisterPage, name= "signup"),
    path('logout/', views.LogoutPage, name='logout'),


#     UserProfile
    path('Profile/<id>',views.userprofile_complete, name= "Profile"),
    path('account/', views.UserAccount, name = "account"),
#     Account Option
    path('profile_view/<id>', views.userprofile_view, name = "userprofile")
]