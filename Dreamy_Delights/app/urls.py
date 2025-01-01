from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('shop_login',views.shop_login),
    path('register',views.register),
    path('logout',views.shop_logout),
    path('view_cupcake',views.view_cupcake),
    path('view_layercake',views.view_layercake),    
    path('view_onelayercake',views.view_onelayercake), 
    path('view_twolayercake',views.view_twolayercake), 
    # path('view_cakes/<id>',views.view_cakes),
# ------------------Admin--------------------------------
    path('shop_home',views.shop_home),
    path('cupcake',views.cupcake),
    path('layercake',views.layercake),
    path('onelayercake',views.onelayercake),
    path('twolayercake',views.twolayercake),

    path('add_cupcake',views.add_cupcake),
    path('edit_cupcake/<id>',views.edit_cake),
    path('delete_cupcake/<id>',views.delete_cupcake),
    path('bookings',views.bookings),


# #------------------------------------- User--------------------------------------------------------------
    path('user_home',views.user_home),
    path('user_cupcake',views.user_cupcake),
    path('user_layercake',views.user_layercake),    
    path('user_onelayercake',views.user_onelayercake), 
    path('user_twolayercake',views.user_twolayercake), 
    path('view_cake/<id>',views.view_cake),   
    path('add_to_cart/<id>',views.add_to_cart, name='add_to_cart'),
    path('cart_display',views.cart_display),
    path('delete_cart/<id>',views.delete_cart), 
    path('buy_pro/<id>',views.buy_pro),
    path('address_page/<id>',views.address_page),
    path('place_order/<id>',views.place_order), 
    path('order_success',views.success),

    path('user_view_bookings',views.user_view_bookings),
     
     

   
    
]