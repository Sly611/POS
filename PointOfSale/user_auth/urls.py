from django.urls import path
from . import views

urlpatterns = [
    path('new_user/', views.UserCreateView.as_view(), name='create_new_user'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
