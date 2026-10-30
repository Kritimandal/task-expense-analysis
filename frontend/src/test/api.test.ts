import { describe, expect, it, vi } from 'vitest';
import { ApiError, api, toApiError, toQuery } from '../api';

function mockFetch(status: number, body: unknown) {
  return vi.spyOn(globalThis, 'fetch').mockResolvedValue(
    new Response(status === 204 ? null : JSON.stringify(body), { status }),
  );
}

describe('toQuery', () => {
  it('skips empty values', () => {
    expect(toQuery({ expense_type: 'Rent', payment_method: '', page: undefined })).toBe('?expense_type=Rent');
  });

  it('returns an empty string when nothing is set', () => {
    expect(toQuery({ year: '' })).toBe('');
  });
});

describe('toApiError', () => {
  it('reads Django REST Framework field errors', () => {
    const error = toApiError(400, { amount: ['Ensure this value is greater than or equal to 0.'] });
    expect(error.status).toBe(400);
    expect(error.fieldErrors.amount).toEqual(['Ensure this value is greater than or equal to 0.']);
  });

  it('uses the detail message when present', () => {
    expect(toApiError(404, { detail: 'Not found.' }).message).toBe('Not found.');
  });

  it('handles bodies that are not JSON objects', () => {
    expect(toApiError(500, null).message).toBe('Request failed with status 500.');
  });
});

describe('api', () => {
  it('sends filters as query parameters', async () => {
    const fetchSpy = mockFetch(200, { count: 0, next: null, previous: null, results: [] });
    await api.listExpenses({ expense_type: 'Rent', page: 2 });
    expect(fetchSpy).toHaveBeenCalledWith('/api/expenses/?expense_type=Rent&page=2', expect.any(Object));
  });

  it('posts new expenses as JSON', async () => {
    const fetchSpy = mockFetch(201, { id: 1 });
    const data = { expense_type: 'Rent' as const, amount: 10, expense_date: null, payment_method: 'Cash' as const };
    await api.createExpense(data);
    const [, init] = fetchSpy.mock.calls[0];
    expect(init?.method).toBe('POST');
    expect(JSON.parse(String(init?.body))).toEqual(data);
  });

  it('returns undefined for 204 responses', async () => {
    mockFetch(204, null);
    await expect(api.deleteExpense(3)).resolves.toBeUndefined();
  });

  it('throws ApiError with field errors on 400', async () => {
    mockFetch(400, { expense_type: ['"Food" is not a valid choice.'] });
    await expect(api.createExpense({} as never)).rejects.toMatchObject({
      status: 400,
      fieldErrors: { expense_type: ['"Food" is not a valid choice.'] },
    });
  });

  it('explains when the server cannot be reached', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'));
    await expect(api.breakdown()).rejects.toBeInstanceOf(ApiError);
    await expect(api.breakdown()).rejects.toThrow('Cannot reach the API');
  });
});
