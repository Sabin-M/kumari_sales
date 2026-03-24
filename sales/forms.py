from django import forms
from django.contrib.auth.models import User


class PostForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Gmail address'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create Password'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    # 🔥 Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail addresses are allowed.")

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already registered.")

        return email

    # 🔥 Full validation
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Name validation
        if name and len(name) < 5:
            self.add_error('name', 'Minimum 5 characters required.')

        # Password validation
        if password:
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")

            if password.isdigit():
                self.add_error('password', "Password cannot be only numbers.")

            if password.isalpha():
                self.add_error('password', "Password must contain at least one number.")

            if password.lower() == password:
                self.add_error('password', "Must contain at least one CAPITAL letter.")

            if password.upper() == password:
                self.add_error('password', "Must contain at least one small letter.")

        # Confirm password
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )