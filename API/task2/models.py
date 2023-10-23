from django.db import models

class Expenses(models.Model):
    expense_type = models.CharField("Expense Type", max_length=255)   # A field to store the type of expense, e.g., "Groceries," "Rent," or "Transportation."
    amount = models.FloatField("Amount")                              # A field to store the expense amount 
    expense_date = models.DateField("Expense Date", auto_now=True)    # A field to store the date of transaction.(format: YYYY-MM-DD) "auto_now=True: It automatically records the current date when the value is added or updated
    payment_method = models.CharField("Payment Method", max_length=255) #A field to store the type of payment method, i.e., "Cash," "Credit Card,"