from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('login',views.shop_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout',views.shop_logout),
    path('view_cupcake',views.view_cupcake),
    path('view_layercake',views.view_layercake),    
    path('view_onelayercake',views.view_onelayercake), 
    path('view_twolayercake',views.view_twolayercake), 
    path('about_us',views.about_us),
    path('visit_us',views.visit_us),
    path('collections',views.collections),


# ------------------Admin--------------------------------
    path('shop_home',views.shop_home),
    path('cupcake',views.cupcake),
    path('layercake',views.layercake),
    path('onelayercake',views.onelayercake),
    path('twolayercake',views.twolayercake),

    path('add_cake',views.add_cake),
    path('edit_cupcake/<id>',views.edit_cake),
    path('delete_cupcake/<id>',views.delete_cupcake),
    # path('bookings',views.bookings),
    # path('search_admin',views.search_admin),
    path('search_admin/', views.search_admin, name='search_admin'),
    path('admin_bookings',views.admin_bookings),
    path('cancel_order/<order_id>',views.cancel_order, name='cancel_order'),
    path('confirm_order/<order_id>',views.confirm_order, name='confirm_order'),




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
    path('buy_pro/<id>',views.buy_pro,name='buy_pro'),
    path('address_page/<id>',views.address_page, name='address_page'),
    path('place_order/<id>',views.place_order), 
    # path('order_success',views.success),
    # path('search',views.search),
    path('search/', views.search, name='search'),


    path('user_view_bookings',views.view_bookings),
    path('user_orders',views.user_orders),

     
    path('order_payment', views.order_payment, name='order_payment'),
    path('pay', views.pay, name='pay'),
     
    path('callback/', views.callback, name='callback'),
     

   
    path('profile/', views.profile_view, name='profile_view'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('update_profile', views.update_profile, name='update_profile'),
    # path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase'),
    path('cart_address_page/', views.cart_address_page, name='cart_address_page'),
    path('cart_place_order', views.cart_place_order, name='cart_place_order'),

    path('order_payment2', views.order_payment2, name='order_payment2'),
    path('pay2', views.pay2, name='pay2'),
    path('callback2/', views.callback2, name='callback2'),


]