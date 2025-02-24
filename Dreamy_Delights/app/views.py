from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def home(req):
    return render(req,'home.html')


def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
    
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname      
                    return redirect(shop_home)
                else:
                    req.session['user']=uname      
                    return redirect(user_home)
            else:
                messages.warning(req,"invalid uname or password")  
        return render(req,'login.html') 
    
def shop_logout(req):
    logout(req)
    req.session.flush()              
    return redirect(shop_login) 

# def  register(req):
#      if req.method=='POST':
#         name=req.POST['name']       
#         email=req.POST['email']
#         password=req.POST['password']
#         send_mail('Dreamy Delights registration', 'Welcome to Dreamy Delights! Your account has been created successfully', settings.EMAIL_HOST_USER, [email])

#         try:
#             data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
#             data.save()
#             return redirect(shop_login)
#         except:
#             messages.warning(req,"user details already exits")
#             return redirect(register)
#      else:
#          return render(req,'register.html')

# def register(req):
#     if req.method == 'POST':
#         name = req.POST.get('name', '').strip()
#         email = req.POST.get('email', '').strip()
#         password = req.POST.get('password', '').strip()

#         if not name or not email or not password:
#             messages.error(req, "All fields are required.")
#             return redirect(register)

#         email_regex = r'^[a-z][a-z0-9._%+-]*\d[a-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,}$'
#         if not re.fullmatch(email_regex, email): 
#             messages.error(req, "Invalid email format.")
#             return redirect(register)

#         if len(password) < 6:
#             messages.error(req, "Password must be at least 6 characters long.")
#             return redirect(register)
#         if not re.search(r'[A-Z]', password):
#             messages.error(req, "Password must contain at least one uppercase letter.")
#             return redirect(register)
#         if not re.search(r'\d', password):
#             messages.error(req, "Password must contain at least one number.")
#             return redirect(register)

#         if User.objects.filter(username=email).exists():
#             messages.warning(req, "User already exists.")
#             return redirect(register)

#         try:
#             user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
#             user.save()

#             send_mail(
#                 'Dreamy Delights registration', 'Welcome to Dreamy Delights! Your account has been created successfully',
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False
#             )

#             messages.success(req, "Registration successful! Please log in.")
#             return redirect(shop_login)

#         except Exception as e:
#             messages.error(req, f"Registration failed: {str(e)}")
#             return redirect(register)

#     return render(req, 'register.html')


def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(req, "Invalid email format.")
            return redirect(register)

        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.match(password_pattern, password):
            messages.error(req, "Password must be at least 8 characters long and include letters and numbers.")
            return redirect(register)

        if User.objects.filter(username=email).exists():
            messages.warning(req, "User with this email already exists.")
            return redirect(register)

        user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
        user.save()

        send_mail(
            'Dreamy Delights Registration',
            '🎉 Welcome to Dreamy Delights! Your account has been created successfully.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        messages.success(req, "Account created successfully! Please log in.")
        return redirect(shop_login)

    return render(req, 'register.html')


def view_cupcake(req):
        cake_category = Category.objects.get(name='CupCakes')
        cupcakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(cupcakes, 6)  
        page_number = req.GET.get('page')  
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
 

def view_layercake(req):
        cake_category = Category.objects.get(name='Layer Cakes')
        layercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(layercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
  

def view_onelayercake(req):
        cake_category = Category.objects.get(name='One Tier Party Cakes')
        onelayercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(onelayercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
  

def view_twolayercake(req):
        cake_category = Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(twolayercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})

# def view_cupcake(req):
#         cake_category=Category.objects.get(name='CupCakes')
#         cupcakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': cupcakes})
    
# def view_layercake(req):
#         cake_category=Category.objects.get(name='Layer Cakes')
#         layercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': layercakes})     

# def view_onelayercake(req):
#         cake_category=Category.objects.get(name='One Tier Party Cakes')
#         onelayercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': onelayercakes})   
    
# def view_twolayercake(req):
#         cake_category=Category.objects.get(name='Two Tier Party Cakes')
#         twolayercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': twolayercakes})   

def about_us(req):
    return render(req,'about_us.html') 

# def visit_us(req):
#     return render(req,'visit_us.html')
# from django.core.mail import send_mail
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.conf import settings

def visit_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                ['dreamydelights.team@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "Your message has been sent successfully!")
        except:
            messages.error(request, "Failed to send your message. Please try again.")

        return redirect(visit_us)

    return render(request, 'visit_us.html')


def collections(req):
    return render(req,'collections.html')

#--------------------- admin-------------------------------------------------------------------------------------------  


def shop_home(req):
    if 'shop' in req.session:
        return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login)
      
def cupcake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='CupCakes')
        cupcakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/cake.html',{'cake': cupcakes})
    else:
        return redirect(shop_login)  
    
def layercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='Layer Cakes')
        layercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/cake.html',{'cake': layercakes})
    else:
        return redirect(shop_login)   
    
def onelayercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='One Tier Party Cakes')
        onelayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/cake.html',{'cake': onelayercakes})
    else:
        return redirect(shop_login)   
    
def twolayercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/cake.html',{'cake': twolayercakes})
    else:
        return redirect(shop_login)      
           

def add_cake(req):
    if req.method == 'POST':
        name = req.POST['name']
        price = req.POST['price']
        file = req.FILES['img']
        category_name = req.POST['category']  
        qty = req.POST['quantity']
        des = req.POST['description']

        try:
            category = Category.objects.get(name=category_name)  
        except Category.DoesNotExist:
            return HttpResponse("Category does not exist.", status=400)  

        data = Cake.objects.create(
            name=name, 
            price=price, 
            img=file, 
            category=category,  
            quantity=qty, 
            description=des
        )

        data.save()
        return redirect(shop_home)

    return render(req, 'shop/add_cake.html')

def search_admin(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')  
        results = Cake.objects.filter(name__icontains=searched) if searched else []
        return render(request, 'shop/search_admin.html', {'searched': searched, 'results': results})
    else:
        return render(request, 'shop/search_admin.html', {'searched': '', 'results': []})    
    
# def add_cupcake(req):
#     if req.method=='POST':
#         id=req.POST['id']
#         name=req.POST['name']       
#         price=req.POST['price']            
#         file=req.FILES['img']
#         category=req.POST['category']
#         qty=req.POST['quantity']
#         des=req.POST['description']
#         data=Cake.objects.create(name=name,price=price,img=file,category=category,quantity=qty,description=des)   
#         data.save()
#         return redirect(shop_home)
#     return render(req,'shop/add_cupcake.html') 


# def edit_cake(req,id):
#         cake = Cake.objects.get(pk=id)
#         category=Category.objects.all()


#         if req.method == 'POST':
#             name = req.POST['name']
#             price = req.POST['price']
#             file = req.FILES.get('img')  
#             cat = req.POST['category']
#             qty = req.POST['quantity']
#             des = req.POST['description']
            
#             print(file)
#             if file:
#                 Cake.objects.filter(pk=id).update(name=name,price=price,img=file,category=cat,quantity=qty,description=des)   
#             else:
#                 Cake.objects.filter(pk=id).update(name=name,price=price,category=cat,quantity=qty,description=des)   

#             return redirect(shop_home)
#         return render(req,'shop/edit_cupcake.html',{'data':cake},{'categories': category}) 


def edit_cake(req,id):
        cake = Cake.objects.get(pk=id)
        category = Category.objects.all()


        if req.method == 'POST':
            name = req.POST['name']
            price = req.POST['price']
            file = req.FILES.get('img')  
            cat = req.POST['category']
            qty = req.POST['quantity']
            des = req.POST['description']

            # category = Category.objects.get(id=Category) 
            if file:
                cake.img =file
            cake.save()    
            
            print(file)
            if file:
                Cake.objects.filter(pk=id).update(name=name,price=price,img=file,quantity=qty,description=des)   
            else:
                Cake.objects.filter(pk=id).update(name=name,price=price,quantity=qty,description=des)   

            return redirect(shop_home)
        return render(req,'shop/edit_cupcake.html',{'data':cake, 'categories': category}) 


# def edit_cupcake(req, id):
#     cupcakes = Cake.objects.get(pk=id)

#     if req.method == 'POST':
#         name = req.POST['name']
#         price = req.POST['price']
#         file = req.FILES.get('img')  
#         cat = req.POST['category']
#         qty = req.POST['quantity']
#         des = req.POST['description']
        

#         if file:
#             cupcakes.img = file 

#         cupcakes.name = name
#         cupcakes.price = price
#         cupcakes.category = cat
#         cupcakes.quantity = qty
#         cupcakes.description = des

#         cupcakes.save()

#         return redirect('shop_home')

#     return render(req, 'shop/edit_cupcake.html', {'data': cupcakes})

def delete_cupcake(req,id):
        data=Cake.objects.get(pk=id)
        url=data.img.url
        url=url.split('/')[-1]
        os.remove('media/'+url)  
        data.delete()
        return redirect(shop_home) 

def bookings(req):
    bookings=Buy.objects.all()[::-1][:10]
    return render(req,'shop/bookings.html',{'data':bookings})


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        # products=Cake.objects.all()
        return render(req,'user/user_home.html')  


def user_cupcake(req):
    if 'user' in req.session:
        cake_category = Category.objects.get(name='CupCakes')
        cupcakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(cupcakes, 6)  
        page_number = req.GET.get('page')  
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
    else:
        return redirect(shop_login)

def user_layercake(req):
    if 'user' in req.session:
        cake_category = Category.objects.get(name='Layer Cakes')
        layercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(layercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
    else:
        return redirect(shop_login)

def user_onelayercake(req):
    if 'user' in req.session:
        cake_category = Category.objects.get(name='One Tier Party Cakes')
        onelayercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(onelayercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
    else:
        return redirect(shop_login)

def user_twolayercake(req):
    if 'user' in req.session:
        cake_category = Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes = Cake.objects.filter(category=cake_category)

        paginator = Paginator(twolayercakes, 6)
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(req, 'user/cake.html', {'page_obj': page_obj})
    else:
        return redirect(shop_login)

# def user_cupcake(req):
#     if 'user' in req.session:
#         cake_category=Category.objects.get(name='CupCakes')
#         cupcakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': cupcakes})
#     else:
#         return redirect(shop_login)
    
# def user_layercake(req):
#     if 'user' in req.session:
#         cake_category=Category.objects.get(name='Layer Cakes')
#         layercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': layercakes})
#     else:
#         return redirect(shop_login)      


# def user_onelayercake(req):
#     if 'user' in req.session:
#         cake_category=Category.objects.get(name='One Tier Party Cakes')
#         onelayercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': onelayercakes})
#     else:
#         return redirect(shop_login)   
    
# def user_twolayercake(req):
#     if 'user' in req.session:
#         cake_category=Category.objects.get(name='Two Tier Party Cakes')
#         twolayercakes=Cake.objects.filter(category=cake_category)
#         return render(req,'user/cake.html',{'cake': twolayercakes})
#     else:
#         return redirect(shop_login)     


def view_cake(req,id):
     if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cake=Cake.objects.get(pk=id)
        try:
            cart=Cart.objects.get(Cake=cake,user=user)
        except:
            cart=None    
        return render(req,'user/view_cakes.html',{'cake':cake,'cart':cart}) 
     else:
         return redirect(shop_login)  

def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '') 
        results = Cake.objects.filter(name__icontains=searched) if searched else []
        return render(request, 'user/search_user.html', {'searched': searched, 'results': results})
    else:
        return render(request, 'user/search_user.html', {'searched': '', 'results': []})         
         

def add_to_cart(req,id):
     Product=Cake.objects.get(pk=id)
     print(Product)
     user=User.objects.get(username=req.session['user'])
     print(user)
     data=Cart.objects.create(user=user,cake=Product)
     data.save()
     return redirect(cart_display)


def cart_display(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart_display.html',{'data':data})  


def delete_cart(req,id):
    data=Cart.objects.get(pk=id) 
    data.delete()
    return redirect(cart_display)

def buy_pro(req,id):
    cake=Cake.objects.get(pk=id)
    return redirect(address_page, id=id)

# def address_page(req,id):
#     cake = Cake.objects.get(id=id)
    
#     if req.method == 'POST':
#         name = req.POST.get('name')
#         address = req.POST.get('address')
#         phone_number = req.POST.get('phone_number')


#         user_address = Address(user=req.user, name=name, address=address, phone_number=phone_number)
#         user_address.save()

#         buy = Buy(user=req.user, cake=cake, price=cake.price, address=user_address)
#         buy.save()

#         return redirect(user_view_bookings) 

#     return render(req, 'user/order_details.html', {
#         'cake': cake,
#     })

# def address_page(req, id):
#     cake = Cake.objects.get(id=id)
    
#     if req.method == 'POST':
#         name = req.POST.get('name')
#         address = req.POST.get('address')
#         phone_number = req.POST.get('phone_number')

#         user_address = Address(user=req.user, name=name, address=address, phone_number=phone_number)
#         user_address.save()

#         buy = Buy(user=req.user, cake=cake, price=cake.price, address=user_address)
#         buy.save()

#         return redirect(user_view_bookings)

#     return render(req, 'user/order_details.html', {
#         'cake': cake,
#     })
def address_page(req, id):
    cake = Cake.objects.get(id=id)
    user = User.objects.get(username=req.session['user'])  # Verify user retrieval

    # ✅ Check if address exists for user
    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        user_address = Address(user=user, name=name, address=address, phone_number=phone_number)
        user_address.save()

        return redirect(profile_view)  # Redirect to profile after saving

    return render(req, 'user/order_details.html', {
        'cake': cake,
        'user_address': user_address  # 🔄 Pass this to the template
    })



# def pay(req):
#     user = User.objects.get(username=req.session['user'])
#     cake = Cake.objects.get(pk=req.session['cake_id'])  
#     quantity = int(req.GET.get('quantity', 1))
#     order = Order.objects.get(pk=req.session['order_id'])

#     if req.method == 'GET':
#         user_address = Address.objects.filter(user=user).order_by('-id').first()

#         data = Buy.objects.create(
#             user=user,
#             cake=cake,
#             price=cake.price * quantity,  
#             address=user_address,
#             quantity=quantity,
#             order=order
#         )
#         data.save()
#         return redirect(order_payment)

#     return render(req, 'user/user_bookings.html')


# def order_payment(req):
#     if 'user' in req.session:
#         user = User.objects.get(username=req.session['user'])
#         cake = Cake.objects.get(pk=req.session['cake_id'])
#         amount = cake.price

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create({
#             "amount": int(amount) * 100,  
#             "currency": "INR",
#             "payment_capture": "1"
#         })
#         order_id = razorpay_order['id']

#         order = Order.objects.create(
#             user=user,
#             price=amount,
#             provider_order_id=order_id
#         )
#         order.save()
#         req.session['order_id'] = order.pk

#         return render(req, "user/order_details.html", {
#             "callback_url": "http://127.0.0.1:8000/callback/",
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "order": order,
#         })
#     else:
#         return redirect('login')
# def order_payment(req):
#     if 'user' in req.session:
#         user = User.objects.get(username=req.session['user'])
#         cake = Cake.objects.get(pk=req.session['cake_id'])
#         amount = cake.price

#         # Fetch the latest saved address
#         user_address = Address.objects.filter(user=user).order_by('-id').first()

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create({
#             "amount": int(amount) * 100,  
#             "currency": "INR",
#             "payment_capture": "1"
#         })
#         order_id = razorpay_order['id']

#         order = Order.objects.create(
#             user=user,
#             price=amount,
#             provider_order_id=order_id
#         )
#         order.save()
#         req.session['order_id'] = order.pk

#         return render(req, "user/order_details.html", {
#             "callback_url": "http://127.0.0.1:8000/callback/",
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "order": order,
#             "cake": cake,
#             "user_address": user_address  # Pass saved address to template
#         })
#     else:
#         return redirect('login')


# @csrf_exempt
# def callback(request):
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         return client.utility.verify_payment_signature(response_data)

#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")

#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id

#         try:
#             verify_signature(request.POST)
#             order.status = PaymentStatus.SUCCESS
#         except:
#             order.status = PaymentStatus.FAILURE
        
#         order.save()

#         return redirect("pay") if order.status == PaymentStatus.SUCCESS else redirect("payment_failed")
#     else:
#         error_data = json.loads(request.POST.get("error[metadata]", "{}"))
#         provider_order_id = error_data.get("order_id", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.status = PaymentStatus.FAILURE
#         order.save()

#         return redirect("payment_failed")
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from django.contrib import messages
# from .models import Cake, Order, Buy, Address
# from .constants import PaymentStatus
# import razorpay
# import json

# Razorpay Client Initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# -----------------------------------
# 🧾 ORDER PAYMENT (Initiate Payment)
# -----------------------------------
@login_required
def order_payment(req):
    if 'username' in req.session:
        user = get_object_or_404(User, username=req.session['username'])
        cake = Cake.objects.get(pk=req.session['id'])
        amount = cake.price

        # Create Razorpay Order
        razorpay_order = razorpay_client.order.create({
            "amount": int(amount) * 100,  # Amount in paisa
            "currency": "INR",
            # "payment_capture": "1"
        })

        # Create Local Order
        order = Order.objects.create(
            user=user,
            price=amount,
            provider_order_id=razorpay_order['id']
        )
        req.session['order_id'] = order.pk

        return render(req, "user/address.html", {
            "callback_url": "http://127.0.0.1:8000/callback/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        })
    else:
        return redirect('login')

# -----------------------------------
# 💸 PAY & CREATE BUY ENTRY
# -----------------------------------
@login_required
def pay(req):
    user = get_object_or_404(User, username=req.session['user'])

    cart_item = Cart.objects.filter(user=user).order_by('-id').first()

    if not cart_item:
        messages.error(req, "Your cart is empty. Please add a cake first.")
        return redirect('cart_display')

    cake = cart_item.cake
    quantity = int(req.GET.get('quantity', 1))
    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id) if order_id else None

    if req.method == 'GET':
        user_address = Address.objects.filter(user=user).order_by('-id').first()

        data = Buy.objects.create(
            user=user,
            cake=cake,
            price=cake.price * quantity,  # Price multiplied by quantity
            address=user_address,
            order=order
        )
        data.save()

        return redirect(user_view_bookings)

    return render(req, 'user/view_bookings.html')



# -----------------------------------
# 🧾 RAZORPAY CALLBACK (Verify Payment)
# -----------------------------------
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        # Update Order
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        # Verify Signature
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect("pay")

    else:
        # Handle Payment Failure
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect("pay")


def place_order(req,id):
    Product=Cake.objects.get(pk=id)
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.create(user=user,cake=Product)
    data.save()
    return redirect(user_home)


def user_view_bookings(req):
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/view_bookings.html',{'data':data})         


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile, 'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address_text = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if name and address_text and phone_number:
            address = Address.objects.create(
                user=request.user,
                name=name,
                address=address_text,
                phone_number=phone_number
            )

            profile, created = Profile.objects.get_or_create(user=request.user)
            if not profile.primary_address:
                profile.primary_address = address
                profile.save()

            messages.success(request, "Address added successfully.")
            return redirect('profile_view')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'user/profile.html')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        address_text = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if name and address_text and phone_number:
            address.name = name
            address.address = address_text
            address.phone_number = phone_number
            address.save()

            messages.success(request, "Address updated successfully.")
            return redirect('profile_view')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'user/profile.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    profile = get_object_or_404(Profile, user=request.user)

    if profile.primary_address == address:
        profile.primary_address = None
        profile.save()

    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect(profile_view)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('login')
    
    return render(request, "user/profile.html")



@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get("first_name", "").strip()
        username = request.POST.get("username", "").strip()

        if not first_name or not username:
            messages.error(request, "Both fields are required.")
            return render(request, "user/profile.html", {"user": user})

        try:
            validate_email(username)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "user/profile.html", {"user": user})

        if user.username != username and user.__class__.objects.filter(username=username).exists():
            messages.error(request, "This email is already in use.")
            return render(request, "user/profile.html", {"user": user})

        user.first_name = first_name
        user.username = username
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile_view")

    return render(request, "user/profile.html", {"user": request.user})

# from django.http import HttpResponseNotAllowed

# def buy_all(request):
#     user = User.objects.get(username=request.session['user'])
#     item_ids = request.GET.get('items', '').split(',')

#     if not item_ids or item_ids == ['']:
#         messages.error(request, "No items provided.")
#         return redirect('cart_display')

#     cart_items = Cart.objects.filter(cake__pk__in=item_ids, user=user)
#     addresses = Address.objects.filter(user=user)

#     if not cart_items.exists():
#         messages.warning(request, "No valid items found in the cart.")
#         return redirect('cart_display')

#     if request.method == 'POST':
#         # Get or create user address
#         user_address, created = Address.objects.get_or_create(
#             user=user,
#             name=request.POST.get('name'),
#             address=request.POST.get('address'),
#             phone_number=request.POST.get('phone_number')
#         )

#         total_price = 0
#         for cart in cart_items:
#             item_price = int(cart.cake.price)
#             item_quantity = int(cart.quantity)
#             price = item_price * item_quantity
#             total_price += price

#             # Create Buy entry
#             Buy.objects.create(
#                 user=user,
#                 cake=cart.cake,
#                 price=price,
#                 address=user_address,
#                 is_confirmed=False
#             )

#         cart_items.delete()  # Clear cart after purchase

#         return redirect(order_payment2)

#     return render(request, 'user/cart_order.html', {
#         'cart_items': cart_items,
#         'addresses': addresses
#     })

# def order_payment2(req):
#     if 'user' in req.session:
#         user = User.objects.get(username=req.session['user'])
#         cart_items=Cart.objects.filter(user=user)


#         amount = 0
#         for cart in cart_items:
#             category = cart.category
#             quantity = cart.quantity
#             price = category.offer_price * quantity
#             amount += price

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create({
#             "amount": int(amount) * 100, 
#             "currency": "INR",
#             "payment_capture": "1"
#         })
#         order_id=razorpay_order['id']
#         order = Order.objects.create(
#             user=user,
#             price=amount,
#             provider_order_id=order_id
#         )
#         order.save()
#         print(order.pk)
#         req.session['order_id']=order.pk
#         return render(req, "user/cart_address.html", {
#             "callback_url": "http://127.0.0.1:8000/callback2/",
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "order": order,
#         })
#     else:
#         return redirect('login') 

# @csrf_exempt
# def callback2(request):
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         return client.utility.verify_payment_signature(response_data)

#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")

#         # Update Buy model with payment details
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()

#         if not verify_signature(request.POST):
#             order.status = PaymentStatus.SUCCESS
#             order.save()
#             return redirect("checkout_all") 
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return redirect("checkout_all")

#     else:
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id =json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         # order.payment_id = payment_id
#         order.status = PaymentStatus.FAILURE
#         order.save()

#         return redirect("checkout_all")


# def buy_all(request):
#     user = User.objects.get(username=request.session['user'])
#     item_ids = request.GET.get('items', '').split(',')

#     if not item_ids or item_ids == ['']:
#         messages.error(request, "No items provided.")
#         return redirect('cart_display')

#     cart_items = Cart.objects.filter(cake__pk__in=item_ids, user=user)
#     addresses = Address.objects.filter(user=user)

#     if not cart_items.exists():
#         messages.warning(request, "No valid items found in the cart.")
#         return redirect('cart_display')

#     if request.method == 'POST':
#         # Get or create user address
#         user_address, created = Address.objects.get_or_create(
#             user=user,
#             name=request.POST.get('name'),
#             address=request.POST.get('address'),
#             phone_number=request.POST.get('phone_number')
#         )

#         total_price = 0
#         for cart in cart_items:
#             item_price = int(cart.cake.price)
#             item_quantity = int(cart.quantity)
#             price = item_price * item_quantity
#             total_price += price

#             # Create Buy entry (Order without Payment Gateway)
#             Buy.objects.create(
#                 user=user,
#                 cake=cart.cake,
#                 price=price,
#                 address=user_address,
#                 is_confirmed=True  # Directly confirm the order
#             )

#         cart_items.delete()  # Clear cart after purchase

#         messages.success(request, "All items purchased successfully!")
#         return redirect(cart_display)

#     return render(request, 'user/cart_order.html', {
#         'cart_items': cart_items,
#         'addresses': addresses
#     })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

# @login_required
# def cart_address_page(req):
#     cart_items = Cart.objects.filter(user=req.user)
#     user_address = Address.objects.filter(user=req.user).first()  # Fetch saved address if exists

#     if req.method == 'POST':
#         use_saved_address = req.POST.get('use_saved_address')

#         if use_saved_address == 'yes' and user_address:
#             selected_address = user_address
#         else:
#             name = req.POST.get('name')
#             address = req.POST.get('address')
#             phone_number = req.POST.get('phone_number')

#             if not cart_items.exists():
#                 messages.error(req, "Your cart is empty.")
#                 return redirect('cart_view')

#             selected_address = Address(
#                 user=req.user,
#                 name=name,
#                 address=address,
#                 phone_number=phone_number
#             )
#             selected_address.save()

#         # Save address in session for place_order
#         req.session['address_id'] = selected_address.id

#         return redirect(cart_place_order)

#     return render(req, 'user/cart_order.html', {
#         'cart_items': cart_items,
#         'user_address': user_address
#     })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
import re

@login_required
def cart_address_page(req):
    cart_items = Cart.objects.filter(user=req.user)
    user_address = Address.objects.filter(user=req.user).first()  # Fetch saved address if exists

    if req.method == 'POST':
        use_saved_address = req.POST.get('use_saved_address')

        if use_saved_address == 'yes' and user_address:
            selected_address = user_address
        else:
            name = req.POST.get('name')
            address = req.POST.get('address')
            phone_number = req.POST.get('phone_number')

            # ✅ Phone Number Validation (Exactly 10 digits)
            if not re.fullmatch(r'\d{10}', phone_number):
                messages.error(req, "Phone number must be exactly 10 digits.")
                return redirect('cart_address_page')

            if not cart_items.exists():
                messages.error(req, "Your cart is empty.")
                return redirect('cart_view')

            selected_address = Address(
                user=req.user,
                name=name,
                address=address,
                phone_number=phone_number
            )
            selected_address.save()

        # Save address in session for place_order
        req.session['address_id'] = selected_address.id

        return redirect(cart_place_order)

    return render(req, 'user/cart_order.html', {
        'cart_items': cart_items,
        'user_address': user_address
    })


def cart_place_order(req):
    cart_items = Cart.objects.filter(user=req.user)
    address_id = req.session.get('address_id')

    if not address_id or not cart_items.exists():
        messages.error(req, "Order cannot be placed. Address missing or cart empty.")
        return redirect('cart_view')

    user_address = Address.objects.get(id=address_id)

    for item in cart_items:
        Buy.objects.create(
            user=req.user,
            cake=item.cake,  # Assuming Cart has ForeignKey to Cake
            price=item.cake.price,
            address=user_address
        )

    # Clear cart after placing order
    cart_items.delete()
    del req.session['address_id']  # Clear session data

    messages.success(req, "Order placed successfully!")
    return redirect(user_view_bookings)
