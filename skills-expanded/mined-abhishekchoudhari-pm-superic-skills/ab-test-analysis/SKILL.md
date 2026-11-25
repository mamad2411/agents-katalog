---
name: ab-test-analysis
description: "Analyze A/B test results with statistical significance, practical significance, sample size validation, sequential vs fixed-horizon guidance, and ship/extend/stop recommendations. Use when evaluating experiment results, checking if a test reached significance, interpreting split test data, deciding whether to ship a variant, or validating experiment setup."
---

# A/B Test Analysis

Evaluate A/B test results with statistical rigor and translate findings into clear, defensible product decisions.

---

## Context

You are analyzing A/B test results for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, or analytics exports), read and analyze them directly. Generate Python scripts for statistical calculations when needed.

---

## Part 1: Sample Size and MDE — Before the Test Runs

The most common A/B testing mistake is starting a test without knowing how much traffic is needed. Answer these questions before collecting data.

### Minimum Detectable Effect (MDE) selection

MDE is the smallest lift you care about. Choosing it correctly determines whether your test is practical.

| Test type | Typical MDE | Rationale |
|---|---|---|
| Checkout conversion rate | 10-20% relative lift | Below 10% is often not worth engineering cost |
| Onboarding completion | 5-15% relative lift | Higher-traffic step, smaller MDE is feasible |
| Feature CTR | 15-25% relative lift | Usually lower traffic, must target larger effects |
| Email open rate | 5-10% relative lift | High volume, small MDE is achievable |
| Revenue per user | 5-10% relative lift | High variance metric, requires more traffic |

**Rule:** smaller MDE requires exponentially more sample. Cutting MDE in half quadruples the required sample size. If you cannot collect enough traffic for a 10% MDE in under 4 weeks, target a 15-20% MDE or do not run the test.

### Sample size formula

For a two-proportion test at 95% confidence (alpha = 0.05) and 80% power (beta = 0.20):

```
n = (Z_alpha/2 + Z_beta)^2 * 2 * p * (1-p) / MDE^2

Where:
  Z_alpha/2 = 1.96 (95% confidence)
  Z_beta = 0.84 (80% power)
  p = baseline conversion rate
  MDE = absolute difference you want to detect
```

**Worked example:** baseline conversion 8%, MDE = 10% relative = 0.8% absolute
- n per variant = (1.96 + 0.84)^2 * 2 * 0.08 * 0.92 / 0.008^2 = approximately 45,000

**Benchmarks:**
- Conversion rate tests at 95% confidence, 10% relative MDE: 50,000+ users per variant
- Conversion rate tests at 95% confidence, 20% relative MDE: 13,000+ users per variant
- Typical B2C experiment duration: 2-4 weeks to collect sufficient sample and cover weekly seasonality

---

## Part 2: Test Design Validation

Before reading any results, validate the test was run correctly.

### Checklist

1. **Sample ratio mismatch (SRM):** Was the actual traffic split within 5% of the intended split? A 50/50 split producing 52/48 is an SRM flag — the randomization may be broken. Run a chi-squared test on the user counts alone.

2. **Test duration:** Did the test run for at least one full 7-day business cycle? Tests shorter than 7 days may capture a day-of-week bias. Minimum recommended: 14 days for most B2C products.

3. **Novelty effect:** For UI changes, users may behave differently purely because something is new. If possible, check if the lift erodes after the first 3-4 days for new users vs existing users. Novelty effects typically wash out in 1-2 weeks.

4. **SUTVA (Stable Unit Treatment Value Assumption):** Each user's outcome must be independent of other users' treatment assignment. This is violated in social products (one user's variant affects their contacts), marketplace products (demand/supply interactions), and referral programs. If SUTVA is violated, standard A/B testing overestimates the true effect.

5. **Network interference:** In products with virality or sharing, treating one user can affect control users. Consider cluster-based randomization (randomize by network cluster, not individual user) for these products.

---

## Part 3: Sequential vs Fixed-Horizon Testing

Choose the right testing approach before collecting data.

| Approach | When to use | Key rule | Risk |
|---|---|---|---|
| Fixed-horizon | Accuracy is critical, traffic is predictable | Commit to a sample size upfront; read results only once | Inflated false positive rate if you peek |
| Sequential testing | Fast-moving products, need to stop early | Uses alpha-spending function to allow interim looks | Slightly less statistical power |
| Bayesian testing | When you want probability-of-being-best, not binary significance | Specify priors, interpret posterior | Requires more setup, harder to explain |

**Peeking problem:** Reading fixed-horizon results before the planned sample size is reached inflates your false positive rate. A test designed for p<0.05 becomes effectively p<0.15 if you check results 5 times and stop at the first significant result. Use sequential testing if you need to monitor actively.

---

## Part 4: Metric Selection

Every A/B test needs three metric categories defined before launch.

### Primary metric
The one metric that drives the go/no-go decision. Must be:
- Measurable at the user level
- Sensitive enough to move in the test window
- Directly connected to the product change

### Guardrail metrics
Metrics that must not regress. A variant can win on the primary metric but fail if:
- Revenue per user drops
- Core feature engagement drops
- Error rate or load time increases
- Support ticket volume rises

### Secondary metrics
Directional signals. These do not determine the decision but inform the interpretation. Include them to understand the mechanism of the effect.

---

## Part 5: Statistical and Practical Significance

Statistical significance (p<0.05) is not the same as practical significance. Both must be true for a result to be actionable.

### Statistical significance

- **p-value:** Probability of seeing a result this extreme if there is actually no effect. p<0.05 means less than 5% chance this is noise.
- **Confidence interval:** The 95% CI for the difference should not include zero to claim significance.
- **Two-tailed test:** Use by default unless you specified directional hypotheses before the test started.

### Practical significance

Ask: "Even if this is real, is it worth the engineering cost to ship it?"

| Test result | Ship? | Reasoning |
|---|---|---|
| Conversion rate +12%, p=0.02 | Yes | Statistically and practically significant |
| Conversion rate +0.3%, p=0.04 | No | Statistically significant but 0.3pp absolute is below engineering break-even |
| Conversion rate +8%, p=0.09 | Extend | Directionally meaningful, underpowered - need more data |
| Conversion rate +0.5%, p=0.60 | Drop | Neither significant nor meaningful |

**Engineering break-even heuristic:** If the feature requires 2 sprint weeks of engineering work, the lift should generate at least as much revenue as the engineer cost over the next 12 months. Calculate this before calling a small lift a win.

---

## Part 6: Segmentation and Simpson's Paradox

A test can show a positive result overall while being negative for a specific, important segment. This is Simpson's Paradox.

**Example:** A new checkout flow shows +5% conversion overall. But mobile users (60% of traffic) show -3% conversion and desktop users (40%) show +18% conversion. The overall positive is driven entirely by desktop — mobile is being harmed.

**Standard segmentation cuts to always run:**
1. Device type (mobile vs desktop vs tablet)
2. New vs returning users
3. Acquisition channel
4. User tenure bucket (day 1-7, day 8-30, 30+ days)
5. Geography (if the product varies by region)

Flag any segment where the direction of the result is opposite to the overall result. This is not a post-hoc rationalization — it is a data safety check.

---

## Part 7: Decision Framework

| Statistical significance | Practical significance | Guardrails | Decision |
|---|---|---|---|
| Yes (p<0.05) | Yes (lift > break-even) | No regression | Ship to 100% |
| Yes (p<0.05) | Yes | Regression in guardrail | Investigate and fix before shipping |
| Yes (p<0.05) | No (lift < break-even) | No regression | Deprioritize — real effect but not worth cost |
| No (p>0.05, positive trend) | Directional | N/A | Extend test (if still underpowered) or redesign hypothesis |
| No (p>0.05, flat) | No | N/A | Drop — no signal, move on |
| Yes (p<0.05, negative) | — | — | Do not ship — revert variant, investigate root cause |

---

## Part 8: Analysis Output Format

Produce the following when analyzing test results.

```
## A/B Test Results: [Test Name]

**Hypothesis:** [what was expected to happen and why]
**Variant:** [what was changed]
**Duration:** [X days]  |  **Sample:** [N control / M variant]
**Primary metric:** [metric name]
**Guardrail metrics:** [list]

### Statistical results

| Metric | Control | Variant | Absolute lift | Relative lift | p-value | 95% CI | Significant? |
|---|---|---|---|---|---|---|---|
| [Primary] | X% | Y% | +Z pp | +W% | 0.0X | [a, b] | Yes/No |
| [Guardrail 1] | ... | ... | ... | ... | ... | ... | ... |

### Sample size check
- Required sample (at planned MDE): [N]
- Actual sample: [M]
- Test powered? [Yes / No — if no, results are unreliable]

### Segmentation check
| Segment | Control | Variant | Lift | Consistent with overall? |
|---|---|---|---|---|
| Mobile | | | | |
| Desktop | | | | |
| New users | | | | |
| Returning users | | | | |

### Decision
**Recommendation:** [Ship / Extend / Deprioritize / Drop / Investigate]
**Reasoning:** [2-3 sentences]
**Next step:** [specific action with owner and timeline]
```

---

## Part 9: Common Mistakes Reference

| Mistake | Effect | Fix |
|---|---|---|
| Peeking at results before planned end date | False positive rate inflates from 5% to 15-30% | Use sequential testing or commit to a fixed end date |
| No pre-registration of hypothesis | Post-hoc analysis finds significance by chance | Write hypothesis and metrics before starting the test |
| Ignoring novelty effect | Overestimates long-term lift | Run for 2+ weeks, compare first-week vs second-week lift |
| Running without a guardrail | Ships variant that harms retention | Always define at least one guardrail before launch |
| Single-metric analysis | Missing regressions in other areas | Check 3-5 metrics minimum |
| Stopping at first significant result | False discovery | Honor the planned end date |

---

### Further Reading

- [A/B Testing 101 + Examples](https://www.productcompass.pm/p/ab-testing-101-for-pms)
- [Testing Product Ideas: The Ultimate Validation Experiments Library](https://www.productcompass.pm/p/the-ultimate-experiments-library)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
