import type {
  Breakdown,
  Expense,
  ExpenseFilters,
  ExpenseInput,
  MonthlyTotal,
  Page,
  TotalsByType,
} from './types';

const BASE_URL = import.meta.env.VITE_API_URL ?? '/api';

export const PAGE_SIZE = 50;

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public fieldErrors: Record<string, string[]> = {},
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function toApiError(status: number, body: unknown): ApiError {
  if (body && typeof body === 'object' && !Array.isArray(body)) {
    const record = body as Record<string, unknown>;
    if (typeof record.detail === 'string') {
      return new ApiError(status, record.detail);
    }
    const fieldErrors = Object.fromEntries(
      Object.entries(record).map(([field, value]) => [
        field,
        Array.isArray(value) ? value.map(String) : [String(value)],
      ]),
    );
    return new ApiError(status, 'Please fix the highlighted fields.', fieldErrors);
  }
  return new ApiError(status, `Request failed with status ${status}.`);
}

export function toQuery(params: Record<string, string | number | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== '') {
      search.set(key, String(value));
    }
  }
  const query = search.toString();
  return query ? `?${query}` : '';
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: { Accept: 'application/json', 'Content-Type': 'application/json', ...init.headers },
    });
  } catch {
    throw new ApiError(0, 'Cannot reach the API. Is the Django server running?');
  }
  if (response.status === 204) {
    return undefined as T;
  }
  const body: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    throw toApiError(response.status, body);
  }
  return body as T;
}

export const api = {
  listExpenses: (filters: ExpenseFilters = {}) =>
    request<Page<Expense>>(`/expenses/${toQuery({ ...filters })}`),
  createExpense: (data: ExpenseInput) =>
    request<Expense>('/expenses/', { method: 'POST', body: JSON.stringify(data) }),
  updateExpense: (id: number, data: ExpenseInput) =>
    request<Expense>(`/expenses/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteExpense: (id: number) => request<void>(`/expenses/${id}/`, { method: 'DELETE' }),
  totalsByType: () => request<TotalsByType>('/expense_by_type/'),
  monthlyTotals: (year?: string) => request<MonthlyTotal[]>(`/monthly_expenses/${toQuery({ year })}`),
  breakdown: () => request<Breakdown>('/detailed_breakdown/'),
};
