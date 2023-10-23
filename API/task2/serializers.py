from rest_framework import serializers
from .models import Expenses

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['id', 'expense_type', 'amount', 'expense_date', 'payment_method']

class ExpensetypeSerializer(serializers.Serializer):
    Groceries = serializers.FloatField()
    Transport = serializers.FloatField()
    Entertainment = serializers.FloatField()
    Rent = serializers.FloatField()
    Utilities = serializers.FloatField()

class ExpensemonthSerializer(serializers.Serializer):
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


class ExpensebdSerializer(serializers.Serializer):
    Credit_Card = serializers.FloatField()
    Cash = serializers.FloatField()
    Total = serializers.FloatField()

class ExpensebdtSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100)
    payment_breakdown = ExpensebdSerializer(many=True)
    Grand_Total = serializers.FloatField()

