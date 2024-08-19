from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from .serializers import ExpenseSerializer, StoreSerializer, Expense_categorySerializer, StaffSerializer

# Example schema for StaffListView
staff_list_schema = extend_schema(
    description="This endpoint returns a list of all staffs.",
    request=StaffSerializer,
    responses={
        200: OpenApiResponse(response=StaffSerializer)
    }
)

# Example schema for StaffCreateView
staff_create_schema = extend_schema(
        description="This endpoint creates a new staff",
        request=StaffSerializer,
        responses={
            201: OpenApiResponse(response=StaffSerializer),
            400: OpenApiResponse(description="Invalid input")
        },
        parameters=[
        OpenApiParameter(name='first_name', type=OpenApiTypes.STR, description='Staff first_name'),
        OpenApiParameter(name='last_name', type=OpenApiTypes.STR, description='Staff last_name'),
        OpenApiParameter(name='gender', type=OpenApiTypes.STR, description='Staff gender (male(M) or female(F))'),
        OpenApiParameter(name='email', type=OpenApiTypes.EMAIL, description='Staff email address'),
        OpenApiParameter(name='phone', type=OpenApiTypes.STR, description='Staff phone nunber'),
        OpenApiParameter(name='address', type=OpenApiTypes.STR, description='Staff home address'),
        OpenApiParameter(name='salary', type=OpenApiTypes.NUMBER, description='Staff salary'),
        OpenApiParameter(name='role', type=OpenApiTypes.STR, description='Staff role(i.e manager, security, sales_person etc.)'),
    ]
)


# Example schema for ExpensesListView
expense_schema = extend_schema(
        description="This endpoint returns a list of all expenses.",
        responses={200: OpenApiResponse(response=ExpenseSerializer(many=True))}
)


# Example schema for ExpensesCreateView
expense_create_schema = extend_schema(
        description="This endpoint creates a new expense.",
        request=ExpenseSerializer,
        responses={
            201: OpenApiResponse(response=ExpenseSerializer),
            400: OpenApiResponse(description="Invalid input"),
        },
        parameters=[
        OpenApiParameter(name='title', type=OpenApiTypes.STR, description='Expense title'),
        OpenApiParameter(name='description', type=OpenApiTypes.STR, description='Expense description'),
        OpenApiParameter(name='category', type=OpenApiTypes.STR, description='Expense category'),
        OpenApiParameter(name='amount', type=OpenApiTypes.NUMBER, description='Expense cost'),
    ]
)

# Example schema for ExpensesDetailView
expense_detail_get_schema = extend_schema(
        description="Retrieve the details of a single expense.",
        parameters=[
            OpenApiParameter(name='pk', description='Expense ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={200: OpenApiResponse(response=ExpenseSerializer)},
)

expense_detail_put_schema = extend_schema(
        description="Update the details of a single expense.",
        request=ExpenseSerializer,
        parameters=[
            OpenApiParameter(name='pk', description='Expense ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={
            202: OpenApiResponse(response=ExpenseSerializer),
            400: OpenApiResponse(description="Invalid input"),
        }
)

expense_detail_delete_schema = extend_schema(
        description="Delete a single expense.",
        parameters=[
            OpenApiParameter(name='pk', description='Expense ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={200: OpenApiResponse(description="Deleted successfully")},
    )


# Example schema for BestSellingProductView
bestselling_product_schema = extend_schema(
        description="This endpoint retrieves the top 5 best-selling products based on a specified filter.",
        parameters=[
            OpenApiParameter(name='filter', description='Filter by time period (day, week, month, year)', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT)},
)

store_detail_schema = extend_schema(
        description="This endpoint returns a list of all stores.",
        responses={200: OpenApiResponse(response=StoreSerializer(many=True))}
)


store_create_schema = extend_schema(
        description="This endpoint creates a new store.",
        request=StoreSerializer,
        responses={
            201: OpenApiResponse(response=StoreSerializer),
            400: OpenApiResponse(description="Invalid input"),
        }
)

# Expense Category Endpoints
expense_category_list_schema = extend_schema(
        description="This endpoint returns a list of all expense categories.",
        responses={200: OpenApiResponse(response=Expense_categorySerializer(many=True))}
)

expense_category_create_schema = extend_schema(
        description="This endpoint creates a new expense category.",
        request=Expense_categorySerializer,
        responses={
            201: OpenApiResponse(response=Expense_categorySerializer),
            400: OpenApiResponse(description="Invalid input"),
        }
)

expense_category_detail_get_schema = extend_schema(
        description="Retrieve the details of a single expense category.",
        parameters=[
            OpenApiParameter(name='pk', description='Expense Category ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={200: OpenApiResponse(response=Expense_categorySerializer)},
)

expense_category_detail_put_schema = extend_schema(
        description="Update the details of a single expense category.",
        request=Expense_categorySerializer,
        parameters=[
            OpenApiParameter(name='pk', description='Expense Category ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={
            202: OpenApiResponse(response=Expense_categorySerializer),
            400: OpenApiResponse(description="Invalid input"),
        }
)

expense_category_detail_get_schema = extend_schema(
        description="Delete a single expense category.",
        parameters=[
            OpenApiParameter(name='pk', description='Expense Category ID', required=True, type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={200: OpenApiResponse(description="Deleted successfully")},
)




