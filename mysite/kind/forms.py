from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import password_validation
from django.core.mail import send_mail
from mysite.settings import ALLOWED_HOSTS
from django.core.signing import Signer
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm


from .models import AbvUser, Product, Types,Category, UserData



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, label='Login', widget=forms.TextInput(attrs={'class': 'form-control','id':'name','name':'name','placeholder':'Login' }))
    password = forms.CharField(max_length=120, label='Password',  widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','name':'password','placeholder':'Password'}))

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'class': 'form-control','id':'name','name':'name','placeholder':'Email' ,'required':True}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','name':'password','placeholder':'Password','required':True}))
    password2 = forms.CharField(label='Confirm password',  widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','name':'password','placeholder':'Password','required':True}))
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={'class': 'form-control','id':'name','name':'name','placeholder':'Login', 'required':True}))
    
    
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1:
            password_validation.validate_password(password1)

        if password1 and password2 and password2 != password1:
            errors = {'password2': ValidationError('Password don`t match.', code='password_mismatch')}
            raise ValidationError(errors)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated=False
        user.is_active = False
        if commit:
            user.save()
        
        signer = Signer()

        if ALLOWED_HOSTS:
            host = 'http://' + ALLOWED_HOSTS[0]
        else:
            host = 'http://localhost:8000'
        context = {'user':user, 'host' : host, 'sign' : signer.sign(user.username)}
        subject = render_to_string('email/activation_letter_subject.txt', context)
        body_text = render_to_string('email/activation_letter_body.txt', context)


        send_mail(subject,body_text,'from@example.com',[user.email],fail_silently=False)
        return user
    
    
    class Meta:
        model = AbvUser
        fields = ('username','email','password1','password2')

class ConfirmFormPassword(SetPasswordForm):
    new_password1 = forms.CharField(label=("New password"),widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','name':'password','placeholder':'Password'}),strip=False,help_text=password_validation.password_validators_help_text_html(),)
    new_password2 = forms.CharField(label=("New password confirmation"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','name':'password','placeholder':'Confirm your password'}),)
    


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=40, label='',widget=forms.TextInput(attrs={'class':"form-control", 'id':'search_input','placeholder':"Search Here"}))

class ProductCategoryForm(forms.ModelForm):
    category= forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, label='Category', required=True)
    types= forms.ModelChoiceField(queryset=Types.objects.all(), empty_label=None, label='Types', required=False)
    class Meta:
        model = Product
        fields = '__all__'

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(required=True, label='', widget=forms.NumberInput(attrs={'class':"product_count_item input-number",'type':'text','value':'1','min':'0','max':'99'}) )
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)


class UserDetailForm(forms.ModelForm):
    address = forms.CharField(max_length=200, required=True,widget=forms.TextInput(attrs={'class':'post_code','type':'text','placeholder':'Address'}))

    country = forms.CharField(max_length=60,required=True,widget=forms.TextInput(attrs={'class':'post_code','type':'text','placeholder':'Country'}))
    postcode = forms.CharField(max_length=80,required=True,widget=forms.TextInput(attrs={'class':'post_code','type':'text','placeholder':'PostCode'}))
    phoneNumber = forms.CharField(required=True, max_length=16,widget=forms.NumberInput(attrs={'class':'post_code','type':'text','placeholder':'Phone number'}))
    
    name = forms.CharField(max_length=60, label='Name' ,required=True,widget=forms.TextInput(attrs={'class':'post_code','type':'text','placeholder':'Name'}))

    class Meta:
        model = UserData
        fields = ('name','country','address','postcode','phoneNumber')
