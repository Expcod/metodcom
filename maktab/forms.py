from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        }),
        label="Telefon raqam"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting'
        }),
        label="Parol"
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Telefon raqam formatini tekshirish
        if username:
            # Faqat raqamlarni qoldirish
            phone_clean = re.sub(r'\D', '', username)
            if len(phone_clean) >= 9:
                if phone_clean.startswith('998'):
                    return '+' + phone_clean
                else:
                    return '+998' + phone_clean[-9:]
            else:
                raise forms.ValidationError("Telefon raqam noto'g'ri formatda")
        return username

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingizni kiriting'
        }),
        label="Ism"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiyangizni kiriting'
        }),
        label="Familiya"
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        }),
        label="Telefon raqam"
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Tug'ilgan sana"
    )
    birth_place = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Shahar, viloyat'
        }),
        label="Tug'ilgan joy"
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Rol"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting'
        }),
        label="Parol"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting'
        }),
        label="Parolni tasdiqlash"
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'birth_date', 'birth_place', 'role', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Telefon raqam formatini standardlash
            phone_clean = re.sub(r'\D', '', phone_number)
            if len(phone_clean) >= 9:
                if phone_clean.startswith('998'):
                    formatted_phone = '+' + phone_clean
                else:
                    formatted_phone = '+998' + phone_clean[-9:]
                
                # Mavjud telefon raqamini tekshirish
                if CustomUser.objects.filter(phone_number=formatted_phone).exists():
                    raise forms.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
                
                return formatted_phone
            else:
                raise forms.ValidationError("Telefon raqam noto'g'ri formatda")
        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmaydi.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_date = self.cleaned_data['birth_date']
        user.birth_place = self.cleaned_data['birth_place']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
