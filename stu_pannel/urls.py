from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views import View
from . import views

urlpatterns = [
path('',views.hello, name = "helo")
]