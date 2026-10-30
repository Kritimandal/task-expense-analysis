import { formatAmount, formatMonth } from '../format';
import type { Breakdown, MonthlyTotal } from '../types';

interface Props {
  breakdown: Breakdown;
  months: MonthlyTotal[];
}

export function SummaryCards({ breakdown, months }: Props) {
  const largest = [...breakdown.expense_types].sort((a, b) => b.total - a.total)[0];
  const busiest = [...months].sort((a, b) => b.total - a.total)[0];
  const average = months.length ? months.reduce((sum, m) => sum + m.total, 0) / months.length : 0;

  return (
    <div className="stats">
      <div className="stat">
        <span className="stat-label">Total spent</span>
        <span className="stat-value">{formatAmount(breakdown.grand_total)}</span>
      </div>
      <div className="stat">
        <span className="stat-label">Largest category</span>
        <span className="stat-value">{largest ? largest.expense_type : '—'}</span>
        {largest && <span className="stat-note">{formatAmount(largest.total)}</span>}
      </div>
      <div className="stat">
        <span className="stat-label">Busiest month</span>
        <span className="stat-value">{busiest ? formatMonth(busiest.month) : '—'}</span>
        {busiest && <span className="stat-note">{formatAmount(busiest.total)}</span>}
      </div>
      <div className="stat">
        <span className="stat-label">Monthly average</span>
        <span className="stat-value">{formatAmount(average)}</span>
        <span className="stat-note">{months.length} months with dated expenses</span>
      </div>
    </div>
  );
}
