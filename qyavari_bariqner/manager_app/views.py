from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from qb_app import models
from django.db.models import Sum, F


def is_superuser(user):
    return user.is_superuser

def manager_login(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access the manager login page.')
        return redirect('home')

    if request.method == 'POST':
        form = forms.ManagerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('manager_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = forms.ManagerLoginForm()  

    return render(request, 'manager_login.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def manager_dashboard(request):
    all_profiles = models.UserProfile.objects.all()
    active_threshold = timezone.now() - timedelta(minutes=15)

    print(f'total profiles: {all_profiles.count()}')

    orders = models.Order.objects.annotate(
        total_price=Sum(F('orderitem__price') * F('orderitem__quantity'))
    )

    active_profiles = all_profiles.filter(
        last_activity__gte=active_threshold
    ).exclude(last_logout__gte=F('last_activity'))

    inactive_profiles = all_profiles.exclude(pk__in=active_profiles)

    return render(request, 'manager_dashboard.html', {
        'profiles': all_profiles,
        'active_profiles': active_profiles,
        'inactive_profiles': inactive_profiles,
        'orders': orders
    })


@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=order_id)
        order.delete()
        return redirect('manager_dashboard')  
    else:
        return redirect('manager_dashboard')  
    
    