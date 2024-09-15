from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate
from . import forms

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def manager_login(request):
    if request.method == 'POST':
        form = forms.ManagerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('manager_dashboard')
    else:
        form = forms.ManagerLoginForm()  # Исправлено

    return render(request, 'manager_login.html', {'form': form})

@user_passes_test(is_superuser)
def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')
