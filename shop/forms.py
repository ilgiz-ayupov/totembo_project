from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils import timezone

from django.utils.translation import ugettext as _
from .models import Customers, Orders


# Аунтефикация - процесс входа в систему
# Авторизация - процесс выдачи прав

class CustomersRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control"
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control"
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Customers
        fields = ("first_name", "last_name", "username", "email", "address", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


class CustomersLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autocomplete": "username",
        "id": "login_username",
        "class": "form-control"
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            "class": "form-control"
        }),
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ("username", "first_name", "last_name", "address", "currency")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ("first_name", "last_name", "address", "phone", "comment", "time_order")
        widgets = {
            "time_order": forms.TextInput(attrs={
                "type": "date",
                "min": timezone.now().date()
            })
        }
