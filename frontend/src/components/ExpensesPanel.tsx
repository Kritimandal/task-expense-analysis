import { useState } from 'react';
import { PAGE_SIZE, api } from '../api';
import { formatAmount } from '../format';
import { EXPENSE_TYPES, PAYMENT_METHODS, type Expense, type ExpenseInput } from '../types';
import { useAsync } from '../useAsync';
import { ExpenseForm } from './ExpenseForm';

export function ExpensesPanel({ onChanged }: { onChanged: () => void }) {
  const [expenseType, setExpenseType] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('');
  const [page, setPage] = useState(1);
  const [editing, setEditing] = useState<Expense | 'new' | null>(null);
  const [actionError, setActionError] = useState('');

  const list = useAsync(
    () => api.listExpenses({ expense_type: expenseType, payment_method: paymentMethod, page }),
    [expenseType, paymentMethod, page],
  );

  const pageCount = Math.max(1, Math.ceil((list.data?.count ?? 0) / PAGE_SIZE));

  function changeFilter(setter: (value: string) => void) {
    return (event: { target: { value: string } }) => {
      setter(event.target.value);
      setPage(1);
    };
  }

  async function save(data: ExpenseInput) {
    if (editing === 'new') {
      await api.createExpense(data);
    } else if (editing) {
      await api.updateExpense(editing.id, data);
    }
    setEditing(null);
    list.reload();
    onChanged();
  }

  async function remove(expense: Expense) {
    if (!window.confirm(`Delete expense #${expense.id} (${expense.expense_type}, ${formatAmount(expense.amount)})?`)) {
      return;
    }
    setActionError('');
    try {
      await api.deleteExpense(expense.id);
      if (list.data?.results.length === 1 && page > 1) {
        setPage(page - 1);
      } else {
        list.reload();
      }
      onChanged();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : 'Could not delete the expense.');
    }
  }

  return (
    <section className="card" aria-labelledby="expenses-title">
      <div className="card-head">
        <h2 id="expenses-title" className="card-title">Expenses</h2>
        <button type="button" className="button primary" onClick={() => setEditing('new')}>Add expense</button>
      </div>

      <div className="filters">
        <label className="inline-field">
          <span>Category</span>
          <select value={expenseType} onChange={changeFilter(setExpenseType)}>
            <option value="">All</option>
            {EXPENSE_TYPES.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </label>
        <label className="inline-field">
          <span>Payment</span>
          <select value={paymentMethod} onChange={changeFilter(setPaymentMethod)}>
            <option value="">All</option>
            {PAYMENT_METHODS.map((method) => (
              <option key={method} value={method}>{method}</option>
            ))}
          </select>
        </label>
        <span className="muted">{list.data ? `${list.data.count} records` : ''}</span>
      </div>

      {(list.error || actionError) && <p className="alert" role="alert">{list.error || actionError}</p>}

      <div className="table-scroll">
        <table aria-busy={list.loading}>
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Date</th>
              <th scope="col">Category</th>
              <th scope="col">Payment</th>
              <th scope="col" className="num">Amount</th>
              <th scope="col"><span className="visually-hidden">Actions</span></th>
            </tr>
          </thead>
          <tbody>
            {list.data?.results.map((expense) => (
              <tr key={expense.id}>
                <td className="muted">{expense.id}</td>
                <td>{expense.expense_date ?? <span className="muted">No date</span>}</td>
                <td>{expense.expense_type}</td>
                <td>{expense.payment_method}</td>
                <td className="num">{formatAmount(expense.amount)}</td>
                <td className="row-actions">
                  <button type="button" className="link" onClick={() => setEditing(expense)}>Edit</button>
                  <button type="button" className="link danger" onClick={() => remove(expense)}>Delete</button>
                </td>
              </tr>
            ))}
            {list.data && list.data.results.length === 0 && (
              <tr>
                <td colSpan={6} className="empty">No expenses match these filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <nav className="pager" aria-label="Pages">
        <button type="button" className="button" disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</button>
        <span className="muted">Page {page} of {pageCount}</span>
        <button type="button" className="button" disabled={page >= pageCount} onClick={() => setPage(page + 1)}>Next</button>
      </nav>

      {editing && (
        <div className="overlay" role="dialog" aria-modal="true" aria-label={editing === 'new' ? 'Add expense' : 'Edit expense'}>
          <div className="dialog">
            <ExpenseForm initial={editing === 'new' ? undefined : editing} onSubmit={save} onCancel={() => setEditing(null)} />
          </div>
        </div>
      )}
    </section>
  );
}
