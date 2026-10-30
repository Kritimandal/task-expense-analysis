from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Expense

ZERO = Decimal('0.00')


def total_by_type():
    rows = Expense.objects.values('expense_type').annotate(total=Sum('amount')).order_by('expense_type')
    return {row['expense_type']: row['total'] for row in rows}


def total_by_month(year=None):
    queryset = Expense.objects.filter(expense_date__isnull=False)
    if year:
        queryset = queryset.filter(expense_date__year=year)
    rows = (
        queryset.annotate(month=TruncMonth('expense_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    return [{'month': row['month'].strftime('%Y-%m'), 'total': row['total']} for row in rows]


def breakdown_by_type_and_payment():
    rows = (
        Expense.objects.values('expense_type', 'payment_method')
        .annotate(total=Sum('amount'))
        .order_by('expense_type', 'payment_method')
    )
    breakdown = {}
    for row in rows:
        item = breakdown.setdefault(row['expense_type'], {method: ZERO for method in Expense.PaymentMethod.values})
        item[row['payment_method']] = row['total']
    expense_types = [
        {'expense_type': name, **totals, 'total': sum(totals.values(), ZERO)}
        for name, totals in breakdown.items()
    ]
    return {
        'expense_types': expense_types,
        'grand_total': sum((item['total'] for item in expense_types), ZERO),
    }
