from django.db import models

class Expenses(models.Model):
    expense_type = models.CharField("Expense Type", max_length=255)
    amount = models.FloatField("Amount")
    expense_date = models.DateField("Expense Date", auto_now=True)
    payment_method = models.CharField("Payment Method", max_length=255)