import argparse
import csv
from collections import defaultdict
from decimal import Decimal

ZERO = Decimal('0.00')


def load_expenses(path):
    with open(path, newline='', encoding='utf-8') as file:
        return [
            {
                'type': row['expense_type'].strip() or 'Uncategorized',
                'amount': Decimal(row['amount']) if row['amount'].strip() else ZERO,
                'date': row['expense_date'].strip() or None,
                'payment_method': row['payment_method'].strip() or 'Unknown',
            }
            for row in csv.DictReader(file)
        ]


def total(expenses):
    return sum((e['amount'] for e in expenses), ZERO)


def total_by(expenses, key):
    totals = defaultdict(lambda: ZERO)
    for expense in expenses:
        totals[key(expense)] += expense['amount']
    return dict(sorted(totals.items()))


def by_type(expenses):
    return total_by(expenses, lambda e: e['type'])


def by_payment_method(expenses):
    return total_by(expenses, lambda e: e['payment_method'])


def by_month(expenses):
    return total_by([e for e in expenses if e['date']], lambda e: e['date'][:7])


def highest_day(expenses):
    days = total_by([e for e in expenses if e['date']], lambda e: e['date'])
    return max(days.items(), key=lambda item: item[1]) if days else None


def breakdown(expenses):
    table = defaultdict(lambda: defaultdict(lambda: ZERO))
    for expense in expenses:
        table[expense['type']][expense['payment_method']] += expense['amount']
    return {name: dict(methods) for name, methods in sorted(table.items())}


def print_section(title, totals):
    print(title)
    for name, amount in totals.items():
        print(f'  {name:<15} {amount:>12,.2f}')
    print()


def print_report(expenses):
    print(f'Total expense: {total(expenses):,.2f}\n')
    print_section('By expense type', by_type(expenses))
    print_section('By payment method', by_payment_method(expenses))
    print_section('By month', by_month(expenses))

    day = highest_day(expenses)
    if day:
        print(f'Day with highest expenses: {day[0]} ({day[1]:,.2f})\n')

    methods = sorted(by_payment_method(expenses))
    print(f'{"Expense type":<15}' + ''.join(f'{m:>14}' for m in methods) + f'{"Total":>14}')
    print('-' * (15 + 14 * (len(methods) + 1)))
    for name, row in breakdown(expenses).items():
        cells = ''.join(f'{row.get(m, ZERO):>14,.2f}' for m in methods)
        print(f'{name:<15}{cells}{sum(row.values(), ZERO):>14,.2f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print an expense summary from a CSV file.')
    parser.add_argument('csv_path', nargs='?', default='expenses.csv')
    print_report(load_expenses(parser.parse_args().csv_path))
