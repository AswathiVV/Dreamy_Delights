from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('shop_login',views.shop_login),
    path('register',views.register),
    path('logout',views.shop_logout),
# ------------------Admin--------------------------------
    path('shop_home',views.shop_home),
    path('add_cupcake',views.add_cupcake),
    path('cupcake',views.cupcake),
    path('edit_cupcake/<id>',views.edit_cupcake),
    path('delete_cupcake/<id>',views.delete_cupcake),


# #------------------------------------- User--------------------------------------------------------------
    path('user_home',views.user_home),
    path('view_cupcake',views.view_cupcake),
    ]