---
name: emplaw-wage-hour-qa
version: 1.0.0
description: Answer a specific wage-and-hour question on overtime, minimum wage, meal and rest breaks, off-the-clock work, or tips.
author: matrixx0070
tags: [employment-law, wage-and-hour, overtime, flsa, breaks]
capabilities: []
---

## When to use
Use this when someone has a concrete wage-and-hour question — is this overtime owed, is this the right minimum wage, are breaks required, is this off-the-clock time compensable, how do tips work — and needs an accurate, jurisdiction-aware answer. This skill applies the FLSA plus state overlays. **Not for:** deciding if the worker is exempt or a contractor in the first place (use emplaw-worker-classification), reviewing a hire or offer (use emplaw-hiring-review), reviewing a firing or final-pay dispute at separation (use emplaw-termination-review), investigating a complaint (use emplaw-internal-investigation), leave questions (use emplaw-leave-tracker), or writing pay policy (use emplaw-policy-drafting).

## Method
1. Restate the question and confirm the operating state and the worker's status. Decision point: if exempt/non-exempt is unknown, resolve that first via emplaw-worker-classification — exempt employees are not owed FLSA overtime.
2. Identify the topic: overtime, minimum wage, breaks, off-the-clock, or tips.
3. Apply the federal floor. Decision point: for overtime, compute 1.5x the regular rate for hours over 40 in the workweek; the regular rate must include nondiscretionary bonuses.
4. Layer the state/local rule. Decision point: if the state sets a higher minimum wage or daily overtime (e.g., California), the more protective rule governs.
5. For breaks, check state law — the FLSA does not mandate meal/rest breaks. Decision point: if in a break state (e.g., California), apply the meal and rest thresholds.
6. For off-the-clock, ask whether the employer knew or should have known the work occurred; if so, it is compensable.
7. Show the calculation and cite the governing rule.
8. Apply the attorney-escalation gate: back-pay exposure and close calls — confirm with licensed counsel in the operating state; this is not legal advice.

## Example
A non-exempt California employee works 10 hours Monday and 45 hours that week, and earned a $200 production bonus. You compute daily overtime for the 2 hours over 8 on Monday, weekly overtime for hours over 40, fold the nondiscretionary bonus into the regular rate before the 1.5x multiplier, and confirm she was owed a meal break by the 5th hour and a paid 10-minute rest break per 4 hours worked.

## Pitfalls
- **Using base pay as the regular rate.** Nondiscretionary bonuses, shift differentials, and commissions must be included before applying the 1.5x multiplier.
- **Assuming federal breaks exist.** The FLSA requires no meal or rest breaks; break rights are state-created (California is strict).
- **Averaging hours across two weeks.** Overtime is computed per workweek, not per pay period.
- **Ignoring off-the-clock knowledge.** Pre-shift setup, post-shift cleanup, and answering messages count if the employer knew or should have known.

## Output format
```
WAGE-HOUR Q&A — <worker/role> @ <state>
QUESTION: <restated>
STATUS: <non-exempt | exempt — if exempt, no FLSA OT>
TOPIC: <overtime | minimum wage | breaks | off-the-clock | tips>
FEDERAL RULE: <FLSA floor applied>
STATE OVERLAY: <higher minimum / daily OT / breaks>
CALCULATION: <regular rate incl. bonuses → multiplier → total>
ANSWER: <bottom line>
ATTORNEY GATE: Confirm with licensed counsel in <state>; not legal advice.
```

## Reference
General reference only, not tailored legal advice.
- **Overtime (FLSA)**: non-exempt employees earn **1.5x the regular rate** for hours worked over **40 in a workweek**. The **regular rate** must include nondiscretionary bonuses, commissions, and shift differentials — not just base hourly pay.
- **Minimum wage**: federal is **$7.25/hour**; many state and local minimums are higher, and the more protective rate applies.
- **California overlays**: **daily overtime** at 1.5x for hours over **8 in a day** and **double time** for hours over **12**; a **meal break** by the end of the **5th hour** of work and a paid **10-minute rest break** per **4 hours** (or major fraction) worked.
- **Breaks generally**: the FLSA does not require meal or rest breaks; short rest breaks that are provided are typically paid. Break entitlements are set by state law.
- **Off-the-clock**: time is compensable if the employer knew or had reason to know the work was performed, even outside scheduled hours.
- **Tips**: tip credits, tip pooling, and required cash-wage minimums are governed by the FLSA and stricter state rules. Figures and state rules change — direct to current DOL and state labor-agency figures.
