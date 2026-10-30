import csv
import unittest
from decimal import Decimal
from pathlib import Path

import report

SAMPLE = Path(__file__).resolve().parent / 'expenses.csv'


def expense(type_, amount, date, method):
    return {'type': type_, 'amount': Decimal(amount), 'date': date, 'payment_method': method}


EXPENSES = [
    expense('Rent', '800', '2023-01-01', 'Cash'),
    expense('Rent', '200', '2023-01-15', 'Credit Card'),
    expense('Groceries', '50.25', '2023-02-03', 'Credit Card'),
    expense('Groceries', '10', None, 'Cash'),
]


class ReportTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(report.total(EXPENSES), Decimal('1060.25'))

    def test_by_type(self):
        self.assertEqual(report.by_type(EXPENSES), {'Groceries': Decimal('60.25'), 'Rent': Decimal('1000')})

    def test_by_month_skips_missing_dates(self):
        self.assertEqual(report.by_month(EXPENSES), {'2023-01': Decimal('1000'), '2023-02': Decimal('50.25')})

    def test_highest_day(self):
        self.assertEqual(report.highest_day(EXPENSES), ('2023-01-01', Decimal('800')))

    def test_breakdown_keeps_cash_and_card_separate(self):
        rent = report.breakdown(EXPENSES)['Rent']
        self.assertEqual(rent, {'Cash': Decimal('800'), 'Credit Card': Decimal('200')})


class SampleFileTests(unittest.TestCase):
    def test_loads_every_row(self):
        with open(SAMPLE, newline='', encoding='utf-8') as file:
            row_count = sum(1 for _ in csv.DictReader(file))
        self.assertEqual(len(report.load_expenses(SAMPLE)), row_count)

    def test_totals_add_up(self):
        expenses = report.load_expenses(SAMPLE)
        self.assertEqual(sum(report.by_type(expenses).values()), report.total(expenses))
        self.assertEqual(sum(report.by_payment_method(expenses).values()), report.total(expenses))


if __name__ == '__main__':
    unittest.main()
