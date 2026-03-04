import { useEffect, useState } from 'react';
import { Pie, PieChart, Cell, Tooltip } from 'recharts';
import { api } from '../api/client';

const COLORS = ['#16a34a', '#dc2626'];

export default function DashboardPage() {
  const [summary, setSummary] = useState({ total_days: 0, late_days: 0 });

  useEffect(() => {
    const now = new Date();
    api.get(`/attendance/report/monthly?month=${now.getMonth() + 1}&year=${now.getFullYear()}`)
      .then((res) => setSummary(res.data))
      .catch(() => {});
  }, []);

  const data = [
    { name: 'On Time', value: Math.max(summary.total_days - summary.late_days, 0) },
    { name: 'Late', value: summary.late_days }
  ];

  return (
    <div>
      <h2>Monthly Attendance Summary</h2>
      <PieChart width={320} height={260}>
        <Pie data={data} dataKey="value" outerRadius={90} label>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip />
      </PieChart>
    </div>
  );
}
