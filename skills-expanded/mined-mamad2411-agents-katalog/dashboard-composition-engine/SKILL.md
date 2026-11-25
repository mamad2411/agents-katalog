---
name: "Dashboard Composition Engine"
version: "1.0.0"
description: "Composes data-rich dashboards from modular widget systems. Handles layout grids, data fetching, real-time updates, and responsive widget reflow."
author: "workspace"
activated: false
---

# Dashboard Composition Engine

Composes data-rich dashboards from modular widget systems. Handles layout grids, data fetching, real-time updates, and responsive widget reflow.

## Decision Framework

### When to Apply
Use when: Admin panels, analytics dashboards, monitoring UIs, data-heavy views

### When NOT to Apply
Don't use when: Simple data display, single chart, marketing pages

## Anti-Patterns

### 1. Too Many Widgets
Loading 20+ widgets simultaneously causes slow page load and high memory.

### 2. No Loading States
```javascript
// BAD: Blank space while loading
<Widget data={data} />

// GOOD: Skeleton loading
{loading ? <WidgetSkeleton /> : <Widget data={data} />}
```

### 3. Hardcoded Data
```javascript
// BAD: Static mock data
const revenue = 125000;

// GOOD: Fetch with error handling
const { data: revenue, error, loading } = useQuery('revenue', fetchRevenue);
```


## Trigger Phrases

- "Build dashboard"
- "Admin panel"
- "Widget layout"
- "Analytics view"
- "Monitoring dashboard"

## Patterns

### Widget Grid
```javascript
const DashboardGrid = ({ widgets, layouts }) => (
  <ResponsiveGridLayout layouts={layouts} breakpoints={{ lg: 1200, md: 996, sm: 768 }}>
    {widgets.map(w => (
      <div key={w.id}>
        <WidgetContainer title={w.title} loading={w.loading} error={w.error}>
          <w.component {...w.props} />
        </WidgetContainer>
      </div>
    ))}
  </ResponsiveGridLayout>
);
```

## Integration
- Works with: data-visualization-engine, performance-budget-enforcer, search-experience-designer

