from django.http import JsonResponse
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
from memory_profiler import profile
import logging
logger = logging.getLogger('myapp')
import objgraph  # 📦 Debug tool
import gc        # 🧹 Garbage Collector
from guppy import hpy
h = hpy()
class ProductListView(APIView):
    def get(self, request):
        # ✅ Step 1: মূল কোড
        objgraph.show_growth()
        products = Product.objects.filter(name__isupper=True)
        serializer = ProductSerializer(products, many=True)

        # ✅ Step 2: Garbage collect (পরিষ্কার করে fresh memory status দেখতে)
        gc.collect()

        # ✅ Step 3: Console এ top object types report
        objgraph.show_most_common_types(limit=10)

        # ✅ Step 4: PNG output for memory reference graph
        objgraph.show_backrefs(
            [serializer.data],
            max_depth=3,
            filename='product_memory_debug.png'
        )
        objgraph.show_growth()
        print(h.heap())
        # ✅ Step 5: Return response
        return Response(serializer.data)

@profile
def test_view(request):
    # products = list(Product.objects.all())
    products = list(Product.objects.values('id', 'name'))
    return JsonResponse({'count': len(products)})
# @profile
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
        logger.info("successfully blogs data read")

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