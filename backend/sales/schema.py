from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from .serializers import CategorySerializer, Order_itemSerializer, ProductSerializer, OrderSerializer, PaymentSerializer

#===================================================================================================================================================
# ProductListView Schema
#===================================================================================================================================================
product_list_schema = extend_schema(
    responses={status.HTTP_200_OK: ProductSerializer(many=True)},
)


#===================================================================================================================================================
# ProductCreateView Schema
#===================================================================================================================================================
product_create_schema = extend_schema(
    request=ProductSerializer,
    responses={
        status.HTTP_201_CREATED: ProductSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation errors")
    },
    parameters=[
        OpenApiParameter(name='name', type=OpenApiTypes.STR, description='Product name'),
        OpenApiParameter(name='category', type=OpenApiTypes.STR, description='Product category'),
        OpenApiParameter(name='upc', type=OpenApiTypes.STR, description='Product UPC'),
        OpenApiParameter(name='size', type=OpenApiTypes.STR, description='Product size'),
        OpenApiParameter(name='quantity', type=OpenApiTypes.NUMBER, description='Product quantity'),
        OpenApiParameter(name='cost', type=OpenApiTypes.NUMBER, description='Product cost_price'),
        OpenApiParameter(name='price', type=OpenApiTypes.NUMBER, description='Product selling_price'),
    ],
)


#===================================================================================================================================================
# ProductDetailView Schema
#===================================================================================================================================================
product_detail_schema = extend_schema(
    responses={
        status.HTTP_200_OK: ProductSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Product not found")
    },
    request=ProductSerializer,
    # parameters=[
    #     OpenApiParameter(name='id', type=OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description='Product id'),
    # ],
)


#===================================================================================================================================================
# CategoryListView Schema
#===================================================================================================================================================
category_list_schema = extend_schema(
    responses={status.HTTP_200_OK: CategorySerializer(many=True)},
)


#===================================================================================================================================================
# CategoryCreateView Schema
#===================================================================================================================================================
category_create_schema = extend_schema(
    request=CategorySerializer,
    responses={
        status.HTTP_201_CREATED: CategorySerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation errors")
    },
    # parameters=[
    #     OpenApiParameter(name='name', type=OpenApiTypes.STR, description='Category name'),
    # ],
)


#===================================================================================================================================================
# CategoryDetailView Schema
#===================================================================================================================================================
category_detail_schema = extend_schema(
    responses={
        status.HTTP_200_OK: CategorySerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Category not found")
    },
    request=CategorySerializer,
    # parameters=[
    #     OpenApiParameter(name='id', type=OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description='Category id'),
    # ],
)


#===================================================================================================================================================
# OrderListView Schema
#===================================================================================================================================================
order_list_schema = extend_schema(
    responses={status.HTTP_200_OK: OrderSerializer(many=True)},
)


#===================================================================================================================================================
# OrderCreateView Schema
#===================================================================================================================================================
order_create_schema = extend_schema(
    request=OrderSerializer,
    responses={
        status.HTTP_201_CREATED: OrderSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation errors")
    },
    parameters=[
        OpenApiParameter(name='status', type=OpenApiTypes.STR, description='Order status'),
        OpenApiParameter(name='total_amount', type=OpenApiTypes.NUMBER, description='Order total_amount'),
        OpenApiParameter(name='payment_method', type=OpenApiTypes.STR, description='Order payment_method'),
    ],
)


#===================================================================================================================================================
# OrderCancelView Schema
#===================================================================================================================================================
order_cancel_schema = extend_schema(
    responses={
        status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Order successfully canceled"),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order not found")
    }
)


#===================================================================================================================================================
# OrderDetailView Schema
#===================================================================================================================================================
order_detail_schema = extend_schema(
    responses={
        status.HTTP_200_OK: OrderSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order not found")
    },
    request=OrderSerializer,
    # parameters=[
    #     OpenApiParameter(name='id', type=OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description='Order id'),
    # ],
)


#===================================================================================================================================================
# CheckStockView Schema
#===================================================================================================================================================
check_stock_schema = extend_schema(
    # request=OpenApiTypes.OBJECT(
    #     properties={
    #         'id': OpenApiTypes.NUMBER,
    #         'quantity': OpenApiTypes.NUMBER
    #     },
    # ),
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Stock is available"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid request"),
    }
)


#===================================================================================================================================================
# OrderItemDetailView Schema
#===================================================================================================================================================
orderItem_detail_schema = extend_schema(
    responses={
        status.HTTP_200_OK: Order_itemSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order item not found")
    },
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description='Order_item id'),
    ],
)


#===================================================================================================================================================
# PaymentView Schema
#===================================================================================================================================================
payment_schema = extend_schema(
    responses={
        status.HTTP_200_OK: PaymentSerializer(many=True),
        status.HTTP_201_CREATED: PaymentSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation errors")
    },
    request=PaymentSerializer,
    parameters=[
        OpenApiParameter(name='payment_method', type=OpenApiTypes.STR, description='Payment_method name'),
    ],
)


#===================================================================================================================================================
# ProductSearchAPIView Schema
#===================================================================================================================================================
product_search_schema = extend_schema(
    parameters=[
        OpenApiParameter(name='name', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Product name'),
        OpenApiParameter(name='category', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Product category'),
        OpenApiParameter(name='upc', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Product UPC'),
        OpenApiParameter(name='price', type=OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description='Product price'),
        OpenApiParameter(name='size', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Product size'),
    ],
    responses={
        status.HTTP_200_OK: ProductSerializer(many=True),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No products found")
    }
)


#===================================================================================================================================================
# OrderSearchAPIView Schema
#===================================================================================================================================================
order_search_schema = extend_schema(
    parameters=[
        OpenApiParameter(name='status', type=OpenApiTypes.STR, description='Order status'),
        OpenApiParameter(name='payment', type=OpenApiTypes.STR, description='Payment method'),
        OpenApiParameter(name='date_created', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Date order was created'),
        OpenApiParameter(name='from_date', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Start date for filtering'),
        OpenApiParameter(name='upto_date', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='End date for filtering'),
    ],
    responses={
        status.HTTP_200_OK: OrderSerializer(many=True),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="No orders found")
    }
)
