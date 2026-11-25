---
name: productize-validate-data
description: >-
  QA an analysis before sharing, including methodology, accuracy, calculation, visualization,
  and bias checks. Use when reviewing analysis for stakeholders, spot-checking SQL results,
  validating aggregation logic, or assessing whether conclusions are supported by the data.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Validate Data

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

- **Skill**: `validate-data`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Data validation report with quality issues, methodology checks, and confidence level

Review an analysis for accuracy, methodology, and potential bias before it is shared with stakeholders.

## Argument Hint

`<analysis to review>`

## Usage

```text
/validate-data <analysis to review>
```

The analysis can be a document, report, file, SQL query and results, chart, dataset, notebook, spreadsheet, or methodology summary.

## Workflow

### 1. Review Methodology and Assumptions

Check:
- Question framing: whether the analysis answers the right question.
- Data selection: source tables, files, date ranges, and inclusion criteria.
- Population definition: who or what is included and excluded.
- Metric definitions: whether definitions are explicit and stakeholder-compatible.
- Baseline and comparison: whether comparison periods, cohorts, and contexts are fair.
- Assumptions: whether assumptions are stated and defensible.

### 2. Run Pre-Delivery QA

Review data quality:
- Sources are correct.
- Data freshness and "as of" date are stated.
- Time series and segments are complete.
- Null handling is appropriate.
- Deduplication and filters are correct.

Review calculations:
- Aggregation grain matches the analysis question.
- Denominators are correct and non-zero.
- Date comparisons use equal and complete periods unless caveated.
- Join types are intentional.
- Many-to-many joins are not inflating counts.
- Metrics match stakeholder definitions.
- Subtotals reconcile with totals where expected.

Review reasonableness:
- Numbers are plausible.
- Percentages are between 0 and 100 when applicable.
- Trends do not have unexplained jumps.
- Results reconcile with dashboards, finance reports, or prior analyses when possible.
- Boundary cases are sensible.

Review presentation:
- Charts use honest axes and consistent scales.
- Titles, labels, date ranges, and units are clear.
- Number formatting is appropriate.
- Caveats are explicit.
- The analysis is reproducible.

### 3. Check Analytical Pitfalls

Look specifically for:
- Join explosion from many-to-many joins.
- Survivorship bias.
- Partial-period comparisons.
- Denominator shifting.
- Average of averages.
- Timezone mismatches.
- Selection bias in segmentation.
- Simpson's paradox.
- Correlation presented as causation.
- Small sample overclaiming.
- Outlier-distorted averages.
- Multiple testing and cherry-picking.
- Look-ahead bias.
- Cherry-picked time ranges.

### 4. Verify Calculations

Where possible:
- Recalculate key numbers independently.
- Check row counts before and after joins.
- Confirm subtotals and percentages.
- Verify YoY, MoM, and WoW base periods.
- Check that filters are applied consistently.
- Spot-check individual records or small slices.
- Calculate the same metric two ways when feasible.

For SQL, inspect grain, joins, filters, grouping, denominator logic, and null handling. Use `sql-queries` for dialect-specific review when needed.

### 5. Assess Visualizations

If charts are included, verify:
- Bar charts start at zero.
- Scales are consistent across comparison panels.
- Titles accurately describe what is shown.
- Axes, units, date ranges, and sources are visible.
- Visual encodings do not mislead fast readers.
- No 3D effects, unexplained truncation, or inconsistent intervals.

Use `data-visualization` if chart-design guidance is needed.

### 6. Evaluate Narrative and Conclusions

Review whether:
- Conclusions are directly supported by the data.
- Alternative explanations are acknowledged.
- Uncertainty is communicated.
- Recommendations follow from findings.
- Confidence level matches evidence strength.
- Practical significance is separated from statistical significance.

Use `statistical-analysis` for significance, outlier, anomaly, correlation, or sample-size concerns.

### 7. Produce Confidence Assessment

Choose one:
- **Ready to share**: sound methodology, verified calculations, caveats noted.
- **Share with noted caveats**: largely correct, but limitations must be communicated.
- **Needs revision**: errors, methodological issues, or missing analyses should be fixed first.

## Output Format

```markdown
## Validation Report

### Overall Assessment: [Ready to share | Share with caveats | Needs revision]

### Methodology Review
[Findings about approach, data selection, definitions, comparison logic, and assumptions]

### Issues Found
1. [Severity: High/Medium/Low] [Issue description, evidence, and impact]

### Calculation Spot-Checks
- [Metric]: [Verified / Discrepancy found / Could not verify] - [notes]

### Visualization Review
[Chart issues or confirmation that visuals are sound]

### Suggested Improvements
1. [Improvement and why it matters]

### Required Caveats for Stakeholders
- [Caveat that must be communicated]
```

## Pitfall Reference

### Join Explosion

Many-to-many joins silently multiply rows and inflate counts or sums. Check row counts before and after joins, investigate unexpected increases, and use `COUNT(DISTINCT entity_id)` when counting entities through joins.

### Survivorship Bias

Analyzing only current or surviving entities ignores churned, deleted, failed, or excluded entities. Ask who is missing from the dataset.

### Incomplete Period Comparison

Do not compare a partial week, month, or quarter to a full prior period unless explicitly caveated. Use complete periods or same-number-of-days comparisons.

### Denominator Shifting

Rate changes are not comparable if the eligible population or active-user definition changed between periods.

### Average of Averages

Never average pre-computed averages when group sizes differ. Recompute from raw numerators and denominators or use weighted averages.

### Timezone Mismatches

Standardize timestamps before comparison and document the timezone used.

### Selection Bias

Do not define segments using the outcome being measured. Prefer pre-treatment characteristics.

## Red Flags

Investigate:
- Metrics changing more than 50 percent without an obvious cause.
- Exact round-number counts or sums.
- Rates exactly 0 percent or 100 percent.
- Results that perfectly confirm the hypothesis.
- Identical values across periods or segments.
- Percentages that should sum to 100 percent but do not.

## Reproducibility Standard

For non-trivial analyses, ensure the report includes:
- Specific question.
- Data sources and "as of" dates.
- Metric and segment definitions.
- Time period and timezone.
- Methodology.
- Assumptions and limitations.
- Queries or code.
- Caveats and known gaps.
