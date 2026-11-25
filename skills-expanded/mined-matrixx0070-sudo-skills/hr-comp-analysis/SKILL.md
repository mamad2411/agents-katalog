---
name: hr-comp-analysis
version: 1.0.0
description: Benchmark a role's pay, place it in a band by level/geo/function, and model base/bonus/equity trade-offs with sourced numbers.
author: matrixx0070
tags: [compensation, benchmarking, equity, pay-bands, total-rewards, compa-ratio]
capabilities: []
---

## When to use

Reach for this when you are sizing an offer, resolving a pay-equity question, setting or auditing a band for a role, or deciding a merit/promotion increase. Ground every number in a named source plus the role's level, location, and function.

**Not for:** drafting the offer letter itself (use hr-draft-offer), broad headcount/budget planning (use hr-org-planning), or workforce metrics reporting (use hr-people-report).

## Method

1. **Define the role precisely** — title, job family, level (IC or manager), primary geo tier, and remote policy. These drive every comparison.
2. **Gather benchmarks** — cite sources (survey data, competing offers, published ranges) with percentiles (25th/50th/75th). Decision point: if data is thin, self-reported, or older than ~12 months, widen your range and lower confidence instead of forcing a point estimate.
3. **Set the band** — pick a target percentile per your comp philosophy, then define min / midpoint / max. Compute compa-ratio = actual ÷ midpoint.
4. **Place the candidate** — map experience and skills to a point in the band. Decision point: if they land below min or above max, state why and whether the band or the placement is wrong.
5. **Model total comp** — break out base, target bonus (% and $), equity (grant value, vesting, strike/FMV if options), and benefits. Show year-1 vs. steady-state.
6. **Check equity** — compare against peers at the same level/geo. Any gap over a few percent needs a documented justification or a correction plan.

State assumptions and confidence explicitly. Never present a single number as fact when the underlying data is a range.

## Example

Senior Backend Engineer (IC, L5), Austin (Tier 2), remote-eligible. Survey 50th = $185k base; you target 60th → ~$195k. Band: min $170k / mid $195k / max $225k. Candidate has 8 yrs, strong distributed-systems signal → place at $205k (compa-ratio 1.05). Total comp year-1: $205k base + 15% target bonus ($30.75k) + $400k RSU over 4yr ($100k/yr) = ~$335k; steady-state ~$336k. Peer check: two L5 peers at $200k/$208k — placement is equitable.

## Pitfalls

- Benchmarking by title alone — a "Senior Engineer" at two firms can be two levels apart. Match on scope, not label.
- Comparing across geos without adjusting for the location tier or the company's remote-pay policy.
- Presenting the 50th percentile as "the market rate" and hiding the spread.
- Modeling equity at grant value without noting vesting schedule, cliff, or dilution/strike reality.

## Output format

```
Role: <title> | Level: <L#> | Geo: <tier> | Source + date: <...>
Market table:
  pctile | base | bonus | equity | total
  25th   | ...  | ...   | ...    | ...
  50th   | ...  | ...   | ...    | ...
  75th   | ...  | ...   | ...    | ...
Recommended band: min <$> / mid <$> / max <$> | target compa-ratio <x>
Placement: <$> at compa-ratio <x> — rationale: <...>
Total-comp model: year-1 <$> | steady-state <$>
Risks / equity flags / assumptions: <...>
```

## Reference

### Compa-ratio bands — how to read and place

Compa-ratio = actual salary ÷ band midpoint. The midpoint is your target-market rate for a fully-competent performer at that level. Use these bands to interpret any number:

| Compa-ratio | Zone | What it means | Typical action |
|---|---|---|---|
| < 0.80 | Below band | Underpaid vs. market, or misleveled high | Correct upward or re-level; retention risk |
| 0.80–0.90 | Lower third | New in role, still ramping, or recently promoted | Fine short-term; plan growth to mid |
| 0.90–1.10 | **Mid / control zone** | Solid, fully-competent performer | Normal merit; most of the org sits here |
| 1.10–1.20 | Upper third | Consistently exceeds, deep expertise | Slow base growth; lean on bonus/equity |
| > 1.20 | Above band | Topped out, or misleveled low | Freeze base or promote to next band |

Rules of thumb: a healthy population clusters 0.95–1.05 with a group-average compa-ratio near 1.00. A team averaging 1.15+ is likely misleveled or the band is stale; averaging 0.85 signals systemic underpayment and attrition risk. New hires typically enter 0.90–1.00; reserve 1.05+ entry for candidates whose scope genuinely exceeds the level.

### Band geometry

Bands are usually built as ±15–20% around the midpoint (min = mid × 0.85, max = mid × 1.15 for a ±15% band; wider for senior/exec). Consecutive levels overlap ~20–40% — an L4 max should sit near or above an L5 min, which is why a strong L4 can out-earn a new L5. Range spread (max−min ÷ min) is typically 30–40% for ICs, widening to 50–70% for director+ where individual impact varies more.

### Market-percentile guidance

Pick a target percentile as an explicit comp-philosophy decision, not per-candidate:

- **P50 (median)** — "pay at market." Default for most companies; sustainable, defensible.
- **P60–P65** — "slightly above market." Common in competitive talent markets (senior eng, ML, security).
- **P75** — "lead the market." Used for critical/scarce roles or a deliberate high-bar culture; expensive, hard to sustain org-wide.
- **P25–P40** — "lag the market," usually paired with strong equity or mission pull; high attrition risk if equity underdelivers.

When placing against survey data, weight sources by recency and match quality. Age survey data forward ~3–4% per year if it is >6 months old. Prefer aged, well-matched data over fresh, poorly-matched data.

### Geo differentials

Common tiering approach (relative to a Tier-1 hub like SF/NYC = 100%):

| Tier | Example markets | Typical factor |
|---|---|---|
| Tier 1 | SF Bay, NYC, Seattle | 100% |
| Tier 2 | Austin, Denver, Boston, London | 85–95% |
| Tier 3 | most of US midwest/south, secondary EU | 75–85% |
| Tier 4 | low-cost domestic / offshore hubs | 55–75% |

State the company's remote-pay policy explicitly: national-single-band vs. geo-adjusted vs. hub-anchored. Do not silently mix policies in one comparison.

### Total-comp mechanics

- **Target cash** = base + target bonus. Compare offers on target cash, not base alone.
- **Bonus** — express as % of base and $; note whether it is guaranteed year-1, prorated for start date, and individual vs. company-funded.
- **Equity** — always state grant value, vesting schedule (commonly 4-year, 1-year cliff, then monthly/quarterly), and refresh expectation. For options, annual value ≈ (FMV − strike) × shares vesting that year; note strike, 409A/FMV date, and dilution. RSU annual value = grant ÷ vest years (public) or last-round PPS × shares (private, illiquid — discount heavily).
- **Steady-state vs. year-1** — sign-on and cliff distort year-1. Show both so the candidate and finance see the run-rate.

### Pay-equity check

Regress or group-compare pay within the same level + geo + function; anything unexplained beyond ~5% needs a documented reason (tenure, performance, hot-skill premium) or a correction. Watch for cohort effects (people hired in a hot market sit higher) and manager-discretion drift. Never justify a gap by a protected characteristic.

### Quick formulas

```
compa-ratio      = salary ÷ midpoint
range penetration = (salary − min) ÷ (max − min)      # 0%=min, 100%=max
midpoint          = min ÷ (1 − spread/2)  (approx)
range spread      = (max − min) ÷ min
merit budget draw = Σ(increase $) ÷ Σ(current base)   # keep ≤ approved %
aged market rate  = survey rate × (1 + annual_growth)^years_old
```

### Merit / promotion sizing

Merit increases are typically 2–5% for meets-expectations, tapering as compa-ratio rises (someone at 1.15 gets less %-wise than someone at 0.92, to pull the group toward 1.00). Promotion increases usually land 8–15% and should place the person near the new band's min-to-lower-third, not its midpoint. Always confirm the post-increase compa-ratio stays inside the target band before committing.
