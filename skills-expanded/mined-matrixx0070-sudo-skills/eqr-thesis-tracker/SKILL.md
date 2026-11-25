---
name: eqr-thesis-tracker
version: 1.0.0
description: Track a live investment thesis against evidence — pillars, milestones, disconfirming signals, and a rules-based verdict to hold, revise, or exit.
author: matrixx0070
tags: [equity-research, thesis, monitoring, discipline, exit]
capabilities: []
---

## When to use

Use this to keep an active thesis honest over time: check whether the reasons you own (or rate) the name are still intact, whether milestones are being hit, and whether any disconfirming evidence has arrived. It exists to fight anchoring and thesis creep — the tendency to keep a call alive by quietly rewriting why you hold it.

**Not for:** forming the thesis (use `eqr-initiating-coverage`), rebuilding numbers (use `eqr-model-update`), or reacting to a single print (use `eqr-earnings-analysis` — its output feeds this tracker). Outputs are research and education, not personalized investment advice.

## Method

1. **Restate the original thesis verbatim.** Pull the pillars and the variant view exactly as written at initiation. *Decision point:* if you can't state them precisely, the thesis was never testable — fix that first.
2. **List the pre-committed proof points.** For each pillar, the milestone that confirms it and the signal that disconfirms it — decided at initiation, not now.
3. **Score each pillar against evidence.** On-track / stalled / broken, citing the specific data since last review. No narrative substitution.
4. **Check for thesis creep.** Are you defending the position with reasons that weren't in the original thesis? Flag any new justification as a rewrite, not a confirmation.
5. **Update the variant view.** Has the market moved toward your view (edge captured) or away (edge widened or wrong)?
6. **Apply the exit rules.** Compare evidence to the pre-committed downgrade/exit triggers. *Decision point:* if a trigger is hit, the default is act — overriding requires a written reason.
7. **Render the verdict.** Hold / add / trim / exit, with the evidence, and set the next review date and what to watch.

## Example

Tracker on a cloud-software long. Original pillars: (1) 30% durable growth, (2) margin inflection, (3) net-retention >120%. Proof points since last review: growth decel to 24% two quarters running (pillar 1 = broken vs. pre-committed trigger "sub-27% two quarters"), margins inflected as expected (pillar 2 on-track), NRR slipped to 118% (pillar 3 stalled). Thesis-creep check: recent bull case leaned on "AI upsell optionality" — not in the original thesis → flagged as a rewrite. Exit rule on pillar 1 hit. Verdict: trim/exit per rule; document any override. Next review: next print; watch NRR and growth stabilization.

## Pitfalls

- **Thesis creep.** Keeping the call alive by swapping in new reasons. If today's rationale wasn't in the original, it's a rewrite.
- **Narrative over evidence.** Scoring pillars on story rather than the specific data since last review.
- **No pre-committed triggers.** Exit rules invented after the fact bend to the position you already hold.
- **Confusing price with thesis.** A falling price isn't disconfirmation; a broken pillar is. Judge the fundamentals.
- **Skipping reviews when it's working.** Winners breed complacency; unchecked theses are how gains round-trip.

## Output format

```
THESIS TRACKER: <ticker> | initiated <date> | review <date>
ORIGINAL THESIS (verbatim): pillars 1-n | variant view
PROOF POINTS (pre-committed): pillar | confirm milestone | disconfirm signal
SCORECARD: pillar | on-track/stalled/broken | evidence since last review
THESIS-CREEP CHECK: new justifications not in original? <flagged>
VARIANT VIEW: market moved toward/away — edge captured/wrong
EXIT RULES: trigger | hit? | default action
VERDICT: hold/add/trim/exit + reason | override note if any
NEXT REVIEW: <date> | watch: …
Note: research/education, not personalized investment advice.
```

## Reference

Research process: restate the thesis verbatim from initiation, score each pillar against specific evidence since the last review rather than narrative, and run an explicit thesis-creep check that flags any current justification absent from the original as a rewrite. Modeling and discipline: apply pre-committed exit/downgrade triggers with act-by-default, route number changes to `eqr-model-update`, and ingest single-print reads from `eqr-earnings-analysis`; the original pillars come from `eqr-initiating-coverage`. Disclosure: a thesis tracker is research and education, its verdicts are rules-based analytical opinions dependent on assumptions that can prove wrong, and it is not personalized investment advice or a recommendation to buy, hold, or sell.
