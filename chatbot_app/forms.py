from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FAQ


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        required=True
    )

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

class LoginForm(forms.Form):

    username = forms.CharField(max_length=100)

    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class FAQForm(forms.ModelForm):

    class Meta:
        model = FAQ
        fields = "__all__"