from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from .serializer import *


register_user_schema = extend_schema(
    request=CreateSuperUserSerializer,
    responses={
        status.HTTP_201_CREATED: CreateSuperUserSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation errors")
    },
    parameters=[
        OpenApiParameter(name='username', type=OpenApiTypes.STR, description='New user username'),
        OpenApiParameter(name='email', type=OpenApiTypes.EMAIL, description='New user email'),
        OpenApiParameter(name='password', type=OpenApiTypes.STR, description='New user password'),
        OpenApiParameter(name='password_confirm', type=OpenApiTypes.STR, description='New user password confirmation'),
    ],
)