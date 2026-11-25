---
name: eqr-idea-generation
version: 1.0.0
description: Generate and pre-screen equity investment ideas from screens, catalysts, and anomalies — into a ranked shortlist with a one-line variant thesis and a kill test for each.
author: matrixx0070
tags: [equity-research, idea-generation, screening, variant-perception, pipeline]
capabilities: []
---

## When to use

Use this when you need new names to work on — a screen came back, a theme is emerging, a peer moved, or the pipeline is thin — and you want to convert raw candidates into a ranked shortlist worth real diligence. The job is to find where you might have a differentiated view, not to confirm what is already consensus.

**Not for:** deep diligence on a name you've already chosen (use `eqr-initiating-coverage`), tracking a live position (use `eqr-thesis-tracker`), or building numbers (use `eqr-model-update`). This fills the funnel; it does not underwrite. Outputs are research and education, not personalized investment advice.

## Method

1. **Choose the source.** Quant screen, catalyst-driven, thematic, spin-off/special-situation, anomaly (insider buying, guidance/estimate divergence, unusual price action), or peer read-across. *Decision point:* name the source so the bias of each is explicit.
2. **Cast wide, then filter for a variant view.** For each candidate ask: where could my view differ from consensus (numbers, narrative, or time horizon)? Discard names where you'd just be agreeing with the tape.
3. **Do the 15-minute triage.** Business quality, why it might be mispriced, obvious red flags (accounting, leverage, governance, liquidity), and whether it's investable (size, borrow, restrictions).
4. **Write a one-line variant thesis** per survivor: the specific thing you believe that the market does not.
5. **Attach a kill test** — the single fastest check that would disprove the idea. Cheap disconfirmation first.
6. **Rank by edge × feasibility.** Edge = size of variant view. Feasibility = how knowable it is with the time you have.
7. **Assign next action.** Kill, park (with a trigger), or promote to full diligence.

## Example

Estimate-revision screen surfaces an industrial with rising forward EPS but a flat stock. Triage: quality decent, possible mispricing = market anchored to an old cyclical narrative; red flags none material; investable. Variant thesis: "Aftermarket mix shift lifts through-cycle margins 200bps that consensus still models as peak." Kill test: check whether aftermarket revenue is actually growing faster than OE in the last two 10-Qs. Edge high, feasibility high → promote. A second name fails its kill test in ten minutes (mix not shifting) → kill.

## Pitfalls

- **Consensus in disguise.** Generating ideas that just restate what's priced in — no variant view, no edge.
- **Falling in love pre-diligence.** Skipping the kill test because the story is exciting. Disconfirm cheaply first.
- **Screen worship.** Treating a screen output as an idea; it's only a candidate until triaged.
- **Ignoring investability.** A brilliant thesis on an untradeable microcap or hard-to-borrow name is not an idea you can use.
- **No ranking.** A flat list of 40 names stalls; force edge × feasibility and assign an action.

## Output format

```
IDEA GENERATION | source: <screen/catalyst/theme/anomaly/read-across> | as of <date>
CANDIDATE | ticker | business (1 line) | why mispriced | red flags | investable?
VARIANT THESIS: <the thing the market doesn't believe>
KILL TEST: <fastest disconfirming check>
RANK: edge 1-10 x feasibility 1-10
ACTION: kill / park (trigger: …) / promote to diligence
SHORTLIST (promoted): 1) … 2) … 3) …
Note: research/education, not personalized investment advice.
```

## Reference

Research process: name the idea source so its bias is explicit, cast wide, and filter for a differentiated variant view rather than confirmation of consensus. Triage each candidate for business quality, the mispricing mechanism, red flags (accounting, leverage, governance, liquidity), and investability, then write a one-line variant thesis and the cheapest disconfirming kill test. Modeling: promoted names go to `eqr-initiating-coverage` for diligence and `eqr-model-update` for numbers; this stage does not underwrite. Disclosure: idea generation is preliminary research and education, screens and triage are not a recommendation, and nothing here is personalized investment advice.
