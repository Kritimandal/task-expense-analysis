from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_type', 'amount', 'expense_date', 'payment_method']
    list_filter = ['expense_type', 'payment_method']
    date_hierarchy = 'expense_date'
