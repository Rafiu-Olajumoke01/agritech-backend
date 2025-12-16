from django.contrib import admin
from django.urls import path

# Users
from users.views import signup, login, get_user, update_user, delete_user

# Farmers
from farmers.views import (
    create_farmer, get_farmer, update_farmer, get_my_products,
    create_product, list_products, update_product, delete_product
)

# Buyers
from buyers.views import create_buyer, get_buyer, update_buyer

# Content
from content.views import (
    create_content, list_content, get_content,
    update_content, delete_content
)

# Orders
from orders.views import (
    create_order, get_my_orders, get_farmer_orders,
    update_order, delete_order
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------------- User endpoints ----------------
    path('api/users/signup/', signup, name='signup'),
    path('api/users/login/', login, name='login'),
    path('api/users/<int:user_id>/', get_user, name='get_user'),
    path('api/users/<int:user_id>/update/', update_user, name='update_user'),
    path('api/users/<int:user_id>/delete/', delete_user, name='delete_user'),

    # ---------------- Farmer profile endpoints ----------------
    path('api/farmers/create/', create_farmer, name='create_farmer'),
    path('api/farmers/me/', get_farmer, name='get_farmer'),
    path('api/farmers/update/', update_farmer, name='update_farmer'),

    # ---------------- Farmer product endpoints ----------------
    path('api/farmers/products/', list_products, name='list_products'),       
    path('api/farmers/products/create/', create_product, name='create_product'),
    path('api/farmers/products/my/', get_my_products, name='get_my_products'),
    path('api/farmers/products/<int:product_id>/update/', update_product, name='update_product'),
    path('api/farmers/products/<int:product_id>/delete/', delete_product, name='delete_product'),

    # ---------------- Buyer endpoints ----------------
    path('api/buyers/create/', create_buyer, name='create_buyer'),
    path('api/buyers/me/', get_buyer, name='get_buyer'),
    path('api/buyers/update/', update_buyer, name='update_buyer'),

    # ---------------- Content endpoints ----------------
    path('api/content/create/', create_content, name='create_content'),         
    path('api/content/', list_content, name='list_content'),                     
    path('api/content/<int:content_id>/', get_content, name='get_content'),      
    path('api/content/<int:content_id>/update/', update_content, name='update_content'),  
    path('api/content/<int:content_id>/delete/', delete_content, name='delete_content'),  

    # ---------------- Order endpoints ----------------
    path('api/orders/create/', create_order, name='create_order'),               
    path('api/orders/my/', get_my_orders, name='get_my_orders'),                 
    path('api/orders/farmer/', get_farmer_orders, name='get_farmer_orders'),     
    path('api/orders/<int:order_id>/update/', update_order, name='update_order'),
    path('api/orders/<int:order_id>/delete/', delete_order, name='delete_order'),
]
