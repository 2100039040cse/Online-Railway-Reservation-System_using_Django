from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    email = forms.EmailField()

class PassengerForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=10)
    nationality = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=200)
    berth = forms.CharField(max_length=20)
    acCategory = forms.CharField(max_length=20)