---
name: data-visual-report-builder
description: Use this skill when the user provides tabular or structured data and needs statistical insight, chart selection, KPI summaries, or a data visualization report, especially Markdown or self-contained HTML reports. Do not use for software UI prototypes or general frontend application development.
meta:
  version: 2
  display_name: 数据可视化报告生成器
  source: claude-office-skills data-analysis/chart-designer/excel-automation; coffeefuelbump/csv-data-summarizer-claude-skill; anthropics/skills xlsx reviewed-not-bundled
  license: MIT
---

# Data Visual Report Builder

## Trigger

Use this Skill when:

- The user uploads or pastes CSV, Excel/xlsx, JSON, Markdown tables, TSV, small copied tables, exported reports, logs with structured fields, or spreadsheet-like data.
- The user asks to analyze table data, find patterns, summarize metrics, compare categories, inspect data quality, or extract data-backed insights.
- The user asks to inspect schema, clean or normalize tabular text, reconcile records, define metrics, or validate calculated results.
- The user asks for a data report, statistical summary, KPI report, trend analysis, dashboard-like report, visualization report, or chart recommendation.
- The user asks for an HTML report with charts, KPI cards, highlighted tables, timelines, funnels, comparison matrices, or visual data sections.
- The user asks to compare options, departments, regions, channels, products, cohorts, scenarios, campaigns, vendors, or time periods using data.
- The user asks to turn data into findings, risks, recommendations, executive summaries, appendix tables, or report specifications.

Prefer this Skill when structured data and analysis are central. If the request is only about final HTML packaging, visual layout, print styling, or single-file report assembly from already analyzed material, use `html-report-builder`.

## Non-goals

This Skill does not own:

- Software UI prototypes.
- App pages or product interfaces.
- Web frontend engineering.
- React, Vue, Next.js, Vite, Tailwind, shadcn/ui, or component projects.
- SaaS dashboard product design.
- Database modeling.
- ETL platform construction.
- BI platform configuration.
- External SaaS connection, Google Sheets API, Composio automation, MCP server setup, or remote data sync.
- Spreadsheet file generation as the primary deliverable; use spreadsheet-specific tools or Skills when available.
- Automatic deployment, GitHub Pages, Vercel, Netlify, iframe publishing, plugin marketplace, or local listener workflows.
- Artifact lifecycle management, storage policy, file permission policy, or final artifact validation ownership; use `artifact-management` for artifact lifecycle when visible.
- Replacing `html-report-builder` for final HTML visual wrapping when that Skill exists and the user needs polished single-file HTML.
- Inventing conclusions, numbers, baselines, causes, dates, targets, or recommendations without data support.

## Inputs

Acceptable inputs include:

- Data files: CSV, TSV, Excel/xlsx, JSON, exported spreadsheet tables, log/event files, or query outputs.
- Pasted data: Markdown tables, copied spreadsheet ranges, key-value lists, compact JSON arrays, or small text tables.
- Metadata: field definitions, data dictionary, units, formulas, metric definitions, source notes, time zone, currency, filters, or inclusion/exclusion rules.
- Business context: user question, decision need, audience, target metric, reporting period, comparison dimensions, or action constraints.
- User-specified chart type, output format, report language, privacy limits, sampling rules, and known data caveats.

If input is too large or not loaded yet, use visible XAgent tools to inspect or request the smallest useful sample, schema, summary, or file path. Do not assume access to files, spreadsheets, databases, SaaS, or web resources that are not visible in the session.

## Output Contract

Produce one or more of:

- Brief conclusion with data-backed findings.
- Data quality note.
- Field and schema summary.
- Statistical summary.
- Grouped aggregation table.
- KPI summary.
- Trend or comparison analysis.
- Chart recommendations.
- Chart specification for native SVG/HTML/CSS/vanilla JS rendering.
- Markdown data analysis report.
- HTML data report when explicitly requested and feasible.
- `report-spec` JSON or Markdown that can be handed to `html-report-builder`.
- Limitations, assumptions, unverified items, and follow-up data needs.
- Degraded output when data cannot be analyzed.

Default `report-spec` shape:

```json
{
  "title": "Report title",
  "audience": "target reader",
  "data_sources": ["source or file reference"],
  "data_quality": ["quality note"],
  "kpis": [{"label": "metric", "value": "value", "unit": "unit", "basis": "source field or formula"}],
  "sections": [{"title": "section", "finding": "data fact", "interpretation": "marked interpretation"}],
  "charts": [{"type": "bar|line|area|table|funnel|waterfall|timeline|matrix", "title": "chart title", "fields": ["x", "y"], "unit": "unit", "source": "source"}],
  "tables": [{"title": "table title", "columns": ["field"], "notes": "limits"}],
  "recommendations": [{"action": "suggested action", "evidence": "supporting data"}],
  "limitations": ["assumption or unverified item"]
}
```

When producing HTML directly, follow the HTML Report Rules below and keep the result data/report-oriented, not app-like.

## Workflow

1. Clarify the business question only when necessary.
2. Inspect available data and source material.
3. Identify fields, types, units, time ranges, dimensions, and measures.
4. Check data quality before drawing conclusions.
5. Decide whether the task needs cleaning, transformation, descriptive statistics, comparison, anomaly inspection, chart selection, or report narrative.
6. Run, request, or manually reason through appropriate analysis using only visible tools and inspected data.
7. Validate results against row counts, totals, samples, formulas, denominators, and source constraints.
8. Separate data facts, interpretations, recommendations, and unknowns.
9. Choose visualizations only when they clarify the question.
10. Generate the requested analysis, chart spec, report handoff, or concise answer.
11. State limitations and follow-up data needs.

## Data Understanding Modules

Cover these input and analysis situations when relevant:

- CSV, TSV, Excel/xlsx, JSON, Markdown tables, pasted spreadsheet ranges, and small copied tables.
- Multiple tables that need joining, reconciliation, or side-by-side comparison.
- Data dictionary, field comments, known formulas, source system notes, and user-supplied metric definitions.
- Business question, intended audience, reporting period, and required decision.
- Wide tables, long tables, nested JSON, time series, categorical survey responses, funnel stages, event logs, and financial/expense rows.

For each dataset, identify:

- row count, column count, source reference, and time range;
- field names and likely types;
- dimensions, measures, IDs, dates, categories, and free-text fields;
- unit, currency, percentage basis, denominator, and aggregation level;
- source quality and privacy sensitivity.

## Data Quality Rules

- Mark unknown field meaning instead of guessing.
- Report missing values, duplicate records, suspicious duplicates, abnormal blanks, and parse failures.
- Report outliers or unusual values and explain the detection rule.
- Warn when sample size is too small, filtered, sampled, truncated, or not representative.
- State unclear metric definitions, units, currencies, time zones, date ranges, and denominators.
- Check date parsing, time granularity, partial periods, and mixed time zones before trend claims.
- Check categorical unique values, inconsistent spelling, unexpected categories, and high-cardinality fields.
- Check numeric ranges, negative values, zeros, impossible values, and unit mismatches.
- Do not hide low-quality data or anomalies to make a smoother story.
- Do not over-infer causal explanations from correlation.
- Treat personal, financial, medical, legal, employment, education, and regulated data with high caution; minimize exposure and require human review for high-impact decisions.

## Statistics Rules

- Default to descriptive statistics before advanced analysis.
- Compute counts, totals, means, medians, min/max, quantiles, standard deviation, proportions, and rankings when appropriate.
- Use grouped aggregation for category, region, product, channel, cohort, owner, department, or time-period comparisons.
- Normalize time series to a clear time grain before comparing trends.
- For ratio metrics, name the numerator, denominator, and excluded rows.
- For growth rates, name the base period and calculation formula.
- For rankings, state the sort metric, tie handling, and filter scope.
- For year-over-year or period-over-period comparisons, state the windows being compared.
- For completion, conversion, funnel, retention, churn, margin, or utilization rates, define the denominator.
- For outliers, state the rule such as IQR, z-score threshold, percentile cutoff, business threshold, or explicit user rule.
- Use inferential statistics only when the sample, assumptions, independence, and uncertainty are explicit.

## Trend And Insight Rules

Look for:

- upward or downward trends;
- step changes and phase changes;
- peaks, troughs, seasonal patterns, and unusual volatility;
- structural shifts in mix or composition;
- head concentration and long-tail distributions;
- category, region, channel, department, product, cohort, or segment differences;
- anomalies, data gaps, and possible operational causes;
- risks, constraints, and actionable follow-ups.

Separate:

- `Data facts`: directly computed or observed values.
- `Interpretations`: plausible business explanations.
- `Recommendations`: actions supported by data and context.
- `Unknowns`: claims requiring more data or user confirmation.

Use cautious language for explanations: `可能`, `suggests`, `consistent with`, `needs confirmation`. Do not write correlation as causation.

## Chart Selection Rules

- Trends use line charts or area charts.
- Category comparison uses bar charts, column charts, or ranked lists.
- Composition uses stacked bars by default; use pie or donut charts only for simple proportions with few categories and clear totals.
- Distribution uses histograms, box plots, or a density-like binned summary.
- Relationships use scatter plots.
- Conversion paths use funnel charts.
- Stepwise contribution or variance decomposition uses waterfall charts.
- Multi-metric comparison uses radar charts only when dimensions are few and comparable; otherwise prefer scorecards or comparison matrices.
- Time events use timelines or milestone views.
- KPI overviews use KPI cards.
- Detailed records remain in tables, highlighted tables, or appendices.

Every chart must have:

- clear title;
- unit and source;
- axis labels or equivalent explanatory labels;
- visible denominator or sample size for rates;
- caption or insight sentence;
- accessible table or text summary for the same information.

Avoid:

- 3D charts;
- misleading truncated axes;
- decorative charts with no analytical purpose;
- too many colors;
- color as the only signal;
- dense labels that overlap;
- pie charts with many slices;
- charts that imply precision the data does not support.

## HTML Report Rules

If output is HTML:

- Default to one local `.html` file.
- Use inline CSS.
- Use inline vanilla JavaScript only for optional local interactions.
- Use native SVG, semantic HTML tables, CSS, and vanilla JavaScript for charts by default.
- Do not use CDN, remote fonts, remote images, iframe, analytics, React, Vue, Next.js, npm, pnpm, yarn, external APIs, local servers, MCP, Figma, Google Stitch, design platforms, GitHub Pages, Vercel, or Netlify.
- The report must open from local disk and remain readable if JavaScript is disabled.
- Interactions may include tabs, filters, expand/collapse, local sorting, copy buttons, and lightweight chart toggles.
- For large data tables, summarize, paginate, or place samples in appendices. Do not inline huge raw datasets without warning.
- Use safe DOM construction for dynamic user data; do not inject variable data through `innerHTML`.
- Use deterministic chart ordering and stable IDs. Do not use randomness or animation as the default.
- Support local opening, print, screenshots, and archiving.

If `html-report-builder` exists or is loaded in the same task, stop at the analysis/report-spec boundary and hand off final HTML packaging to it. Do not write the final `.html` artifact directly from this Skill.

## Accessibility And Print Rules

- Use semantic HTML: header, main, section, figure, figcaption, table, caption, details, summary, footer.
- Keep title hierarchy clear and scannable.
- Tables need captions or explanatory notes.
- Charts need text summaries and, when possible, adjacent tables.
- Color must not be the only information carrier.
- Use reasonable contrast for text, chart labels, and controls.
- Include print styles for HTML reports.
- Keep A4-friendly page width and avoid page-level horizontal overflow.
- Let long tables, long labels, URLs, paths, and IDs wrap or scroll inside bounded containers.
- Preserve key context for screenshots and archived copies: report title, date, source scope, caveats, and version note.

## Report Structure Templates

### Executive KPI Report

1. Title, audience, reporting period.
2. Executive summary.
3. KPI cards with status and denominator.
4. Top drivers and notable changes.
5. Risks, caveats, and recommended actions.
6. Appendix with metric definitions and source notes.

### Trend Analysis Report

1. Title and time window.
2. Data source and time-grain note.
3. Trend chart.
4. Peak/trough and phase-change findings.
5. Possible explanations separated from facts.
6. Forecast caution or follow-up data needs.

### Comparison Matrix Report

1. Title and candidates.
2. Criteria and weights or unweighted comparison basis.
3. Score or metric table.
4. Highlighted winner by criterion.
5. Trade-offs, hard requirements, and caveats.
6. Recommendation and next decision.

### Funnel / Conversion Report

1. Funnel definition and denominator.
2. Stage counts and conversion rates.
3. Funnel chart.
4. Drop-off analysis.
5. Segment differences.
6. Action recommendations and measurement gaps.

### Survey / Feedback Report

1. Survey scope, sample size, and respondent caveats.
2. Response distribution.
3. Key themes and representative counts.
4. Segment comparison.
5. Sentiment or rating summary.
6. Limitations and follow-up questions.

### Financial / Expense Summary

1. Reporting period, currency, and accounting caveats.
2. Total, average, variance, and budget/actual summary.
3. Category breakdown.
4. Trend or anomaly view.
5. Cost drivers, risks, and review items.
6. Appendix with exclusions and formula definitions.

### Project Metrics Report

1. Project scope and date window.
2. Delivery, quality, throughput, blocker, or incident KPIs.
3. Trend and workstream breakdown.
4. Risks and dependencies.
5. Recommended action plan.
6. Source notes and unresolved data issues.

### Research Data Appendix

1. Dataset and method note.
2. Field dictionary.
3. Cleaning and quality notes.
4. Descriptive statistics.
5. Supporting tables and chart specs.
6. Limitations and reproducibility notes.

## Integration With html-report-builder

When `html-report-builder` exists:

- `data-visual-report-builder` owns data understanding, data quality review, statistics, aggregations, chart selection, chart specs, data-backed insights, and report narrative.
- `html-report-builder` owns final single-file HTML packaging, visual layout, print styling, static report implementation, and HTML validation.
- Handoff by producing Markdown analysis plus `report-spec` with sources, KPIs, charts, tables, insights, limitations, and recommended structure.
- When both Skills are active, the final `fs_create_text` or `fs_append_text` for an `.html` report should follow `html-report-builder` templates, components, audit markers, and print/PDF rules.
- Do not duplicate broad HTML report packaging rules when the task only needs analysis. Use `html-report-builder` for final HTML assembly when the user asks for a polished HTML artifact.

When `html-report-builder` does not exist:

- This Skill may produce a self-contained data/report HTML file.
- Keep the artifact report-like and data-oriented.
- Do not turn it into a software UI prototype, SaaS dashboard product, or frontend app.

## Integration With artifact-management

When `artifact-management` is visible:

- Use it for artifact lifecycle, naming, saving, traceability, validation state, and handoff conventions.
- This Skill only defines what analytical content, chart specs, report narrative, and caveats should exist.
- Do not copy artifact storage policy, path ownership, or lifecycle rules into this Skill.

## Validation Checklist

- Input data was inspected.
- Fields and metric definitions are stated or marked unknown.
- Data quality issues are disclosed.
- Statistics trace to source data.
- Chart types match the data and analytical question.
- Key conclusions have data support.
- Facts, interpretations, recommendations, and unknowns are separated.
- Uncertainty and assumptions are visible.
- HTML output has no external dependency.
- HTML output can open locally.
- Tables, charts, and text agree with each other.
- No data, metric, date, source, or recommendation is fabricated.
- No undisclosed assumption is required to trust the conclusion.
- Output matches the user's audience, language, and requested format.

## Failure And Escalation

- No data: do not generate data conclusions. Produce a report framework, data request list, or analysis plan.
- Damaged data: describe corruption, parsing failure, unreadable rows, and recovery options.
- Unknown field meanings: produce schema and structural summary first; mark unknown fields before calculating business conclusions.
- Conflicting metric definitions: list conflicts and ask the user to choose, or proceed with a conservative clearly labeled assumption.
- Oversized data: sample, summarize, or aggregate first; state sample size and limits.
- Missing tools: explain what analysis cannot be verified and provide a manual/partial alternative.
- Formula or calculated-field uncertainty: state the formula, source fields, denominator, and validation method before relying on the result.
- HTML not verified: mark it as not browser-verified.
- High-impact decisions: require human review and avoid final authority claims.

## References Reviewed

Reviewed sources and absorbed patterns:

- `coffeefuelbump/csv-data-summarizer-claude-skill`: CSV profiling, automatic field/type inspection, missing data notes, adaptive chart choice. Excluded Python/pandas/matplotlib/seaborn scripts and dependencies.
- `claude-office-skills/skills/data-analysis`: spreadsheet overview, statistics, insight report, pivot/cohort ideas, quality checklist. Excluded `office-mcp` and spreadsheet automation dependencies.
- `claude-office-skills/skills/chart-designer`: chart selection guide, decision tree, chart spec format. Excluded ECharts/Chart.js default configs.
- `claude-office-skills/skills/infographic`: visual storytelling structures, statistical/timeline/process/comparison infographic thinking. Excluded design-asset and production-graphic assumptions.
- `careerhackeralex/visualize`: single-file visual report ambition, report/dashboard/infographic/timeline taxonomy, accessibility/print checklist. Excluded plugin install, CDN libraries, localStorage default, and broad UI/prototype scope.
- `f-labs-io/agent-html-skills`: data explorer, comparison matrix, timeline, research report structure, semantic HTML, no unsafe dynamic HTML, print/accessibility rules. Excluded local listener, submit server, plugin assets, remote font allowance, and clipboard/server workflow.
- `matsonj/mviz`: KPI/chart/table taxonomy, compact report-spec thinking, grid sizing and lint mindset. Excluded npm/npx CLI, external renderer, ECharts/Chart.js runtime, and iframe/embed flow.
- `benchflow-ai/skillsbench d3-visualization`: deterministic chart output, stable sorting, fixed dimensions, SVG verification, no CDN discipline. Excluded D3 as a required dependency and bundled JS scripts.
- `ComposioHQ/awesome-claude-skills`: directory-level index of data/visual/chart skills. Used only to identify relevant categories; excluded Composio app automation, API keys, MCP, SaaS integrations, and connect-app workflows.
- `anthropics/skills xlsx`: spreadsheet reading, field inspection, formula/error discipline, and xlsx quality ideas. Excluded proprietary material, scripts, LibreOffice assumptions, and spreadsheet-file deliverable requirements.
- `claude-office-skills/skills/excel-automation`: spreadsheet/pivot/chart automation concepts. Excluded xlwings, live Excel, VBA, office-mcp, and code execution patterns.
- `claude-office-skills/skills/financial-modeling`: financial metric discipline, scenario assumptions, and model caveats. Excluded 3-statement model generation as a default data-report workflow.

## Boundary

Skill owns data-analysis workflow, data quality review, statistics rules, chart selection, visualization report structure, report-spec generation, HTML data-report constraints, and limitation disclosure.

It does not own XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, artifact lifecycle, HTML packaging when `html-report-builder` is a better fit, spreadsheet file generation, BI platform configuration, external SaaS access, legal/financial/medical authority, or deployment. It must not run shell, Python, Node, npm, pnpm, yarn, curl, MCP, browser-open, local server, listener, deploy, publish, Excel, Google Sheets, Figma, Google Stitch, BI, spreadsheet recalculation, or external API commands by itself; those actions belong to XAgent tools visible in the current session and require current task context.
