---
name: data-visualization
description: Data visualization patterns — Charts, graphs, dashboards, D3, Recharts, Chart.js design and implementation
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "**/*.html"]
alwaysApply: false
---

# Data Visualization Standards

Data visualization transforms raw numbers into insights. Good charts are clear, accessible, performant, and respect user intent.

---

## Chart Selection & Best Practices

**ALWAYS**:
- Choose chart type based on data: bar (categories), line (trends), pie (proportions), scatter (correlation)
- Use consistent color palette (brand colors, semantic meaning)
- Label axes, provide legend, add tooltips
- Make charts responsive (resize on mobile)
- Test accessibility: sufficient contrast, text labels, not color-only

**NEVER**:
- Use 3D effects (confuse data)
- Mix chart types without clear reason
- Truncate axis ranges to manipulate perception
- Use pie charts for >5 slices (use bar instead)
- Omit units or scales (10 what? Hours? Users? Revenue?)

### ✅ GOOD Chart Patterns

```typescript
// Recharts (React) — clean, responsive charting
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// Sample data
const data = [
  { month: 'Jan', users: 4000, revenue: 2400, expenses: 2200 },
  { month: 'Feb', users: 5200, revenue: 3000, expenses: 2100 },
  { month: 'Mar', users: 3800, revenue: 2200, expenses: 2290 },
];

// Line chart: trends over time
export function UserGrowthChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis label={{ value: 'Users', angle: -90, position: 'insideLeft' }} />
        <Tooltip formatter={(value) => `${value.toLocaleString()}`} />
        <Legend />
        <Line
          type="monotone"
          dataKey="users"
          stroke="#0066cc"
          name="Monthly Users"
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

// Bar chart: category comparison
export function RevenueComparison() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis label={{ value: 'Amount ($)', angle: -90, position: 'insideLeft' }} />
        <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
        <Legend />
        <Bar dataKey="revenue" fill="#0066cc" name="Revenue" />
        <Bar dataKey="expenses" fill="#ef4444" name="Expenses" />
      </BarChart>
    </ResponsiveContainer>
  );
}

// Tooltip with formatted values
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 border border-gray-200 rounded shadow">
        <p className="font-semibold">{label}</p>
        {payload.map((entry: any, i: number) => (
          <p key={i} style={{ color: entry.color }}>
            {entry.name}: {entry.value.toLocaleString()}
          </p>
        ))}
      </div>
    );
  }
  return null;
};
```

### ❌ BAD Chart Patterns

```typescript
// ❌ 3D pie chart (confuses data)
<PieChart data={data} type="3d" />

// ❌ No labels, units, or legend
<LineChart data={data}>
  <Line dataKey="value" stroke="blue" />
</LineChart>

// ❌ Truncated axis to exaggerate difference
<BarChart data={data}>
  <YAxis domain={[95, 100]} />  /* 5% difference looks huge */
</BarChart>

// ❌ Pie chart with 8+ slices (impossible to read)
<PieChart data={veryLargeArray} />
```

---

## Dashboard Layouts

**ALWAYS**:
- Use grid layout (3-column desktop, 1-column mobile)
- Prioritize metrics (top-left = most important)
- Group related charts (sales together, usage together)
- Provide time range selector (last 7 days, month, year)
- Update on schedule or manual refresh (not real-time polling)
- Show loading state and last update time

**NEVER**:
- Pack charts too densely (overwhelming)
- Use different scales for same metric across dashboard
- Auto-refresh every second (kills performance)
- Leave data stale (> 1 hour old)

### ✅ GOOD Dashboard Layout

```typescript
import { useState } from 'react';
import { Button, Card, Grid, DatePicker } from '@/components';

export function Dashboard() {
  const [dateRange, setDateRange] = useState<[Date, Date]>([
    new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    new Date(),
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const handleRefresh = async () => {
    setIsLoading(true);
    await fetchDashboardData(dateRange);
    setLastUpdate(new Date());
    setIsLoading(false);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header with controls */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex gap-4 items-center">
          <DatePicker value={dateRange} onChange={setDateRange} />
          <Button
            onClick={handleRefresh}
            isLoading={isLoading}
            variant="secondary"
          >
            Refresh
          </Button>
          <p className="text-sm text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </p>
        </div>
      </div>

      {/* Key metrics row */}
      <Grid cols={1} md={2} lg={4} gap={4} className="mb-6">
        <MetricCard label="Total Users" value="12,453" change="+12% this month" />
        <MetricCard label="Revenue" value="$48,200" change="+5% this month" />
        <MetricCard label="Conversion" value="3.2%" change="+0.4% this month" />
        <MetricCard label="Avg Order Value" value="$89.50" change="-2% this month" />
      </Grid>

      {/* Chart section */}
      <Grid cols={1} lg={2} gap={6}>
        <Card>
          <h2 className="text-xl font-bold mb-4">Revenue Trend</h2>
          <UserGrowthChart />
        </Card>
        <Card>
          <h2 className="text-xl font-bold mb-4">Traffic by Source</h2>
          <TrafficChart />
        </Card>
      </Grid>

      {/* Data table section */}
      <Card className="mt-6">
        <h2 className="text-xl font-bold mb-4">Recent Transactions</h2>
        <TransactionTable data={transactions} />
      </Card>
    </div>
  );
}

// Reusable metric card
function MetricCard({
  label,
  value,
  change,
}: {
  label: string;
  value: string;
  change: string;
}) {
  const isPositive = change.startsWith('+');
  return (
    <Card className="p-4">
      <p className="text-sm text-gray-600 mb-1">{label}</p>
      <p className="text-2xl font-bold mb-2">{value}</p>
      <p
        className={`text-sm ${
          isPositive ? 'text-green-600' : 'text-red-600'
        }`}
      >
        {change}
      </p>
    </Card>
  );
}
```

---

## D3.js Advanced Patterns

**ALWAYS**:
- Use D3 for custom, highly interactive visualizations
- Separate data transformation from rendering
- Use scales (linear, time, ordinal) for coordinate mapping
- Add transitions for smooth animations
- Bind data with proper D3 patterns (enter/update/exit)

**NEVER**:
- Use D3 for simple charts (Recharts is easier)
- Forget to clean up D3 selections (memory leaks)
- Mix D3 with React state (use React for interactivity)

### ✅ GOOD D3 Pattern

```typescript
import * as d3 from 'd3';
import { useEffect, useRef } from 'react';

interface DataPoint {
  x: number;
  y: number;
  group: string;
}

export function D3ScatterPlot({ data }: { data: DataPoint[] }) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || data.length === 0) return;

    const margin = { top: 20, right: 20, bottom: 30, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Scales
    const xScale = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.x) as number])
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.y) as number])
      .range([height, 0]);

    const colorScale = d3
      .scaleOrdinal<string>()
      .domain([...new Set(data.map((d) => d.group))])
      .range(['#0066cc', '#f59e0b', '#ef4444', '#10b981']);

    // Select/create SVG
    let svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous render

    svg = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add grid
    svg
      .append('g')
      .attr('class', 'grid')
      .attr('opacity', 0.1)
      .call(
        d3
          .axisLeft(yScale)
          .tickSize(-width)
          .tickFormat(() => '')
      );

    // Add circles with transitions
    svg
      .selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', (d) => xScale(d.x))
      .attr('cy', (d) => yScale(d.y))
      .attr('r', 4)
      .attr('fill', (d) => colorScale(d.group))
      .attr('opacity', 0.7)
      .on('mouseover', function () {
        d3.select(this).transition().attr('r', 6);
      })
      .on('mouseout', function () {
        d3.select(this).transition().attr('r', 4);
      });

    // Add axes
    svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale));

    svg.append('g').call(d3.axisLeft(yScale));

    // Add labels
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', height + 30)
      .attr('text-anchor', 'middle')
      .text('X Axis');

    svg
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -45)
      .attr('x', -height / 2)
      .attr('text-anchor', 'middle')
      .text('Y Axis');
  }, [data]);

  return <svg ref={svgRef} />;
}
```

---

## Chart Accessibility

**ALWAYS**:
- Provide text alternative (table of data below chart)
- Use sufficient color contrast (WCAG AA)
- Add axis labels and legend
- Make charts keyboard accessible (arrow keys navigate)
- Include data table for screen readers

**NEVER**:
- Use color alone to convey meaning (use patterns + labels)
- Create charts without legends
- Forget alt text for chart images

### ✅ GOOD Accessible Chart

```typescript
export function AccessibleChart({ data }: { data: DataPoint[] }) {
  return (
    <figure>
      {/* Chart with ARIA label */}
      <div
        role="img"
        aria-label="Revenue trend from January to March: $2400, $3000, $2200"
      >
        <RevenueChart data={data} />
      </div>

      {/* Data table for screen readers */}
      <figcaption>
        <h3 className="font-bold mb-2">Data Summary</h3>
        <table className="w-full text-sm border-collapse">
          <thead className="border-b-2">
            <tr>
              <th className="text-left">Month</th>
              <th className="text-right">Revenue</th>
              <th className="text-right">Change</th>
            </tr>
          </thead>
          <tbody>
            {data.map((d) => (
              <tr key={d.month} className="border-b">
                <td>{d.month}</td>
                <td className="text-right">${d.revenue}</td>
                <td className="text-right">{d.change}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </figcaption>
    </figure>
  );
}
```

---

## Performance Optimization

**ALWAYS**:
- Lazy-load chart libraries (don't bundle D3 on every page)
- Limit data points (aggregate or sample if > 1000 points)
- Use canvas for very large datasets (> 10k points)
- Debounce resize handlers
- Memoize expensive calculations

**NEVER**:
- Re-render entire chart on every data point change
- Load D3 + Recharts simultaneously
- Keep full dataset in memory

### ✅ GOOD Performance Pattern

```typescript
import { useMemo, useCallback } from 'react';
import dynamic from 'next/dynamic';

// Lazy load chart library
const RevenueChart = dynamic(() => import('./RevenueChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

export function DashboardChart({ data }: { data: DataPoint[] }) {
  // Aggregate data if too many points
  const aggregatedData = useMemo(() => {
    if (data.length > 1000) {
      return aggregateByDay(data);
    }
    return data;
  }, [data]);

  // Debounce resize
  const handleResize = useCallback(
    debounce(() => {
      // Re-render chart
    }, 300),
    []
  );

  useEffect(() => {
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [handleResize]);

  return <RevenueChart data={aggregatedData} />;
}
```

---

## Data Visualization Checklist

- [ ] Chart type matches data (bar/line/pie/scatter)
- [ ] Axes labeled with units
- [ ] Legend provided
- [ ] Colors accessible (WCAG AA contrast)
- [ ] Responsive on mobile
- [ ] Tooltip/hover interaction
- [ ] Data table alternative provided
- [ ] No 3D effects
- [ ] No pie charts with > 5 slices
- [ ] Performance optimized (< 1000 points)
- [ ] Lazy-loaded if heavy library (D3)
- [ ] Last update time displayed

---

## Summary

Good data visualization:
1. **Accurate** — Truthfully represents data
2. **Clear** — Easy to understand at a glance
3. **Accessible** — Color contrast, labels, alternatives
4. **Responsive** — Works on mobile and desktop
5. **Performant** — Aggregates large datasets, lazy-loaded
6. **Interactive** — Tooltips, hover states, drill-down options

Choose the right chart type and keep it simple.
