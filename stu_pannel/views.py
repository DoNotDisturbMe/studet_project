import datetime
import socketserver
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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
from .models import Product, ExtendedUser, CartItem, wislist, Order, SupportUser
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, SupportUser
from django.db import IntegrityError

from django.shortcuts import render, redirect, get_object_or_404
from .models import ExtendedUser

import re
#payment
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay




import re

def RegisterPage(request):
    if request.method == "POST":
        user_from = request.POST.get('form_username')
        user_pass1 = request.POST.get('form_pass1')
        user_pass2 = request.POST.get('form_pass2')
        print(user_from, user_pass2, user_pass1)
        # Password Requirement Regular Expression
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if user_pass1 != user_pass2:
            messages.add_message(request, messages.WARNING, 'Your password did not match.')
        elif not re.match(password_pattern, user_pass1):
            messages.add_message(request, messages.WARNING, 'Password must contain at least one character, one number, and one special symbol (@ $ ! % * # ? &), and be at least 8 characters long.')
        else:
            try:
                create_user = User.objects.create_user(username=user_from, password=user_pass1)
                create_user.save()
                return redirect('login')
            except IntegrityError:
                messages.add_message(request, messages.WARNING, 'Username already exists.')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('lg_user')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Valid user credentials, log the user in
            login(request, user)
            return redirect('home')
        else:
            # Invalid user credentials, show error message
            messages.add_message(request, messages.ERROR, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')
@login_required()
def LogoutPage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='/login')
def deleteAccount(request):
    try:
        User.objects.filter(username=request.user).delete()
        messages.success(request,'Account Deleted Successfully!')
        return redirect('home')
    except User.DoesNotExist:
        return render(request, 'stu_pannel/error.html', {'error_message': 'User Does not exits.'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})


@login_required(login_url='/login')
def userprofile_complete(request):
    if request.method == "POST":
        try:
            ex_user = User.objects.get(username=request.user)
            user_name_v = request.POST.get("name")
            user_mobile_v = request.POST.get('mobile')
            user_email_v = request.POST.get('email')
            user_address_v = request.POST.get('address')
            user_pincode_v = request.POST.get('pincode')
            user_disctrict_v = request.POST.get('district')
            user_photo_v = request.FILES.get('photo')
            # Create the ExtendedUser object
            user_details = ExtendedUser.objects.create(user_id=ex_user, user_name=user_name_v,
                                                       Phone_number=user_mobile_v, email=user_email_v,
                                                       address=user_address_v,
                                                       pincode=user_pincode_v, district=user_disctrict_v,
                                                       photo_user=user_photo_v)
            user_details.save()
            return redirect('account')
        except ObjectDoesNotExist:
            # Handle case when the User object does not exist for the logged-in user
            return render(request, 'stu_pannel/error.html', {'error_message': 'User not found.'})

        except IntegrityError:
            # Handle IntegrityError when creating the ExtendedUser object
            return render(request, 'stu_pannel/error.html', {'error_message': 'An error occurred while saving the user details.'})
    return render(request, 'stu_pannel/userprofile_complete.html')



@login_required(login_url='/login')
def edit_profile(request, id):
    try:
        # Get the ExtendedUser object for the logged-in user
        ex_user = get_object_or_404(ExtendedUser, user_id=request.user)
        ex_user1 = User.objects.get(username=request.user)
        print("Exuser:", ex_user, '\n', "Ex-user1:", ex_user1)
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
    except ExtendedUser.DoesNotExist:
        # Handle case when the ExtendedUser object does not exist for the logged-in user
        return render(request, 'stu_pannel/error.html', {'error_message': 'User profile not found.'})
    except User.DoesNotExist:
        # Handle case when the User object does not exist for the logged-in user
        return render(request, 'stu_pannel/error.html', {'error_message': 'User not found.'})
    except Exception as e:
        # Handle other potential errors during the update process
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})
    return render(request, 'stu_pannel/userprofile_complete.html', {'ex_user': ex_user})


@login_required(login_url='/login')
def UserAccount(request):
    is_operation_done = True
    return render(request, "stu_pannel/account.html",{'com_done':is_operation_done})
@login_required(login_url='/login')
def userprofile_view(request, id):
    print(id)
    user_prfoile = ExtendedUser.objects.filter(user_id= id).order_by("-id")[:1]
    return render(request, "stu_pannel/userprofile_view.html", {'user_prfoile':user_prfoile})


# ---------------------------------- Redisen section
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
    try:
        # Try to get the Product object with the provided id
        product = Product.objects.filter(id=id)

        data = {
            "pdata": product,
            # "off": discount_in_percentage (if you want to include discount data)
        }

        return render(request, 'stu_pannel/ProductDetails.html', data)

    except Product.DoesNotExist:
        # Handle the case when the Product object with the provided id does not exist
        return render(request, 'stu_pannel/error.html', {'error_message': 'Product not found.'})

    except Exception as e:
        # Handle other potential errors
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})

# --------------------------------------------------end here

@login_required(login_url='/login')
def add_to_cart(request, product_id):
    try:
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
    except Product.DoesNotExist:
        return render(request, "stu_pannel/error.html", {"error_message":"Product not found ."})
    except Exception as e:
        return render(request, "stu_pannel/error.html", {"erro_message":str(e)})

@login_required(login_url='/login')
def cartItem(request):
    try:
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
    except Product.DoesNotExist:
        return render(request,'stu_pannel/error.html', {'error_message':'Product Doestnot Exit'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message':str(e)})

@login_required(login_url='/login')
def remove_cart_item(request, id):
    try:
        cart_item = get_object_or_404(CartItem, id=id)
        cart_item.delete()
        return redirect('cart')
    except CartItem.DoesNotExist:
        return render(request, 'stu_pannel/error.html', {'error_message': 'Product Doestnot Exit'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})


@login_required(login_url='/login')
def add_to_wishlist(request, id):
    try:
        user = request.user
        product = get_object_or_404(Product, id=id)
        if wislist.objects.filter(user=user, product=product).exists():
             pass
        else:
            wishlist_item = wislist.objects.create(user=user, product=product)
            wishlist_item.save()
        return redirect('cart')
    except wislist.DoesNotExist:
        return render(request, 'stu_pannel/error.html', {'error_message': 'Product Doestnot Exit'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})


@login_required(login_url='/login')
def show_wislist(request):
    try:
        users = request.user
        data = wislist.objects.filter(user = users)
        dataset = {
            "data":data,
        }
        return render(request, 'stu_pannel/wislist.html', dataset)
    except wislist.DoesNotExist:
        return render(request, 'stu_pannel/error.html', {'error_message': 'Product Doestnot Exit'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})


RAZORPAY_API_KEY = "rzp_test_MTWvtlzlyTazey"
RAZORPAY_API_SECRET = "LTU55dGZMZdNc30Ie0i008OF"
order_user = []
@login_required(login_url='/login')
def payment(request):
    try:
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
    except Warning:
        return render(request, 'stu_pannel/error.html', {'error_message': 'Payment Server Not Reponds'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': f"Pls Check your network connection{str(e)}"})


@login_required(login_url='/login')
@csrf_exempt
def payment_success(request):
    try:
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
    except Warning:
        return render(request, 'stu_pannel/error.html', {'error_message': 'Payment not Success full pls try again after some time.'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})

@login_required(login_url='/login')
def user_oderview(request):
    try:
        order_data = Order.objects.filter(user_id=request.user).order_by("-id")[:5]
        data = {
            'orders':order_data
        }
        return render(request, 'stu_pannel/user_order.html', data)
    except Warning:
        return render(request, 'stu_pannel/error.html', {'error_message': 'You order is note done. try again proccess.'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})


@login_required(login_url='/login')
def support(request):
    if request.method == 'POST':
        user_name = request.user
        support_user_name = request.POST.get('name')
        support_user_mobileno = request.POST.get('mobile')
        support_user_email = request.POST.get('email')
        support_user_pro_id = request.POST.get('product_id')
        support_user_pro_date = request.POST.get('product_date')
        support_user_upi_id = request.POST.get('upi_id')
        try:
            order = Order.objects.filter(user_id=request.user).latest('id')
            payment_idd = order.payment_id
            total_amount = order.total_amount
            print(payment_idd, total_amount)

            if total_amount > 0 and str(payment_idd) == support_user_upi_id:
                with transaction.atomic():
                    order_support = SupportUser.objects.create(
                        user_name=user_name, support_uname=support_user_name,
                        support_umno=support_user_mobileno, support_uemail=support_user_email,
                        support_proid=support_user_pro_id, support_uprodate=support_user_pro_date,
                        support_uupid=support_user_upi_id, support_totalpayment=total_amount
                    )
                return redirect('home')
            else:
                return render(request, 'stu_pannel/error.html', {'error_message':"Invalid Payment Infromation" })
        except ObjectDoesNotExist:
            return render(request, 'stu_pannel/error.html', {'error_message':"Order not found for this user."})
        except Exception as e:
            # Handle any other unexpected exceptions here.
            return render(request, 'stu_pannel/error.html', {'error_message':f"An error occurred: {str(e)}"})
    return render(request, 'admin_pannel/support.html')

@login_required(login_url='/login')
def download(request):
    try:
        user_request = request.user
        order_data = SupportUser.objects.filter(user_name=user_request).order_by("-id")
        support_proid = []  # We will store the values of prod_intalized here
        for order in order_data:
            support_proid.append(order.support_proid) # Append the values to the support_proid list

        product_dow = Product.objects.filter(product_id__in=support_proid)
        data = {
            'product_dow': product_dow
        }
        print(user_request, support_proid)  # Print to check the results in the console
        return render(request, 'stu_pannel/download.html', data)
    except Warning:
        return render(request, 'stu_pannel/error.html', {'error_message': 'You have no purchase product.'})
    except Exception as e:
        return render(request, 'stu_pannel/error.html', {'error_message': str(e)})

