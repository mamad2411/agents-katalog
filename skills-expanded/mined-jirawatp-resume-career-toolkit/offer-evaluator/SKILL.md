---
name: Offer Evaluator
description: Compare multiple job offers using total compensation analysis and weighted decision criteria. Use this skill when someone has more than one job offer and needs to decide, or wants to evaluate a single offer against market benchmarks. Trigger for "compare offers", "which job should I take", "offer comparison", "deciding between jobs", "evaluate this offer", or any request to weigh multiple opportunities against each other.
---

# Offer Evaluator

Make a data-informed decision between competing job offers.

## Total Compensation Calculation

For each offer, compute:

```
YEAR 1 TOTAL
Base salary: $X
Signing bonus: $X (non-recurring)
Target bonus: X% of base = $X
Equity: total grant / vesting years = $X/year
401k match: X% of base up to limit = $X
Health insurance: employer portion = ~$X
Other perks: (PTO value, remote savings, dev budget) = ~$X
TOTAL: $X

ONGOING TOTAL (exclude signing bonus)
$X
```

## Non-Monetary Scoring

Rate each offer 1-10 on these dimensions:

- **Career growth:** Learning opportunity, brand value, promotion path, scope
- **Work-life:** Expected hours, flexibility, commute, PTO culture
- **Team quality:** Manager, peers, culture, team health
- **Stability:** Company financial health, funding, market position, layoff risk

## Weighted Decision

Assign weights based on what matters most to you (must total 100%):

```
Compensation: X%
Career growth: X%
Work-life: X%
Team quality: X%
Stability: X%
```

Multiply each score by its weight and sum. The highest weighted score is the analytical recommendation.

## Gut Check Questions

After the math, ask:
- Which offer would I regret not taking?
- Which Monday morning sounds more appealing?
- Which role will I be proudest of in 3 years?
- Which failure scenario is more tolerable?

If the gut and the math disagree, dig into why. The disagreement itself is informative.

## Output Format

```
OFFER COMPARISON

                    Offer A         Offer B
Base                $X              $X
Year 1 Total        $X              $X
Ongoing Total       $X              $X

Career Growth       X/10            X/10
Work-Life           X/10            X/10
Team Quality        X/10            X/10
Stability           X/10            X/10

Weighted Score      X.XX            X.XX

RECOMMENDATION: [Offer A/B] based on [reasoning]
THINGS TO CLARIFY BEFORE DECIDING: [list]
NEGOTIATION OPPORTUNITIES: [list]
```
