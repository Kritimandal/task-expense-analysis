from django.urls import path

from . import views

urlpatterns = [
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('expense_by_type/', views.expense_by_type, name='expense-by-type'),
    path('monthly_expenses/', views.monthly_expenses, name='monthly-expenses'),
    path('detailed_breakdown/', views.detailed_breakdown, name='detailed-breakdown'),
]
