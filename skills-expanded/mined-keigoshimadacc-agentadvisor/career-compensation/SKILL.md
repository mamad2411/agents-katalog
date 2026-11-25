# Skill: Career moves and compensation

Domain guidance for job-change, offer-comparison and compensation decisions.

## What a serious answer must contain

- **Total compensation decomposed and risk-adjusted.** Base, bonus (with realization
  history, not target), equity (with a stated valuation method), benefits, and pension
  or retirement matching. Private-company equity is not cash and must be discounted with
  a stated assumption.
- **Vesting and cliff mechanics.** State what the user forfeits by leaving early and what
  the effective annualized value is over the realistic tenure, not the grant headline.
- **Option value of the move, not just the salary delta.** Skills acquired, network,
  optionality on the next move. These are real and should be argued, not asserted.
- **The downside case.** Probability the role does not work out within 18 months, and
  what the user's position looks like then.

## Standard alternatives to consider

Stay and negotiate; stay and do nothing; take the offer; keep searching for a stated
period; and, where relevant, a lateral internal move.

## Source hierarchy for this domain

1. The written offer, plan documents, and the equity grant agreement.
2. Employer filings and funding records for equity valuation inputs.
3. Named compensation datasets with sample size and vintage.
4. Direct conversations with current or former employees, with date and role recorded.
5. Aggregated self-reported salary sites and forums. Directional only; self-reporting
   bias is severe and upward.

Recruiter statements and the company careers page are one source.

## Domain-specific traps

- **Headline equity value at the last round price.** Apply a discount and say what it is.
- **Comparing gross numbers across tax regimes or locations.** Normalize.
- **Ignoring the counterfactual raise.** The relevant comparison is the offer against
  where the current role goes in two years, not against today's salary.
- **Underweighting manager quality and team stability.** These predict experience better
  than company brand; if unknown, record as a high-materiality assumption.
- **Sunk tenure.** Time already served is not a reason to stay.

## Quantitative expectations

Build a multi-year total-compensation comparison with explicit equity valuation
assumptions and a probability-weighted downside. Sensitivity on equity value and tenure.
Code under `analysis/`.
