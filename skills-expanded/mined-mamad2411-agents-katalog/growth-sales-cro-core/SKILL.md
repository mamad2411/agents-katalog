---
name: growth-sales-cro-core
description: "Shared reference for the growth-sales-cro cluster: the conversion funnel, the baseline → hypothesis → test → decide measurement loop, the metric-per-stage matrix, and the rule that you optimize on evidence not opinion. USE WHEN proposing a conversion/pricing/retention change, designing an A/B test, or planning a growth experiment — the interlocking discipline every spoke shares."
cluster: growth-sales-cro
version: 1.0.0
---

# Growth-Sales-CRO Core

Shared model for the `growth-sales-cro` cluster. Every CRO, growth, monetization, retention,
and sales spoke depends on the same two things: **a funnel you can see** and **a loop that
proves a change worked**. Keep them consistent here so no spoke optimizes on vibes or
double-counts a win.

## 1. The one decision this domain turns on

> **Optimize on evidence, not opinion.** Before any change earns the word "win", it must be
> tied to a single metric, framed as a hypothesis, and validated against a measured baseline —
> ideally by a controlled test.

Everything below exists to make that decision honest. The failure mode of growth/CRO work is
shipping opinion-driven changes, declaring victory from noise, and stacking unmeasured tweaks
until nobody can attribute the result. The cluster's job is to prevent that.

## 2. The funnel (the map every spoke lives on)

Pirate-metrics order, plus the parallel human-assisted path:

```
ACQUIRE ─→ CONVERT ─→ ACTIVATE ─→ MONETIZE ─→ RETAIN ─→ EXPAND
   │          │           │           │          │         │
 paid-ads   page-cro   onboarding   pricing    churn-    referral-
            form-cro    -cro        -strategy  prevention program
            popup-cro              paywall-
            signup-flow-cro        upgrade-cro

          ── parallel SELL path (human-assisted) ──
   revops → sales → sales-enablement → pitchdeck-skill → lead-research-assistant

          ── cross-cutting EVIDENCE (feeds every stage) ──
   analytics-tracking · ab-test-setup · customer-research · company-research
   competitor-alternatives · competitor-teardown
```

**Rule:** locate every task at exactly one **stage** and one **lever**. "Grow revenue" is not a
task; "lift trial→paid on the paywall" is. Vague asks get decomposed into stage-specific,
single-metric tasks before any spoke runs.

## 3. The measurement loop (how a change becomes a "win")

Self-serve or sales, the loop is the same:

```
BASELINE ─→ HYPOTHESIS ─→ TEST ─→ DECIDE ─→ (ship or kill) ─→ re-baseline
```

- **Baseline** — instrument the metric *before* changing anything. No instrumentation → start at `analytics-tracking`; you cannot improve what you can't see. → `analytics-tracking`
- **Hypothesis** — "Changing X will move *metric M* by ~N because *reason grounded in evidence*." One change, one primary metric. Evidence comes from `customer-research` or competitor findings, not taste.
- **Test** — a controlled comparison where stakes justify it. Respect **statistical significance** and a **minimum runtime / sample size**; don't peek-and-stop. → `ab-test-setup`
- **Decide** — ship, kill, or iterate based on the result and its guardrail metrics (did the win cannibalize another stage?). Then re-baseline; the funnel moved.

## 4. Metric-per-stage matrix

| Stage | Primary metric | Lead spokes | Evidence input |
|---|---|---|---|
| Acquire | CPA / ROAS, qualified traffic | `paid-ads` | `competitor-*`, `analytics-tracking` |
| Convert | conversion rate (visit→action) | `page-cro`, `form-cro`, `popup-cro`, `signup-flow-cro` | `customer-research`, `ab-test-setup` |
| Activate | activation rate, time-to-value | `onboarding-cro` | `customer-research`, `analytics-tracking` |
| Monetize | trial→paid, ARPU, win rate | `paywall-upgrade-cro`, `pricing-strategy`, `sales`, `sales-enablement` | `pricing-strategy`, `customer-research` |
| Retain | churn rate, recovered revenue | `churn-prevention` | `customer-research`, `analytics-tracking` |
| Expand | referral / viral coefficient, NRR | `referral-program` | `analytics-tracking` |
| Sell (parallel) | pipeline, MQL→SQL, close rate | `revops`, `sales`, `sales-enablement`, `pitchdeck-skill`, `lead-research-assistant` | `company-research`, `competitor-*` |
| Mobile listing | store conversion, keyword rank | `app-store-optimization`, `app-store-screenshots`, `aso-appstore-screenshots` | `customer-research`, `competitor-*` |

Cross-cutting evidence spokes (`analytics-tracking`, `ab-test-setup`, `customer-research`,
`company-research`, `competitor-alternatives`, `competitor-teardown`) are not a funnel stage —
they are the substrate the stages cite.

## 5. Conventions

- **Voice of customer over copywriter instinct.** Headlines, offers, and objection handling
  should quote real customer language (`customer-research`), not invented benefits.
- **One change per test.** Stacking changes destroys attribution. If you must ship a bundle,
  say so and accept you've traded learning for speed.
- **Guardrail metrics.** Every primary metric has a guardrail (e.g. lifting signups but
  tanking activation is a loss). Name it before shipping.
- **Public pricing vs in-app upgrade are different surfaces.** `pricing-strategy` sets what you
  charge on the marketing site; `paywall-upgrade-cro` is the in-product moment after value is felt.
- **Self-serve and sales are two paths to the same revenue.** `revops` is the seam — lead
  scoring/routing and the marketing→sales handoff — not a funnel stage of its own.

## 6. Shared guardrails

- **One change, one metric, one hypothesis** — name the number before touching the funnel.
- **No win without a baseline.** Don't call an untested change a win; instrument first.
- **Respect significance + minimum runtime.** No peeking-and-stopping; no declaring victory from noise.
- **Ground copy and offers in evidence** (voice of customer, competitor data) — never fabricate
  metrics, lift percentages, or competitor claims.
- **State the blast radius of revenue changes.** Pricing and paywall edits affect real money and
  often other stages — call out the assumption and what could regress.
- **Decompose vague asks.** "Grow faster" → a specific stage, lever, metric, and test before any spoke runs.
- This cluster owns **convert → monetize → retain → sell**; top-of-funnel *creation* (brand voice,
  long-form, launch campaigns, investor narrative) lives in the `business-content` cluster — hand off
  rather than duplicate.
