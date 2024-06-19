from django.urls import path
from .import views

urlpatterns = [
    path('expenses/', views.ExpensesListView.as_view(), name="list_of_expenses"),
    path('expense/<int:pk>', views.ExpensesDetailView.as_view(), name="expense_details"),
    path('expense_category/', views.ExpenseCategoryListView.as_view(), name="expense_category_list"),
    path('expense_category/<int:pk>', views.ExpenseCategoryDetailView.as_view(), name="expense_category_details"),
    path('create_store/', views.StoreCreateApiView.as_view(), name="create_store"),
]