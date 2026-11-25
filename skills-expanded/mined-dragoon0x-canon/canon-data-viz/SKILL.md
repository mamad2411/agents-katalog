---
name: canon-data-viz
description: Use when designing dashboards, metrics displays, KPI widgets, sparklines, progress indicators, or any data-dense UI that isn't a standard chart. Covers the big-number pattern, sparklines, progress bars, gauges, metric comparison, and dashboard composition. Trigger when the user mentions dashboard, KPI, metric, progress bar, gauge, sparkline, or data display.
---

# CANON · Data Visualization (Beyond Charts)

`canon-charts` covers standard chart types. This skill covers the smaller, denser data displays that fill dashboards and metric screens.

## Big number + context

The most effective data display is a large number with a small piece of context.

```
$2.4M
Revenue · ↑12% vs Q3
```

| Element | Spec |
|---|---|
| Number | 28–48px, font-weight 700, `tabular-nums` |
| Label | 12–14px, muted color, below or above |
| Trend indicator | ↑↓ arrow or colored percentage, 13–14px |
| Sparkline (optional) | 80–160px wide, 24–40px tall, below the number |

## Sparklines

Tiny line charts without axes. Show shape, not precision.

- Width: 80–160px. Height: 24–40px.
- No labels, no axes, no grid.
- Color: single color for the line. Optional fill gradient below (10–20% opacity).
- Hover: show exact value at the point.
- End dot: highlight current/latest value.

## Progress bars

| Type | Use |
|---|---|
| Determinate (%) | Known total (file upload, form completion) |
| Indeterminate | Unknown duration (processing, searching) |
| Segmented | Multi-step with known stages |
| Circular | Compact display (loading, completion %) |

Spec:
- Height: 4–8px for linear, 40–80px diameter for circular.
- Border radius: fully rounded.
- Color: brand for progress, muted for track.
- Percentage label: optional, but show it for determinate bars > 50px wide.
- `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`.

## Metric comparison

When showing before/after or period-over-period:

```
Revenue           Costs
$2.4M  ↑12%      $1.1M  ↓3%
vs $2.1M Q3      vs $1.13M Q3
```

- Align numbers right for comparison.
- Green for positive trends, red for negative (with ↑↓ arrows for colorblind safety).
- Comparison row in smaller, muted text.
- Use `tabular-nums` everywhere.

## Dashboard composition

- Most important metric: top-left (F-pattern entry).
- Max 6–8 widgets per screen before it needs drill-down.
- Consistent card heights per row.
- Global timeframe selector (don't make each widget have its own).
- Refresh indicator for live dashboards.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Giant chart where a big number would do | Overcomplicates a simple insight |
| Dashboard with 15 widgets | Information overload |
| Sparkline with axes | Defeats the purpose — too much detail for the space |
| Progress bar without ARIA | Screen readers don't announce progress |
| Red/green only for trends | Colorblind fail — add ↑↓ arrows |
| Each widget has its own date range | Confusing, not comparable |

## Audit checklist

- [ ] Big numbers use `tabular-nums` and bold weight
- [ ] Trend indicators pair color with ↑↓ arrows
- [ ] Sparklines have no axes (shape only)
- [ ] Progress bars have `role="progressbar"` + aria values
- [ ] Dashboard ≤ 8 widgets before drill-down
- [ ] Global timeframe selector
- [ ] Muted comparison text for context

## Sources

- Stephen Few · Information Dashboard Design
- Edward Tufte · sparkline concept
- `canon-charts` for standard chart types
- WCAG 2.2 · 1.4.1 Use of Color, 4.1.2 Name Role Value
