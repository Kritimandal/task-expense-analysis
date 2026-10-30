import { useMemo, useState } from 'react';
import { api } from './api';
import { BreakdownTable } from './components/BreakdownTable';
import { ExpensesPanel } from './components/ExpensesPanel';
import { MonthlyChart } from './components/MonthlyChart';
import { SummaryCards } from './components/SummaryCards';
import { TypeChart } from './components/TypeChart';
import { useAsync } from './useAsync';

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [year, setYear] = useState('');

  const reports = useAsync(
    () => Promise.all([api.totalsByType(), api.monthlyTotals(), api.breakdown()]),
    [refreshKey],
  );

  const [totals, allMonths, breakdown] = reports.data ?? [];
  const years = useMemo(
    () => [...new Set((allMonths ?? []).map((m) => m.month.slice(0, 4)))].sort(),
    [allMonths],
  );
  const months = (allMonths ?? []).filter((m) => !year || m.month.startsWith(year));

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Expense Dashboard</h1>
          <p className="muted">React frontend for the Django REST expense API</p>
        </div>
      </header>

      {reports.error && (
        <p className="alert" role="alert">
          {reports.error}{' '}
          <button type="button" className="link" onClick={reports.reload}>Try again</button>
        </p>
      )}
      {reports.loading && !reports.data && <p className="muted">Loading reports…</p>}

      {totals && breakdown && allMonths && (
        <>
          <SummaryCards breakdown={breakdown} months={allMonths} />
          <div className="grid">
            <TypeChart totals={totals} />
            <MonthlyChart months={months} years={years} year={year} onYearChange={setYear} />
          </div>
          <BreakdownTable breakdown={breakdown} />
        </>
      )}

      <ExpensesPanel onChanged={() => setRefreshKey((key) => key + 1)} />
    </div>
  );
}
