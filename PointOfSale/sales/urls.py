from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# ------------------------------------------------------------
#     URLCONFIG FOR SALES APP
# ------------------------------------------------------------

urlpatterns = [
    #Handles Get, Post, Update and Delete for Product entity
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_details'),
    path('products/search/', views.ProductSearchAPIView.as_view(), name='products_search'),

    #Handles Get, Post, Update and Delete for Category entity
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_details'),

    #Handles Get, Post, Update and Delete for Order entity
    path('order/', views.OrderListView.as_view(), name='order_history'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_details'),
    path('order/search/', views.OrderSearchAPIView.as_view(), name='order_search'),


]
urlpatterns = format_suffix_patterns(urlpatterns)
