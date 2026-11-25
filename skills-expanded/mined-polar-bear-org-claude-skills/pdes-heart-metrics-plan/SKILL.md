---
name: pdes-heart-metrics-plan
description: Builds a HEART Metrics Plan with the two or three dimensions that matter, a goal, signal and metric for each, today's baseline or "baseline needed", the data owner, instrumentation asks and guardrails. Use for "run pdes-heart-metrics-plan", "HEART framework", "goals signals metrics", "what does design success look like", "UX metrics for this feature", "how do we measure this redesign", "agree success metrics with my PM", "design success metrics", part of the Claude for Product Designers Pack by 90n.
---

# HEART Metrics Plan

## When To Use
The project starts and nobody agreed what design success will look like, so later you have screens and no outcome. Run it early, before the first release, while tracking can still be added. It answers: which user outcomes is this work meant to move, what behaviour would show it, how is that counted, and where does each number come from today?

## When Not To Use
If the work already shipped and you need to say what it changed, run Design Impact Write-Up: this plan is written before release and holds no results. If the product tracks nothing and nobody will add tracking, skip the table and agree one instrumentation ask plus a check with real users instead.

## Inputs
- The problem and the outcome sought, in two lines or as a framing brief you already have
- What the product tracks today: event names, dashboards, survey or support data, with periods. Optional: a connector to Amplitude or Mixpanel, to read event names and baselines
- Who owns each data source and who would build new tracking, by role
If you have none of this, I start from the problem statement alone, mark every baseline `[baseline needed]` and mark the output as a first draft.

## Approach
HEART, from Rodden, Hutchinson and Fu (CHI 2010): five user-centred dimensions, Happiness, Engagement, Adoption, Retention and Task success, with a process that maps Goals to Signals to Metrics. The judgment is in the order. Start from the goal, or you will adopt whatever the dashboard already counts. The failure it prevents: a redesign judged on page views because page views were the only number to hand, while the task it was meant to fix got slower and nobody was watching.

## Workflow
1. Ask three questions: what should change for users when this ships, what does the product already track (paste it), and who agrees the plan with you on the product and data side, by role?
2. Pick two or three of the five dimensions for this piece of work, and say which were dropped and why. All five by default means nothing gets watched properly.
3. Per chosen dimension, in fixed order: the Goal (what users should be able to do or feel), then the Signal (one behaviour or attitude that shows success, and one that shows failure), then the Metric (a rate or average with its period). A metric with no signal behind it comes out.
4. Baseline per metric: today's value from your data with source and date range, or `[baseline needed]`. I never estimate one. A connector read is quoted with its query and period.
5. Per metric, name the data owner by role, whether it is tracked today, and if not, the instrumentation ask and who would build it. Engineering owns that build; your part is asking in time.
6. Add guardrails: the metrics that must not get worse, such as time on the old path or support contacts, each with an owner.
7. Write the watch agreement: what you and the product manager look at together, how often, and the minimum sample or period before a change is read. You set that threshold; I only record it.

## Output Format
```markdown
# HEART Metrics Plan
**Work:** [feature or flow] | **Designer:** [role] | **Product manager:** [role] | **Data owner:** [role] | **Date:** [date]
**Dimensions chosen:** [dimension, why] | **Dropped:** [dimension, why]
## Goals, signals, metrics
| Dimension | Goal | Success signal | Failure signal | Metric and period | Baseline (source, dates) |
|---|---|---|---|---|---|
| [dimension] | [user outcome] | [behaviour or attitude] | [behaviour or attitude] | [rate or average, period] | [value, source, dates] or [baseline needed] |
## Data and instrumentation
| Metric | Data owner | Tracked today | Instrumentation ask | Builder |
|---|---|---|---|---|
| [metric] | [role] | [yes / no] | [event or property needed] | [role] |
## Guardrails
| Must not get worse | Today (source, dates) | Owner |
|---|---|---|
| [metric] | [value] or [baseline needed] | [role] |
## Watch agreement
Reviewed together: [metrics], every [interval]. Minimum before reading a change: [sample or period, set by you].
## Decision
[Product manager] and [designer] agree the plan, and [data owner] confirms the baselines and accepts or declines each instrumentation ask, by [date], before the first release.
```

## Done When
- Every metric traces back to a signal and a goal, and every chosen dimension has at least one metric
- Every baseline is a sourced value or `[baseline needed]`, and the dropped dimensions are named with a reason
- Every untracked metric has an instrumentation ask and a builder by role, and the minimum sample or period came from you

## Quality Bar
- Goals are user outcomes, never features shipped or screens delivered
- Metrics describe product use in aggregate, never one person's activity, and nothing measures a designer
- The plan holds no results; numbers will show what people did, not why, so pair it with sessions with real users
- No baseline or target is estimated; the product manager and you agree the plan, and the numbers come from real data.

## Next
Run pdes-design-principles (Design Principles) to write what this product chooses before options are compared.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
