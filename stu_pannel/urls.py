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
    path('productdetails/<int:id>', views.productdetails, name = "pdetails")
]