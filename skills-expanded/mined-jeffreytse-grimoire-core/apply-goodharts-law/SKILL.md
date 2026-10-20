---
name: apply-goodharts-law
description: Use when choosing what to measure for a KPI, OKR, ML training objective, or SLO — or when a metric that once tracked real performance keeps rising while the underlying outcome doesn't — to diagnose or prevent the specific mechanism by which a measure degrades once people optimize directly against it.
source: 'Charles Goodhart, Reserve Bank of Australia lecture on UK monetary policy (1975) — original formulation; Marilyn Strathern "Improving ratings: audit in the British University system", Social Anthropology (1997) — generalized the law to "When a measure becomes a target, it ceases to be a good measure"; Donald T. Campbell "Assessing the Impact of Planned Social Change" (1976) — independently derived "Campbell''s Law" in social-science evaluation; John Doerr "Measure What Matters" (2018) — OKR guidance against tying objectives to compensation for this reason'
tags: [metrics, incentive-design, kpi, measurement, systems-thinking, gaming, unintended-consequences]
related: [design-incentive-systems, design-feedback-loops, write-okrs, design-kpi-dashboard, apply-poison-cure-diagnostic, apply-earnings-myopia-defense, apply-statistical-process-control]
---

# Apply Goodhart's Law

Treat any metric adopted as an optimization target as a metric that will start diverging from the outcome it was meant to represent — and design measurement systems that detect or resist that divergence instead of assuming a good proxy stays good once targeted.

## Why This Is Best Practice

**Origin:** Charles Goodhart formulated the law in 1975 while critiquing UK monetary policy: once a central bank targets a particular measure of money supply, its statistical relationship with inflation breaks down, because people change behavior specifically to hit the targeted measure. Marilyn Strathern's 1997 generalization — "When a measure becomes a target, it ceases to be a good measure" — is the widely cited modern form and extends the mechanism far beyond monetary policy to any human system with a measured target.

**Adopted by:** Independently rediscovered in social science as Campbell's Law (Donald Campbell, 1976) for evaluating social programs and test-based education metrics — two separate fields converging on the same mechanism is itself evidence of how general the failure mode is. OKR literature (Doerr, *Measure What Matters*) explicitly warns against tying OKRs to compensation for exactly this reason, and ML engineering practice treats "reward hacking" / "specification gaming" in trained models as a direct instance of the same law applied to a training objective rather than a human incentive.

**Impact:** Historical instances are well documented and falsifiable: the Soviet nail-factory quota (measuring nails by weight produced a few giant useless nails; measuring by count produced huge numbers of tiny useless ones), UK police forces improving "crimes solved" rates by reclassifying or declining to record crimes rather than solving more of them, and standardized-testing "teaching to the test" narrowing actual educational outcomes while scores rise. In ML, models trained against a proxy reward metric repeatedly find degenerate policies that maximize the metric while failing the actual task (documented specification-gaming case collections from DeepMind and OpenAI).

**Why best:** This is a different failure mode than the ones adjacent skills already cover. `design-feedback-loops` names "distorted signal: metric measures proxy, not actual outcome" as one bullet inside general systems-thinking loop-mapping; `design-incentive-systems` cites the law once to justify structural-incentive over virtue-reliance auditing; `write-okrs` bans compensation-linked OKRs as one specific rule. None of them teach the underlying mechanism — that *targeting itself*, not bad metric selection, is what corrupts a measure — or give a general method to detect and design against it across KPI, OKR, ML-objective, and SLO contexts alike.

Sources: Goodhart, Reserve Bank of Australia (1975); Strathern, *Social Anthropology* (1997); Campbell, "Assessing the Impact of Planned Social Change" (1976); Doerr, *Measure What Matters* (2018).

## Steps

### 1. Distinguish the true outcome from the proxy metric

State the actual outcome you care about in words first ("customers succeed at their task," "code changes don't break production"), then identify the metric you're about to target. Write both down separately — if you can't articulate the outcome independent of the metric, you have no way to detect divergence later.

### 2. Ask what the cheapest way to move the metric is, without moving the outcome

For any candidate metric, deliberately search for the lowest-effort way to increase it that does nothing for the real outcome — reclassifying data, narrowing scope, gaming a reset window, hard-coding to a benchmark. If a cheap, outcome-free way to move the metric exists, expect it to get found once the metric becomes a target, especially under time or resource pressure.

### 3. Prefer metrics that are expensive or impossible to game without also achieving the outcome

Favor outcome-adjacent measures that are structurally hard to hit any other way (e.g., independently audited or randomly sampled measurements, holdout data the target-setter can't see in advance, multiple metrics that must move together) over easily-manipulated single proxies.

### 4. Add a paired counter-metric that would catch gaming

For every target metric, add at least one counter-metric that would move in a suspicious direction if the target were being gamed rather than genuinely improved (e.g., pair "tickets closed" with "ticket reopen rate," pair "test coverage %" with "bugs escaping to production," pair a model's reward score with held-out task performance it was never trained against).

### 5. Re-validate the metric-outcome relationship on a cadence, not just at design time

A metric that correlated with the outcome when chosen can decorrelate after months of being targeted. Periodically re-check the correlation against independent evidence (customer interviews, audits, holdout evaluation) rather than assuming the original validation still holds.

### 6. Keep some evaluation un-gameable by keeping it un-targeted

Hold back at least one evaluation signal that is never itself set as a target and never disclosed in advance to the people being measured — this is what keeps a holdout/audit/spot-check useful long after the primary metric has been optimized against.

## Rules

- Never assume a good proxy metric stays good once it becomes a target — treat divergence as the expected default, not an edge case.
- Don't tie compensation, promotion, or high-stakes evaluation directly to a single easily-gamed metric; pair it with a counter-metric or an un-targeted holdout check.
- Re-validate metric-outcome correlation periodically — a metric chosen well a year ago can have already decoupled from the outcome it was meant to track.

## Common Mistakes

- **Treating a validated metric as permanently validated.** The validation was true before the metric became a target; targeting is exactly what breaks it.
- **Adding more precision to a metric instead of questioning whether it's still measuring the outcome.** A more precisely measured proxy is still a corrupted proxy if the underlying behavior has shifted to game it.
- **Punishing the people who found the gaming loophole instead of fixing the metric.** If a cheap way to move the metric without moving the outcome exists, someone will eventually find it under pressure — that's a metric design failure, not a discipline failure.
- **Using a single metric with no counter-metric or holdout check for anything high-stakes.** Single-metric optimization is the exact setup Goodhart's Law predicts will fail.

## When NOT to Use

- Low-stakes, informational-only metrics that no one is being evaluated or rewarded against — Goodhart's mechanism requires the metric to actually function as a target; a dashboard number nobody optimizes toward doesn't need this level of defense.
- Metrics that are inherently the outcome itself, not a proxy for it (e.g., literal revenue for a revenue objective) — the law describes proxy-target divergence specifically; it doesn't apply where the "measure" and the "outcome" are the same thing.
