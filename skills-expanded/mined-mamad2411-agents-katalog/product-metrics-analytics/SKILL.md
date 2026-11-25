---
name: product-metrics-analytics
description: When the agent needs product metrics, a north star metric, KPI trees, activation and retention definitions, or funnel analysis for product decisions — a metric system that explains the business, not a vanity dashboard.
department: Product
source: helm
---

# Product Metrics & Analytics

You build metric systems like the growth teams at Amplitude-native companies: one north star that proxies delivered value, a small input tree everyone can move, and definitions so precise nobody argues about the numbers — only about what to do.

## Operating principles

1. **North star = value delivered, not value extracted.** Revenue is an output; the north star is the usage moment that CAUSES revenue ("weekly active workspaces running ≥ 1 automation", Slack's "messages sent in teams of 3+"). Test: if the metric doubled but customers got nothing more, it's the wrong metric.
2. **Inputs over outputs.** Decompose the north star into 3–5 INPUT metrics teams can actually move (new activated accounts × activation rate × frequency × retention). Output metrics are for judging quarters; input metrics are for running weeks.
3. **Definitions are contracts.** Every metric gets: exact event(s), filters, unit of analysis (user vs account — pick account for B2B), time window, and owner. "Active" without a definition is a fight scheduled for later.
4. **Ratios and cohorts, not totals.** Cumulative charts and all-time totals only go up — they're PR, not analysis. Retention reads by weekly/monthly signup cohort; conversion reads as rate per cohort; growth reads as net (new + resurrected − churned).

## The framework (adapted AARRR)

- **Acquisition**: signups by channel (with cost where paid).
- **Activation**: the "aha" — defined as the earliest action pattern that PREDICTS retention (find it: compare week-4 retention of users who did X in week 1 vs not; pick the X with the biggest lift and a plausible causal story). Target: % of signups reaching it in ≤ N days.
- **Retention**: cohort curves for the natural frequency (daily tool → weekly cohorts; monthly job → monthly). The curve must FLATTEN — a curve to zero means no product-market fit for that segment, and no acquisition spend fixes it.
- **Revenue**: conversion to paid, ARPA, net revenue retention (NRR > 100% means the base compounds).
- **Referral**: % of new accounts from invites/word-of-mouth.

## Workflow

1. State the business model in one sentence; derive the north star candidate; run the "doubled but no value?" test.
2. Build the input tree with current values (or instrument to get them). Mark each input: who owns it, current, target.
3. Write the definitions table (event names from the actual tracking plan; flag missing instrumentation as work items).
4. Establish baselines + honest benchmarks for the model (e.g. B2B SaaS: activation 25–40%, m12 logo retention ~85–95% enterprise / 60–75% SMB, NRR 100–120% — state assumptions).
5. Set the weekly review ritual: the tree with deltas, one anomaly investigated to root cause, one experiment decision. Kill any dashboard chart nobody acted on in a month.

## Output contract

Deliver: north star + rationale + the failed alternatives · input tree with owners/targets · definitions table (event-level) · cohort retention read + flattening verdict · instrumentation gap list · the weekly review template.

## Quality bar

- Every metric: defined, owned, and attached to a decision it informs.
- No cumulative vanity charts; no metric without a unit of analysis.
- The activation definition is EVIDENCED (predicts retention), not aspirational.
