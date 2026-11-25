---
name: pe-deal-screening
version: 1.0.0
description: Run a fast, structured go/no-go screen of a single private-equity opportunity against the fund's investment criteria, scoring it across weighted dimensions to a pursue / pass / park decision with the rationale.
author: matrixx0070
tags: [deal-screening, go-no-go, investment-criteria, scoring-rubric, deal-triage, private-equity]
capabilities: []
---

## When to use

Use this when a specific opportunity has landed — a teaser, a CIM, a banker call, a proprietary intro — and the fund needs a quick, disciplined verdict on whether to spend real diligence time on it. Reach for it to triage inbound flow, to impose consistency across a deal team so screens are comparable, and to kill weak deals early before they burn analyst weeks. It is the first quality gate after sourcing and before diligence. The output is a one-page screen: a weighted score across the fund's criteria, the two or three swing factors, and a clear **pursue / pass / park** recommendation with the reasoning and the open questions that would change the answer.

**Not for:** filling the top of the funnel or deciding where deals should come from (use pe-deal-sourcing — screening judges one item the funnel already produced); running the full diligence workstream once you decide to pursue (use pe-dd-checklist); preparing management-meeting questions (use pe-dd-meeting-prep); writing the IC memo that formally proposes the investment (use pe-ic-memo — the screen precedes and feeds it); building the full returns model (use pe-returns-analysis — a screen uses only a rough returns sketch); deep-diving unit economics (use pe-unit-economics); assessing AI maturity (use pe-ai-readiness); building the value-creation plan (use pe-value-creation-plan); or monitoring a company after close (use pe-portfolio-monitoring).

## Method

1. Confirm the deal clears the fund's hard filters first. These are binary gates — sector mandate, check size / EBITDA band, geography, control vs minority, no excluded industries. **Decision:** if any hard filter fails, stop and pass immediately; do not score a deal outside the mandate no matter how attractive, because the fund cannot or should not do it.
2. Pull the minimum facts. From the teaser/CIM: revenue, EBITDA and margin, growth rate, business model, market position, ownership/reason for sale, and asking price or expected multiple. Note explicitly what is missing.
3. Score each screening dimension on a 1–5 scale (see Reference for the dimension set and anchors): market, business quality, financial profile, valuation/entry, deal dynamics/winnability, and fit with fund thesis and value-creation angle.
4. Apply weights and compute a weighted score. **Decision:** set the pursue threshold before scoring, not after — a common cut is pursue ≥ 3.5, park 2.8–3.5, pass < 2.8 — so the number disciplines the decision rather than the decision rationalizing the number.
5. Override on deal-breakers and swing factors. A single 1 on a critical dimension (e.g. a structurally declining market, or an un-winnable competitive auction) can override a decent average. Name the two or three factors actually driving the verdict.
6. Sketch — do not model — the return. A back-of-envelope: plausible entry multiple, a base-case exit multiple and EBITDA growth, rough leverage, and whether that clears the fund's return hurdle. If the rough case can't clear the hurdle, the deal fails regardless of qualitative appeal.
7. Write the verdict: pursue / pass / park, the rationale, the swing factors, and the specific open questions whose answers would move a "park" to a "pursue." Keep it to one page; screening's value is speed and consistency.

## Example

A generalist mid-market fund receives a teaser for a regional industrial-parts distributor: $60M revenue, $7M EBITDA (11.7% margin), ~4% growth, family-owned, seller retiring, guided at ~7x ($49M EV). Hard filters pass (industrials in mandate, EBITDA in the $5–15M band, control deal, US). Scoring: market 3 (stable, low-growth, fragmented), business quality 3 (sticky customers but thin margins and customer concentration flagged), financial profile 3 (steady cash conversion, modest growth), valuation 4 (7x is reasonable for the quality), deal dynamics 4 (proprietary, retiring owner, limited competition), thesis fit 4 (a buy-and-build distribution platform the fund has done before). Weighted score ≈ 3.5. Rough returns: enter 7x, exit 8x on $10M EBITDA in 5 years with 50% leverage → roughly 2.5–3x MOIC, clearing the hurdle if the buy-and-build works. Swing factors: customer concentration and whether add-on targets exist regionally. Verdict: **pursue**, conditional on confirming top-customer concentration under 20% and mapping at least three add-on candidates in early diligence.

## Pitfalls

- **Scoring a deal outside the mandate.** Enthusiasm for a "great business" that fails a hard filter wastes the whole team's time and, if pursued, strains the fund's strategy and LP expectations. Gate on hard filters before you ever open the scorecard.
- **Anchoring on EBITDA and ignoring quality of earnings.** Headline EBITDA in a teaser is seller-adjusted and often flattering. Treat it as a claim, not a fact; a strong screen flags add-backs, one-offs, and margin trajectory as questions rather than accepting the number.
- **Averaging away a deal-breaker.** A weighted average can hide a fatal 1 — a dying market, a customer at 60% of revenue, an un-winnable auction. Let critical-dimension floors override the average.
- **Setting the threshold after seeing the score.** If the cut line moves to fit the deal you already like, the rubric is theater. Fix pursue/park/pass thresholds before scoring.
- **Turning a screen into diligence.** The screen's job is a fast, consistent triage decision, not to answer every question. Over-investing in a screen defeats its purpose — capture the open questions and move the decision, don't resolve them here.

## Output format

```
# Deal Screen — <target> — <date> — <analyst>

## Snapshot
Sector <...> | Revenue <$> | EBITDA <$> (<margin>%) | Growth <%> | Ask <x / $EV>
Ownership / reason for sale: <...>   Source / channel: <...>

## Hard filters (all must pass)
[ ] Sector in mandate  [ ] Size in band  [ ] Geography  [ ] Control type  [ ] Not excluded

## Scorecard
| Dimension | Weight | Score (1-5) | Weighted | Note |
| Market attractiveness | 0.15 | | | |
| Business quality / moat | 0.20 | | | |
| Financial profile | 0.20 | | | |
| Valuation / entry | 0.15 | | | |
| Deal dynamics / winnability | 0.10 | | | |
| Thesis fit / value-creation angle | 0.20 | | | |
| **Weighted total** | 1.00 | | **<x.x>** | |

## Rough return sketch
Entry <x> → Exit <x> on <$EBITDA> in <n> yrs, <leverage> → ~<MOIC>x / <IRR>%  | Hurdle cleared? Y/N

## Verdict: PURSUE | PASS | PARK
Swing factors: <2-3>
Open questions that would change the answer: <...>
```

## Reference

Screening is deliberate triage: enough rigor to be consistent and defensible, little enough to be done in an hour. The material below reflects standard fund practice.

### Hard filters vs scored dimensions

Two different logics. **Hard filters** are binary and mandate-defining — fail one and the deal is out regardless of quality. **Scored dimensions** are matters of degree where a weighted view produces a comparable number across deals.

| Hard filters (binary gate) | Scored dimensions (1–5, weighted) |
|----------------------------|-----------------------------------|
| In-sector / in-mandate | Market attractiveness |
| Check size / EBITDA in band | Business quality & moat |
| Target geography | Financial profile |
| Control vs minority as mandated | Valuation / entry |
| Not an excluded industry (e.g. ESG-restricted) | Deal dynamics / winnability |
| Fund has capital & capacity | Thesis fit / value-creation angle |

### Screening dimensions and score anchors

| Dimension | 1 (poor) | 3 (acceptable) | 5 (excellent) |
|-----------|----------|----------------|----------------|
| **Market attractiveness** | Declining, structurally challenged | Stable, low-growth, fragmented | Large, growing, favorable tailwind |
| **Business quality / moat** | Commoditized, no differentiation | Some stickiness, moderate concentration | Strong moat, recurring revenue, diversified |
| **Financial profile** | Weak margins, poor cash conversion, erratic | Steady margins, modest growth, decent cash | High-margin, high-growth, strong FCF conversion |
| **Valuation / entry** | Expensive vs quality; auction bid up | Fair multiple for the quality | Attractive entry, proprietary discount |
| **Deal dynamics / winnability** | Broad auction, no angle to win | Limited process, some edge | Proprietary, motivated seller, clear angle |
| **Thesis fit / VC angle** | Off-thesis, no clear lever | Adjacent, generic levers | On-thesis, specific playbook & operating edge |

### Weighting and the decision rule

Weights encode the fund's philosophy: a buy-and-build fund weights thesis fit and market fragmentation; a value fund weights valuation and financial profile. A common default set is Business quality 20 / Financial profile 20 / Thesis fit 20 / Market 15 / Valuation 15 / Deal dynamics 10.

Set thresholds **before** scoring:

| Weighted score | Decision | Meaning |
|----------------|----------|---------|
| ≥ 3.5 | **Pursue** | Warrants diligence time now |
| 2.8 – 3.5 | **Park** | Interesting but needs a specific question answered to advance |
| < 2.8 | **Pass** | Not worth diligence resources |

Overlay critical-dimension floors: a 1 on market, business quality, or winnability can override an otherwise-passing average.

### The rough return sketch (why a screen still needs numbers)

A qualitative screen that never touches returns will pursue quality businesses at prices that can't produce fund-level returns. The one-line sketch — entry multiple, base-case exit multiple × EBITDA growth, rough leverage → MOIC/IRR vs hurdle — is the cheapest way to catch an over-priced good business early. The full model (entry/exit bridge, leverage schedule, value-creation waterfall) belongs to returns analysis, not the screen.

### Screen → IC memo

A screen that reaches "pursue" becomes the seed of the IC memo: its scorecard rationale, swing factors, and open questions map directly onto the memo's investment thesis, key risks, and diligence plan. Keeping the screen disciplined and written makes the later memo faster and keeps a paper trail of why the fund chose to spend diligence dollars.
