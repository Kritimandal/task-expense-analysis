import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { formatCompact } from '../format';
import type { TotalsByType } from '../types';
import { ChartTooltip } from './ChartTooltip';

export function TypeChart({ totals }: { totals: TotalsByType }) {
  const data = Object.entries(totals)
    .map(([name, total]) => ({ name, total }))
    .sort((a, b) => b.total - a.total);

  return (
    <figure className="card chart" aria-labelledby="type-chart-title">
      <figcaption id="type-chart-title" className="card-title">Spending by category</figcaption>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 16, bottom: 4, left: 8 }} barCategoryGap={6}>
          <CartesianGrid horizontal={false} stroke="var(--grid)" />
          <XAxis type="number" tickFormatter={formatCompact} stroke="var(--axis)" tick={{ fill: 'var(--muted)', fontSize: 12 }} />
          <YAxis type="category" dataKey="name" width={104} stroke="var(--axis)" tick={{ fill: 'var(--text)', fontSize: 13 }} tickLine={false} />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'var(--hover)' }} />
          <Bar dataKey="total" fill="var(--series)" isAnimationActive={false} radius={[0, 4, 4, 0]} maxBarSize={22} />
        </BarChart>
      </ResponsiveContainer>
    </figure>
  );
}
