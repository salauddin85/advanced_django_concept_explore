from django.urls import path
from .views import ProductListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet,TeamView,test_view



urlpatterns = [
    path('products/uppercase/', ProductListView.as_view(), name='uppercase-products'),
    path('blogs/', BlogViewSet.as_view(), name='blogs'),
    path('teams/', TeamView.as_view(), name='teams'),
    path('test_memory/', test_view, name='test_memory'),
]
