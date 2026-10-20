---
name: dynamic-chart-y-axis-scaling
description: "Dynamic Y-axis zoom for log-scaled Canvas 2D charts \u2014 auto-scale to data range, show floating goal indicators when targets are above viewport."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [canvas, charting, visualization, y-axis, zoom, log-scale]
    triggers: [chart zoom, Y-axis scaling, chart too zoomed out, too much headroom on chart, dynamic zoom, log scale viewport]
    related_skills: [canvas-2d-chart-implementation]
---

# Dynamic Y-axis Scaling for Log Charts

When a log-scale chart shows the full range ($100→$10M) but all data points cluster near the bottom, you need dynamic zooming.

## Pattern

1. **Find the data max** — max of current bankrolls and historical maxes
2. **Compute a tight ceiling** — ~1.5x headroom above max, rounded up to next nice number (1×, 2×, 5×, 10× of the current power-of-10)
3. **Clamp to absolute max** — never exceed the hard target (e.g., $10M)
4. **Draw grid levels dynamically** — only show horizontal lines within the visible range
5. **Floating goal indicator** — when the goal line is above the viewport, show a badge with an up-arrow instead

## Implementation (Canvas 2D)

### Dynamic ceiling calculation
```javascript
get yMaxLog() {
  const maxB = this.maxBankroll;
  let ceiling;
  if (maxB <= 100) {
    ceiling = 150;
  } else {
    const raw = maxB * 1.5;          // ~1.5x headroom
    const pow10 = Math.pow(10, Math.floor(Math.log10(raw)));
    const mantissa = raw / pow10;
    if (mantissa <= 1) ceiling = 1 * pow10;
    else if (mantissa <= 2) ceiling = 2 * pow10;
    else if (mantissa <= 5) ceiling = 5 * pow10;
    else ceiling = 10 * pow10;
  }
  ceiling = Math.min(ceiling, 10000000);
  return Math.log10(ceiling);
}
```

### Log scale Y mapping
```javascript
toPlotY(bankroll) {
  const minLog = 2; // $100 floor
  const maxLog = this.yMaxLog;
  const lv = Math.log10(bankroll);
  const norm = Math.max(0, Math.min(1, (lv - minLog) / (maxLog - minLog)));
  return this.margin.top + this.plotH * (1 - norm);
}
```

### Dynamic grid levels
Generate nice log-spaced levels within the visible range using {1, 2, 5} × 10ⁿ steps. Only draw lines that fall between `margin.top` and `margin.top + plotH`.

### Floating goal indicator
When `toPlotY(goal)` returns a Y above the visible area, render a small badge at the top of the chart showing the target and an up-arrow. When the goal comes into range, draw the actual line instead.

## Pitfalls

- **Too much headroom frustrates users** who want to see fine details at low levels. Start tight (1.5x) and only loosen if they complain the chart looks clipped. "Still too much headroom" means tighten the multiplier.
- **Empty data edge case** — always ensure at least 2 players or a reasonable default max before computing the ceiling.
- **Log of zero** — clamp bankroll to a minimum (e.g., $100 = log 2) before computing.
- **getter duplication** — if you patch a getter inline, the old declaration can get trapped inside the new one. Check for `get yMaxLog()` appearing exactly once.

## References

See `references/tac-odds-zoom-implementation.md` for the specific TAC Odds dashboard implementation details.

