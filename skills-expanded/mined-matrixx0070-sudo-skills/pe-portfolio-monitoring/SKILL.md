---
name: pe-portfolio-monitoring
version: 1.0.0
description: Track a portfolio company post-close — build the monthly/quarterly KPI pack, covenant compliance (leverage and interest cover), variance against budget and the value-creation plan, early-warning indicators, and the board-reporting cadence, rolled up to a portfolio-level view.
author: matrixx0070
tags: [portfolio-monitoring, kpis, covenants, board-reporting, variance-analysis, early-warning, roll-up]
capabilities: []
---

## When to use

Use this after close, when you own the company and need a running view of whether it is on plan — the KPIs to report each month and quarter, whether it is inside its debt covenants, how actuals compare to budget and to the value-creation plan, what early-warning signs to watch, and how it all rolls up to a board pack and a portfolio-level dashboard. Reach for it when standing up reporting in the first 100 days, running the monthly/quarterly cycle, preparing a board meeting, or building the fund-level portfolio roll-up for the investment team and LPs. The output is a monitoring system: a KPI pack, a covenant tracker, variance analysis, an early-warning panel, and a portfolio roll-up.

**Not for:** assessing AI maturity or an AI opportunity (use pe-ai-readiness), pre-close diligence workstreams (use pe-dd-checklist), diligence-meeting prep (use pe-dd-meeting-prep), the go/no-go screen (use pe-deal-screening), origination and pipeline (use pe-deal-sourcing), the committee memo (use pe-ic-memo), modeling MOIC/IRR and the returns bridge (use pe-returns-analysis), defining the value-creation initiatives that this skill then tracks (use pe-value-creation-plan — it sets the KPIs and targets; this monitors them), or deep-diving LTV/CAC and cohort economics behind a commercial KPI (use pe-unit-economics).

## Method

1. Define the KPI set from the VCP and the deal thesis. Pull the KPIs, baselines, and targets the value-creation plan established, plus the standard financial and operational metrics, and the ones the debt documents require. **Decision:** cap the board-level KPI set to the ~10–15 metrics that actually signal thesis progress and risk — a 60-line pack no one reads is worse than a focused one.
2. Set the cadence. Establish monthly management reporting (flash P&L, cash, KPIs) and a quarterly board pack (full financials, VCP progress, covenant certificate, forecast reforecast). **Decision:** decide the reporting depth by situation — a company off-plan or near a covenant moves to a tighter cadence (weekly cash, monthly board touchpoints) until it stabilizes.
3. Build the KPI pack. Lay out each KPI with actual, budget, prior period, and VCP target, plus trend, so the reader sees performance and direction at a glance.
4. Track covenants. Compute the covenant ratios each period against their thresholds — typically net leverage (net debt / EBITDA) and interest cover (EBITDA / interest), sometimes fixed-charge cover and a capex or minimum-liquidity limit — with headroom shown. **Decision:** define a warning band (e.g. <20% headroom) that triggers escalation before an actual breach, and confirm the exact covenant definitions from the credit agreement, since add-backs and EBITDA definitions vary.
5. Run variance analysis. Compare actuals to both budget and the VCP, decompose the gap into drivers (volume, price, mix, cost), and separate timing from structural misses.
6. Maintain early-warning indicators. Watch leading signals — cash-runway/liquidity trend, covenant-headroom trend, order book/pipeline, churn, DSO creep, margin compression, key-person and customer-concentration risk — and flag deterioration before it hits the P&L.
7. Reforecast and act. Update the full-year forecast when variance is structural, log the management action per off-track item, and confirm the VCP owner and date.
8. Roll up to portfolio level. Aggregate each company's status (on/ahead/behind plan, covenant status, valuation mark, key risks) into a fund-level dashboard for the investment team and LP reporting.

## Example

A sponsor monitors a $50m-EBITDA services platform against a VCP targeting $80m by exit. The monthly pack shows revenue 4% below budget but EBITDA in line — a mix shift toward lower-margin work, flagged as structural, not timing, and reforecast down 2% for the year. The covenant tracker computes net leverage at 4.6x against a 5.5x springing covenant (16% headroom → inside the warning band, escalated to the board) and interest cover at 3.1x against a 2.5x floor (comfortable). Variance analysis attributes the revenue miss to slower new-segment ramp (a VCP structural initiative running late), while the pricing quick win beat target and is holding EBITDA. Early-warning panel flags DSO creeping from 45 to 58 days (a cash and covenant risk given the leverage headroom) and rising concentration as the top customer grows. The COO owns a receivables-collection push with a 30-day target; the new-segment VP owns a revised ramp plan. At the portfolio level, the company is marked "behind plan / covenant watch," one of two amber names in an otherwise green fund dashboard.

## Pitfalls

- **A pack no one reads.** Sixty metrics with no hierarchy bury the two that matter. Curate to the ~10–15 KPIs that signal thesis progress and risk, lead with covenant headroom and cash, and put detail in an appendix.
- **Covenants computed on the wrong definition.** Credit agreements define EBITDA, net debt, and add-backs specifically; monitoring against a generic definition can miss a real breach or manufacture a false alarm. Lift the exact definitions and the test dates from the documents and reconcile every add-back.
- **Variance vs budget only.** Budget is last year's guess; the VCP is the return thesis. Track actuals against both, and separate timing misses from structural ones — the latter demand a reforecast and an owned action, not a footnote.
- **Lagging, not leading.** By the time a covenant breaches or cash runs short it is too late to act cheaply. Maintain early-warning indicators (headroom trend, runway, DSO, pipeline, churn) with a warning band that escalates before the P&L confirms the problem.
- **No action loop.** A pack that reports variance without a named owner, action, and date is a status report, not monitoring. Every off-track item needs an owner and a date, tied back to the VCP.

## Output format

```
# Portfolio Monitoring — <company> — <period> — v<n>
Status: on plan | ahead | behind | covenant watch
Cadence: monthly flash | quarterly board pack

## KPI pack
| KPI | Actual | Budget | Prior | VCP target | Var vs budget | Var vs VCP | Trend |
|-----|--------|--------|-------|------------|---------------|------------|-------|

## Covenant compliance
| Covenant | Definition (per agreement) | Threshold | Actual | Headroom | Status |
|----------|----------------------------|-----------|--------|----------|--------|
| Net leverage (net debt/EBITDA) |  | ≤ x |  |  | ok/warning/breach |
| Interest cover (EBITDA/interest) |  | ≥ x |  |  |  |

## Variance analysis
| Line | Actual vs budget | Driver (vol/price/mix/cost) | Timing or structural | Reforecast |
|------|------------------|-----------------------------|----------------------|-----------|

## Early-warning panel
- Liquidity / runway: <trend>   Covenant headroom trend: <...>   DSO: <...>
- Pipeline / order book: <...>   Churn: <...>   Concentration / key-person: <...>

## Actions
| Issue | Owner | Action | Target date | VCP link |
|-------|-------|--------|-------------|----------|

## Portfolio roll-up (fund level)
| Company | Status | Net leverage | Covenant | Rev/EBITDA vs plan | Mark | Key risk |
|---------|--------|--------------|----------|--------------------|------|----------|
```

## Reference

Substantive overview of post-close portfolio monitoring. Metrics and thresholds are illustrative; covenant definitions and test dates must be taken from the specific credit agreement, and reporting rights from the shareholders' agreement.

### The reporting cadence

| Cadence | Contents | Audience |
|---------|----------|----------|
| Monthly (flash) | P&L vs budget, cash/liquidity, core KPIs, covenant estimate | Deal team, operating partners |
| Quarterly (board pack) | Full financials, VCP progress, covenant certificate, reforecast, risks | Board |
| Annual | Audited accounts, valuation/mark, strategy review, exit-readiness | Board, LPs |
| Ad hoc / heightened | Weekly cash, tighter touchpoints for off-plan or near-covenant names | Deal team, board |

Companies performing to plan sit on the standard cadence; underperformers or near-covenant situations escalate to a tighter cadence until they stabilize.

### The KPI pack

A focused pack blends financial, operational, and VCP-specific metrics, each shown against actual / budget / prior / VCP target:

| Category | Typical KPIs |
|----------|-------------|
| Financial | Revenue, gross margin, EBITDA, EBITDA margin, free cash flow, net debt |
| Cash & liquidity | Cash balance, available facility, runway, DSO/DPO/inventory |
| Operational | Volume, price realization, utilization, churn/retention, pipeline/order book, headcount |
| VCP-specific | The named value-creation initiatives' own KPIs and milestones |

Lead with covenant headroom and cash, keep the board view to ~10–15 lines, and push granularity to an appendix.

### Covenant tracking

Leveraged deals carry maintenance and/or incurrence covenants tested at defined dates. Monitor the ratios each period with headroom, using the exact definitions from the credit agreement:

| Covenant | Formula | Typical direction |
|----------|---------|-------------------|
| Net leverage | Net debt / EBITDA | ≤ threshold (e.g. ≤ 5.5x, often stepping down over time) |
| Interest cover | EBITDA / interest expense | ≥ threshold (e.g. ≥ 2.5x) |
| Fixed-charge cover | (EBITDA − capex) / (interest + scheduled debt service) | ≥ threshold |
| Capex limit / minimum liquidity | Capex ≤ limit; cash ≥ floor | as specified |

Headroom = distance from threshold, in ratio turns and in EBITDA/cash terms. Set a warning band (e.g. <20% headroom) that escalates to the board before a breach, and remember that covenant EBITDA usually includes contractually specified add-backs that differ from reported EBITDA — compute on the agreement's definition, not a generic one. A breach typically triggers cure rights, lender negotiation, or in the worst case default, so leading visibility is essential.

### Variance analysis

Compare actuals against two baselines and decompose the gap:

- vs budget — the operating plan for the year.
- vs the VCP — the value-creation thesis that underwrites the return.

Decompose material variances into volume, price, mix, and cost drivers, and classify each as timing (will reverse) or structural (won't — requires a reforecast and an owned action). A miss against budget that is still on the VCP is different from one that puts the return thesis at risk; the distinction should be explicit.

### Early-warning indicators

Leading signals surface problems before they reach the P&L or a covenant test:

| Indicator | What it warns of |
|-----------|------------------|
| Liquidity / runway trend | Cash crunch, need for facility or sponsor support |
| Covenant-headroom trend | Approaching breach even if currently compliant |
| Pipeline / order book | Forward revenue softness |
| Churn / retention | Deteriorating commercial quality and future revenue |
| DSO / working-capital creep | Cash tied up; strain on covenant headroom |
| Margin compression | Cost or pricing/mix problem eroding EBITDA |
| Customer concentration / key-person | Fragility of the earnings base |

### VCP tracking and the portfolio roll-up

Monitoring closes the loop the value-creation plan opens: each VCP initiative's KPIs and milestones are tracked against target, and off-track items get an owner and a date. At the fund level, individual company statuses aggregate into a portfolio dashboard — status (ahead / on / behind plan / covenant watch), leverage and covenant standing, revenue/EBITDA vs plan, valuation mark, and key risks — giving the investment team and LPs a single view of portfolio health and where attention is needed.
