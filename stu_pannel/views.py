import datetime
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import message
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, request
from  django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views import View
from  django.urls import  reverse_lazy
from django.views.generic.edit import CreateView
from .decorators import login_required_with_autologout
from .models import Product

def hello(request):
    Product_data = Product.objects.all()
    data = {"Product_data":Product_data}
    return render(request, "stu_pannel/HomePage.html", data)