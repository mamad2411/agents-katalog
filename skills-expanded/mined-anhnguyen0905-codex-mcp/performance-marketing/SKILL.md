---
name: performance-marketing
description: Diagnose and optimize paid media performance — CPI, CPM, CTR, CVR, ROAS and tROAS bidding, creative fatigue and refresh cadence, audience overlap, placement quality, ads account audit, campaign structure for Meta Ads and Google App Campaigns, and a daily optimization SOP for a performance marketing team.
---

# Performance Marketing (paid acquisition diagnosis & optimization)

## Decompose before you touch anything

Never optimize a moved metric directly — decompose it and find which factor actually moved:

```
CPI = CPM / 1000 ÷ (CTR × CVR_install)
CPA_purchase = CPI ÷ CVR_purchase
ROAS = revenue_attributed / spend
```

So "CPI +40%" is exactly one of: CPM rose (auction/competition/seasonality), CTR fell (creative
fatigue, wrong audience), or CVR fell (store page, onboarding, tracking break, geo mix shift).
Pull all three before proposing anything. If CPM rose while CTR/CVR held, the market changed and
creative work is the wrong fix.

## Diagnosis order

1. **Verify the measurement first.** SDK/tracking break, attribution window change, or a
   reporting-lag artifact explains more "sudden" moves than real performance does.
2. **Check the mix.** Aggregate CPI can rise while every campaign's CPI falls, if spend shifted to
   an expensive geo/placement (Simpson's paradox). Always segment by geo, placement, campaign, OS.
3. **Then look at creative and audience.**

## Creative fatigue

- Signals: CTR decaying vs its own first-72h baseline, frequency climbing (>2.5–3 on Meta for
  prospecting), CPM stable but CTR falling, spend concentrating on one ageing asset.
- Refresh when CTR drops ~20–30% from the asset's own baseline — not on a fixed calendar.
- Judge a creative only after enough impressions/conversions for stability; daily swings on a
  new asset are noise, and killing early is the most common way to starve a winner.

## Bidding guardrails (tROAS / tCPA)

- Smart bidding needs a minimum conversion volume per week or it never leaves the learning phase;
  under that, consolidate campaigns instead of splitting them.
- Change one variable per learning window (typically 3–7 days). Stacked changes make the result
  uninterpretable.
- Target moves in small steps (±10–20%); a large tROAS jump collapses delivery.
- Every guardrail needs a floor and a ceiling: min spend to stay in learning, max CPI/CPA at which
  you pause.

## Account audit checklist

Audience overlap between ad sets · duplicated targeting bidding against yourself · placement quality
(broad networks/audience-network junk) · geo and OS bid differentiation · budget trapped in learning
phase · dead creatives still drawing spend · frequency caps · broken deep links · exclusion lists
(existing users in prospecting) · campaign count vs conversion volume.

## Daily SOP (junior-safe)

Check spend pacing → check the metric tree per campaign vs its 7-day baseline → segment before
concluding → make at most one change per campaign per learning window → log every change with
timestamp and reason (a change log is what makes later diagnosis possible) → escalate anything
outside guardrails instead of improvising.

## Failure modes

- Treating platform-reported conversions as incremental (they are not — that needs a holdout).
- Comparing periods with different spend levels: CPI rises with spend by construction (marginal
  cost). Compare at comparable spend, or compare marginal CPI.
- Optimizing installs when the business is paid by revenue (or vice versa).
- Ignoring seasonality and competitive auction pressure (Q4, holidays, a rival's launch).
- Averaging over cohorts with different intent (retargeting mixed into prospecting).

## Reviewer checklist

- [ ] Metric tree shown with all three factors, not just the headline metric
- [ ] Segmented by geo/placement/campaign before any conclusion
- [ ] Measurement validity checked before performance is blamed
- [ ] Recommendations name one variable each, with a learning window
- [ ] Guardrails have both a floor and a ceiling
- [ ] Incrementality claims are labelled as platform-reported unless a holdout exists

## Provenance

Standard paid-acquisition practice (metric decomposition, learning-phase and frequency thresholds,
one-variable-per-window discipline). Numeric thresholds are **derived, unverified** rules of thumb —
confirm against the account's own historical distribution before treating them as targets.
