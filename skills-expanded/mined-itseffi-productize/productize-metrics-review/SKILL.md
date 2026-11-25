---
name: productize-metrics-review
description: >-
  Review and analyze product metrics with trend analysis and actionable insights. Use when
  running a weekly, monthly, or quarterly metrics review, investigating a spike or drop,
  comparing against targets, or turning raw numbers into a scorecard with recommended actions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Metrics Review

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

- **Skill**: `metrics-review`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Metric scorecard, trend diagnosis, and recommended action plan

Review product metrics, identify trends, and surface action-oriented insights.

## Argument Hint

`<time period or metric focus>`

## Usage

```text
/metrics-review $ARGUMENTS
```

## Workflow

### 1. Gather Data

If product analytics, warehouse, spreadsheet, or dashboard tools are connected, use them to pull the relevant time period, comparison period, targets, and segment breakdowns.

If no data tool is connected, ask for the minimum needed input:
- Time period: weekly, monthly, quarterly, or custom range.
- Metric focus: full product suite or specific metric.
- Current values, prior values, and targets.
- Known context: launches, incidents, campaigns, seasonality, tracking changes.

### 2. Organize Metrics

Use a hierarchy:
- North Star metric: the clearest proxy for delivered user value.
- L1 health indicators: acquisition, activation, engagement, retention, monetization, satisfaction.
- L2 diagnostics: funnel steps, feature usage, segments, performance, errors, support volume.

If the user has no hierarchy, propose one before analyzing.

### 3. Analyze Trends

For each key metric, determine:
- Current value and previous period value.
- Change, rate of change, and whether the movement is meaningful.
- Target status: on track, at risk, or miss.
- Anomalies, spikes, drops, or discontinuities.
- Segment drivers and leading indicators.

Be careful about attribution. Distinguish correlation, plausible explanation, and proven cause.

### 4. Generate Review

Return:
- **Summary**: 2-3 sentences on overall product health and the most important callout.
- **Metric Scorecard**: table with Metric, Current, Previous, Change, Target, Status.
- **Trend Analysis**: what changed, likely why, and whether it is one-time or sustained.
- **Bright Spots**: metrics beating targets or improving.
- **Areas of Concern**: misses, deteriorating trends, early warnings, or visibility gaps.
- **Recommended Actions**: investigations, experiments, investments, alerts, or dashboard changes.
- **Context and Caveats**: data quality issues, comparability notes, missing metrics.

### 5. Follow Up

Offer useful next artifacts:
- Deep dive on one metric.
- Dashboard spec for ongoing monitoring.
- Experiment proposals for problem areas.
- Recurring metrics review template.

## Metrics Guidance

North Star metrics should be value-aligned, leading, actionable, and understandable.

Common L1 metrics:
- Acquisition: signups, visitor conversion, channel mix, acquisition cost.
- Activation: activation rate, time to activate, onboarding completion, first value moment.
- Engagement: DAU, WAU, MAU, stickiness, core action frequency, feature adoption.
- Retention: D1, D7, D30, D90, churn, cohort retention curves, resurrection.
- Monetization: conversion, MRR, ARR, ARPU, expansion revenue, net revenue retention.
- Satisfaction: NPS, CSAT, support volume, resolution time, review sentiment.

## Output Rules

- Lead with the so-what.
- Always show comparison context, not raw numbers alone.
- Segment aggregates when possible.
- Do not over-explain noise.
- Every missed target should have a recommended next action.
