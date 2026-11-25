# Skill: Build versus buy and vendor selection

Domain guidance for decisions between building software capability in-house, buying a
vendor product, or adopting an open-source base.

## What a serious answer must contain

- **Total cost of ownership over a stated horizon, both sides.** Build cost is not the
  initial engineering estimate: include maintenance, on-call, security patching, staff
  turnover and the opportunity cost of the engineers. Buy cost includes integration,
  data migration, per-seat growth, and the renewal-price trajectory.
- **Switching cost and lock-in, quantified.** State what it would cost to reverse the
  decision in two years. A cheap decision that is expensive to reverse is not cheap.
- **Whether this capability is differentiating.** Building commodity infrastructure is
  the classic error; buying the thing that is your actual product is the mirror error.
  Say which category this is and why.
- **Time to value.** A build that lands in nine months against a buy that lands in six
  weeks is a materially different decision even at equal cost.

## Standard alternatives to consider

Buy; build; adopt open source and self-host; do nothing and keep the current process;
and a staged approach that buys now with a defined migration trigger.

## Source hierarchy for this domain

1. Vendor contracts, SLAs, security documentation and published pricing.
2. The organization's own data: current spend, incident history, engineering velocity.
3. Independent evaluations and reference customers of comparable size.
4. Analyst reports and comparison matrices. Note who paid for them.
5. Vendor marketing, case studies and sales-engineer claims. Treat as claims.

A vendor's own case study, blog and sales deck are one source.

## Domain-specific traps

- **Underestimating build by the usual factor.** Engineering estimates for
  infrastructure work run low; state the multiplier you applied and why.
- **Ignoring the maintenance tail.** Most of build cost arrives after launch.
- **Pricing the pilot, not the steady state.** Check renewal terms and seat growth.
- **Feature-matrix theatre.** Long checklists favour whoever wrote the checklist. Weight
  by the small number of features that actually gate the workflow.
- **Assuming the team that builds it will still be there.** Key-person risk is real.

## Quantitative expectations

Produce a TCO model over at least three years for each alternative, with sensitivity on
engineering cost, headcount growth, seat growth and renewal uplift. Include the reversal
cost. Code under `analysis/`.
