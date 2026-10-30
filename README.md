# Expense Analysis — Django REST API + React Dashboard

![tests](https://github.com/Kritimandal/task-expense-analysis/actions/workflows/tests.yml/badge.svg)

A full-stack expense tracker. The backend is a REST API built with Django and Django REST Framework that imports expense records from CSV, validates them and returns reports as JSON. The frontend is a React + TypeScript dashboard that shows the reports as charts and lets you add, edit, filter and delete expenses. A small command-line report also works on the CSV directly.

![Dashboard](docs/dashboard.png)

## Backend features

- CSV import command with row-level validation. A file with bad rows is rejected as a whole and every bad line is reported. Running the import again updates rows instead of creating duplicates.
- CRUD API for expenses with filtering and pagination
- Report endpoints that use database aggregation (`SUM`, `GROUP BY`, month truncation), not Python loops
- `Decimal` amounts, so totals have no floating-point rounding errors
- Settings read from environment variables

## Frontend features

- Summary cards, spending-by-category and spending-by-month charts with hover tooltips, and a category × payment-method table
- Expenses table with category and payment filters and server-side pagination
- Add and edit form with client-side validation, plus field errors from the API shown next to each field
- Typed API client that turns network failures and Django REST Framework errors into clear messages
- Works in light and dark mode and on small screens

## Tests

51 automated tests run on every push with GitHub Actions:

| Part | Tests | Tool |
|---|---|---|
| API, CSV import, reports | 19 | Django test runner |
| CLI report | 7 | unittest |
| React components and API client | 25 | Vitest + React Testing Library |

## Tech stack

- **Backend:** Python 3.12, Django 5.1, Django REST Framework 3.15, SQLite
- **Frontend:** React 18, TypeScript, Vite, Recharts, Vitest, React Testing Library
- **CI:** GitHub Actions

## Run the backend

```bash
git clone https://github.com/Kritimandal/task-expense-analysis.git
cd task-expense-analysis
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd API
python manage.py migrate
python manage.py import_expenses ../expenses.csv
python manage.py runserver
```

The API runs at http://127.0.0.1:8000. The browsable DRF interface opens in a browser.

## Run the frontend

In a second terminal, with the backend running:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server forwards `/api/*` requests to the Django server, so no CORS setup is needed. To use another API address, set `VITE_API_URL` (for example `VITE_API_URL=https://api.example.com npm run build`).

## Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/expenses/` | List expenses. Filters: `?expense_type=Rent&payment_method=Cash`. Paginated (50 per page). |
| POST | `/expenses/` | Create an expense |
| GET, PUT, PATCH, DELETE | `/expenses/<id>/` | Read, update or delete one expense |
| GET | `/expense_by_type/` | Total amount for each expense type |
| GET | `/monthly_expenses/` | Total per month. Optional `?year=2023`. |
| GET | `/detailed_breakdown/` | Each expense type split by payment method, plus a grand total |

### Example: `GET /detailed_breakdown/`

```json
{
  "expense_types": [
    {"expense_type": "Rent", "Cash": 20130.53, "Credit Card": 24335.58, "Unknown": 829.08, "total": 45295.19}
  ],
  "grand_total": 59725.64
}
```

### Example: validation error on `POST /expenses/`

```json
{
  "expense_type": ["\"Food\" is not a valid choice."],
  "amount": ["Ensure this value is greater than or equal to 0."]
}
```

## Data rules

The sample `expenses.csv` has 300 rows and some have missing values. The import handles them like this:

| Missing value | Stored as |
|---|---|
| `amount` | `0.00` |
| `expense_type` | `Uncategorized` |
| `payment_method` | `Unknown` |
| `expense_date` | empty. The row counts in type totals but not in monthly totals. |

Values that are present but wrong (for example `amount=abc`, `expense_type=Food` or a bad date) are errors, and nothing is imported until they are fixed.

## Command-line report

```bash
python report.py expenses.csv
```

This prints the total, totals by type, by payment method and by month, the day with the highest spending, and a type × payment-method table.

## Run the tests

```bash
python -m unittest test_report
cd API && python manage.py test
cd ../frontend && npm test
```

## Project structure

```
├── expenses.csv               sample data (300 rows)
├── report.py                  command-line report
├── test_report.py
├── frontend/
│   └── src/
│       ├── api.ts             typed API client and error handling
│       ├── App.tsx            dashboard layout
│       ├── components/        charts, tables, expense form
│       └── test/              Vitest tests
└── API/
    ├── config/                settings and root URLs
    └── expenses/
        ├── models.py          Expense model with choices and indexes
        ├── csv_import.py      CSV parsing and validation
        ├── management/commands/import_expenses.py
        ├── reports.py         aggregation queries
        ├── views.py           API views
        └── tests.py
```
