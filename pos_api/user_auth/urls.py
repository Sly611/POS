from django.urls import path
from . import views

urlpatterns = [
    path('register/admin/', views.RegisterSuperUserView.as_view(), name='create_super_user'),
    path('register/staff/', views.RegisterUserView.as_view(), name="create_new_user"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
