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
    path('cart/remove/<int:item_id>/', views.remove_cart, name='remove_cart'),
    path('user_profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('product/<int:prod_id>/like/', views.like_product, name='like_product'),
    path('product/like/', views.liked_products_view, name='like_products'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify-email'),
    path('email-confirmation-pending/', views.email_confirmation_pending, name='email_confirmation_pending'),
    path('email-verification-success/', views.email_verification_success, name='email_verification_success'),
    path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),
]
