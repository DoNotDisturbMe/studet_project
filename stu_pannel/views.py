import datetime
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import message
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, request, JsonResponse
from  django.shortcuts import redirect

# Authentication System Module
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#
from django.contrib import messages
from django.urls import reverse
from django.views import View
from  django.urls import  reverse_lazy
from django.views.generic.edit import CreateView
from .decorators import login_required_with_autologout
from .models import Product, ExtendedUser, CartItem




def LoginPage(request):
    if request.method =='POST':
        username = request.POST.get('lg_user')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username = username, password = pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('user name and passwrod is not match...')
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def RegisterPage(request):
    if request.method == "POST":
        user_from = request.POST.get('form_username')
        user_pass1 = request.POST.get('form_pass1')
        user_pass2= request.POST.get('form_pass2')
        print(user_from, user_pass2, user_pass1)
        if user_pass1 != user_pass2:
            messages.add_message(request,messages.WARNING, 'Your password did not math.')
        else:
            create_user = User.objects.create_user(username= user_from, password=user_pass1)
            create_user.save()
            return redirect('login')
    return render(request, 'signup.html')


def userprofile_complete(request, id):
    user_re = request.user
    ex_user = ExtendedUser.user_id
    if user_re == ex_user:
        return redirect('home')
    elif request.method== "POST":
        user_id_v = request.user
        user_name_v= request.POST.get("name")
        user_mobile_v = request.POST.get('mobile')
        user_email_v = request.POST.get('email')
        user_address_v = request.POST.get('address')
        user_pincode_v = request.POST.get('pincode')
        user_disctrict_v = request.POST.get('district')
        user_photo_v = request.FILES.get('photo')
        print(user_id_v, user_name_v, user_mobile_v, user_email_v, user_address_v, user_pincode_v,
              user_disctrict_v, user_photo_v)
        user_details = ExtendedUser.objects.create(user_id = user_id_v, user_name = user_name_v, Phone_number=user_mobile_v,
                                    email= user_email_v, address= user_address_v,
                                    pincode=user_pincode_v, district=user_disctrict_v,
                                    photo_user=user_photo_v, )
        user_details.save()
        return redirect('account')
    else:
        data_user = ExtendedUser.objects.filter(id = id)
        return render(request, 'stu_pannel/userprofile_complete.html', {"data":data_user})
    return render(request, 'stu_pannel/userprofile_complete.html')


def UserAccount(request):
    return render(request, "stu_pannel/account.html")

def userprofile_view(request, id):
    print(id)
    user_prfoile = ExtendedUser.objects.filter(user_id= id).order_by("-id")[:1]
    return render(request, "stu_pannel/userprofile_view.html", {'user_prfoile':user_prfoile})





def home(request):
    Product_data = Product.objects.all()
    data = {"Product_data":Product_data}
    return render(request, "stu_pannel/HomePage.html", data)

def about(request):
    return  render(request, "admin_pannel/about.html")


def career(request):
    return render(request, "admin_pannel/career.html")

def contact(request):
    return  render(request, "admin_pannel/contact.html")


def productdetails(request, id):
    id_data = Product.objects.filter(id = id)
    data = {
        "pdata":id_data,
        # "off":discount_in_percentage
    }
    return render(request, 'stu_pannel/ProductDetails.html', data)


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    # Get the user (assuming you have user authentication)
    user = request.user
    # Check if the product is already in the cart for this user
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
    # If the item already exists in the cart, increase the quantity by 1
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')  # Assuming you have a URL named 'cart' to display the cart

def cartItem(request):
    data_cart = CartItem.objects.all()
    totalPrice = []
    GST = []
    GST_Total = []


    for x in data_cart:
        new_price = x.product.dicount_product_price * x.quantity
        totalPrice.append(new_price)
        GST1 = (new_price /100) * 27
        GST.append(GST1)
        GST_Total.append(GST1 + new_price)
    # print(totalPrice,'\n', GST_Total)

    data = {
        "data_cart":data_cart,
        "totalPrice":totalPrice,
        "GST":GST,
        "GST_Total":GST_Total
    }
    return render(request,'stu_pannel/cart_item.html', data)





