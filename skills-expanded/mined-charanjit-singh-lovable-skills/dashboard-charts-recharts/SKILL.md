---
name: dashboard-charts-recharts
description: >-
  Use when building dashboards, charts, KPI cards, trend lines, or analytics UI
  with Recharts or shadcn's chart components. Not for static landing-page
  graphics or product analytics tracking (use analytics-events).
---

# Dashboards and charts (Recharts)

Use **Recharts** (wrapped by shadcn's `Chart` components when available). One chart library per app — don't mix Recharts, Chart.js, and Victory.

## Data shape

Aggregate **on the server** (SQL `group by`, RPC, materialized view) — never load 50k rows and group in the browser.

```ts
type DailyRevenue = { day: string; revenue_cents: number };

export async function fetchDailyRevenue(orgId: string, days = 30): Promise<DailyRevenue[]> {
  const { data, error } = await supabase.rpc("daily_revenue", { p_org: orgId, p_days: days });
  if (error) throw error;
  return data;
}
```

## KPI card

Show **value + delta + sparkline**. A bare number is rarely enough.

```tsx
<Card>
  <CardHeader>
    <CardDescription>Revenue (30d)</CardDescription>
    <CardTitle>${formatMoney(total)}</CardTitle>
    <DeltaBadge value={delta} />
  </CardHeader>
  <CardContent className="h-16">
    <Sparkline data={series} />
  </CardContent>
</Card>
```

## Line / area chart

```tsx
<ResponsiveContainer width="100%" height={260}>
  <AreaChart data={data}>
    <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
    <XAxis dataKey="day" tickFormatter={formatShortDate} />
    <YAxis tickFormatter={formatMoney} />
    <Tooltip content={<ChartTooltip />} />
    <Area
      dataKey="revenue_cents"
      stroke="hsl(var(--primary))"
      fill="hsl(var(--primary) / 0.15)"
    />
  </AreaChart>
</ResponsiveContainer>
```

Read colors from CSS variables so charts respect light/dark theme (`dark-mode-and-theming`).

## Empty, loading, error

Charts are data UI — apply `error-states-and-empty-ui`:

- Loading: skeleton matching chart bounds (avoid layout shift).
- Empty: "No data yet — your first events will appear here."
- Error: retry button.

## Performance

- Aggregate server-side; cap returned points (≤ 365 days, ≤ 100 points for sparklines).
- Lazy-load chart routes (`React.lazy`) — Recharts adds bundle weight.
- Memoize derived series with `useMemo` keyed on raw data.

## Accessibility

- Provide a textual summary near each chart (`<span className="sr-only">Revenue rose 14% in 30 days</span>`).
- Don't rely on color alone to differentiate series — use line style or labels too.

## Avoid

- Grouping/filtering large datasets in the browser.
- Charts inside infinite-scroll lists without virtualization.
- Hardcoded chart colors that break in dark mode.
- Pie charts with > 5 slices (use a bar chart).

## Checklist

- [ ] Aggregation in SQL / RPC.
- [ ] Loading / empty / error states.
- [ ] Theme-aware colors.
- [ ] Accessible summary text.
