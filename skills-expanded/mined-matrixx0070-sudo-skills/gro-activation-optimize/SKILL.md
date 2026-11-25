---
name: gro-activation-optimize
version: 1.0.0
description: Find the aha-moment and improve activation by getting more new users to first value faster.
author: matrixx0070
tags: [growth, activation, onboarding, aha-moment, conversion]
capabilities: []
---

## When to use

Use this when signups are healthy but users don't stick — the gap between "created account" and "got value." Reach for it to define an activation metric, redesign onboarding, or diagnose why new users go dark in the first session or week.

**Not for:** long-run repeat usage (use gro-retention-analysis), mid/late funnel steps like payment (gro-funnel-analysis), or acquisition/traffic problems. Activation is specifically the *first value* zone.

## Method

1. Define the aha-moment: the earliest action that predicts long-run retention. Find it empirically — for each candidate early action, compare downstream retention of users who did vs didn't do it. Pick the one with the biggest, most reliable gap that a new user can plausibly reach fast.
2. Quantify it as "X actions in Y days" (the classic magic-number pattern) by scanning where the retention-vs-count curve bends. Decision point: choose the count at the *elbow*, not the max — beyond the elbow, extra actions add little.
3. Measure current activation rate = % of new users who hit the aha-moment in the window.
4. Map the onboarding path to the aha-moment step by step and find the biggest drop (this reuses gro-funnel-analysis on the activation sub-funnel).
5. Decision point: is the blocker setup friction (too many steps), the empty state (nothing to do), or unclear value (they don't know why)? Remove steps, seed the empty state with templates/sample data, or add value messaging accordingly.
6. Reduce time-to-value: default choices, pre-fill, defer non-essential setup. Ship one change and validate activation-rate lift with gro-ab-test-design.

## Example

For a note app, candidates: "wrote a note," "installed mobile app," "created 2 notes." Users with ≥2 notes in 3 days retain at 48% vs 11%. The curve elbows at 2 notes. Activation = "2 notes in 3 days," currently 30%. Onboarding funnel shows 40% never leave the empty home screen. Fix: seed the account with 3 starter templates. Test lift on activation rate.

## Pitfalls

- Picking a vanity aha-moment (profile completed) that doesn't actually predict retention.
- Choosing the magic number at the max instead of the elbow, setting an unreachable bar.
- Adding onboarding steps ("complete your profile!") that add friction before value.
- Optimizing activation while ignoring that you attract the wrong users upstream.

## Output format

```
Aha-moment:      <action> — retention <did %> vs <didn't %>
Magic number:    <X actions> in <Y days> (elbow of retention curve)
Activation rate: <current %> of new users
Activation funnel biggest drop: <step> (−<X>%)
Blocker type:    <friction | empty state | unclear value>
Fix:             <one change: remove steps | seed empty state | value msg>
Time-to-value:   <before> → <target>
Validation:      A/B on activation rate via gro-ab-test-design
```
