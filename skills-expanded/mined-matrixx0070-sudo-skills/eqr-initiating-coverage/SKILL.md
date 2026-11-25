---
name: eqr-initiating-coverage
version: 1.0.0
description: Build a full initiation on a stock — business, thesis, model, valuation, risks, and a rating with target and time horizon — into a structured coverage-launch note.
author: matrixx0070
tags: [equity-research, initiation, coverage, valuation, thesis]
capabilities: []
---

## When to use

Use this when you're launching coverage on a name for the first time and need the complete, defensible package: what the business is, why your view is differentiated, the numbers, the valuation, the risks, and a rating with a target and horizon. This is the deepest note in the vertical — the foundation everything later (previews, updates, thesis tracking) refers back to.

**Not for:** finding the name (use `eqr-idea-generation`), a quarterly update (use `eqr-model-update`), or a quick sector map (use `eqr-sector-overview`). Outputs are research and education, not personalized investment advice; ratings and targets are analytical opinions, not recommendations tailored to any individual.

## Method

1. **Describe the business.** What it sells, to whom, how it makes money, unit economics, and where it sits in the value chain. If you can't explain the model simply, you're not ready to rate it.
2. **Map the industry.** TAM, growth, structure, competition, and the company's moat and share trajectory. *Decision point:* if there's no durable competitive advantage, the thesis must rest on price/mispricing, not quality.
3. **State the thesis and the variant view.** The three or four pillars and, explicitly, what you believe that consensus does not.
4. **Build the model.** Revenue drivers, margin path, capital intensity, and free cash flow — with assumptions stated and stress-tested (see `eqr-model-update` for mechanics).
5. **Value it.** Use at least two methods (e.g., DCF + comps/multiple) and reconcile them. *Decision point:* if methods disagree widely, resolve why before setting a target.
6. **Set rating, target, and horizon.** Derive the target from the valuation, define upside/downside vs. current price, and state the time horizon (typically 12 months).
7. **Enumerate risks and what breaks the thesis.** Key risks, the bear case, and the specific evidence that would force a downgrade — pre-committed, not retrofitted.

## Example

Initiate on a payments network. Business: take-rate on transaction volume, near-zero incremental cost, two-sided network. Industry: secular cash-to-card shift, oligopoly, wide moat. Thesis pillars: (1) volume compounding, (2) mix shift to higher-yield cross-border, (3) operating leverage; variant view = consensus undermodels cross-border recovery. Model: 11% revenue CAGR, margins +300bps over three years. Valuation: DCF $X, 28x forward EPS comps $Y, reconciled to a $Z target. Rating: Outperform, 12-mo target implies +22% upside. Risks: regulation of interchange, recession volume hit, FX. Downgrade trigger: cross-border volume stalls two consecutive quarters.

## Pitfalls

- **Model before understanding.** A spreadsheet on a business you can't explain simply produces false precision.
- **No variant view.** A thorough note that agrees with consensus adds no edge; state where you differ.
- **Single valuation method.** One DCF with a hand-picked terminal value isn't a valuation; triangulate.
- **Target reverse-engineered from the rating.** Decide the value, then the rating — not the other way around.
- **Risks as boilerplate.** Generic "competition and regulation" risks are useless; name the specific thesis-breakers and their triggers.

## Output format

```
INITIATION: <ticker> | rating <Buy/Hold/Sell> | target <price> | horizon <months> | as of <date>
BUSINESS: model | unit economics | value-chain position
INDUSTRY: TAM/growth | structure | moat | share trajectory
THESIS: pillars 1-4 | VARIANT VIEW: <vs consensus>
MODEL: revenue drivers | margin path | capex/FCF | key assumptions
VALUATION: method 1 <value> | method 2 <value> | reconciliation -> target
RATING: <rating> | upside/downside vs current | horizon
RISKS: key risks | bear case | DOWNGRADE TRIGGER: <specific>
Note: research/education, not personalized investment advice.
```

## Reference

Research process: ground the initiation in a plainly explained business model and industry map before any numbers, state the thesis pillars and an explicit variant view versus consensus, and pre-commit the downgrade triggers rather than retrofitting risks. Modeling and valuation: build stated, stress-tested assumptions (mechanics in `eqr-model-update`), value with at least two reconciled methods, and derive the target from value before assigning the rating. Disclosure: an initiation, its rating, and its price target are the analyst's research opinion for education, depend on assumptions that can prove wrong, and are not personalized investment advice or a recommendation suited to any particular person's circumstances; note any position or conflict per applicable policy.
