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
    path('product/new/', views.ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_details'),
    path('products/search/', views.ProductSearchAPIView.as_view(), name='products_search'),

    #Handles Get, Post, Update and Delete for Category entity
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/new/', views.CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_details'),

    #Handles Get, Post, Update and Delete for Order entity
    path('orders/', views.OrderListView.as_view(), name='order_history'),
    path('order/new/', views.OrderCreateView.as_view(), name='create_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_details'),
    path('order/search/', views.OrderSearchAPIView.as_view(), name='order_search'),
    path('order-cancel/<int:pk>/', views.OrderCancelView.as_view(), name='order_cancel' ),

    #Handles Get, Post, Update and Delete for Order_item entity
    path('order-item/<int:pk>', views.OrderItemDetailView.as_view(), name='order_item_detail'),

    path('check-stock/', views.CheckStockView.as_view(), name='check_stock'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
