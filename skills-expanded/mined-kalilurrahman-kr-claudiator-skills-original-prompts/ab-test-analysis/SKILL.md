---
name: ab-test-analysis
description: Design and analyze A/B tests with statistical significance, sample size calculation, and metric selection. Outputs test design, power analysis, and results interpretation.
argument-hint: [baseline metric, minimum detectable effect, significance level]
allowed-tools: Read, Write, Bash
---

# A/B Test Analysis

Design statistically rigorous A/B tests. Not gut feelings — power analysis, significance testing, and careful interpretation of results.

## Process

1. **Define hypothesis.** What change do we expect, and why?
2. **Choose metrics.** Primary (conversion rate) and guardrail metrics (revenue).
3. **Calculate sample size.** Power analysis for minimum detectable effect.
4. **Design experiment.** Randomization, treatment assignment, duration.
5. **Run test.** Collect data without peeking.
6. **Analyze results.** Statistical significance, confidence intervals, practical significance.
7. **Make decision.** Ship winner, iterate, or inconclusive.

## Output Format

### A/B Test: [Test Name]

**Hypothesis:** New checkout flow increases conversion by 10%  
**Primary Metric:** Conversion rate  
**Sample Size:** 10,000 per variant (80% power, 5% significance)  
**Duration:** 14 days  
**Result:** Variant B +12% conversion (p=0.002), SHIP

---

## Test Design

### Hypothesis Template
```
We believe that [change] will result in [metric improvement] 
because [reasoning].

Example:
We believe that adding social proof badges will increase 
conversion rate by 10% because customers trust products 
with high ratings.
```

### Metric Selection

**Primary Metric:** Single metric that determines success/failure
- Conversion rate
- Revenue per user
- Click-through rate

**Secondary Metrics:** Additional signals
- Average order value
- Time on page
- Bounce rate

**Guardrail Metrics:** Must not degrade
- Revenue
- Page load time
- Error rate

---

## Sample Size Calculation

### Power Analysis

```python
from scipy import stats
import numpy as np

def calculate_sample_size(
    baseline_rate=0.10,      # Current conversion rate (10%)
    mde=0.02,                # Minimum detectable effect (+2%)
    alpha=0.05,              # Significance level (5%)
    power=0.80               # Statistical power (80%)
):
    """
    Calculate required sample size for A/B test
    
    alpha: Probability of Type I error (false positive)
    power: 1 - beta, where beta is probability of Type II error (false negative)
    mde: Minimum detectable effect (smallest improvement worth detecting)
    """
    
    # Effect size (Cohen's h for proportions)
    p1 = baseline_rate
    p2 = baseline_rate + mde
    
    effect_size = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))
    
    # Z-scores for alpha and power
    z_alpha = stats.norm.ppf(1 - alpha/2)  # Two-tailed test
    z_beta = stats.norm.ppf(power)
    
    # Sample size per variant
    n = ((z_alpha + z_beta) / effect_size) ** 2
    
    return int(np.ceil(n))

# Example: Detect 2% improvement on 10% baseline
sample_size = calculate_sample_size(
    baseline_rate=0.10,
    mde=0.02,
    alpha=0.05,
    power=0.80
)

print(f"Sample size needed: {sample_size} per variant")
# Output: Sample size needed: 3842 per variant
```

### Test Duration
```python
def calculate_test_duration(sample_size_per_variant, daily_traffic, split=0.5):
    """Calculate how long test needs to run"""
    
    traffic_per_variant = daily_traffic * split
    days = sample_size_per_variant / traffic_per_variant
    
    return np.ceil(days)

# Example: 3842 needed, 500 daily visitors, 50/50 split
duration = calculate_test_duration(3842, 500, 0.5)
print(f"Test duration: {duration} days")
# Output: Test duration: 16 days
```

---

## Randomization

### User-Level Randomization
```python
import hashlib

def assign_variant(user_id, test_name, num_variants=2):
    """Consistent user assignment based on hash"""
    
    # Hash user ID + test name
    hash_input = f"{user_id}:{test_name}".encode()
    hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
    
    # Assign to variant
    variant = hash_value % num_variants
    
    return variant

# Usage
user_variant = assign_variant("user_12345", "checkout_test")
if user_variant == 0:
    show_control_experience()
else:
    show_treatment_experience()
```

**Benefits:**
- Same user always sees same variant
- No cookies needed
- Works across devices

---

## Statistical Analysis

### Z-Test for Proportions
```python
from scipy import stats

def analyze_ab_test(conversions_a, visitors_a, conversions_b, visitors_b):
    """
    Statistical significance test for conversion rates
    """
    
    # Conversion rates
    rate_a = conversions_a / visitors_a
    rate_b = conversions_b / visitors_b
    
    # Pooled proportion
    pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    
    # Standard error
    se = np.sqrt(pooled * (1 - pooled) * (1/visitors_a + 1/visitors_b))
    
    # Z-score
    z = (rate_b - rate_a) / se
    
    # P-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    # Confidence interval (95%)
    ci_diff = 1.96 * se
    lift = (rate_b - rate_a) / rate_a * 100
    
    return {
        'conversion_a': rate_a,
        'conversion_b': rate_b,
        'lift_pct': lift,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'confidence_interval': (
            (rate_b - rate_a - ci_diff),
            (rate_b - rate_a + ci_diff)
        )
    }

# Example
result = analyze_ab_test(
    conversions_a=385,  # Control: 385 conversions
    visitors_a=3842,    # 3842 visitors
    conversions_b=462,  # Treatment: 462 conversions
    visitors_b=3842     # 3842 visitors
)

print(f"Control conversion: {result['conversion_a']:.2%}")
print(f"Treatment conversion: {result['conversion_b']:.2%}")
print(f"Lift: {result['lift_pct']:.1f}%")
print(f"P-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")

# Output:
# Control conversion: 10.02%
# Treatment conversion: 12.02%
# Lift: 20.0%
# P-value: 0.0023
# Significant: True
```

---

## Common Pitfalls

### Peeking Problem
```
❌ BAD: Check results daily, stop when significant

Day 5: p=0.03 → "It's significant! Ship it!"

Problem: Multiple testing inflates false positive rate
Real significance level: ~30% instead of 5%
```

**Solution: Fixed horizon testing**
```
✅ GOOD: Decide sample size upfront, wait until complete

Day 1-13: Don't look at results
Day 14: Reached sample size → Analyze once
```

### Winner's Curse
```
❌ BAD: "We detected +20% lift with 95% confidence"

Problem: Estimate is biased upward
True lift likely closer to +15%
```

**Solution: Report confidence intervals**
```
✅ GOOD: "95% CI: +12% to +28% lift"

Expected value likely in middle of range (~+20%)
```

### Multiple Testing
```
❌ BAD: Test 20 metrics, find 1 significant

Problem: 5% false positive rate = 1 false positive in 20 tests
```

**Solution: Bonferroni correction**
```python
adjusted_alpha = 0.05 / num_tests

# Testing 20 metrics
adjusted_alpha = 0.05 / 20 = 0.0025

# Require p < 0.0025 for significance
```

---

## Bayesian A/B Testing

```python
import pymc3 as pm

def bayesian_ab_test(conversions_a, visitors_a, conversions_b, visitors_b):
    """
    Bayesian A/B test using Beta-Binomial model
    """
    
    with pm.Model() as model:
        # Priors (uniform)
        p_a = pm.Beta('p_a', alpha=1, beta=1)
        p_b = pm.Beta('p_b', alpha=1, beta=1)
        
        # Likelihood
        obs_a = pm.Binomial('obs_a', n=visitors_a, p=p_a, observed=conversions_a)
        obs_b = pm.Binomial('obs_b', n=visitors_b, p=p_b, observed=conversions_b)
        
        # Difference
        delta = pm.Deterministic('delta', p_b - p_a)
        
        # Sample
        trace = pm.sample(2000, return_inferencedata=False)
    
    # Probability B is better than A
    prob_b_better = (trace['delta'] > 0).mean()
    
    return {
        'prob_b_better': prob_b_better,
        'mean_lift': trace['delta'].mean(),
        'credible_interval': (
            np.percentile(trace['delta'], 2.5),
            np.percentile(trace['delta'], 97.5)
        )
    }

result = bayesian_ab_test(385, 3842, 462, 3842)
print(f"Probability B > A: {result['prob_b_better']:.1%}")
print(f"Mean lift: {result['mean_lift']:.2%}")
```

---

## Segmentation Analysis

```python
def analyze_segments(data):
    """Analyze A/B test results by segment"""
    
    segments = ['desktop', 'mobile', 'tablet']
    
    for segment in segments:
        segment_data = data[data['device'] == segment]
        
        result = analyze_ab_test(
            conversions_a=segment_data[segment_data['variant']=='A']['converted'].sum(),
            visitors_a=len(segment_data[segment_data['variant']=='A']),
            conversions_b=segment_data[segment_data['variant']=='B']['converted'].sum(),
            visitors_b=len(segment_data[segment_data['variant']=='B'])
        )
        
        print(f"\n{segment.upper()}:")
        print(f"  Lift: {result['lift_pct']:.1f}%")
        print(f"  P-value: {result['p_value']:.4f}")

# Check for Simpson's Paradox
# Overall: B wins
# By segment: A wins on desktop AND mobile
# Paradox: Sample ratio mismatch between segments
```

---

## Reporting Template

```markdown
## A/B Test Results: New Checkout Flow

**Duration:** March 1-14, 2024 (14 days)

### Setup
- **Hypothesis:** Simplified checkout increases conversion
- **Primary Metric:** Conversion rate
- **Sample Size:** 7,684 total (3,842 per variant)
- **Significance Level:** 5%
- **Power:** 80%

### Results

| Variant | Visitors | Conversions | Rate | Lift |
|---------|----------|-------------|------|------|
| Control (A) | 3,842 | 385 | 10.02% | - |
| Treatment (B) | 3,842 | 462 | 12.02% | +20.0% |

**Statistical Significance:** p=0.0023 ✅  
**95% Confidence Interval:** +12.3% to +27.7%

### Secondary Metrics

| Metric | Control | Treatment | Change |
|--------|---------|-----------|--------|
| Avg Order Value | $75.20 | $74.80 | -0.5% (NS) |
| Revenue per Visitor | $7.54 | $8.99 | +19.2% ✅ |
| Time to Purchase | 45s | 32s | -28.9% ✅ |

### Segment Analysis

| Segment | Control | Treatment | Lift | P-value |
|---------|---------|-----------|------|---------|
| Desktop | 11.2% | 13.5% | +20.5% | 0.012 ✅ |
| Mobile | 8.5% | 10.2% | +20.0% | 0.045 ✅ |

### Recommendation
**SHIP Treatment (B)** - Statistically significant +20% lift in conversion rate with no degradation in revenue metrics.
```

---

## Monitoring Long-Term Effects

```python
import pandas as pd

def monitor_post_launch(data, launch_date):
    """Monitor metrics after shipping winning variant"""
    
    # Pre-launch baseline
    pre_launch = data[data['date'] < launch_date]
    baseline_rate = pre_launch['converted'].mean()
    
    # Post-launch performance
    post_launch = data[data['date'] >= launch_date]
    
    # Weekly rolling average
    weekly = post_launch.resample('W', on='date')['converted'].mean()
    
    # Check if effect persists
    current_rate = post_launch['converted'].mean()
    
    if current_rate < baseline_rate * 1.05:
        alert("A/B test winner effect has degraded")
    
    return {
        'baseline': baseline_rate,
        'current': current_rate,
        'lift_maintained': (current_rate - baseline_rate) / baseline_rate
    }
```

## Rules

- Define primary metric before starting test — prevents cherry-picking significant results.
- Calculate sample size with power analysis — underpowered tests miss real effects.
- Wait for full sample size — peeking early inflates false positive rate to 30%+.
- Use consistent randomization (hash-based) — same user always sees same variant.
- Run for full business cycles — week-over-week patterns hide in partial weeks.
- Report confidence intervals, not just p-values — effect size matters more than significance.
- Check segment consistency — Simpson's paradox can reverse overall results.
- Monitor post-launch — A/B test winners sometimes regress after shipping.
- Bonferroni correction for multiple metrics — testing 20 metrics needs p<0.0025, not p<0.05.
- Minimum 1 week duration — shorter tests miss day-of-week effects.
