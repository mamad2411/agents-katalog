---
name: productize-create-viz
description: >-
  Create publication-quality visualizations with Python. Use when turning query results or a
  DataFrame into a chart, selecting the right chart type for a trend or comparison, generating
  a plot for a report or presentation, or creating an interactive chart with hover and zoom.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Create Viz

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

- **Skill**: `create-viz`
- **Lifecycle**: Design
- **Category**: Analytics
- **Primary artifact**: Create Viz UX/design review with findings, constraints, fixes, and acceptance checks

Create publication-quality data visualizations using Python.

## Argument Hint

`<data source> [chart type]`

## Usage

```text
/create-viz <data source> [chart type] [additional instructions]
```

## Workflow

### 1. Understand Request

Determine:
- Data source: query results, pasted data, CSV/XLSX, existing DataFrame, or data to query.
- Chart type: explicit or to be recommended.
- Purpose: exploration, presentation, report, dashboard component.
- Audience: technical, executive, external, or internal.

### 2. Get Data

If data tools are connected, query and load results into pandas.

If data is pasted or uploaded, parse and clean it. Convert dates, numeric columns, categories, and nulls deliberately.

### 3. Select Chart Type

If chart type is not specified, choose based on relationship:
- Trend over time: line chart.
- Category comparison or ranking: bar chart, horizontal for many categories.
- Part-to-whole: stacked bar or area. Avoid pie charts unless fewer than six categories and rough proportions are enough.
- Distribution: histogram, box plot, or violin plot.
- Correlation: scatter plot.
- Matrix: heatmap.
- Flow: Sankey.
- Geographic: map if location data exists.

Briefly explain the recommendation.

### 4. Generate Visualization

Use:
- matplotlib + seaborn for static publication-quality charts.
- plotly for interactive charts with hover, zoom, or HTML export.

Always include:
- Clear title that states the insight.
- Axis labels and units.
- Appropriate number formatting.
- Colorblind-friendly palette.
- Removed chart junk.
- Saved output file.

### 5. Quality Checks

- Bar charts start at zero.
- Labels and legends are readable.
- Categories are sorted meaningfully.
- Precision is appropriate.
- Color is meaningful, not decorative.
- Chart works in grayscale or has labels/line styles.
- Include data source and date range when known.

### 6. Save and Present

Save as PNG for static charts or HTML for interactive charts. Display or reference the file, include the code used, and suggest useful variants.

## Python Defaults

Use pandas, matplotlib, seaborn, and plotly where available. Prefer explicit imports, stable filenames, and reproducible code. For reports and presentations, use larger fonts and higher contrast.
