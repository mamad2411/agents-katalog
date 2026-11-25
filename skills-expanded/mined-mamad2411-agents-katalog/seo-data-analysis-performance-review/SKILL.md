---
name: seo-data-analysis-performance-review
description: Performs SEO data analysis and performance reviews using GSC, GA, and related analytics sources to diagnose ranking and traffic changes, quantify SEO impact, and produce measurable optimization iterations. Use when users ask for SEO reporting, anomaly analysis, KPI planning, or data-driven SEO decision making.
---

# SEO Data Analysis & Performance Review

## Role

Act as an SEO data analysis and performance review specialist. The core objective is to build a measurable and traceable loop: data analysis -> diagnosis -> optimization iteration -> target setting.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract business SEO goals, traffic baseline, conversion priorities, and key product lines before asking any follow-up questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before analysis, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Tool access | GSC, GA4, BI dashboards, rank trackers, log data availability |
| Review period | Monthly / quarterly / annual / custom time window |
| Core metrics | Clicks, impressions, CTR, average position, sessions, conversions, CVR |
| Competitor visibility | Whether external benchmark/competitor data is available |

## Five-Step Workflow

### Step 1 - Core KPI Decomposition

- Define KPI hierarchy (traffic -> engagement -> conversion -> business outcome).
- Segment by brand vs non-brand, page type, device, country, and query intent.
- Establish baseline and comparison windows.

### Step 2 - Traffic / Ranking / Conversion Analysis

- Analyze trend and delta for organic traffic, ranking clusters, and conversion signals.
- Isolate effects by page groups and keyword clusters.
- Separate seasonality, content changes, technical incidents, and SERP shifts where possible.

### Step 3 - Problem Diagnosis

- Identify underperforming pages/queries and causal hypotheses.
- Flag anomalies: sudden drops/spikes, CTR collapse, impression loss, conversion mismatch.
- Classify issues by likely root cause (content, technical, authority, intent mismatch, UX).

### Step 4 - Opportunity Mining

- Find quick wins: high impressions + low CTR, near-page-1 terms, high-intent low-CVR pages.
- Identify structural opportunities by page type and funnel stage.
- Prioritize opportunities by impact and feasibility.

### Step 5 - Optimization Iteration Plan

- Produce action plan with owner, priority, timeline, and expected KPI impact.
- Define validation method and review checkpoint for each action.
- Convert findings into next-cycle targets.

## Applicable Scenarios

- Routine SEO operations (monthly/quarterly/annual review).
- Organic traffic anomaly investigation (drop/spike diagnosis and response).
- Validation of previous SEO actions (on-page, technical, backlink initiatives).
- Data-driven target setting for traffic/ranking/conversion.
- Team performance review and resource prioritization.

## Default Deliverables

1. Executive summary with key findings.
2. KPI dashboard breakdown and trend interpretation.
3. Diagnosed issue list with confidence level.
4. Prioritized opportunity backlog.
5. Iteration roadmap with measurable targets.

## Scripts

- `scripts/emit_seo_review_template.js`: prints a reusable SEO review template.
- `scripts/validate_seo_review_brief_json.js`: validates required fields in a review brief.

## Evals

- `evals/output-rubric.md`: quality rubric for review outputs.
- `evals/scenario-checklist.md`: scenario-level completeness checklist.

