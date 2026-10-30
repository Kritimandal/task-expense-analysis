import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { ApiError } from '../api';
import { ExpenseForm, validateExpense } from '../components/ExpenseForm';

describe('validateExpense', () => {
  it('requires an amount', () => {
    expect(validateExpense({ amount: '', payment_method: 'Cash' }).amount).toEqual(['Enter an amount.']);
  });

  it('rejects negative amounts', () => {
    expect(validateExpense({ amount: '-1', payment_method: 'Cash' }).amount).toEqual(['Amount cannot be negative.']);
  });

  it('accepts valid input', () => {
    expect(validateExpense({ amount: '12.50', payment_method: 'Cash' })).toEqual({});
  });
});

describe('ExpenseForm', () => {
  it('does not submit when the amount is missing', async () => {
    const onSubmit = vi.fn();
    render(<ExpenseForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(screen.getByText('Enter an amount.')).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('submits typed values', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<ExpenseForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    await userEvent.selectOptions(screen.getByLabelText('Category'), 'Rent');
    await userEvent.type(screen.getByLabelText('Amount'), '850.25');
    await userEvent.type(screen.getByLabelText('Date'), '2023-05-01');
    await userEvent.selectOptions(screen.getByLabelText('Payment method'), 'Credit Card');
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(onSubmit).toHaveBeenCalledWith({
      expense_type: 'Rent',
      amount: 850.25,
      expense_date: '2023-05-01',
      payment_method: 'Credit Card',
    });
  });

  it('sends null when the date is empty', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<ExpenseForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    await userEvent.type(screen.getByLabelText('Amount'), '5');
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(onSubmit.mock.calls[0][0].expense_date).toBeNull();
  });

  it('shows field errors returned by the API', async () => {
    const onSubmit = vi.fn().mockRejectedValue(
      new ApiError(400, 'Please fix the highlighted fields.', { amount: ['Ensure that there are no more than 12 digits in total.'] }),
    );
    render(<ExpenseForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    await userEvent.type(screen.getByLabelText('Amount'), '1');
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Please fix the highlighted fields.');
    expect(screen.getByText('Ensure that there are no more than 12 digits in total.')).toBeInTheDocument();
    expect(screen.getByLabelText('Amount')).toHaveAttribute('aria-invalid', 'true');
  });

  it('fills in values when editing', () => {
    const expense = { id: 7, expense_type: 'Transport' as const, amount: 20, expense_date: '2023-02-02', payment_method: 'Cash' as const };
    render(<ExpenseForm initial={expense} onSubmit={vi.fn()} onCancel={vi.fn()} />);
    expect(screen.getByText('Edit expense #7')).toBeInTheDocument();
    expect(screen.getByLabelText('Amount')).toHaveValue(20);
    expect(screen.getByLabelText('Category')).toHaveValue('Transport');
  });
});
