
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .utilities import timestapppp
class AbvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Subscribe?')



    class Meta(AbstractUser.Meta):
        pass
# Create your models here.
    def __str__(self) -> str:
        return self.username

class UserData(models.Model):
    address = models.CharField(max_length=200, verbose_name='Address', blank=True)
    postcode = models.CharField(max_length=80, blank=True, verbose_name='PostCode')
    country = models.CharField(max_length=60, verbose_name='Country',blank=True)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = False, verbose_name='Phone Number', blank=True)
    name = models.CharField(max_length=60, verbose_name='Name',blank=True)
    userr = models.ForeignKey(AbvUser,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Data'
        verbose_name_plural = 'User Data'
    
    def user_first_name(self):
        return self.userr.first_name
    
    def user_last_name(self):
        return self.userr.last_name

    def user_name(self):
        return self.userr.username
    def email(self):
        return self.userr.email

class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Name',default=None, unique=True)
    is_active = models.BooleanField(default=False, verbose_name='In job?')

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = ['name']
    
    def __str__(self):
        return self.name
class Types(models.Model):
    name = models.CharField(max_length=40,verbose_name='name',default=None, unique=True)
    is_active = models.BooleanField(default=False, verbose_name='In job?')

    class Meta:
        verbose_name_plural = 'Types'
        verbose_name = 'Type'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80,verbose_name='Name',default=None)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    description = models.CharField(max_length=200, verbose_name='Description',default=None)
    image = models.ImageField(blank=True, verbose_name='Image', upload_to=timestapppp)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0 ,verbose_name='Price')
    is_active = models.BooleanField(default=True, verbose_name='In shop list?')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Create')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    types = models.ForeignKey(Types, on_delete=models.PROTECT, verbose_name='Type')

    def category_name(self):
        return self.category.name

    def delete(self, *args, **kwargs):
        for i in self.additionalimage_set.all():
            i.delete()
        super().delete(*args, **kwargs)

    
    class Meta:
        index_together  = (('id','slug'),)
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering=['create_at']


    def __str__(self):
        return self.name

class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='P')
    image = models.ImageField(upload_to=timestapppp, verbose_name='Image')

    class Meta:
        verbose_name='AddImage'

class BuyData(models.Model):
    name = models.CharField(max_length=40, verbose_name='Name',default=None)
    link = models.CharField(unique=True, verbose_name='Link', max_length=400)

    is_active=models.BooleanField(verbose_name='Is active', default=True)
    class Meta:
        verbose_name = 'Buy Data'
        verbose_name_plural = 'Buy Datas'
        ordering = ['is_active']

    def __str__(self):
        return self.name

class About(models.Model):
    text = models.CharField(default=None, verbose_name='Text', max_length=200)
    link = models.CharField(verbose_name='Link Video', default=None, max_length=200)
    is_active = models.BooleanField(default=False,verbose_name='In page?')

    

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
        ordering = ['-is_active']

    def __str__(self):
        return self.text