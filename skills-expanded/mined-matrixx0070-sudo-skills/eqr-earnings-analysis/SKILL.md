---
name: eqr-earnings-analysis
version: 1.0.0
description: Analyze a company's reported quarter — beat/miss versus estimates, quality of results, guidance change, and thesis impact — into a decision-ready post-earnings note.
author: matrixx0070
tags: [equity-research, earnings, results, quality, guidance]
capabilities: []
---

## When to use

Use this right after a company reports, when you have the release, the financials, and the call, and need to judge what actually happened versus expectations and whether the thesis still holds. This is the post-mortem of a print: what beat, what missed, whether the beat was real, and what changed forward.

**Not for:** setting up expectations before the print (use `eqr-earnings-preview`), a one-line desk blast (use `eqr-morning-note`), or the mechanical model rebuild afterward (use `eqr-model-update` — this note tells it what to change). Outputs are research and education, not personalized investment advice.

## Method

1. **Anchor to expectations.** Pull consensus and your own estimates for revenue, key segments, margins, and EPS. Beat/miss is meaningless without the bar.
2. **Compute the deltas.** Actual vs. consensus vs. your model, in absolute and percent, line by line. Flag which lines drove the surprise.
3. **Judge quality, not just direction.** *Decision point:* is the beat operational (volume, price, mix, share) or low-quality (one-time items, tax, buyback EPS, pull-forward, accruals, FX)? Low-quality beats fade.
4. **Read the guidance change.** Compare new guide to old and to consensus. Note raise/cut/reaffirm, and whether the shape (H2 weighting, segment mix) is credible.
5. **Mine the call.** Management tone, unprompted disclosures, changed language, analyst pushback, and what they avoided answering.
6. **Test the thesis.** Map results to each thesis pillar: confirmed, damaged, or unchanged. *Decision point:* if a core pillar broke, escalate to a thesis review, not just an estimate tweak.
7. **State the number and view implication.** What EPS/estimate direction this implies and the two or three things to watch next.

## Example

Software name reports: revenue +3% vs. consensus, EPS +9%. Deltas show EPS beat came from a lower tax rate and buyback, not operating leverage — margin was in line, billings decelerated. Guidance reaffirmed (consensus expected a raise → effectively a soft signal). Call: CFO dodged a net-retention question. Quality verdict: low. Thesis pillar "durable 30% growth" damaged by billings decel. Implication: estimates flat to down despite the headline EPS beat; watch next-quarter billings and NRR disclosure.

## Pitfalls

- **Headline-EPS trap.** Celebrating an EPS beat driven by tax/buyback/one-timers while the operating story weakened.
- **No bar.** Reporting "revenue grew 20%" without saying versus what — the surprise is the whole point.
- **Ignoring guidance shape.** A raised full-year guide that back-end-loads H2 can be a warning, not a win.
- **Skipping the call.** The release rarely contains the tell; language changes and dodged questions do.
- **Confusing a miss with a broken thesis.** One weak line ≠ thesis break; map to pillars before escalating.

## Output format

```
EARNINGS ANALYSIS: <ticker> <quarter> | reported <date>
BAR: consensus / our est (rev, segments, margin, EPS)
RESULTS vs BAR: line | actual | cons Δ | our Δ | driver
QUALITY: <operational | low-quality: one-timers/tax/buyback/pull-forward> — verdict
GUIDANCE: old -> new vs cons | shape/credibility
CALL: tone | new disclosures | changed language | dodges
THESIS CHECK: pillar-by-pillar (confirmed/damaged/unchanged)
IMPLICATION: estimate direction | escalate to thesis review? | watch next: 1) 2) 3)
Note: research/education, not personalized investment advice.
```

## Reference

Research process: judge a print against a stated bar (consensus plus your own estimates), decompose the surprise line by line, and separate operational drivers from low-quality sources (one-time items, tax, buyback-driven EPS, pull-forward, FX) before concluding. Read guidance for both level and shape, and mine the call for tone and changed language. Modeling: this note specifies what to change and why; the mechanical rebuild belongs in `eqr-model-update`, and a broken thesis pillar routes to `eqr-thesis-tracker`. Disclosure: results analysis is research and education based on reported data and estimates that can be revised, and is not personalized investment advice or a recommendation to buy or sell.
