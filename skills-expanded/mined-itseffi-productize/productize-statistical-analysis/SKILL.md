---
name: productize-statistical-analysis
description: >-
  Apply statistical methods including descriptive stats, trend analysis, outlier detection,
  and hypothesis testing. Use when analyzing distributions, testing significance, detecting
  anomalies, computing correlations, or interpreting statistical results.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Statistical Analysis

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

- **Skill**: `statistical-analysis`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Statistical Analysis analytics diagnosis with metric readout, caveats, decision, and next instrumented step

Helper skill for descriptive statistics, trends, outliers, hypothesis testing, and caution around statistical claims.

## Invocation

This is primarily a support skill for `analyze`, `explore-data`, `metrics-review`, `create-viz`, and `build-dashboard`. Use it explicitly when statistical method selection or interpretation matters.

## Descriptive Statistics

Choose the right center:

| Situation | Use | Why |
|---|---|---|
| Symmetric distribution, no outliers | Mean | Efficient estimator |
| Skewed distribution | Median | Robust to outliers |
| Categorical or ordinal data | Mode | Only option for non-numeric |
| Highly skewed business metric | Median + mean | The gap shows skew |

Always report mean and median together for business metrics. If they diverge meaningfully, the mean alone is misleading.

Measure spread:
- Standard deviation: use with roughly normal data.
- IQR: robust to outliers; use with skewed data.
- Coefficient of variation: standard deviation divided by mean; useful across different scales.
- Range: quick extent, but highly outlier-sensitive.

Use percentiles for business context:
- p1: floor or bottom 1 percent.
- p5: low end of normal.
- p25: first quartile.
- p50: median.
- p75: third quartile.
- p90: power-user threshold.
- p95: high end of normal.
- p99: extreme users or values.

Characterize every numeric distribution by shape, center, spread, outliers, and natural bounds.

## Trend Analysis

Use moving averages to smooth noise:

```python
df["ma_7d"] = df["metric"].rolling(window=7, min_periods=1).mean()
df["ma_28d"] = df["metric"].rolling(window=28, min_periods=1).mean()
```

Use period comparisons deliberately:
- Week over week: same day last week.
- Month over month: prior month.
- Year over year: best for seasonal businesses.
- Same-day-last-year: useful for calendar-day effects.

Growth rates:

```text
Simple growth = (current - previous) / previous
CAGR = (ending / beginning) ^ (1 / years) - 1
Log growth = ln(current / previous)
```

Check seasonality before declaring a trend:
1. Plot raw time series.
2. Compare day-of-week averages.
3. Compare month-of-year averages.
4. Prefer YoY or same-period comparisons when seasonality is present.

For lightweight forecasts, use naive, seasonal naive, linear trend, or moving-average forecasts. Always communicate a range, not false precision.

Escalate to a data scientist when the trend is non-linear, has multiple seasonalities, depends on external drivers, or forecast accuracy drives resource allocation.

## Outliers and Anomalies

Use the right method:

```python
# Z-score: use for approximately normal data
z_scores = (df["value"] - df["value"].mean()) / df["value"].std()
outliers = df[abs(z_scores) > 3]

# IQR: robust for skewed data
q1 = df["value"].quantile(0.25)
q3 = df["value"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
outliers = df[(df["value"] < lower) | (df["value"] > upper)]

# Percentile: simple boundary method
outliers = df[
    (df["value"] < df["value"].quantile(0.01)) |
    (df["value"] > df["value"].quantile(0.99))
]
```

Do not automatically remove outliers:
1. Investigate whether they are errors, real extremes, or another population.
2. Fix or remove true data errors.
3. Keep genuine extremes but use robust statistics when appropriate.
4. Segment different populations rather than averaging them together.

For time series anomalies:
1. Compute expected value using moving average or same-period history.
2. Compute deviation from expected.
3. Flag deviations beyond 2-3 standard deviations of residuals.
4. Distinguish point anomalies from sustained change points.

Always report how outliers were handled.

## Hypothesis Testing

Use hypothesis testing when deciding whether an observed difference could be due to chance:
- A/B test results.
- Before/after comparisons.
- Segment comparisons.

Framework:
1. Define null hypothesis: no difference.
2. Define alternative hypothesis: there is a difference.
3. Choose alpha, usually 0.05.
4. Compute test statistic and p-value.
5. If p < alpha, reject the null.

Common tests:

| Scenario | Test | Use when |
|---|---|---|
| Two group means | Independent t-test | Normal data, two groups |
| Two proportions | Z-test for proportions | Conversion or binary outcomes |
| Paired measurements | Paired t-test | Before/after on same entities |
| Three or more means | ANOVA | Multiple segments or variants |
| Non-normal two groups | Mann-Whitney U | Skewed or ordinal data |
| Categorical association | Chi-squared | Two categorical variables |

Always separate statistical significance from practical significance. Report:
- Effect size.
- Confidence interval.
- Business impact.
- Sample size and power caveats.

Rule of thumb: for proportions, require at least 30 events per group for basic reliability. Small samples need explicit caution.

## Statistical Cautions

### Correlation Is Not Causation

When reporting correlation, consider reverse causation, confounders, and coincidence.

Say: "Users who use feature X have 30 percent higher retention."

Do not say without stronger evidence: "Feature X causes 30 percent higher retention."

### Multiple Comparisons

If many metrics or segments were tested, some significant results will appear by chance. Note how many tests were run and consider Bonferroni correction or other multiple-testing controls.

### Simpson's Paradox

Aggregated trends can reverse after segmentation. Check whether the conclusion holds across key segments before acting.

### Survivorship Bias

Ask who is missing from the dataset. Active-user-only analyses exclude churned users and can overstate product health.

### Ecological Fallacy

Do not apply aggregate group trends to individuals without individual-level evidence.

### False Precision

Round to match uncertainty. Prefer "about 5 percent" or "4-6 percent" over "4.73 percent" when the latter implies unjustified certainty.

## Output Rules

- State the method used and why.
- State assumptions and sample limitations.
- Prefer ranges and confidence intervals over point estimates when uncertainty matters.
- Explain results in business language without overstating causality.
