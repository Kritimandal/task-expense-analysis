export const EXPENSE_TYPES = [
  'Groceries',
  'Transport',
  'Entertainment',
  'Rent',
  'Utilities',
  'Uncategorized',
] as const;

export const PAYMENT_METHODS = ['Cash', 'Credit Card', 'Unknown'] as const;

export type ExpenseType = (typeof EXPENSE_TYPES)[number];
export type PaymentMethod = (typeof PAYMENT_METHODS)[number];

export interface Expense {
  id: number;
  expense_type: ExpenseType;
  amount: number;
  expense_date: string | null;
  payment_method: PaymentMethod;
}

export type ExpenseInput = Omit<Expense, 'id'>;

export interface Page<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type TotalsByType = Record<string, number>;

export interface MonthlyTotal {
  month: string;
  total: number;
}

export type BreakdownRow = { expense_type: string; total: number } & Record<PaymentMethod, number>;

export interface Breakdown {
  expense_types: BreakdownRow[];
  grand_total: number;
}

export interface ExpenseFilters {
  expense_type?: string;
  payment_method?: string;
  page?: number;
}
