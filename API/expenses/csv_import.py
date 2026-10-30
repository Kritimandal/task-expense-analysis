import csv
from datetime import date
from decimal import Decimal, InvalidOperation

from .models import Expense

REQUIRED_COLUMNS = {'expense_id', 'expense_type', 'amount', 'expense_date', 'payment_method'}


class CsvImportError(Exception):
    pass


def parse_amount(value):
    value = (value or '').strip()
    if not value:
        return Decimal('0.00')
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise CsvImportError(f'invalid amount "{value}"')
    if amount < 0:
        raise CsvImportError(f'negative amount "{value}"')
    return amount


def parse_date(value):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise CsvImportError(f'invalid date "{value}"')


def parse_choice(value, choices, default):
    value = (value or '').strip()
    if not value:
        return default
    if value not in choices:
        raise CsvImportError(f'unknown value "{value}"')
    return value


def parse_row(row):
    try:
        expense_id = int(row['expense_id'])
    except (TypeError, ValueError):
        raise CsvImportError(f'invalid expense_id "{row["expense_id"]}"')
    return Expense(
        id=expense_id,
        expense_type=parse_choice(row['expense_type'], Expense.Type.values, Expense.Type.UNCATEGORIZED),
        amount=parse_amount(row['amount']),
        expense_date=parse_date(row['expense_date']),
        payment_method=parse_choice(row['payment_method'], Expense.PaymentMethod.values, Expense.PaymentMethod.UNKNOWN),
    )


def read_expenses(file):
    reader = csv.DictReader(file)
    missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
    if missing:
        raise CsvImportError(f'missing columns: {", ".join(sorted(missing))}')
    expenses, errors = [], []
    for line_number, row in enumerate(reader, start=2):
        try:
            expenses.append(parse_row(row))
        except CsvImportError as error:
            errors.append(f'line {line_number}: {error}')
    return expenses, errors
