import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { formatCompact, formatMonth } from '../format';
import type { MonthlyTotal } from '../types';
import { ChartTooltip } from './ChartTooltip';

interface Props {
  months: MonthlyTotal[];
  years: string[];
  year: string;
  onYearChange: (year: string) => void;
}

export function MonthlyChart({ months, years, year, onYearChange }: Props) {
  const data = months.map((m) => ({ name: m.month, total: m.total }));

  return (
    <figure className="card chart" aria-labelledby="monthly-chart-title">
      <div className="card-head">
        <figcaption id="monthly-chart-title" className="card-title">Spending by month</figcaption>
        <label className="inline-field">
          <span>Year</span>
          <select value={year} onChange={(event) => onYearChange(event.target.value)}>
            <option value="">All</option>
            {years.map((y) => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </label>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 4, right: 8, bottom: 4, left: 0 }} barCategoryGap={4}>
          <CartesianGrid vertical={false} stroke="var(--grid)" />
          <XAxis
            dataKey="name"
            tickFormatter={(value: string) => formatMonth(value).split(' ')[0]}
            stroke="var(--axis)"
            tick={{ fill: 'var(--muted)', fontSize: 12 }}
            tickLine={false}
            interval={0}
          />
          <YAxis tickFormatter={formatCompact} width={44} stroke="var(--axis)" tick={{ fill: 'var(--muted)', fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip content={<ChartTooltip formatLabel={formatMonth} />} cursor={{ fill: 'var(--hover)' }} />
          <Bar dataKey="total" fill="var(--series)" isAnimationActive={false} radius={[4, 4, 0, 0]} maxBarSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </figure>
  );
}
