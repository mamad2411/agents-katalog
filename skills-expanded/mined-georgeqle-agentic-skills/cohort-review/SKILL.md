---
name: cohort-review
description: Post-launch metrics & funnel analysis — cohort retention, channel performance, and progress against targets from $metrics
type: analysis
version: v0.3
argument-hint: "[file path to data, pasted data, or empty to be prompted]"
interview_depth: none
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Cohort Review — Post-Launch Metrics & Funnel Analysis

Invoke as `$cohort-review`.

Takes real usage/revenue data and analyzes against targets from `$metrics`. Performs cohort analysis, funnel analysis, and channel performance review. Identifies where the funnel leaks, which cohorts retain, and whether activation targets are being hit. Append-style output for tracking performance over time.

## Prerequisites

- **Hard**: `research/metrics.md` (or `research/{slug}/metrics.md`) must exist. If not, tell the user to run `$metrics` first and stop.
- **Soft**: Read these if they exist for richer analysis:
  - `research/icp.md` — segment analysis against ICP profiles
  - `research/gtm.md` — channel strategy to compare against actual channel performance
  - `research/monetization.md` — revenue targets and unit economics to validate
  - `research/assumption-tracker.md` — assumptions to validate or invalidate with real data

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Context & Data

**Load research context:**
- Read `research/metrics.md` — extract all metric definitions, targets, and North Star metric
- Read other research docs as listed in prerequisites

**Ingest performance data:**
Check `$ARGUMENTS`:
- **File path provided**: Read the file (CSV, JSON, markdown table, or any structured format)
- **Text provided**: Parse the data directly
- **Empty**: Ask the user to provide data — accept any format: analytics exports, dashboard screenshots described in text, spreadsheet pastes, database query results. If the session is already in Plan mode and there are 2-3 concrete input-source choices, prefer `request_user_input`.

Clarify with the user. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- What date range does this data cover?
- What's the data source? (analytics tool, database, manual tracking)
- Any known data quality issues?

### 2. Funnel Analysis

Map the data against the funnel stages defined in `research/metrics.md`:

1. **Top of funnel** — visitors, signups, leads (from Growth metrics)
2. **Activation** — users who reach aha moment (from Activation metrics)
3. **Engagement** — active usage patterns (from Engagement metrics)
4. **Retention** — users still active at D7/D30/D90 (from Retention metrics)
5. **Revenue** — paying users, ARPU, expansion (from Business metrics)

For each stage:
- **Actual vs. Target**: Compare real numbers against targets from metrics.md
- **Conversion rate**: What % moves to the next stage?
- **Drop-off analysis**: Where exactly do users fall off? What's the biggest leak?
- **Trend**: Is it improving, declining, or flat compared to previous cohort reviews?

### 3. Cohort Analysis

If the data supports cohort segmentation:

- **Time-based cohorts**: Group users by signup week/month. Compare retention curves across cohorts — are newer cohorts retaining better or worse?
- **Source-based cohorts**: If channel data is available, compare retention by acquisition channel
- **Segment-based cohorts**: If ICP segment data is available, compare performance across ICP segments
- **Behavioral cohorts**: Group by activation behavior — users who did X vs. didn't

Identify:
- Which cohorts are strongest/weakest?
- Is there a trend in cohort quality over time?
- Are certain channels or segments significantly better?

### 4. Channel Performance Review

If channel/attribution data is available:

| Channel | Volume | CAC | Activation Rate | D30 Retention | LTV (est.) | ROI |
|---------|--------|-----|-----------------|---------------|------------|-----|
| [channel] | [count] | [$] | [%] | [%] | [$] | [ratio] |

Compare against:
- GTM channel strategy recommendations (from `research/gtm.md`)
- Budget allocation — is spend aligned with performance?
- Channel-specific benchmarks from research

Flag:
- Channels performing above/below expectations
- Channels with high volume but poor retention (leaky bucket)
- Channels with low volume but high quality (scale opportunity)

### 5. Key Findings & Present

Synthesize findings into:

1. **Health summary** — overall: on track, at risk, or off track against metrics targets
2. **Top 3 wins** — what's working better than expected
3. **Top 3 concerns** — what's underperforming, where the funnel leaks
4. **Biggest lever** — the single change that would most improve metrics
5. **Assumption updates** — which assumptions from `$assumption-tracker` are validated or invalidated by this data

**Present to the user.** If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Here's what the data shows. Which conclusions need adjustment based on data quality limits, missing fields, or known operational context?"
- "Any data quality issues that would change these conclusions?"

Incorporate feedback before proceeding.

### 6. Populate Next Steps

Include 3–5 applicable items with "Pick one:" framing:

- IF activation below target: `$experiment` — Design an experiment to improve the activation funnel
- IF channel performing poorly: `$gtm` — Revisit channel strategy with real performance data
- IF pricing/revenue below target: `$monetization` — Update monetization strategy with real unit economics
- IF assumptions invalidated: `$assumption-tracker` — Update register with real-data validations
- IF metrics targets need adjustment: `$metrics` — Revisit targets based on baseline reality
- IF overall on track: `$research-roadmap` — Check what's next in the project lifecycle

### 7. Write Output

Present final analysis to user. Ask:
- "Ready to write this analysis? Anything to adjust?"

Only after confirmation, write the output file.

## Output

### `research/cohort-review-[YYYY-MM-DD].md` (or `research/{slug}/cohort-review-[YYYY-MM-DD].md`)

```markdown
# Cohort Review: [Date Range]

> Date: [current date]
> Data source: [analytics tool / database / manual]
> Period: [start date] — [end date]
> Based on: research/metrics.md

## Health Summary

**Overall**: [On Track / At Risk / Off Track]
[2-3 sentences: the headline — are we hitting our numbers? What's the biggest story?]

### North Star Metric
**Target**: [from metrics.md]
**Actual**: [real number]
**Status**: [On Track / Below / Above] — [trend: improving / declining / flat]

## Funnel Analysis

| Stage | Metric | Target | Actual | Delta | Trend |
|-------|--------|--------|--------|-------|-------|
| Acquisition | [metric] | [target] | [actual] | [+/-] | [↑↓→] |
| Activation | [metric] | [target] | [actual] | [+/-] | [↑↓→] |
| Engagement | [metric] | [target] | [actual] | [+/-] | [↑↓→] |
| Retention | [metric] | [target] | [actual] | [+/-] | [↑↓→] |
| Revenue | [metric] | [target] | [actual] | [+/-] | [↑↓→] |

### Biggest Leak
**Stage**: [where the biggest drop-off occurs]
**Conversion**: [actual %] vs. target [target %]
**Analysis**: [why this is happening — evidence from data]
**Recommendation**: [what to do about it]

## Cohort Analysis

### Retention Curves
| Cohort | D1 | D7 | D14 | D30 | D60 | D90 |
|--------|----|----|-----|-----|-----|-----|
| [cohort] | [%] | [%] | [%] | [%] | [%] | [%] |

### Cohort Quality Trend
[Are newer cohorts better or worse? What's driving the trend?]

### Segment Performance
| Segment | Activation | D30 Retention | Revenue/User | Notes |
|---------|------------|---------------|-------------|-------|
| [segment] | [%] | [%] | [$] | [observation] |

## Channel Performance

| Channel | Volume | CAC | Activation | D30 Retention | Est. LTV | ROI |
|---------|--------|-----|-----------|---------------|----------|-----|
| [channel] | [n] | [$] | [%] | [%] | [$] | [x] |

### Channel Insights
- **Best performer**: [channel] — [why]
- **Worst performer**: [channel] — [why]
- **Scale opportunity**: [channel] — [evidence]
- **Cut/reduce**: [channel] — [evidence]

## Key Findings

### Wins
1. [What's working — with data]
2. [What's working — with data]
3. [What's working — with data]

### Concerns
1. [What's underperforming — with data and impact]
2. [What's underperforming — with data and impact]
3. [What's underperforming — with data and impact]

### Biggest Lever
[The single change that would most improve overall metrics — with reasoning]

## Assumption Validations

| Assumption | Previous Status | New Status | Evidence |
|-----------|----------------|------------|----------|
| [assumption from tracker] | [old status] | Validated/Invalidated | [data point] |

## Next Steps

Pick one:
- [conditional items from step 6 — only include items whose conditions are met]
```

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Data-driven.** Every claim must reference specific numbers from the provided data. Do not fabricate data or fill in placeholders.
- **Compare to targets.** Always reference metric targets from `research/metrics.md`. The value of this skill is target vs. actual, not just reporting numbers.
- **Handle incomplete data gracefully.** If data doesn't cover all funnel stages or cohort dimensions, analyze what's available and note gaps. Don't skip the analysis.
- **Append-style.** Each cohort review is a separate dated file. Previous reviews are not modified.
- **Present before writing.** Never write output files until the analysis has been presented and validated.
- **Be honest about data quality.** If the data is too sparse for statistical significance, say so. Don't over-interpret small samples.
- **Recommend actions.** Every finding should connect to a concrete next step.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/cohort-review-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
