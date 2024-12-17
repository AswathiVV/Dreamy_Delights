from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings


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
     
# def home_cupcake(req):
#     if 'user' in req.session:
#         cupcakes=CupCake.objects.all()
#         return render(req,'user/view_cupcake.html',{'cupcake': cupcakes})
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
    if req.method=='POST':
        id=req.POST['id']
        name=req.POST['name']       
        price=req.POST['price']            
        file=req.FILES['img']
        cat=req.POST['category']
        qty=req.POST['quantity']
        des=req.POST['description']
        data=Cake.objects.create(id=id,name=name,price=price,img=file,category=cat,quantity=qty,description=des)   
        data.save()
        return redirect(shop_home)
    return render(req,'shop/add_cupcake.html') 



def edit_cupcake(req, id):
    cupcakes = Cake.objects.get(pk=id)

    if req.method == 'POST':
        name = req.POST['name']
        price = req.POST['price']
        file = req.FILES.get('img')  
        cat = req.POST['category']
        qty = req.POST['quantity']
        des = req.POST['description']
        

        if file:
            cupcakes.img = file 

        cupcakes.name = name
        cupcakes.price = price
        cupcakes.category = cat
        cupcakes.quantity = qty
        cupcakes.description = des

        cupcakes.save()

        return redirect('shop_home')

    return render(req, 'shop/edit_cupcake.html', {'data': cupcakes})

def delete_cupcake(req,id):
        data=Cake.objects.get(pk=id)
        url=data.img.url
        url=url.split('/')[-1]
        os.remove('media/'+url)  
        data.delete()
        return redirect(shop_home) 


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
