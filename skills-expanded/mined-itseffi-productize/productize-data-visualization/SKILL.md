---
name: productize-data-visualization
description: >-
  Create effective data visualizations with Python using matplotlib, seaborn, and plotly. Use
  when choosing chart types, building charts, creating publication-quality figures, or
  applying visualization design principles like accessibility and color theory.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Data Visualization

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `data-visualization`
- **Lifecycle**: Design
- **Category**: Analytics
- **Primary artifact**: Data Visualization UX/design review with findings, constraints, fixes, and acceptance checks

Helper skill for chart selection, Python visualization patterns, design principles, and accessibility.

## Invocation

This is primarily a support skill for `analyze`, `create-viz`, `build-dashboard`, and `metrics-review`. Use it explicitly when chart-design guidance is needed.

Use `visual-decision-making-review` instead when the user asks whether a chart, slide,
dashboard, canvas, or diagram may bias a decision, create overconfidence, hide alternatives,
or distort executive/stakeholder judgment.

## Chart Selection

Choose by data relationship:

| Relationship | Best Chart | Alternatives |
|---|---|---|
| Trend over time | Line chart | Area chart |
| Category comparison | Bar chart | Horizontal bar, lollipop |
| Ranking | Horizontal bar | Dot plot, slope chart |
| Part-to-whole | Stacked bar | Treemap, waffle |
| Composition over time | Stacked area | 100 percent stacked bar |
| Distribution | Histogram | Box, violin, strip |
| Correlation | Scatter | Bubble chart |
| Correlation matrix | Heatmap | Pair plot |
| Geographic | Choropleth | Bubble map |
| Flow | Sankey | Funnel |
| Target performance | Bullet chart | Gauge only for one KPI |
| Many KPIs | Small multiples | Dashboard |

Avoid:
- Pie charts unless fewer than six categories and rough proportion is enough.
- 3D charts.
- Dual-axis charts unless clearly labeled and justified.
- Stacked bars with many middle segments.

## Python Patterns

Use matplotlib + seaborn for static publication charts:

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("colorblind")
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
```

Use plotly for interactive charts:

```python
import plotly.express as px
fig = px.line(df, x="date", y="value", color="category", title="Metric trend")
fig.update_layout(hovermode="x unified")
fig.write_html("interactive_chart.html")
```

Always include:
- Insight-led title.
- Axis labels and units.
- Proper number formatting.
- Data source and date range when known.
- Saved output file.

## Design Principles

Color:
- Use color to encode meaning, not decoration.
- Use a colorblind-friendly palette.
- Highlight the story and gray out context.
- Use sequential palettes for ordered values and diverging palettes around meaningful midpoints.

Typography:
- Title states the insight.
- Subtitle provides scope, date range, or filters.
- Labels are readable.
- Data labels are used only when they add clarity.

Layout:
- Remove chart junk.
- Sort categories by value unless natural order matters.
- Use consistent scales across small multiples.
- Give the chart enough whitespace.

Accuracy:
- Bar charts start at zero.
- Do not hide axis breaks.
- Show uncertainty when relevant.
- Do not overstate precision.

## Accessibility Checklist

- Chart works without relying on color alone.
- Text is readable at standard zoom.
- Title describes the insight.
- Axes include units.
- Legend is clear and unobtrusive.
- Data source and date range are noted.
- Provide a table alternative when possible.
