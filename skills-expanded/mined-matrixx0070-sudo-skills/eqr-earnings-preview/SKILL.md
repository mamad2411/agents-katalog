---
name: eqr-earnings-preview
version: 1.0.0
description: Set up an upcoming earnings print — estimates versus consensus, the bar, key debates, scenarios, and what to watch — into a pre-print preview note.
author: matrixx0070
tags: [equity-research, earnings, preview, estimates, expectations]
capabilities: []
---

## When to use

Use this in the days before a company reports, when you need a clear view of the setup: where your numbers sit versus consensus, what the market is really debating, and how the stock could react across scenarios. A good preview decides in advance what would confirm or break the view, so the print does not catch you improvising.

**Not for:** analyzing the quarter after it lands (use `eqr-earnings-analysis`), rebuilding the model (use `eqr-model-update`), or mapping longer-dated events (use `eqr-catalyst-calendar`). Outputs are research and education, not personalized investment advice.

## Method

1. **Pin the print details.** Report date/time, whether guidance is given, and which segments matter most this quarter.
2. **State the bar.** Consensus for revenue, key segments, margin, and EPS — plus the whisper/buyside bar if it differs from published consensus. *Decision point:* if the whisper is well above consensus, the effective bar is the whisper.
3. **Place your estimates.** Your numbers vs. consensus with the reason for any gap (above/below/in line, and why).
4. **Frame the key debate.** The one or two questions the print will answer (e.g., margin trajectory, demand inflection, guide credibility).
5. **Build scenarios.** Bull / base / bear with the specific line results and the likely stock reaction for each. Assign rough probabilities.
6. **List watch items.** The exact metrics, disclosures, and call topics that will confirm or break the view — decided now, before the emotion of the print.
7. **State setup and skew.** Is expectation high or low into the print, and is the risk/reward skewed up or down given positioning and the bar.

## Example

Consumer name reports Thu AMC, gives annual guide. Consensus rev $2.10B / EPS $1.15; buyside whisper closer to $2.15B (effective bar higher). Our estimate $2.12B — above published, below whisper; gap from stronger units, softer price. Key debate: can gross margin recover after two quarters of promo. Scenarios: bull (margin +150bps, guide raise, +8%), base (margin flat, guide in line, +/-2%), bear (continued promo, guide cut, -12%). Watch: gross margin bridge, inventory days, promo language on the call. Setup: expectations elevated into the print; skew slightly negative given the whisper.

## Pitfalls

- **Consensus ≠ the bar.** The stock reacts to the whisper/buyside bar, which can sit well above published consensus.
- **No pre-committed watch items.** Deciding what matters after the numbers hit invites confirmation bias.
- **Point estimate only.** One number can't capture reaction risk; scenarios with probabilities do.
- **Ignoring positioning.** A great quarter into a crowded long can still sell off; account for setup and skew.
- **Forgetting guidance is the payload.** For many names the guide, not the quarter, moves the stock — preview it explicitly.

## Output format

```
EARNINGS PREVIEW: <ticker> <quarter> | reports <date/time> | guidance: Y/N
BAR: consensus (rev/segments/margin/EPS) | whisper/buyside bar
OUR EST vs CONS: <above/below/in line> — reason
KEY DEBATE: 1-2 questions the print answers
SCENARIOS: bull / base / bear — line results | stock reaction | prob
WATCH (pre-committed): metrics | disclosures | call topics
SETUP & SKEW: expectations high/low | risk-reward skew
Note: research/education, not personalized investment advice.
```

## Reference

Research process: distinguish published consensus from the effective bar (whisper/buyside), place your estimates against both with a reason for any gap, and pre-commit the watch items that would confirm or break the view before the print. Build bull/base/bear scenarios with line-level results, expected reactions, and rough probabilities, and account for positioning so setup and skew are explicit. Modeling: estimates carry into the model via `eqr-model-update`; the post-print reconciliation lives in `eqr-earnings-analysis`. Disclosure: a preview is scenario-based research and education using estimates that will differ from actual results, and is not personalized investment advice or a recommendation to transact around an event.
