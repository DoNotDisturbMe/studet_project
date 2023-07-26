import datetime
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import message
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, request, JsonResponse
from  django.shortcuts import redirect, get_object_or_404
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
import  os
from .models import Product, ExtendedUser, CartItem, wislist, Order

#payment
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay




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
            time.sleep(3)
            return redirect('login')
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


def userprofile_complete(request):
    if request.method == "POST":
        ex_user = User.objects.get(username=request.user)
        user_name_v= request.POST.get("name")
        user_mobile_v = request.POST.get('mobile')
        user_email_v = request.POST.get('email')
        user_address_v = request.POST.get('address')
        user_pincode_v = request.POST.get('pincode')
        user_disctrict_v = request.POST.get('district')
        user_photo_v = request.FILES.get('photo')
        print(ex_user, user_name_v, user_mobile_v, user_email_v, user_address_v, user_pincode_v,
              user_disctrict_v, user_photo_v)
        user_details = ExtendedUser.objects.create(user_id = ex_user, user_name = user_name_v,
                                    Phone_number=user_mobile_v, email= user_email_v, address= user_address_v,
                                    pincode=user_pincode_v, district=user_disctrict_v, photo_user=user_photo_v, )
        user_details.save()
        return redirect('account')
    return render(request, 'stu_pannel/userprofile_complete.html')



from django.shortcuts import render, redirect, get_object_or_404
from .models import ExtendedUser

def edit_profile(request, id):
    ex_user = get_object_or_404(ExtendedUser, user_id=request.user)
    ex_user1 = User.objects.get(username=request.user)
    print("Exuser:", ex_user, '\n', "Ex-user1 :", ex_user1)

    if request.method == "POST":
        user_name_v = request.POST.get("name")
        user_mobile_v = request.POST.get('mobile')
        user_email_v = request.POST.get('email')
        user_address_v = request.POST.get('address')
        user_pincode_v = request.POST.get('pincode')
        user_disctrict_v = request.POST.get('district')
        user_photo_v = request.FILES.get('photo')

        # Update the fields of the ex_user object
        ex_user.user_id = ex_user1
        ex_user.user_name = user_name_v
        ex_user.Phone_number = user_mobile_v
        ex_user.email = user_email_v
        ex_user.address = user_address_v
        ex_user.pincode = user_pincode_v
        ex_user.district = user_disctrict_v
        if user_photo_v:
            ex_user.photo_user = user_photo_v

        # Save the updated user object
        ex_user.save()
        return redirect('account')
    return render(request, 'stu_pannel/userprofile_complete.html', {'ex_user': ex_user})



def UserAccount(request):
    is_operation_done = True
    return render(request, "stu_pannel/account.html",{'com_done':is_operation_done})

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
    user = request.user
    data_cart = CartItem.objects.filter(user = user)
    totalPrice = []  #price without gst
    GST = []  #Total gst on per item
    GST_Total = [] #price with gst
    Total_Qunatity = [] #Total Quantity
    for x in data_cart:
        new_price = x.product.dicount_product_price * x.quantity
        Total_Qunatity.append(x.quantity)
        totalPrice.append(new_price)
        GST1 = (new_price /100) * 27
        GST.append(GST1)
        GST_Total.append(GST1 + new_price)
    # print(totalPrice,'\n',GST_Total,'\n',Total_Qunatity)
    data = {
        "data_cart":data_cart,
        "totalPrice":sum(totalPrice),
        "GST":sum(GST),
        "GST_Total":sum(GST_Total),
        "Quantity":sum(Total_Qunatity)
    }
    return render(request,'stu_pannel/cart_item.html', data)

def remove_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.delete()
    return redirect('cart')

def add_to_wishlist(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    if wislist.objects.filter(user=user, product=product).exists():
         pass
    else:
        wishlist_item = wislist.objects.create(user=user, product=product)
        wishlist_item.save()
    return redirect('cart')

def show_wislist(request):
    users = request.user
    data = wislist.objects.filter(user = users)
    dataset = {
        "data":data,
    }
    return render(request, 'stu_pannel/wislist.html', dataset)
def support(request):
    pass


order_user = []
def payment(request):
    order_users = request.user
    order_user.append(order_users)
    data_cart = CartItem.objects.filter(user=request.user)
    totalPrice = []  # price without gst
    GST = []  # Total gst on per item
    GST_Total = []  # price with gst
    Total_Qunatity = []  # Total Quantity

    productname = ''
    for x in data_cart:
        new_price = x.product.dicount_product_price * x.quantity
        Total_Qunatity.append(x.quantity)
        totalPrice.append(new_price)
        GST1 = (new_price / 100) * 27
        GST.append(GST1)
        GST_Total.append(GST1 + new_price)

        pd_name = x.product.product_name
        productname += pd_name + ','

    print(totalPrice, '\n', GST_Total, '\n', Total_Qunatity)

    amount = int(sum(GST_Total)*100) #100 here means 1 dollar,1 rupree if currency INR
    # quantity = sum(Total_Qunatity)
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
    response = client.order.create(
        {
            'amount':amount,
            'currency':'INR',
            'payment_capture':1,
        })
    print(response)
    context = {'response':response}
    return render(request,"payment/checkout.html",context)


@csrf_exempt
def payment_success(request):
    data_cart = CartItem.objects.filter(user=request.user)
    totalPrice = []  # price without gst
    GST = []  # Total gst on per item
    GST_Total = []  # price with gst

    for x in data_cart:
        new_price = x.product.dicount_product_price * x.quantity
        totalPrice.append(new_price)
        GST1 = (new_price / 100) * 27
        GST.append(GST1)
        GST_Total.append(GST1 + new_price)

    if request.method == "POST":
        print(request.POST)
        pay_id = request.POST.get('razorpay_payment_id')
        order_idd = request.POST.get('razorpay_order_id')
        order_signate = request.POST.get('razorpay_signature')


        # Get the ExtendedUser instance for the current user
        extended_user = get_object_or_404(ExtendedUser, user_id=request.user)

        # Create the Order instance
        new_order = Order.objects.create(
            user=request.user,  # Use the ExtendedUser instance here
            total_amount=sum(GST_Total),
            payment_id=pay_id,
            order_id=order_idd,
            payment_signaure=order_signate,
            mobile_no=extended_user.Phone_number,  # Access the attribute directly from the instance
            shipping_address=extended_user.address,
        )
        new_order.save()
        print("Data saved")
        # Delete all cart items for the current user
        CartItem.objects.filter(user=request.user).delete()
        order_data = Order.objects.filter(user_id=request.user).order_by("-id")[:1]
        data = {
            'orderdata':order_data
        }
        return render(request, 'payment/successfullpayment.html', data)  # Replace with the correct template name
    return HttpResponse("Method not allowed", status=405)

def user_oderview(request):
    order_data = Order.objects.filter(user_id=request.user).order_by("-id")[:5]
    data = {
        'orders':order_data
    }
    return render(request, 'stu_pannel/user_order.html', data)




def support(request):
    return  render(request, 'admin_pannel/support.html')

