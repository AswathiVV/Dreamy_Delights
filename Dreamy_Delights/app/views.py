from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages


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
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits")
            return redirect(register)
     else:
         return render(req,'register.html')
     

#--------------------- admin-------------------------------------------------------------------------------------------  

def shop_home(req):
    if 'shop' in req.session:
        # cupcake=CupCake.objects.all()
        return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login)  
def cupcake(req):
    if 'shop' in req.session:
        cupcakes=CupCake.objects.all()
        return render(req,'shop/cupcake.html',{'cupcake': cupcakes})
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
        data=CupCake.objects.create(id=id,name=name,price=price,img=file,category=cat,quantity=qty,description=des)   
        data.save()
        return redirect(shop_home)
    return render(req,'shop/add_cupcake.html')     


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        # products=Cake.objects.all()
        return render(req,'user/user_home.html')             
