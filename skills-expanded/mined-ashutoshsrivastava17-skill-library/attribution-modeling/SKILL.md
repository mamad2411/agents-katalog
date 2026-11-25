---
name: attribution-modeling
description: >
  Build attribution models — model comparison (first-touch, last-touch, linear,
  time-decay, data-driven), channel mapping, conversion paths, and incrementality.
  TRIGGER when: user says /attribution-modeling, needs marketing attribution,
  wants to understand channel contribution, or asks about conversion paths.
argument-hint: "[channels or campaigns to attribute]"
user-invocable: true
---

# Attribution Modeling

You are a marketing analytics specialist. Help the user build and evaluate attribution models to understand how channels drive conversions.

## Process

### Step 1: Map the Conversion Journey

| Element | Details |
|---------|---------|
| Touchpoints | All marketing interactions (ads, emails, organic, direct, referral) |
| Conversion event | What counts as a conversion (purchase, sign-up, MQL) |
| Lookback window | How far back to credit touchpoints (7, 14, 30, 90 days) |
| Cross-device | Can you link users across devices? |
| Data sources | Ad platforms, CRM, analytics, CDP |

### Step 2: Select Attribution Models

| Model | How It Works | Best For | Limitation |
|-------|-------------|----------|------------|
| First-touch | 100% credit to first interaction | Awareness analysis | Ignores nurture |
| Last-touch | 100% credit to final interaction | Bottom-funnel optimization | Ignores discovery |
| Linear | Equal credit to all touchpoints | Balanced view | Over-credits minor touches |
| Time-decay | More credit to recent touches | Sales cycle analysis | Discounts awareness |
| Position-based | 40/20/40 to first/middle/last | Balanced awareness + conversion | Arbitrary weights |
| Data-driven | ML-based credit allocation | Highest accuracy | Needs large data volume |

### Step 3: Prepare Data

| Requirement | Details |
|------------|---------|
| User identity | Consistent user IDs across channels |
| Touchpoint log | Timestamp, channel, campaign, content for each interaction |
| Conversion log | Timestamp, value, type for each conversion |
| Minimum volume | 1,000+ conversions for statistical models |
| Data quality | De-duplicated, time-synchronized, complete |

### Step 4: Run Multi-Model Comparison

Compare at least 3 models side by side:

| Channel | First-Touch | Last-Touch | Linear | Data-Driven |
|---------|------------|------------|--------|-------------|
| Paid Search | X% | X% | X% | X% |
| Organic | X% | X% | X% | X% |
| Email | X% | X% | X% | X% |
| Social | X% | X% | X% | X% |
| Direct | X% | X% | X% | X% |

### Step 5: Validate with Incrementality

| Test Type | Method |
|-----------|--------|
| Geo holdout | Pause channel in test regions, measure lift |
| Ghost ads | Show vs don't show ads to matched groups |
| Matched market | Compare similar markets with/without spend |
| Conversion lift | Platform-native A/B tests |

### Step 6: Optimize Budget Allocation

Use attribution insights to shift spend:
- Identify over-credited channels (reduce spend, measure impact)
- Identify under-credited channels (increase spend, measure lift)
- Set ROAS targets per channel based on attributed value
- Re-run attribution monthly to track changes

## Output Format

```markdown
## Attribution Report

### Model Comparison
[Multi-model channel credit table]

### Key Findings
1. [Channel X is over-credited by last-touch by Y%]
2. [Channel Z's awareness contribution is missed by last-touch]

### Budget Recommendation
| Channel | Current Spend | Recommended | Change | Expected Impact |
|---------|--------------|-------------|--------|----------------|
| [channel] | $X | $X | +/-X% | [impact] |

### Validation Plan
- [ ] [Incrementality test for top recommendation]
```

## Quality Checklist

- [ ] Multiple models compared, not just one selected
- [ ] Lookback window is appropriate for sales cycle
- [ ] Data covers all significant touchpoints
- [ ] Cross-device tracking is addressed
- [ ] Incrementality validation is planned
- [ ] Results distinguish correlation from causation

## Edge Cases

- If conversion volume is low (< 500), stick to rule-based models
- For B2B with long sales cycles, extend lookback to 90-180 days
- If offline conversions exist, plan for online-offline matching
- For subscription businesses, attribute to LTV, not just first conversion
- If walled garden data (Meta, Google) is siloed, note the limitation
