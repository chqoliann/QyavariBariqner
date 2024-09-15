from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import email_verification_token
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode


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
            models.Cart.objects.create(user=user)
            models.UserProfile.objects.create(user=user)
            send_verification_email(user)
            return redirect('email_confirmation_pending')  # Перенаправляем пользователя на страницу ожидания подтверждения email
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = forms.RegistrationForm()
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
        form = forms.LoginForm()    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def prod_detail_view(request, prod_id):
    prod = get_object_or_404(models.Product, id=prod_id)
    return render(request, 'product_details.html', {'prod': prod})


@login_required
def cart_detail(request):
    cart, created = models.Cart.objects.get_or_create(user=request.user)
    cart_items = models.CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)


    items_with_subtotals = [
        {
            'item': item,
            'subtotal': item.product.price * item.quantity
        }
        for item in cart_items
    ]

    return render(request, 'cart_detail.html', {
        'cart_items': items_with_subtotals,
        'total_price': total_price,
    })

@login_required
@require_POST
def add_to_cart(request, prod_id):
    product = get_object_or_404(models.Product, id=prod_id)
    cart, created = models.Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart_detail')

@login_required
def clear_cart(request):
    cart = get_object_or_404(models.Cart, user=request.user)
    models.CartItem.objects.filter(cart=cart).delete()
    return redirect('cart_detail')


@login_required
def remove_cart(request, item_id):
    cart_item = get_object_or_404(models.CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()

    return redirect('cart_detail')


@login_required
def user_profile_view(request, user_id):
    user_profile = models.UserProfile.objects.get(user_id=user_id)
    return render(request, 'user_profile.html', {'profile': user_profile})


def liked_products_view(request):
    profile = models.UserProfile.objects.get(user=request.user)
    liked_products = profile.liked_products.all()
    return render(request, 'like_products.html', {'liked_products': liked_products})


def like_product(request, prod_id):
    product = models.Product.objects.get(id=prod_id)
    profile, created = models.UserProfile.objects.get_or_create(user=request.user)

    if product in profile.liked_products.all():
        profile.liked_products.remove(product)
    else:
        profile.liked_products.add(product)

    return redirect('like_products')



def send_verification_email(user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
    activation_url = f"http://127.0.0.1:8000/{verification_link}"
    
    send_mail(
        'Verify your email',
        f'Click the following link to verify your email: {activation_url}',
        None,  # Адрес отправителя, например, 'no-reply@example.com'
        [user.email],
        fail_silently=False,
    )



def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Логиним пользователя после успешной активации
        return redirect('email_verification_success')
    else:
        return redirect('email_verification_failed')
  


def email_confirmation_pending(request):
    return render(request, 'email_confirmation_pending.html')


def email_verification_success(request):
    return render(request, 'email_verification_success.html')


def email_verification_failed(request):
    return render(request, 'email_confirmation_failed.html')


