from urllib import request
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


from .permissions import IsAuthorRead
from kind.models import Product
from .serializers import ProductList
@permission_classes((AllowAny,))
class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductList

@permission_classes((IsAuthenticated,IsAuthorRead))
class PostListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True,)
    serializer_class = ProductList
    # Create your views here.
