from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_login, name='manager_login'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard')
]

