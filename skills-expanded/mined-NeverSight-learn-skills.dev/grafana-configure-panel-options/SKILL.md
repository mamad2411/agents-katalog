---
name: grafana-configure-panel-options
description: Configure Grafana panel display options after the query and visualization type are already correct. Use when tuning standard options, thresholds, value mappings, legends, tooltips, field overrides, and data links so a panel reads clearly and accurately.
---

# Grafana Configure Panel Options

Tune how a finished panel reads, not what it queries or which visualization it uses.

## When to Apply

Reference this skill when:

- The query is already correct.
- The visualization type is already correct.
- The remaining work is display tuning: units, decimals, min and max, display names, color behavior, thresholds, value mappings, legends, tooltips, overrides, or data links.
- You need to sort out whether a change belongs under true panel options or under field and display configuration.

Do not use this skill when:

- The query is wrong or incomplete.
- A transformation change is the real fix.
- The visualization type should change.

## Scope Boundary

Treat Grafana's true **Panel options** as the small set of panel-level settings:

- Title
- Description
- Transparent background
- Panel links
- Repeat options

This skill mostly owns the broader field and display surface that operators often call "panel options" in practice:

- Standard options
- Thresholds
- Value mappings
- Legend
- Tooltip
- Field overrides
- Data links

## Upstream Defaults

Official Grafana dashboards in this repo consistently bias toward a few display defaults after the panel type is chosen:

- Time series: `drawStyle = line`, `stacking = none` unless composition is the point, `legend = table` for comparison-heavy panels, and `tooltip = multi` for cross-series hover.
- Stat: `reduceOptions.calcs = ["lastNotNull"]` for current-state tiles, with color on value or background only when color carries meaning. Keep sparklines or graph mode off unless the trend itself matters.
- Gauge: use bounded metrics with explicit `min` and `max`, and pair the gauge with thresholds.
- Units: prefer the most specific built-in or custom unit that matches the metric semantics. Avoid generic units when the meaning is already known.

Grafana's generic docs and visualization-specific docs can drift. If you claim a control exists, confirm that the chosen visualization actually supports it.

## Workflow

1. Confirm the query and visualization are already correct.
2. If the request is really about title, description, transparency, panel links, or repeat behavior, answer that directly as a true panel-options change.
3. Start with [references/standard-options.md](references/standard-options.md) for units, scale, decimals, naming, color scheme, and missing-value display.
4. Use [references/thresholds-mappings.md](references/thresholds-mappings.md) for semantic state, coloring, and text replacement.
5. Use [references/legends-tooltips.md](references/legends-tooltips.md) for comparison-heavy or dense visualizations.
6. Use [references/overrides-links.md](references/overrides-links.md) for per-field exceptions and drill-down behavior.

## Reference Map

- [references/standard-options.md](references/standard-options.md) -> default field and display settings that apply broadly
- [references/thresholds-mappings.md](references/thresholds-mappings.md) -> semantic coloring and text replacement
- [references/legends-tooltips.md](references/legends-tooltips.md) -> scannability and hover behavior
- [references/overrides-links.md](references/overrides-links.md) -> targeted exceptions and click-through behavior

## Output

Return:

- The exact controls to set
- Whether each change is a true panel option or a field and display option
- Why the change improves readability or correctness
- Any visualization-specific support caveat that materially affects the recommendation
