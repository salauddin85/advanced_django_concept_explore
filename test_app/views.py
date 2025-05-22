from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from .models import *
from django.db import connection
from .serializers import *
from rest_framework.permissions import AllowAny

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(name__isupper=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)




class BlogViewSet(APIView):
    # permission_classes = [AllowAny]
    def get(self, request):
        blogs = Blog.objects.all()
        # print(blogs.query)
        # for blog in blogs:
        #     print(blog.author)
        
        # blogs = list(Blog.objects.iterator())
        # print(blogs.explain()) 
        # print(blogs.query)
        # for blog in blogs:
            # print(blog.author)
        # for query in connection.queries:
        #      print(query["sql"])
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)



class TeamView(APIView):
    def get(self,request,user_id):
        try:
            user = User.objects.get(pk = user_id)
            overall_info = Team.objects.filter(user = user)
           
            serializer = TeamSerializer(overall_info,many = True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response("User Does not exist") 
        except Exception as e:
            return Response(str(e))