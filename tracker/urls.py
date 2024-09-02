from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, CustomLoginView, home_view
from django.contrib.auth.views import LogoutView
from .views import (
    category_list_view, category_create_view, category_edit_view, category_delete_view,
    expense_list_view, expense_create_view, expense_edit_view, expense_delete_view,
    income_list_view, income_create_view, income_edit_view, income_delete_view,
    budget_list_view, budget_create_view, budget_edit_view, budget_delete_view,
    report_view
)
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', home_view, name='home'),

    path('categories/', category_list_view, name='category_list'),
    path('categories/add/', category_create_view, name='category_create'),
    path('categories/edit/<int:pk>/', category_edit_view, name='category_edit'),
    path('categories/delete/<int:pk>/', category_delete_view, name='category_delete'),

    path('expenses/', expense_list_view, name='expense_list'),
    path('expenses/add/', expense_create_view, name='expense_create'),
    path('expenses/edit/<int:pk>/', expense_edit_view, name='expense_edit'),
    path('expenses/delete/<int:pk>/', expense_delete_view, name='expense_delete'),

    path('incomes/', income_list_view, name='income_list'),
    path('incomes/add/', income_create_view, name='income_create'),
    path('incomes/edit/<int:pk>/', income_edit_view, name='income_edit'),
    path('incomes/delete/<int:pk>/', income_delete_view, name='income_delete'),

    path('budgets/', budget_list_view, name='budget_list'),
    path('budgets/add/', budget_create_view, name='budget_create'),
    path('budgets/edit/<int:pk>/', budget_edit_view, name='budget_edit'),
    path('budgets/delete/<int:pk>/', budget_delete_view, name='budget_delete'),

    path('report/', report_view, name='report'),
]
