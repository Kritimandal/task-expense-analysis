from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Expenses
from .serializers import ExpenseSerializer
from .serializers import ExpensetypeSerializer
from .serializers import ExpensemonthSerializer
from .serializers import ExpensebdtSerializer
from datetime import datetime
from .serializers import ExpensebdSerializer

@api_view(['GET'])
def totalExpense(request):
    items= Expenses.objects.all()
    serialized_data = []

    for item in items:
        try:
            amount = float(item.amount)
        except (ValueError, TypeError):
            amount = 0.0
        data = {
            'id': item.id,
            'expense_type': item.expense_type,
            'amount': amount,
            'expense_date': item.expense_date,
            'payment_method': item.payment_method
        }

        serialized_data.append(data)
        serializer= ExpenseSerializer(serialized_data, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def expensesByType(request):
        expenses= Expenses.objects.all()
        rent_expense = transport_expense = entertainment_expense = groceries_expense = utilities_expense  = 0
        for expense in expenses:
            try:
                amount = float(expense.amount)
            except (ValueError, TypeError):
                amount = 0.0
            try:
                type = expense.expense_type
            except (AttributeError):
                type = "Groceries"
            match type:
                case "Rent":
                    rent_expense += amount
                case "Transport":
                   transport_expense += amount
                case "Entertainment":
                    entertainment_expense += amount
                case "Groceries":
                    groceries_expense += amount
                case "Utilities":
                    utilities_expense += amount
                case _:
                    groceries_expense += amount
        serialized_data = [{
            "Groceries": groceries_expense,
            "Transport": transport_expense,
            "Entertainment": entertainment_expense,
            "Rent": rent_expense,
            "Utilities": utilities_expense
        }]
        serializer= ExpensetypeSerializer(serialized_data, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def monthlyExpenses(request):
        expenses= Expenses.objects.all()
        month1_expense = month2_expense =month3_expense = month4_expense = month5_expense = month6_expense = month7_expense = month8_expense= month9_expense= month10_expense= month11_expense = month12_expense = 0
        for expense in expenses:
            try:
                amount = float(expense.amount)
            except (ValueError, TypeError):
                amount = 0.0
            try:
                date_value = expense.expense_date
            except (ValueError, TypeError):
                date_value = "2023-12-1"
            if expense.amount != 0.0 and date_value is not None:
                date = date_value.__str__()
                date_val = datetime.strptime(date, "%Y-%m-%d")
                year_month = date_val.strftime("%Y-%m")
               # year_month = f"{date[0]}-{date[1]}"
                match year_month:
                    case "2023-01":
                        month1_expense += amount
                    case "2023-02":
                        month2_expense += amount
                    case "2023-03":
                        month3_expense += amount
                    case "2023-04":
                        month4_expense += amount
                    case "2023-05":
                        month5_expense += amount
                    case "2023-06":
                        month6_expense += amount
                    case "2023-07": 
                        month7_expense += amount
                    case "2023-08":
                        month8_expense += amount
                    case "2023-09": 
                        month9_expense += amount
                    case "2023-10":
                        month10_expense += amount
                    case "2023-11":
                        month11_expense += amount
                    case "2023-12":  
                        month12_expense += amount  
                    case _:
                        month12_expense += amount 
        serialized_data = [{
            "Month_01": month1_expense,
            "Month_02": month2_expense,
            "Month_03": month3_expense,
            "Month_04": month4_expense,
            "Month_05": month5_expense,
            "Month_06": month6_expense,
            "Month_07": month7_expense,
            "Month_08": month8_expense,
            "Month_09": month9_expense,
            "Month_10": month10_expense,
            "Month_11": month11_expense,
            "Month_12": month12_expense
            
        }]
        serializer= ExpensemonthSerializer(serialized_data, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def breakExpenses(request):
    expenses= Expenses.objects.all()
    Groceries_cash_expense = Groceries_credit_expense = Transport_cash_expense = Transport_credit_expense = Entertainment_cash_expense = Entertainment_credit_expense = Rent_cash_expense = Rent_credit_expense = Utilities_cash_expense = Utilities_credit_expense = 0
    Utilities_expense = Groceries_expense = Entertainment_expense = Rent_expense  = Transport_expense = 0
    serialized_data = []
    expense_type_set = set()
    for expense in expenses:
        try:
            amount = float(expense.amount)
        except(ValueError, TypeError):
            amount = 0.0
        try:
            type = expense.expense_type
        except (AttributeError):
            type = "Groceries"
        if type:
            expense_type_set.add(type)
        match type:
            case "Rent":
                
                if expense.payment_method == "Cash":
                    Rent_cash_expense += amount
                else:
                    Rent_credit_expense += amount
                Rent_expense = Rent_cash_expense + Rent_credit_expense
            case "Transport":
                
                if expense.payment_method == "Cash":
                    Transport_cash_expense += amount
                else:
                    Transport_credit_expense += amount
                Transport_expense = Transport_cash_expense + Transport_credit_expense
            case "Entertainment":
                
                if expense.payment_method == "Cash":
                    Entertainment_cash_expense += amount
                else:
                    Entertainment_credit_expense += amount
                Entertainment_expense = Entertainment_cash_expense + Entertainment_credit_expense
            case "Groceries":
                
                if expense.payment_method == "Cash":
                    Groceries_cash_expense += amount
                else:
                    Groceries_credit_expense += amount
                Groceries_expense = Groceries_cash_expense + Groceries_credit_expense
            case "Utilities":
                
                if expense.payment_method == "Cash":
                    Utilities_cash_expense += amount
                else:
                    Utilities_credit_expense += amount
                Utilities_expense = Utilities_cash_expense + Utilities_credit_expense
        grand_total = Utilities_expense +   Groceries_expense  + Entertainment_expense + Rent_expense  + Transport_expense
    var_values = {
    "Rent": {
        "credit_expense": Rent_cash_expense,
        "cash_expense": Rent_cash_expense,
        "expense": Rent_expense
    },
    "Utilities": {
        "credit_expense": Utilities_credit_expense,
        "cash_expense": Utilities_cash_expense,
        "expense": Utilities_expense
    },
    "Groceries": {
        "credit_expense": Groceries_credit_expense,
        "cash_expense": Groceries_cash_expense,
        "expense": Groceries_expense
    },
    "Transport": {
        "credit_expense": Transport_credit_expense,
        "cash_expense": Transport_cash_expense,
        "expense": Transport_expense
    },
    "Entertainment": {
        "credit_expense": Entertainment_credit_expense,
        "cash_expense": Entertainment_cash_expense,
        "expense": Entertainment_expense
    },
}    
    for item in expense_type_set:
        if item in var_values:
            val_for_item = var_values[item]
            data = {
                    "type": item,
                    "payment_breakdown":[
                    {
                    "Credit_Card": val_for_item.get("credit_expense", 0), 
                    "Cash": val_for_item.get("cash_expense", 0),
                    "Total" : val_for_item.get("expense", 0)
                    }
                    ],
                    "Grand_Total" : grand_total
            }
            serialized_data.append(data)
            serializer= ExpensebdtSerializer(serialized_data, many=True)
    return Response(serializer.data)