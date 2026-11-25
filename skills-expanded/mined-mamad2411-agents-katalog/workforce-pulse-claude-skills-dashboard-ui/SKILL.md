# Dashboard UI

Next.js App Router page (`src/app/page.tsx`) renders `Dashboard.tsx`, which composes every panel and owns filter state.

## Component map (`src/components/dashboard`)
- `Dashboard.tsx` — top-level state container, fetches `/api/analytics?filters`, renders all sections.
- `DashboardHeader.tsx` — date range, active filter chips, refresh.
- `Sidebar.tsx` — department / task / app / employee `<Select>`s; emits `DashboardFilters`.
- `HeadlineCards.tsx` — recoverable hours/month, recoverable INR/month, repetitive %, anomaly badge.
- `ExecutiveSummary.tsx` + `executive-summary-export` DOM id — also the **export root** (see export skill).
- `TimeSinkBreakdown.tsx` — task category + app breakdowns.
- `DepartmentRepetitiveChart.tsx`, `TaskRecoverableChart.tsx`, `TrendChart.tsx` — Recharts.
- `AutomationRanking.tsx` — top-N table driven by automation score.
- `AnomalyCallout.tsx` — single outlier surfaced by the anomaly rule.
- `EmployeeDrilldown.tsx` — per-employee details when an employee filter is active.
- `CleaningSummary.tsx` — data-quality audit (counts + per-issue rows).
- `MethodologyDrawer.tsx` / `MethodologyPanel.tsx` / `MethodologyContent.tsx` — methodology popout.
- `DeferredMount.tsx` — defers heavy charts until idle to keep first paint snappy.

## UI primitives (`src/components/ui`)
`Badge`, `Button`, `Card`, `Select`, `Tooltip`, `SectionHeader`, `ChartSkeleton`, `SectionSkeleton`, `LoadingScreen`. No external UI kit — Tailwind only.

## Styling
- Tailwind (`tailwind.config.ts`, `globals.css`).
- Chart palette + axes centralized in `src/lib/chartTheme.ts`.

## Filter contract
Filters travel as query params to `/api/analytics`. AND-combined. Resetting clears all four. Active filters are echoed in the export.
