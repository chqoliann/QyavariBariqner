from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib.auth import login, logout, authenticate


def home(request):
    prods = models.Product.objects.all()
    types = models.Type.objects.all()
    return render(request, 'index.html', {'product': prods, 'types': types})


def register_view(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = forms.RegistrationForm
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = forms.LoginForm
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')