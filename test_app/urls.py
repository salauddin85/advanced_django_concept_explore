from django.urls import path
from .views import ProductListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet,TeamView



urlpatterns = [
    path('products/uppercase/', ProductListView.as_view(), name='uppercase-products'),
    path('blogs/', BlogViewSet.as_view(), name='blogs'),
    path('teams/', TeamView.as_view(), name='teams'),
]
