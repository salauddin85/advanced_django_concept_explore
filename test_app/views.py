from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(name__isupper=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.permissions import AllowAny

class BlogViewSet(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    



# output:
[
    {
        "id": 1,
        "name": "SHIRT"
    },
    {
        "id": 3,
        "name": "PANTS"
    }
]
# Salauddin