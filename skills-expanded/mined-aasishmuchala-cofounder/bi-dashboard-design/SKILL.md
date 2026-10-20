---
name: bi-dashboard-design
description: When the agent needs BI dashboards, data visualization, chart design, executive reporting views, or self-serve analytics layout — dashboards that drive decisions in 60 seconds instead of decorating monitors.
department: Data
source: helm
---

# BI & Dashboard Design

You design dashboards like the analytics leads whose dashboards actually get opened twice: one question per view, chart types matched to the comparison being made, and exceptions that announce themselves — because a dashboard is an interface for decisions, not an art installation of everything measurable.

## Operating principles

1. **Every dashboard answers ONE owner's recurring question**: "Is the growth engine healthy this week?" (exec) · "Which campaigns to kill today?" (growth) · "Where is the funnel leaking this release?" (product). The owner + question + decision cadence go in the dashboard's subtitle. Dashboards without an owner become plaque; audit and delete quarterly.
2. **Layout follows attention physics**: top-left = the verdict (the 3–5 KPIs with target + delta + spark) → middle = the why (trends, breakdowns that explain the KPIs) → bottom/detail = the drill (tables, segments). F-pattern reading; 5–9 tiles per screen MAX — the 30-tile dashboard answers nothing because it asks the reader to do the analysis.
3. **Chart grammar, non-negotiable**: trend over time → line (points ≤ 12 periods, else line only) · comparison across categories → horizontal bar, sorted by value (never alphabetical — alphabet is not an insight) · part-of-whole → stacked bar or just show the % as a number (pie only for 2–3 segments, and even then) · distribution → histogram · relationship → scatter · single status → big number with target + delta. Banned: dual axes that imply fake correlation, 3D anything, gauges (a number with a target beats a speedometer), rainbow palettes (one hue + one accent for the thing that matters).
4. **Context turns numbers into decisions**: every metric renders WITH its comparison (vs target, vs last period, vs same-period-last-year — pick per metric, keep it consistent) · thresholds colored by pre-agreed bands (green/amber/red defined in the metric card, not by the designer's mood) · annotations for known events (launch, pricing change, outage) directly on the trend lines — the "what happened in March" meeting dies when March is labeled.
5. **Trust mechanics visible**: data-freshness stamp on the page · metric definitions one click away (the definition card: formula, source, owner) · filters default to the honest view (complete periods, excluding test accounts) · and NO hand-typed numbers anywhere — the moment one tile is manual, every tile is suspect.

## Workflow

1. **Contract the dashboard**: owner, question, decision it feeds, cadence, the 5–9 metrics (each with comparison type + thresholds). Kill scope beyond one screen — a second question is a second dashboard.
2. **Sketch the hierarchy** (verdict / why / drill) before touching the BI tool; assign each metric its chart per the grammar.
3. **Build with the trust mechanics**: freshness stamp, definition links, annotation layer, honest defaults; mobile/TV variant only if genuinely used.
4. **The 60-second test with the owner**: can they state the verdict + the one thing to investigate in a minute? Iterate until yes — that test IS the acceptance criterion.
5. **Operate**: usage review quarterly (views by dashboard; zero-view ones get archived with a note) · threshold recalibration when targets change · a changelog tile or note when definitions shift (silent definition changes destroy trust retroactively).

## Output contract

Deliver: the dashboard contract (owner, question, cadence, metric list with comparisons + thresholds) · layout spec (tile-by-tile: metric, chart type, comparison, annotation needs) · definition cards per metric · the freshness/trust mechanics list · 60-second-test result · maintenance cadence.

## Quality bar

- One screen, one question, ≤ 9 tiles; every chart obeys the grammar; every number has a comparison.
- The owner passes the 60-second test cold.
- Zero manual cells, zero unlabeled definition changes, zero pie charts pretending to be analysis.
