import io
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.core.management import CommandError, call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .csv_import import CsvImportError, parse_amount, read_expenses
from .models import Expense

SAMPLE_CSV_PATH = Path(__file__).resolve().parents[2] / 'expenses.csv'

HEADER = 'expense_id,expense_type,amount,expense_date,payment_method\n'


def make_expense(expense_type, amount, expense_date, payment_method):
    return Expense.objects.create(
        expense_type=expense_type,
        amount=Decimal(amount),
        expense_date=expense_date,
        payment_method=payment_method,
    )


class CsvParsingTests(SimpleTestCase):
    def test_reads_every_row_including_the_first(self):
        file = io.StringIO(HEADER + '1,Rent,100.50,2023-01-05,Cash\n2,Transport,20,2023-02-01,Credit Card\n')
        expenses, errors = read_expenses(file)
        self.assertEqual(errors, [])
        self.assertEqual([e.id for e in expenses], [1, 2])
        self.assertEqual(expenses[0].amount, Decimal('100.50'))
        self.assertEqual(expenses[0].expense_date, date(2023, 1, 5))

    def test_blank_values_use_documented_defaults(self):
        expenses, errors = read_expenses(io.StringIO(HEADER + '7,,,,\n'))
        self.assertEqual(errors, [])
        expense = expenses[0]
        self.assertEqual(expense.expense_type, Expense.Type.UNCATEGORIZED)
        self.assertEqual(expense.amount, Decimal('0.00'))
        self.assertIsNone(expense.expense_date)
        self.assertEqual(expense.payment_method, Expense.PaymentMethod.UNKNOWN)

    def test_bad_rows_are_reported_with_line_numbers(self):
        file = io.StringIO(HEADER + '1,Rent,abc,2023-01-05,Cash\n2,Food,5,2023-13-01,Cash\n')
        expenses, errors = read_expenses(file)
        self.assertEqual(expenses, [])
        self.assertEqual(len(errors), 2)
        self.assertTrue(errors[0].startswith('line 2: invalid amount'))
        self.assertTrue(errors[1].startswith('line 3: unknown value "Food"'))

    def test_missing_columns_are_rejected(self):
        with self.assertRaises(CsvImportError):
            read_expenses(io.StringIO('id,amount\n1,5\n'))

    def test_negative_amount_is_rejected(self):
        with self.assertRaises(CsvImportError):
            parse_amount('-1')


class ImportCommandTests(TestCase):
    def test_imports_sample_file(self):
        call_command('import_expenses', str(SAMPLE_CSV_PATH), stdout=io.StringIO())
        self.assertEqual(Expense.objects.count(), 300)

    def test_running_twice_does_not_duplicate(self):
        call_command('import_expenses', str(SAMPLE_CSV_PATH), stdout=io.StringIO())
        call_command('import_expenses', str(SAMPLE_CSV_PATH), stdout=io.StringIO())
        self.assertEqual(Expense.objects.count(), 300)

    def test_file_with_bad_rows_imports_nothing(self):
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as file:
            file.write(HEADER + '1,Rent,100,2023-01-05,Cash\n2,Rent,oops,2023-01-05,Cash\n')
        try:
            with self.assertRaisesMessage(CommandError, 'line 3'):
                call_command('import_expenses', file.name, stdout=io.StringIO())
        finally:
            Path(file.name).unlink()
        self.assertEqual(Expense.objects.count(), 0)

    def test_missing_file(self):
        with self.assertRaisesMessage(CommandError, 'File not found'):
            call_command('import_expenses', 'no-such-file.csv')


class ReportApiTests(APITestCase):
    def setUp(self):
        make_expense('Rent', '800.00', date(2023, 1, 1), 'Cash')
        make_expense('Rent', '200.00', date(2023, 1, 15), 'Credit Card')
        make_expense('Groceries', '50.25', date(2023, 2, 3), 'Credit Card')
        make_expense('Groceries', '10.00', None, 'Cash')
        make_expense('Transport', '5.00', date(2024, 2, 3), 'Cash')

    def test_expense_by_type(self):
        response = self.client.get(reverse('expense-by-type'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'Groceries': 60.25, 'Rent': 1000.0, 'Transport': 5.0})

    def test_monthly_expenses_skip_rows_without_date(self):
        response = self.client.get(reverse('monthly-expenses'))
        self.assertEqual(response.json(), [
            {'month': '2023-01', 'total': 1000.0},
            {'month': '2023-02', 'total': 50.25},
            {'month': '2024-02', 'total': 5.0},
        ])

    def test_monthly_expenses_filter_by_year(self):
        response = self.client.get(reverse('monthly-expenses'), {'year': '2024'})
        self.assertEqual(response.json(), [{'month': '2024-02', 'total': 5.0}])

    def test_monthly_expenses_reject_bad_year(self):
        response = self.client.get(reverse('monthly-expenses'), {'year': '23'})
        self.assertEqual(response.status_code, 400)

    def test_detailed_breakdown_splits_cash_and_card(self):
        data = self.client.get(reverse('detailed-breakdown')).json()
        rent = next(item for item in data['expense_types'] if item['expense_type'] == 'Rent')
        self.assertEqual(rent['Cash'], 800.0)
        self.assertEqual(rent['Credit Card'], 200.0)
        self.assertEqual(rent['total'], 1000.0)
        self.assertEqual(data['grand_total'], 1065.25)

    def test_report_endpoints_are_read_only(self):
        response = self.client.post(reverse('expense-by-type'), {})
        self.assertEqual(response.status_code, 405)


class ExpenseCrudApiTests(APITestCase):
    def test_create_expense(self):
        payload = {'expense_type': 'Utilities', 'amount': '45.10', 'expense_date': '2023-03-01', 'payment_method': 'Cash'}
        response = self.client.post(reverse('expense-list'), payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.get().amount, Decimal('45.10'))

    def test_create_rejects_invalid_data(self):
        payload = {'expense_type': 'Food', 'amount': '-5', 'payment_method': 'Bitcoin'}
        response = self.client.post(reverse('expense-list'), payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()), {'expense_type', 'amount', 'payment_method'})

    def test_list_filters_by_type_and_is_paginated(self):
        make_expense('Rent', '1', date(2023, 1, 1), 'Cash')
        make_expense('Transport', '2', date(2023, 1, 1), 'Cash')
        response = self.client.get(reverse('expense-list'), {'expense_type': 'Rent'})
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['expense_type'], 'Rent')

    def test_update_and_delete(self):
        expense = make_expense('Rent', '1', date(2023, 1, 1), 'Cash')
        url = reverse('expense-detail', args=[expense.id])
        response = self.client.patch(url, {'amount': '9.99'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)
