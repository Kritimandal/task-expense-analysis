import type { TooltipProps } from 'recharts';
import { formatAmount } from '../format';

interface Props extends TooltipProps<number, string> {
  formatLabel?: (label: string) => string;
}

export function ChartTooltip({ active, payload, label, formatLabel }: Props) {
  if (!active || !payload?.length) {
    return null;
  }
  const name = String(label ?? payload[0].payload?.name ?? '');
  return (
    <div className="tooltip">
      <div className="tooltip-label">{formatLabel ? formatLabel(name) : name}</div>
      <div className="tooltip-value">{formatAmount(Number(payload[0].value))}</div>
    </div>
  );
}
