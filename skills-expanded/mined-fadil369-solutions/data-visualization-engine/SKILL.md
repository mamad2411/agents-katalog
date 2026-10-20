---
name: "Data Visualization Engine"
version: "1.0.0"
description: "Creates interactive charts, graphs, and visual data representations. Supports D3, Chart.js, and custom canvas rendering."
author: "workspace"
activated: false
---

# Data Visualization Engine

Creates interactive charts, graphs, and visual data representations. Supports D3, Chart.js, and custom canvas rendering.

## Decision Framework

### When to Apply
Use when: Dashboards, reports, analytics views, data exploration interfaces

### When NOT to Apply
Don't use when: Simple data tables, single number displays

## Anti-Patterns

### 1. Misleading Charts
```javascript
// BAD: Truncated Y-axis exaggerates differences
options: { scales: { y: { min: 95, max: 100 } } }

// GOOD: Zero-based Y-axis
options: { scales: { y: { beginAtZero: true } } }
```

### 2. 3D Charts
3D charts distort data perception. Always prefer 2D.

### 3. No Legends
Charts without legends are meaningless when multiple series exist.


## Trigger Phrases

- "Create chart"
- "Data visualization"
- "Graph component"
- "Dashboard charts"
- "Interactive visualization"

## Patterns

### Responsive Chart Component
```javascript
const ChartContainer = ({ type, data, options }) => {
  const containerRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) chartRef.current.destroy();
    chartRef.current = new Chart(containerRef.current, {
      type, data,
      options: { responsive: true, maintainAspectRatio: false, ...options }
    });
    return () => chartRef.current?.destroy();
  }, [type, data, options]);

  return <div style={{ position: 'relative', height: '400px' }}>
    <canvas ref={containerRef} />
  </div>;
};
```

## Integration
- Works with: dashboard-composition-engine, performance-budget-enforcer

