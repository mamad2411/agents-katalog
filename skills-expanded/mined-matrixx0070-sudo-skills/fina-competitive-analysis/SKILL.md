---
name: fina-competitive-analysis
version: 1.0.0
description: Assess a company's competitive position (five forces, market share, moat, KPI benchmarking) and translate it into the forecast drivers and assumptions that feed a financial model.
author: matrixx0070
tags: [finance, competitive-analysis, porter-five-forces, moat, tam-sam-som, benchmarking, roic, rule-of-40, forecast-drivers]
capabilities: []
---

# Competitive Analysis for Financial Modeling

## When to use
Use this to judge how defensible and how fast-growing a business is relative to its industry and rivals, and to convert that judgment into the revenue-growth, margin, and reinvestment assumptions a model needs.

**Not for:** deriving a relative valuation from peer multiples (fina-comps-analysis), running the intrinsic valuation those drivers feed (fina-dcf-model), building the projection mechanics themselves (fina-3-statement-model), or benchmarking a single line's variance (fina-financial-statements).

## Method
1. **Frame the market and the unit.** Define the industry, the specific segment the company competes in, the customer, and the unit you measure economics on (per seat, per store, per subscriber). State the time horizon of the analysis.
2. **Size the opportunity (TAM/SAM/SOM).** Estimate total addressable, serviceable-addressable, and serviceable-obtainable market. Decision point: if bottom-up (units x price x buyers) and top-down (industry revenue x reachable share) sizing differ by more than ~2x, reconcile before using either; an unreconciled TAM produces an indefensible growth ceiling.
3. **Run Porter's five forces.** Score rivalry, new entrants, supplier power, buyer power, and substitutes as low/medium/high with evidence. Net them into an industry attractiveness read that caps sustainable margins and pricing power.
4. **Measure market share and trajectory.** Company revenue / market revenue, and the change over time. Rising share in a growing market is the strongest signal; falling share in a growing market flags a competitive problem the forecast must reflect.
5. **Test the moat.** Identify the source (network effects, switching costs, cost advantage, intangibles/brand, efficient scale) and demand evidence: does the company earn ROIC above its cost of capital, and is the spread persistent? Decision point: if ROIC does not exceed WACC over a full cycle, treat the moat as unproven and fade excess returns to the cost of capital in the forecast.
6. **Interrogate unit economics.** Contribution margin, CAC, LTV, payback period, cohort retention/churn. Confirm the business gets more profitable per unit as it scales, not less.
7. **Benchmark KPIs against peers.** Put growth, gross/EBITDA/EBIT margin, ROIC, capital intensity, FCF conversion, and Rule of 40 side by side with 3-6 named comparables to locate the company in the pack.
8. **Translate position into drivers.** Map each finding to a specific model assumption: share trajectory and TAM to revenue growth, five-forces pricing power and scale to margin path, capital intensity to capex and working capital, moat durability to the fade profile and terminal growth.
9. **Stress the assumptions.** State the competitive event that would break each driver (a new entrant, share loss, input-cost spike) and carry it into the model's downside case.

## Example
Vertical SaaS company: revenue $500M growing 25%, in a $10B TAM (SAM $4B), so ~12.5% SAM share and rising ~2 pts/year. Five forces: rivalry medium, entrants low (high switching costs), buyer power low (mission-critical workflow) - attractive. Gross margin 78%, EBITDA margin 22%, ROIC 18% vs WACC 9% (9-pt spread => real moat). Rule of 40 = 25% growth + 22% margin = 47 (healthy, >40).

Translation to model: revenue growth fades 25% -> 12% over 7 years as SAM share approaches ~30% and the market matures; EBITDA margin expands 22% -> 30% on operating leverage from the switching-cost moat; ROIC excess return fades toward WACC by year 10. These become the exact top-line and margin drivers handed to fina-3-statement-model and fina-dcf-model.

## Pitfalls
- **TAM inflation.** A top-down "1% of a huge market" story with no bottom-up reconciliation sets a growth ceiling the model cannot defend.
- **Moat asserted, not measured.** Calling a brand a moat without an ROIC-above-WACC spread lets you forecast excess returns that competition will erode.
- **Share in a shrinking market.** Rising share of a declining market can still mean falling revenue; always read share and market growth together.
- **Peer set drift.** Benchmarking against differently-structured businesses (a services firm vs a software firm) makes the company look artificially good or bad on margins.
- **Static five forces.** Scoring the industry today and forecasting as if it is frozen misses entrants and substitutes that the model's out-years must anticipate.
- **Qualitative dead-end.** Producing a narrative that never becomes a number leaves the model's assumptions unsupported; every finding must map to a driver.

## Output format
```
Company: <name> | Segment: <..> | Horizon: <..>
Market: TAM <..> | SAM <..> | SOM <..> | Share <..>% (trend <+/->)

Five forces: | Force | Level | Evidence |
Rivalry / Entrants / Supplier power / Buyer power / Substitutes
=> Industry attractiveness: <low/med/high>

Moat: source <..> | ROIC <..>% vs WACC <..>% | spread <..> pts | verdict <proven/unproven>
Unit economics: contribution margin <..> | CAC <..> | LTV <..> | payback <..> mo | churn <..>%

KPI benchmark:
| KPI | Company | Peer med | Read |
| Revenue growth | ..% | ..% | .. |
| Gross margin | ..% | ..% | .. |
| EBITDA margin | ..% | ..% | .. |
| ROIC | ..% | ..% | .. |
| FCF conversion | ..% | ..% | .. |
| Rule of 40 | .. | .. | .. |

Drivers into model:
| Position finding | Model assumption | Value/path |
| <..>            | revenue growth   | ..% fading to ..% |
| <..>            | margin path      | ..% -> ..% |
| <..>            | capex/WC         | ..% of rev |
| <..>            | terminal/fade    | .. |
```

## Reference

### Porter's five forces checklist
Net the five into an attractiveness read; the more forces sit "high" against the company, the tighter the ceiling on sustainable margin and growth.

| Force | Raises it (bad for incumbent) | Lowers it (good) |
|---|---|---|
| Competitive rivalry | Many equal rivals, slow growth, high fixed cost, low differentiation | Few players, growing market, differentiated |
| Threat of new entrants | Low capital need, no scale/regulatory barrier, easy access to channel | High capital, network effects, licensing, brand |
| Supplier power | Concentrated suppliers, unique input, high switching cost | Many suppliers, commodity input, backward integration possible |
| Buyer power | Concentrated buyers, undifferentiated product, price transparency | Fragmented buyers, high switching cost, mission-critical |
| Substitutes | Cheap alternatives, low switching cost | No close substitute, high performance gap |

### KPI benchmark formulas
| KPI | Formula | Reads |
|---|---|---|
| Revenue growth | (Rev_t - Rev_t-1) / Rev_t-1 | Demand and share momentum |
| Gross margin | Gross profit / revenue | Pricing power and unit cost |
| EBITDA margin | EBITDA / revenue | Operating profitability pre-capital |
| EBIT margin | EBIT / revenue | Profitability incl. capital intensity |
| ROIC | NOPAT / invested capital | Return vs WACC; moat evidence |
| NOPAT | EBIT x (1 - tax rate) | After-tax operating profit |
| Invested capital | Debt + equity - cash (or net working capital + net PP&E) | Capital at work |
| Capital intensity | Capex / revenue | Reinvestment burden |
| FCF conversion | Free cash flow / EBITDA | How much profit becomes cash |
| Rule of 40 | Revenue growth % + EBITDA (or FCF) margin % | Growth/profit balance (>=40 healthy) |
| CAC payback | CAC / (monthly gross margin per customer) | Months to recover acquisition cost |
| LTV/CAC | Lifetime gross profit per customer / CAC | Efficiency of growth (>3x healthy) |

### Moat evidence tests
A moat is a claim about persistence of excess returns; require evidence, not adjectives.

| Moat source | Evidence test |
|---|---|
| Network effects | Value per user rises with user count; retention improves with scale |
| Switching costs | Low churn, high renewal, expansion revenue (net revenue retention >100%) |
| Cost advantage | Structurally lower unit cost sustained across the cycle |
| Intangibles/brand | Price premium vs substitutes that persists |
| Efficient scale | Market too small to profitably support a second entrant |
| Overall | ROIC > WACC by a durable spread over a full cycle |

### How position maps to model assumptions
| Competitive finding | Feeds | Modeling rule |
|---|---|---|
| SOM headroom + share trend | Revenue growth path | Fade toward market growth as share saturates |
| Five-forces pricing power | Gross/EBITDA margin | Strong forces cap margin expansion |
| Operating leverage evidence | Margin path | Expand margins only where scale evidence exists |
| Capital intensity | Capex, working capital | Tie capex % and WC days to peer norms |
| Moat durability | Fade period, terminal growth | Longer excess-return fade for proven moats; terminal g <= GDP |
| Downside competitive event | Bear case | Model entrant/share-loss as a distinct scenario |

### QC checks
- [ ] TAM reconciled top-down vs bottom-up within ~2x.
- [ ] Every five-forces score has a named piece of evidence.
- [ ] Market share read alongside market growth, not alone.
- [ ] Moat backed by an ROIC-vs-WACC spread, not an adjective.
- [ ] Peer set structurally comparable (same business model).
- [ ] Every qualitative finding maps to a specific numeric driver.
- [ ] At least one competitive-event stress carried into the downside case.
