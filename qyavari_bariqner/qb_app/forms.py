from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .tokens import email_verification_token  # Этот импорт остается


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_confirm = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError(_('Passwords do not match'))
        return password_confirm

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False  # Делаем пользователя неактивным до подтверждения email
        if commit:
            user.save()
            # Импортируем send_verification_email внутри метода
            from qb_app.views import send_verification_email
            send_verification_email(user)  # Отправляем письмо с верификацией
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
