const currency = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const compact = new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 });
const monthName = new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' });

export const formatAmount = (value: number) => currency.format(value);

export const formatCompact = (value: number) => compact.format(value);

export const formatMonth = (month: string) => monthName.format(new Date(`${month}-01T00:00:00Z`));
