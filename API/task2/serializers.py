from rest_framework import serializers
from .models import Expenses

class ExpenseSerializer(serializers.ModelSerializer):  #Model Serializer
    class Meta:
        model = Expenses
        fields = ['id', 'expense_type', 'amount', 'expense_date', 'payment_method']

class ExpensetypeSerializer(serializers.Serializer):   #Seializer class for the total expense amount by expense type
    Groceries = serializers.FloatField()
    Transport = serializers.FloatField()
    Entertainment = serializers.FloatField()
    Rent = serializers.FloatField()
    Utilities = serializers.FloatField()

class ExpensemonthSerializer(serializers.Serializer):   #Seializer class for the monthly total expense amount
    Month_01 = serializers.FloatField()
    Month_02 = serializers.FloatField()
    Month_03 = serializers.FloatField()
    Month_04 = serializers.FloatField()
    Month_05 = serializers.FloatField()
    Month_06 = serializers.FloatField()
    Month_07 = serializers.FloatField()
    Month_08 = serializers.FloatField()
    Month_09 = serializers.FloatField()
    Month_10 = serializers.FloatField()
    Month_11 = serializers.FloatField()
    Month_12 = serializers.FloatField()


class ExpensebdSerializer(serializers.Serializer):   #Seializer class that further subdivides each expense type by `payment_method`
    Credit_Card = serializers.FloatField()
    Cash = serializers.FloatField()
    Total = serializers.FloatField()

class ExpensebdtSerializer(serializers.Serializer):   #Seializer class for that breaks down expenses by `expense_type`
    type = serializers.CharField(max_length=100)
    payment_breakdown = ExpensebdSerializer(many=True) #payment_breakdown field is used to represent a list of expenses, where each expense is serialized using the ExpensebdSerializer
    Grand_Total = serializers.FloatField()

