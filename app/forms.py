from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistraion(UserCreationForm):
    email = forms.CharField(label='Email ID', required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name', 'last_name':'Last Name'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control', 'autofocus':True})
        }

class CustomerLogin(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','password']

class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Enter Old Password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','autofocus':True}))
    new_password1 = forms.CharField(label='Enter New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User

class PasswordReset(PasswordResetForm):
    email = forms.CharField(label='Enter Email ID',widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User

class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(label='Enter New Password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control', 'autofocus':True}))
    new_password2 = forms.CharField(label='Confirm New Password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class CustomerProfile(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','pin','state']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'locality': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'pin': forms.NumberInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'})
        }

