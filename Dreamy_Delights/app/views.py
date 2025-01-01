from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone


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

def  register(req):
     if req.method=='POST':
        name=req.POST['name']       
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Eshop registration', 'E_shop account created', settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits")
            return redirect(register)
     else:
         return render(req,'register.html')


def view_cupcake(req):
    # if 'user' in req.session:
        cake_category=Category.objects.get(name='CupCakes')
        cupcakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/cupcake.html',{'cupcake': cupcakes})
    # else:
    #     return redirect(shop_login)
    
def view_layercake(req):
    if 'user' in req.session:
        cake_category=Category.objects.get(name='Layer Cakes')
        layercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/layercake.html',{'layercake': layercakes})
    # else:
    #     return redirect(shop_login)      


def view_onelayercake(req):
    # if 'user' in req.session:
        cake_category=Category.objects.get(name='One Tier Party Cakes')
        onelayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/onelayercake.html',{'onelayercake': onelayercakes})
    # else:
    #     return redirect(shop_login)   
    
def view_twolayercake(req):
    # if 'user' in req.session:
        cake_category=Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/twolayercake.html',{'twolayercake': twolayercakes})
    # else:
    #     return redirect(shop_login)  

# def view_cakes(req,id):
#      if 'user' in req.session:
#          user=User.objects.get(username=req.session['user'])
#          cake=Cake.objects.get(pk=id)
    #  try:
    #      cart=Cart.objects.get(Cake=cake,user=user)
    #  except:
    #      cart=None    
    #  return render(req,'user/view_cakes.html',{'cake':cake})     
# def home_cupcake(req):
#     if 'user' in req.session:
#         cupcakes=Cake.objects.all()
#         return render(req,'user/view_cake.html',{'cupcake': cupcakes})
#     else:
#         return redirect(shop_login)     


#--------------------- admin-------------------------------------------------------------------------------------------  


def shop_home(req):
    if 'shop' in req.session:
        # cupcake=CupCake.objects.all()
        return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login)
      
def cupcake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='CupCakes')
        cupcakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/cupcake.html',{'cupcake': cupcakes})
    else:
        return redirect(shop_login)  
    
def layercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='Layer Cakes')
        layercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/layercake.html',{'layercake': layercakes})
    else:
        return redirect(shop_login)   
    
def onelayercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='One Tier Party Cakes')
        onelayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/onelayercake.html',{'onelayercake': onelayercakes})
    else:
        return redirect(shop_login)   
    
def twolayercake(req):
    if 'shop' in req.session:
        cake_category=Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'shop/twolayercake.html',{'twolayercake': twolayercakes})
    else:
        return redirect(shop_login)      
           

def add_cupcake(req):
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

    return render(req, 'shop/add_cupcake.html')
    
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


def edit_cake(req,id):
        cake = Cake.objects.get(pk=id)

        if req.method == 'POST':
            name = req.POST['name']
            price = req.POST['price']
            file = req.FILES.get('img')  
            cat = req.POST['category']
            qty = req.POST['quantity']
            des = req.POST['description']
            
            print(file)
            if file:
                Cake.objects.filter(pk=id).update(name=name,price=price,img=file,category=cat,quantity=qty,description=des)   
            else:
                Cake.objects.filter(pk=id).update(name=name,price=price,category=cat,quantity=qty,description=des)   

            return redirect(shop_home)
        return render(req,'shop/edit_cupcake.html',{'data':cake}) 
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
        cake_category=Category.objects.get(name='CupCakes')
        cupcakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/cupcake.html',{'cupcake': cupcakes})
    else:
        return redirect(shop_login)
    
def user_layercake(req):
    if 'user' in req.session:
        cake_category=Category.objects.get(name='Layer Cakes')
        layercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/layercake.html',{'layercake': layercakes})
    else:
        return redirect(shop_login)      


def user_onelayercake(req):
    if 'user' in req.session:
        cake_category=Category.objects.get(name='One Tier Party Cakes')
        onelayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/onelayercake.html',{'onelayercake': onelayercakes})
    else:
        return redirect(shop_login)   
    
def user_twolayercake(req):
    if 'user' in req.session:
        cake_category=Category.objects.get(name='Two Tier Party Cakes')
        twolayercakes=Cake.objects.filter(category=cake_category)
        return render(req,'user/twolayercake.html',{'twolayercake': twolayercakes})
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
    return redirect(address_page)

# views.py



def address_page(req,id):
    cake = Cake.objects.get(id=id)
    
    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        user_address = Address(user=req.user, name=name, address=address, phone_number=phone_number)
        user_address.save()

        buy = Buy(user=req.user, cake=cake, price=cake.price, address=user_address)
        buy.save()

        return redirect(success) 

    return render(req, 'user/order_details.html', {
        'cake': cake,
    })

def place_order(req,id):
    Product=Cake.objects.get(pk=id)
    user=User.objects.get(username=req.session['user'])
    # price=Product.offer_price
    data=Buy.objects.create(user=user,cake=Product)
    data.save()
    return redirect(user_home)

def success(req):
    return render(req,'user/order_success.html')

# def buy_pro(req,id):
#     Product=Cake.objects.get(pk=id)
#     user=User.objects.get(username=req.session['user'])
#     data=Buy.objects.create(user=user,cake=Product)
#     data.save()
#     return redirect(user_home)
#     return render(req, 'order_details.html', {'cake': Cake, 'user': user})

# def place_order(request):
#     if request.method == 'POST':
#         user = User.objects.get(id=request.POST['user'])
#         cake = Cake.objects.get(id=request.POST['cake'])
#         name = request.POST['name']
#         address = request.POST['address']
        
#         buy = Buy.objects.create(user=user, cake=cake, price=cake.price, name=name, address=address,date=timezone.now())
        
#         return redirect('user_home') 
#     else:
#         return HttpResponse("Invalid request", status=400)
    
    

def user_view_bookings(req):
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/view_bookings.html',{'data':data})         