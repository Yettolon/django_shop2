from re import search
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import AbvUser, UserData, AdditionalImage, Product, Types,BuyData, Category, About
from .forms import ProductCategoryForm

@admin.register(AbvUser)
class AbvUserAdmin(admin.ModelAdmin):
    list_display = ('username','email')
    ordering = ['is_activated','username']
    search_fields = ('username','email')

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user_name','phoneNumber','country')
    list_display_links = ('user_name',)

    search_fields = ('user_name', 'phoneNumber')
    list_per_page = 50

# Register your models here.
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('text','is_active')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','imageee','category','types','is_active','create_at')
    def categoryyy(self,obj):
        return '%s - %s' % (obj.category.super_category.name, obj.category.name)
    categoryyy.short_description = 'Category'
    form = ProductCategoryForm
    


    list_display_links = ('name','imageee')
    def imageee(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60'/>".format(obj.image.url))
        return "None"
    imageee.short_description = "Image"
    ordering = ['-create_at',]
    inlines = (AdditionalImageInline,)
    search_fields = ('name','description')
    list_per_page = 50


@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    search_fields = ('name',)
    ordering = ['-is_active']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    search_fields = ('name',)
    ordering = ['-is_active']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    search_fields = ('name',)

@admin.register(BuyData)
class BuyDataAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','link')
    list_display_links = ('name',)
    search_fields = ('name',)

