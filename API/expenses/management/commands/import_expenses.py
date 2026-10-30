from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from expenses.csv_import import CsvImportError, read_expenses
from expenses.models import Expense


class Command(BaseCommand):
    help = 'Import expenses from a CSV file. Rows with the same expense_id are updated.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')

    def handle(self, *args, csv_path, **options):
        try:
            with open(csv_path, newline='', encoding='utf-8') as file:
                expenses, errors = read_expenses(file)
        except FileNotFoundError:
            raise CommandError(f'File not found: {csv_path}')
        except CsvImportError as error:
            raise CommandError(str(error))

        if errors:
            raise CommandError('Nothing imported. Fix these rows first:\n' + '\n'.join(errors))

        with transaction.atomic():
            Expense.objects.bulk_create(
                expenses,
                update_conflicts=True,
                unique_fields=['id'],
                update_fields=['expense_type', 'amount', 'expense_date', 'payment_method'],
            )
        self.stdout.write(self.style.SUCCESS(f'Imported {len(expenses)} expenses.'))
