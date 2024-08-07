from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:prod_id>/', views.prod_detail_view, name='prod_details'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:prod_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart, name='remove_cart')
]

