---
name: productize-build-dashboard
description: >-
  Build an interactive HTML dashboard with charts, filters, and tables. Use when creating an
  executive KPI overview, turning query results into a shareable report, building a monitoring
  snapshot, or combining multiple charts and filters in one browser-openable file.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Build Dashboard

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

- **Skill**: `build-dashboard`
- **Lifecycle**: Design
- **Category**: Analytics
- **Primary artifact**: Build Dashboard UX/design review with findings, constraints, fixes, and acceptance checks

Build a browser-openable interactive HTML dashboard with KPI cards, charts, filters, tables, and professional styling.

## Argument Hint

`<description> [data source]`

## Usage

```text
/build-dashboard <description of dashboard> [data source]
```

## Workflow

### 1. Understand Requirements

Determine:
- Purpose: executive overview, operational monitoring, deep-dive analysis, team report.
- Audience.
- Key metrics.
- Filter dimensions.
- Data source: query, pasted data, CSV/XLSX, or sample data.

### 2. Gather Data

If warehouse, analytics, or spreadsheet tools are connected, query or parse the data and embed results as JSON.

If only a description is provided, create realistic sample data and clearly label it as sample data.

### 3. Design Layout

Default pattern:
- Header with title and filters.
- 2-4 KPI cards.
- 1-3 charts for trends and breakdowns.
- Sortable detail table.
- Footer with data date and source.

Adapt layout to the content. Do not force a table if the data is already summarized.

### 4. Build HTML

Generate one HTML file with:
- Semantic HTML.
- Responsive CSS Grid or Flexbox.
- KPI cards.
- Chart containers.
- Filter controls.
- Sortable and paginated table if needed.
- Embedded JSON data.
- JavaScript class or module to handle filters, charts, KPIs, and table updates.

Use Chart.js or another lightweight chart library. If the dashboard must work offline, vendor or inline the library. If using CDN, state that internet access is required.

### 5. Add Interactivity

Include:
- Dropdown and date filters.
- Shared filter state that updates all cards, charts, and tables.
- Sortable table columns.
- Tooltip formatting.
- Number formatting for currency, percentage, and large numbers.

### 6. Performance Rules

- Under 1,000 rows: embed raw data.
- 1,000-10,000 rows: embed data but pre-aggregate charts where useful.
- 10,000-100,000 rows: embed aggregates and a table sample.
- Over 100,000 rows: recommend BI tooling, pagination, or server-backed dashboard.

Limit visible table rows and avoid rebuilding unnecessary DOM on filter changes.

### 7. Verify

Open the generated HTML in the browser when browser tooling is available. Check layout, console errors, filters, charts, and responsive behavior.

## Output Rules

- Save with a descriptive filename.
- Include where the file was written.
- Note whether data is real or sample.
- Explain how to swap in real data if sample data was used.
