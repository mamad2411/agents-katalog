---
name: gro-funnel-analysis
version: 1.0.0
description: Analyze a conversion funnel end-to-end, locate the biggest drop-off, and prescribe the highest-leverage fix.
author: matrixx0070
tags: [growth, funnel, conversion, analytics, optimization]
capabilities: []
---

## When to use

Use this when you have an ordered sequence of steps users must complete (visit → signup → activate → pay) and you want to know where you lose the most people and what to do about it. Reach for it before any redesign, when a metric drops, or when leadership asks "where should we invest?"

**Not for:** unordered behavior exploration (use gro-cohort-analysis), long-run repeat usage (gro-retention-analysis), or deciding whether a change worked (gro-ab-test-design). Funnel analysis finds *where*; those find *why over time* and *whether*.

## Method

1. Define the funnel as ordered, mutually exclusive steps with an explicit denominator and time window (e.g. "of users who signed up this week, % reaching each step within 7 days"). Decision point: use *unique users* per step, not events, unless you specifically study repeat actions.
2. Pull counts per step. Compute step-to-step conversion (step N+1 / step N) AND overall conversion (step N / step 1).
3. Rank steps by *absolute users lost* (stepN − stepN+1), not by percentage. A 10% drop on a huge step often beats a 60% drop on a tiny one.
4. For the top loss step, segment it: device, source, new vs returning, geo, plan. Decision point: if one segment drives most of the loss, fix that segment; if loss is uniform, the step itself is broken.
5. Diagnose root cause with session data, error logs, or a quick user watch. Classify as friction (too hard), motivation (unclear value), or timing (asked too early).
6. Prescribe ONE fix mapped to the cause, estimate uplift (recovered users × downstream conversion × value), and hand to gro-ab-test-design if the change is risky.

## Example

Signup 10,000 → Verified email 6,000 (−4,000) → Activated 5,400 → Paid 540. Biggest raw loss is email verification (4,000 users). Segmenting: mobile verification converts 45%, desktop 78%. Root cause: the verification link opens in a different browser on mobile, dropping the session. Fix: 6-digit code instead of a link. Estimated recovery: ~2,000 mobile users × 9% paid = ~180 new paying users.

## Pitfalls

- Ranking by percentage instead of absolute loss, so you optimize a step that barely matters.
- Mixing time windows across steps (lifetime signups vs 7-day activation) — conversions become meaningless.
- Treating the funnel as strictly linear when users skip or loop; validate the real path first.
- Proposing five fixes at once so you can never attribute the uplift.

## Output format

```
Funnel: <name> | Window: <N days> | Denominator: <cohort>
Step            Users    Step CR   Overall CR
1 <step>        10000    —         100%
2 <step>         6000    60%        60%
...
Biggest drop:   <step> → <step> (−<X> users, <Y>%)
Top segment:    <segment> (<CR> vs <baseline CR>)
Root cause:     <friction | motivation | timing> — <detail>
Recommended fix: <one change>
Est. impact:    <recovered users> → <downstream value>
Next: <ship | A/B test via gro-ab-test-design>
```
