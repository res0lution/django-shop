from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Your full name"}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Your email"}
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Your message"}
    ))

    def clean_email(self):
        data = self.cleaned_data["email"]

        if not "gmail.com" in data:
            raise forms.ValidationError("Email has to be gmail")

        return data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password != password2:
            raise forms.ValidationError("Passwords must mutch")

        return data
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError("Username is taken")

        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("Email is taken")

        return email
    
    
