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

# def home(req):
#     return render(req,'home.html')


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


# def view_cupcake(req):
#         cake_category = Category.objects.get(name='CupCakes')
#         cupcakes = Cake.objects.filter(category=cake_category)

#         paginator = Paginator(cupcakes, 6)  
#         page_number = req.GET.get('page')  
#         page_obj = paginator.get_page(page_number)

#         return render(req, 'user/cake.html', {'page_obj': page_obj})
 

# def view_layercake(req):
#         cake_category = Category.objects.get(name='Layer Cakes')
#         layercakes = Cake.objects.filter(category=cake_category)

#         paginator = Paginator(layercakes, 6)
#         page_number = req.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         return render(req, 'user/cake.html', {'page_obj': page_obj})
  

# def view_onelayercake(req):
#         cake_category = Category.objects.get(name='One Tier Party Cakes')
#         onelayercakes = Cake.objects.filter(category=cake_category)

#         paginator = Paginator(onelayercakes, 6)
#         page_number = req.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         return render(req, 'user/cake.html', {'page_obj': page_obj})
  

# def view_twolayercake(req):
#         cake_category = Category.objects.get(name='Two Tier Party Cakes')
#         twolayercakes = Cake.objects.filter(category=cake_category)

#         paginator = Paginator(twolayercakes, 6)
#         page_number = req.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         return render(req, 'user/cake.html', {'page_obj': page_obj})


def about_us(req):
    return render(req,'about_us.html') 

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

def delete_cupcake(req,id):
        data=Cake.objects.get(pk=id)
        url=data.img.url
        url=url.split('/')[-1]
        os.remove('media/'+url)  
        data.delete()
        return redirect(shop_home) 

# def bookings(req):
#     bookings=Buy.objects.all()[::-1][:10]
#     return render(req,'shop/bookings.html',{'data':bookings})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Buy, User, Category, Cake
# import os
def admin_bookings(req):
    user = User.objects.all()
    data = Buy.objects.select_related('address', 'cake', 'user', 'cake__category').all()[::-1]
    category = Category.objects.all()
    total_profit = sum(item.price * item.quantity for item in data)

    return render(req, 'shop/admin_bookings.html', {
        'user': user,
        'data': data,
        'category': category,
        'total_profit': total_profit
    })


def cancel_order(req, order_id):
    order = get_object_or_404(Buy, pk=order_id)
    order.delete()
    return redirect("admin_bookings")

# def confirm_order(request, order_id):
#     order = get_object_or_404(Buy, pk=order_id)
    
#     if not order.is_confirmed:
#         order.is_confirmed = True
#         order.save()

#         subject = "Order Confirmation"
#         message = f"Dear {order.user.first_name},\n\nYour order ({order.cake.name}) has been confirmed. Thank you for shopping with us!\n\nBest regards,\nDreamy Delights Team"

#         recipient_email = order.user.email  

#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [recipient_email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print(f"Email sending failed: {e}")

#     return redirect(admin_bookings)


def confirm_order(request, order_id):
    order = get_object_or_404(Buy, pk=order_id)

    if not order.is_confirmed:
        order.is_confirmed = True
        order.save()

        if not order.user or not order.user.email:
            print("Error: User does not have an email address!")
            return redirect('admin_bookings')  # Prevent sending an email to avoid errors

        recipient_email = order.user.email
        print(f"Attempting to send email to: {recipient_email}")  # Debugging

        subject = "Order Confirmation"
        message = f"""
        Dear {order.user.first_name},

        Your order ({order.cake.name}) has been confirmed.
        Thank you for shopping with us!

        Best regards,
        Dreamy Delights Team
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],  # Sends to the user
                fail_silently=False,
            )
            print("Email sent successfully!")  # Debugging
        except Exception as e:
            print(f"Email sending failed: {e}")  # Debugging

    return redirect(admin_bookings)

# def bookings(req):
#     bookings = Buy.objects.all().order_by('-id')[:10]
#     return render(req, 'shop/bookings.html', {'data': bookings})



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
         

# def add_to_cart(req,id):
#      Product=Cake.objects.get(pk=id)
#      print(Product)
#      user=User.objects.get(username=req.session['user'])
#      print(user)
#      data=Cart.objects.create(user=user,cake=Product)
#      data.save()
#      return redirect(cart_display)


def add_to_cart(req, id):
    if 'user' not in req.session:  
        return redirect('login')

    user = get_object_or_404(User, username=req.session['user'])
    cake = get_object_or_404(Cake, pk=id)

    cart_item = Cart.objects.filter(user=user, cake=cake).first()

    if cart_item:
        cart_item.quantity += 1 
        cart_item.save()
    else:
        Cart.objects.create(user=user, cake=cake, quantity=1)  

    return redirect(cart_display)


# def cart_display(req):
#     user=User.objects.get(username=req.session['user'])
#     data=Cart.objects.filter(user=user)
#     return render(req,'user/cart_display.html',{'data':data})  


def delete_cart(req,id):
    data=Cart.objects.get(pk=id) 
    data.delete()
    return redirect(cart_display)

def buy_pro(req,id):
    cake=Cake.objects.get(pk=id)
    return redirect(address_page, id=id)

# def address_page(req, id):
#     cake = Cake.objects.get(id=id)
#     user = User.objects.get(username=req.session['user'])  

#     user_address = Address.objects.filter(user=user).order_by('-id').first()

#     if req.method == 'POST':
#         name = req.POST.get('name')
#         address = req.POST.get('address')
#         phone_number = req.POST.get('phone_number')
#         quantity = req.POST.get('quantity')  

#         Address.objects.filter(user=user).update(name=name, address=address, phone_number=phone_number)

#         req.session['cake'] = id
#         req.session['quantity'] = quantity 

#         return redirect(order_payment)  

#     return render(req, 'user/order_details.html', {
#         'cake': cake,
#         'user_address': user_address  
#     })
def address_page(req, id):
    cake = Cake.objects.get(id=id)
    user = User.objects.get(username=req.session['user'])  
    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')
        quantity = req.POST.get('quantity')  

        # Convert quantity to integer
        if quantity.isdigit():
            quantity = int(quantity)
        else:
            quantity = 1  # Default to 1 if invalid

        Address.objects.filter(user=user).update(name=name, address=address, phone_number=phone_number)

        req.session['cake'] = id
        req.session['quantity'] = quantity  # ✅ Store as integer

        print(f"DEBUG: Stored in session -> Cake: {req.session['cake']}, Quantity: {req.session['quantity']}")  # Debugging

        return redirect(order_payment)  

    return render(req, 'user/order_details.html', {
        'cake': cake,
        'user_address': user_address  
    })

@login_required
def order_payment(req):
    if 'user' in req.session:
        user = get_object_or_404(User, username=req.session['user'])
        cake = Cake.objects.get(pk=req.session['cake'])
        quantity = int(req.session.get('quantity', 1))  
        total_amount = cake.price * quantity  

        print(f"DEBUG: order_payment -> Cake: {cake.id}, Quantity: {quantity}")  # Debugging

        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order = razorpay_client.order.create({
            "amount": int(total_amount * 100),  
            "currency": "INR",
            "payment_capture": "1"
        })

        order = Order.objects.create(
            user=user,
            price=total_amount,  
            provider_order_id=razorpay_order['id']
        )
        
        req.session['order_id'] = order.pk  

        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        })
    
    return redirect(login)

# @login_required
# def order_payment(req):
#     if 'user' in req.session:
#         user = get_object_or_404(User, username=req.session['user'])
#         cake = Cake.objects.get(pk=req.session['cake'])
#         quantity = int(req.session.get('quantity', 1))  
#         total_amount = cake.price * quantity  

#         razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         razorpay_order = razorpay_client.order.create({
#             "amount": int(total_amount * 100),  
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         order = Order.objects.create(
#             user=user,
#             price=total_amount,  
#             provider_order_id=razorpay_order['id']
#         )
        
#         req.session['order_id'] = order.pk  

#         return render(req, "user/payment.html", {
#             "callback_url": "http://127.0.0.1:8000/callback/",
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "order": order,
#         })
    
#     return redirect(login)  


# @login_required
# def pay(req):
#     user = get_object_or_404(User, username=req.session['user'])
#     cake = Cake.objects.get(pk=req.session['cake'])


#     if not cake:
#         messages.error(req, "Your cart is empty. Please add a cake first.")
#         return redirect('cart_display')

#     cake = cake
#     quantity = int(req.GET.get('quantity', 1))
#     order_id = req.session.get('order_id')
#     order = get_object_or_404(Order, pk=order_id) if order_id else None
#     print(cake)


#     if req.method == 'GET':
#         user_address = Address.objects.filter(user=user).order_by('-id').first()

#         data = Buy.objects.create(
#             user=user,
#             cake=cake,
#             # price=cake.price * quantity, 
#              price=cake.price,  # Store only per-unit price
#              quantity=quantity,  
#             address=user_address,
#             order=order
#         )
#         data.save()

#         return redirect(view_bookings)

#     return render(req, 'user/view_bookings.html')

@login_required
def pay(req):
    user = get_object_or_404(User, username=req.session['user'])
    cake = Cake.objects.get(pk=req.session['cake'])

    quantity = int(req.session.get('quantity', 1))  # Retrieve quantity
    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id) if order_id else None

    print(f"DEBUG: pay -> Cake: {cake.id}, Quantity: {quantity}")  # Debugging

    if req.method == 'GET':
        user_address = Address.objects.filter(user=user).order_by('-id').first()

        # data = Buy.objects.create(
        #     user=user,
        #     cake=cake,
        #     price=cake.price * quantity,  
        #     quantity=quantity,  # ✅ Ensure quantity is stored
        #     address=user_address,
        #     order=order
        # )
        data = Buy.objects.create(
            user=user,
            cake=cake,
            price=cake.price,  # ✅ Fix this! Store only the unit price.
            quantity=quantity,  # ✅ Ensure correct quantity is stored
            address=user_address,
            order=order
        )

        data.save()

        return redirect(view_bookings)

    return render(req, 'user/view_bookings.html')


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect(pay)
    

    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay)


def place_order(req,id):
    Product=Cake.objects.get(pk=id)
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.create(user=user,cake=Product)
    data.save()
    return redirect(user_home)


# def user_view_bookings(req):
#     user=User.objects.get(username=req.session['user'])
#     data=Buy.objects.filter(user=user)[::-1]
#     return render(req,'user/view_bookings.html',{'data':data}) 

# def view_bookings(req):
#     user = User.objects.get(username=req.session['user'])
    
#     data1 = Buy.objects.filter(user=user).select_related('cake', 'cake__category').order_by('-id')

#     for booking in data1:
#         price = booking.cake.price  
#         booking.total_price = price * booking.quantity  

#     context = {
#         'data1': data1,
#     }
#     return render(req, 'user/view_bookings.html', context)
# def view_bookings(req):
#     user = User.objects.get(username=req.session['user'])
    
#     data1 = Buy.objects.filter(user=user).select_related('cake', 'cake__category').order_by('-id')

#     for booking in data1:
#         booking.total_price = booking.cake.price * booking.quantity  

#     context = {
#         'data1': data1,
#     }
#     return render(req, 'user/view_bookings.html', context)

def view_bookings(req):
    user = User.objects.get(username=req.session['user'])
    
    data1 = Buy.objects.filter(user=user).select_related('cake', 'cake__category').order_by('-id')

    # Ensure quantity is used correctly
    for booking in data1:
        booking.total_price = booking.price * booking.quantity  # ✅ Correct calculation

    context = {
        'data1': data1,
    }
    return render(req, 'user/view_bookings.html', context)



def user_orders(request):
    user = User.objects.get(username=request.session['user'])
    orders = Buy.objects.filter(user=user).select_related('cake', 'cake__category').order_by('-id')

    for order in orders:
        print(f"Order ID: {order.id}, Is Confirmed: {order.is_confirmed}")

    return render(request, 'user/view_bookings.html', {'data1': orders})



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
            cake=item.cake,  
            price=item.cake.price,
            address=user_address
        )

    cart_items.delete()
    del req.session['address_id']  

    messages.success(req, "Order placed successfully!")
    return redirect(view_bookings)



# @login_required
# def order_payment2(req):
#     if 'user' in req.session:
#         user = get_object_or_404(User, username=req.session['user'])
#         cart_items = Cart.objects.filter(user=req.user)

#         amount = 0

#         for cart_item in cart_items:
#             if cart_item.cake:  # Ensure the cart item has a cake (which it should)
#                 amount += cart_item.cake.price  # Add the price of the cake to the total amount

#         # Print the total amount for debugging purposes
#         print(f"Total amount: {amount}")

#         # Razorpay client setup
#         razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         razorpay_order = razorpay_client.order.create({
#             "amount": int(amount) * 100,  # Convert amount to paise (1 INR = 100 paise)
#             "currency": "INR",    
#             "payment_capture": "1"
#         })

#         order_id = razorpay_order['id']
#         order = Order.objects.create(
#             user=user,
#             price=amount,
#             provider_order_id=razorpay_order['id']
#         )
#         order.save()

#         req.session['order_id'] = order.pk

#         return render(req, "user/payment.html", {
#             "callback_url": "http://127.0.0.1:8000/callback2/",
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "order": order,
#         })
#     else:
#         return redirect('login')


# @login_required
# def pay2(req):
#     user = get_object_or_404(User, username=req.session['user'])

#     cart_items = Cart.objects.filter(user=req.user)

#     if not cart_items.exists():
#         messages.error(req, "Your cart is empty. Please add a cake first.")
#         return redirect(cart_display)

#     quantity = int(req.GET.get('quantity', 1))

#     total_price = sum(item.cake.price * quantity for item in cart_items)

#     order_id = req.session.get('order_id')
#     order = get_object_or_404(Order, pk=order_id) if order_id else None

#     if req.method == 'GET':
#         user_address = Address.objects.filter(user=user).order_by('-id').first()

#         for item in cart_items:
#             Buy.objects.create(
#                 user=user,
#                 cake=item.cake,
#                 quantity=quantity,  
#                 price=item.cake.price * quantity,  
#                 address=user_address,
#                 order=order
#             )

#         cart_items.delete()

#         return redirect(view_bookings)

#     return render(req, 'user/view_bookings.html', {
#         'total_price': total_price,
#         'cart_items': cart_items
#     })



# @csrf_exempt
# def callback2(request):
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

#         if verify_signature(request.POST):
#             order.status = PaymentStatus.SUCCESS
#         else:
#             order.status = PaymentStatus.FAILURE

#         order.save()
#         return redirect(pay2)
    

#     else:
#         payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
#         provider_order_id = payment_data.get("order_id", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.status = PaymentStatus.FAILURE
#         order.save()

#         return redirect(pay2)
    

# -------------------------------------------------------------------------------------------


@login_required
def cart_address_page(req):
    user = get_object_or_404(User, username=req.session['user'])
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.error(req, "Your cart is empty. Please add items first.")
        return redirect('cart_display')

    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        Address.objects.filter(user=user).update(name=name, address=address, phone_number=phone_number)

        req.session['cart_items'] = list(cart_items.values_list('id', flat=True))

        return redirect(order_payment2)

    return render(req, 'user/cart_order.html', {
        'cart_items': cart_items,
        'user_address': user_address
    })

@login_required
def order_payment2(req):
    if 'user' in req.session:
        user = get_object_or_404(User, username=req.session['user'])
        cart_items = Cart.objects.filter(id__in=req.session.get('cart_items', []))

        if not cart_items.exists():
            return redirect('cart_display')

        total_amount = sum(cart.cake.price * cart.quantity for cart in cart_items)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        order = Order.objects.create(
            user=user,
            price=total_amount,
            provider_order_id=razorpay_order['id']
        )

        req.session['order_id'] = order.pk

        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback2/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        })

    return redirect('login')

@login_required
def pay2(req):
    user = get_object_or_404(User, username=req.session['user'])
    cart_items = Cart.objects.filter(id__in=req.session.get('cart_items', []))

    if not cart_items.exists():
        messages.error(req, "Your cart is empty. Please add items first.")
        return redirect(cart_display)

    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id) if order_id else None

    user_address = Address.objects.filter(user=user).order_by('-id').first()

    for cart in cart_items:
        Buy.objects.create(
            user=user,
            cake=cart.cake,
            price=cart.cake.price * cart.quantity,
            quantity=cart.quantity,
            address=user_address,
            order=order
        )

    cart_items.delete() 

    return redirect(view_bookings)


@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect(pay2)
    

    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay2)

@login_required
def cart_display(request):
    cart_items = Cart.objects.filter(user=request.user)  
    return render(request, "user/cart_display.html", {"cart_items": cart_items})


def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(cart_display)

def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect(cart_display)



def delete_order(req,id):
    data=Buy.objects.get(pk=id)
    data.delete()
    return redirect(view_bookings)