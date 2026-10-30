import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { api } from '../api';
import { ExpensesPanel } from '../components/ExpensesPanel';
import type { Expense, Page } from '../types';

const rent: Expense = { id: 1, expense_type: 'Rent', amount: 800, expense_date: '2023-01-01', payment_method: 'Cash' };
const bus: Expense = { id: 2, expense_type: 'Transport', amount: 12.5, expense_date: null, payment_method: 'Credit Card' };

const page = (results: Expense[], count = results.length): Page<Expense> => ({ count, next: null, previous: null, results });

describe('ExpensesPanel', () => {
  beforeEach(() => {
    vi.spyOn(api, 'listExpenses').mockResolvedValue(page([rent, bus]));
  });

  it('lists expenses from the API', async () => {
    render(<ExpensesPanel onChanged={vi.fn()} />);
    expect(await screen.findByText('800.00')).toBeInTheDocument();
    expect(screen.getByText('No date')).toBeInTheDocument();
    expect(screen.getByText('2 records')).toBeInTheDocument();
  });

  it('filters by category and resets to page 1', async () => {
    render(<ExpensesPanel onChanged={vi.fn()} />);
    await screen.findByText('800.00');
    await userEvent.selectOptions(screen.getByLabelText('Category'), 'Rent');
    expect(api.listExpenses).toHaveBeenLastCalledWith({ expense_type: 'Rent', payment_method: '', page: 1 });
  });

  it('pages through results', async () => {
    vi.mocked(api.listExpenses).mockResolvedValue(page([rent], 120));
    render(<ExpensesPanel onChanged={vi.fn()} />);
    expect(await screen.findByText('Page 1 of 3')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Next' }));
    expect(api.listExpenses).toHaveBeenLastCalledWith({ expense_type: '', payment_method: '', page: 2 });
  });

  it('creates an expense and notifies the dashboard', async () => {
    const onChanged = vi.fn();
    const create = vi.spyOn(api, 'createExpense').mockResolvedValue({ ...rent, id: 3 });
    render(<ExpensesPanel onChanged={onChanged} />);
    await userEvent.click(screen.getByRole('button', { name: 'Add expense' }));
    const dialog = screen.getByRole('dialog');
    await userEvent.type(within(dialog).getByLabelText('Amount'), '45');
    await userEvent.click(within(dialog).getByRole('button', { name: 'Save' }));
    expect(create).toHaveBeenCalledWith(expect.objectContaining({ amount: 45 }));
    expect(onChanged).toHaveBeenCalled();
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('deletes after confirmation', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    const remove = vi.spyOn(api, 'deleteExpense').mockResolvedValue(undefined);
    render(<ExpensesPanel onChanged={vi.fn()} />);
    await screen.findByText('800.00');
    await userEvent.click(screen.getAllByRole('button', { name: 'Delete' })[0]);
    expect(remove).toHaveBeenCalledWith(1);
  });

  it('does not delete when cancelled', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false);
    const remove = vi.spyOn(api, 'deleteExpense');
    render(<ExpensesPanel onChanged={vi.fn()} />);
    await screen.findByText('800.00');
    await userEvent.click(screen.getAllByRole('button', { name: 'Delete' })[0]);
    expect(remove).not.toHaveBeenCalled();
  });

  it('shows an error when the API fails', async () => {
    vi.mocked(api.listExpenses).mockRejectedValue(new Error('Cannot reach the API. Is the Django server running?'));
    render(<ExpensesPanel onChanged={vi.fn()} />);
    expect(await screen.findByRole('alert')).toHaveTextContent('Cannot reach the API');
  });
});
