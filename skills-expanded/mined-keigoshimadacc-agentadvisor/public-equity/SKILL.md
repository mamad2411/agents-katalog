# Skill: Public equity and listed-security investing

Domain guidance for a listed-security decision. This tells you what competent analysis
of this asset class looks like. It does not tell you what to conclude.

## What a serious answer must contain

- **Valuation anchored to a mechanism, not a multiple alone.** A P/E or EV/EBITDA number
  is a starting point. State what has to be true about growth, margin and reinvestment
  for the multiple to be justified, then check whether those conditions are observable.
- **The base rate for the claim being made.** If the thesis assumes 30% revenue growth
  sustained for five years, say how often companies of that size and sector have done
  that historically. Extrapolating a recent growth rate without a base rate is the most
  common failure in this domain.
- **Position sizing and the loss case.** A directional call without a size and a maximum
  tolerable drawdown is not actionable. State the loss the user would have to accept.
- **Timing risk separate from thesis risk.** "Right but early" is a distinct failure mode
  from "wrong". Treat them separately.

## Standard alternatives to consider

Always include at least: do nothing / hold cash; the broad-market index equivalent;
a smaller position in the named security; and a delayed entry conditional on a stated
trigger. A recommendation that beats "buy the index" only on unquantified conviction is
not a recommendation.

## Source hierarchy for this domain

1. Primary filings: 10-K, 10-Q, 8-K, proxy statements, prospectuses. These are the only
   sources where the numbers carry legal liability.
2. Company investor relations material and earnings-call transcripts. Reliable for
   figures, biased in framing.
3. Regulator and exchange data: SEC EDGAR, central-bank and statistical-agency series.
4. Sell-side research and reputable financial press. Secondary; note the incentive.
5. Aggregator sites, forums, social media. Use for hypothesis generation only, never as
   the sole support for a numeric claim.

When several outlets report one company statement, that is **one** source. Record them
under a single `independence_group`.

## Domain-specific traps

- **Consensus-already-priced.** If a fact is widely known, it is likely reflected in the
  price. Ask what the market is getting wrong and why, and record that as an assumption.
- **Survivorship in the comparison set.** Comparable-company sets built from today's
  index members exclude the failures.
- **Cyclical peak earnings.** A low multiple on peak-cycle earnings is expensive.
- **Concentration disguised as diversification.** Several positions with one macro driver
  are one position.
- **Stale price data.** Any price or market-cap figure older than a few days should be
  flagged with its as-of date.

## Quantitative expectations

Sensitivity analysis must vary at least: growth rate, terminal margin, discount rate and
exit multiple. Report the output range, not a point estimate. Any number in prose must
come from executed code under the case's `analysis/` directory.

## Regulatory boundary

This is analysis for a single private user, not investment advice, and the system never
executes a transaction.
