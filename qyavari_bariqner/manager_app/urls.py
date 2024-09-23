from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_login, name='manager_login'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order')
]

