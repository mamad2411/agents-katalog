---
name: follow-lib-tanstack-charts
description: Use TanStack Charts end to end — declarative grammar-of-graphics, series types, axes, tooltips
argument-hint: "[chart-type]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Charts fully — grammar-of-graphics charting: data + axes + series declarative config, series types, interactivity, responsive sizing

## Scope

For data visualization — **0.x (beta)**: the API may change, check `https://tanstack.com/charts/latest` before implementing; if you need a much more mature lib → consider Recharts/d3 via `/ask-me`

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the charts package

```bash
bun add @tanstack/react-charts
```

### 2. Grammar Model

> Goal: understand the grammar — data + scales/axes + series

```tsx
import { Chart } from '@tanstack/react-charts'

<Chart
  options={{
    data,                                        // array of datum objects
    primaryAxis: { getValue: (d) => d.label },   // x / category
    secondaryAxes: [{ getValue: (d) => d.value, elementType: 'bar' }],
  }}
/>
```

- Series `elementType`: `bar`, `line`, `area`, `pie`, `bubble`
- Multi-series: `data` is an array of series + multiple `secondaryAxes`
- Tooltip/hover work out of the box via options — custom renderers are possible

### 3. Patterns

> Goal: real charts

1. **Multiple series**: normalized data shape `{ label, s1, s2 }` + a separate axis per key
2. **Time series**: the primary axis `getValue` returns a Date — time scaling is automatic
3. **Responsive**: the container has a clear size — the chart follows its parent
4. **Theming**: colors via series options — map them to the app's design tokens
5. **Loading/empty**: handle `data: []` and loading states yourself (headless-ish)

### 4. Verify

> Goal: prove the chart renders with correct data before finishing

1. `/run-typecheck` + `/run-test`
2. Real render: axis labels, series shapes, tooltip
3. On failure → `/resolve-errors` max 3 rounds

## Rules

- Keep the `data` reference stable (`useMemo`) — a new array each render = a full chart re-render
- 0.x API — pin the exact version; never assume the API matches Recharts
- Colors via design tokens — no hardcoded hex in chart config
- Complex charts (brushing, custom marks) → read the full grammar docs first

## Expected Outcome

- Charts render correctly per the grammar config
- Responsive + themed to match the design system
