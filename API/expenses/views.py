from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import reports
from .models import Expense
from .serializers import ExpenseSerializer

FILTER_FIELDS = ['expense_type', 'payment_method']


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = Expense.objects.all()
        for field in FILTER_FIELDS:
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


@api_view(['GET'])
def expense_by_type(request):
    return Response(reports.total_by_type())


@api_view(['GET'])
def monthly_expenses(request):
    year = request.query_params.get('year')
    if year and not (year.isdigit() and len(year) == 4):
        raise ValidationError({'year': 'Use a 4-digit year, for example 2023.'})
    return Response(reports.total_by_month(year))


@api_view(['GET'])
def detailed_breakdown(request):
    return Response(reports.breakdown_by_type_and_payment())
