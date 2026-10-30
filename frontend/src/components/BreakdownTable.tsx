import { formatAmount } from '../format';
import { PAYMENT_METHODS, type Breakdown } from '../types';

export function BreakdownTable({ breakdown }: { breakdown: Breakdown }) {
  return (
    <section className="card" aria-labelledby="breakdown-title">
      <h2 id="breakdown-title" className="card-title">Category by payment method</h2>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">Category</th>
              {PAYMENT_METHODS.map((method) => (
                <th key={method} scope="col" className="num">{method}</th>
              ))}
              <th scope="col" className="num">Total</th>
            </tr>
          </thead>
          <tbody>
            {breakdown.expense_types.map((row) => (
              <tr key={row.expense_type}>
                <th scope="row">{row.expense_type}</th>
                {PAYMENT_METHODS.map((method) => (
                  <td key={method} className="num">{formatAmount(row[method] ?? 0)}</td>
                ))}
                <td className="num strong">{formatAmount(row.total)}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <th scope="row">Grand total</th>
              <td colSpan={PAYMENT_METHODS.length} />
              <td className="num strong">{formatAmount(breakdown.grand_total)}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </section>
  );
}
