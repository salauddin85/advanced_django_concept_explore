from django.urls import path
from .views import ProductListView

urlpatterns = [
    path('products/uppercase/', ProductListView.as_view(), name='uppercase-products'),
]
