from rest_framework import serializers
from kind.models import Product

class ProductList(serializers.ModelSerializer):
    class Meta:
        fields = ('id','image','price','category_name')
        model = Product

