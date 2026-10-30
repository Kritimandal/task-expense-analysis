from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Expense(models.Model):
    class Type(models.TextChoices):
        GROCERIES = 'Groceries'
        TRANSPORT = 'Transport'
        ENTERTAINMENT = 'Entertainment'
        RENT = 'Rent'
        UTILITIES = 'Utilities'
        UNCATEGORIZED = 'Uncategorized'

    class PaymentMethod(models.TextChoices):
        CASH = 'Cash'
        CREDIT_CARD = 'Credit Card'
        UNKNOWN = 'Unknown'

    expense_type = models.CharField(max_length=20, choices=Type.choices, default=Type.UNCATEGORIZED)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    expense_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['expense_type', 'payment_method']),
            models.Index(fields=['expense_date']),
        ]

    def __str__(self):
        return f'{self.expense_type} {self.amount} ({self.payment_method})'
