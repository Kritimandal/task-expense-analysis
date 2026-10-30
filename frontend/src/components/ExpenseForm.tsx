import { useState, type FormEvent } from 'react';
import { ApiError } from '../api';
import { EXPENSE_TYPES, PAYMENT_METHODS, type Expense, type ExpenseInput } from '../types';

interface Props {
  initial?: Expense;
  onSubmit: (data: ExpenseInput) => Promise<void>;
  onCancel: () => void;
}

type FieldErrors = Record<string, string[]>;

export function validateExpense(values: { amount: string; payment_method: string }): FieldErrors {
  const errors: FieldErrors = {};
  const amount = Number(values.amount);
  if (values.amount.trim() === '' || Number.isNaN(amount)) {
    errors.amount = ['Enter an amount.'];
  } else if (amount < 0) {
    errors.amount = ['Amount cannot be negative.'];
  }
  if (!values.payment_method) {
    errors.payment_method = ['Choose a payment method.'];
  }
  return errors;
}

export function ExpenseForm({ initial, onSubmit, onCancel }: Props) {
  const [values, setValues] = useState({
    expense_type: initial?.expense_type ?? 'Groceries',
    amount: initial ? String(initial.amount) : '',
    expense_date: initial?.expense_date ?? '',
    payment_method: initial?.payment_method ?? 'Cash',
  });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const update = (field: keyof typeof values) => (event: { target: { value: string } }) =>
    setValues((previous) => ({ ...previous, [field]: event.target.value }));

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const clientErrors = validateExpense(values);
    setErrors(clientErrors);
    setFormError('');
    if (Object.keys(clientErrors).length) {
      return;
    }
    setSaving(true);
    try {
      await onSubmit({
        expense_type: values.expense_type as ExpenseInput['expense_type'],
        amount: Number(values.amount),
        expense_date: values.expense_date || null,
        payment_method: values.payment_method as ExpenseInput['payment_method'],
      });
    } catch (error) {
      if (error instanceof ApiError) {
        setErrors(error.fieldErrors);
        setFormError(error.message);
      } else {
        setFormError('Could not save the expense.');
      }
    } finally {
      setSaving(false);
    }
  }

  const errorProps = (field: string) => ({
    id: `expense-${field}`,
    'aria-invalid': !!errors[field]?.length,
    'aria-describedby': errors[field]?.length ? `expense-${field}-error` : undefined,
  });

  const fieldError = (field: string) =>
    errors[field]?.length ? (
      <span className="field-error" id={`expense-${field}-error`}>{errors[field].join(' ')}</span>
    ) : null;

  return (
    <form className="form" onSubmit={handleSubmit} noValidate>
      <h2 className="card-title">{initial ? `Edit expense #${initial.id}` : 'Add expense'}</h2>
      {formError && <p className="alert" role="alert">{formError}</p>}

      <div className="field">
        <label htmlFor="expense-expense_type">Category</label>
        <select value={values.expense_type} onChange={update('expense_type')} {...errorProps('expense_type')}>
          {EXPENSE_TYPES.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
        {fieldError('expense_type')}
      </div>

      <div className="field">
        <label htmlFor="expense-amount">Amount</label>
        <input
          type="number"
          inputMode="decimal"
          step="0.01"
          min="0"
          value={values.amount}
          onChange={update('amount')}
          {...errorProps('amount')}
        />
        {fieldError('amount')}
      </div>

      <div className="field">
        <label htmlFor="expense-expense_date">Date</label>
        <input type="date" value={values.expense_date} onChange={update('expense_date')} {...errorProps('expense_date')} />
        {fieldError('expense_date')}
      </div>

      <div className="field">
        <label htmlFor="expense-payment_method">Payment method</label>
        <select value={values.payment_method} onChange={update('payment_method')} {...errorProps('payment_method')}>
          {PAYMENT_METHODS.map((method) => (
            <option key={method} value={method}>{method}</option>
          ))}
        </select>
        {fieldError('payment_method')}
      </div>

      <div className="form-actions">
        <button type="button" className="button" onClick={onCancel}>Cancel</button>
        <button type="submit" className="button primary" disabled={saving}>
          {saving ? 'Saving…' : 'Save'}
        </button>
      </div>
    </form>
  );
}
