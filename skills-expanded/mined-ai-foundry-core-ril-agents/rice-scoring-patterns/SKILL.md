---
name: rice-scoring-patterns
description: RICE scoring framework, effort estimation, and impact modeling for feature prioritization. Use when scoring a feature backlog, estimating effort, or modeling expected outcomes before committing to a development cycle.
---

# RICE Scoring Patterns

RICE is a structured framework for scoring features against each other so that prioritization decisions are explicit and defensible. It forces you to estimate four dimensions — Reach, Impact, Confidence, Effort — and produces a comparable score for each feature.

## When to Use This Skill

- Scoring a backlog of features before a planning cycle
- Comparing investment options with different reach/impact profiles
- Communicating prioritization rationale to stakeholders
- Identifying quick wins (high RICE score, low effort)
- Flagging overconfident estimates that need validation

## The RICE Formula

```
RICE Score = (Reach × Impact × Confidence) ÷ Effort
```

Higher score = higher priority.

### Reach

**Definition:** How many users will this affect per time period (typically per quarter)?

- Count users who will encounter the feature, not total users
- Be specific: "users who complete checkout" not "all users"
- Source from analytics data where possible; flag when estimated

```
Examples:
- "All logged-in users" → 50,000 users/quarter
- "Users who reach the checkout screen" → 12,000 users/quarter
- "Sellers with >100 listings" → 800 users/quarter
```

### Impact

**Definition:** How much does this affect each user who encounters it? Use a fixed scale:

| Score | Definition |
|-------|-----------|
| 3 | Massive impact — transforms the experience or drives a step-change in the key metric |
| 2 | High impact — meaningfully improves a key metric |
| 1 | Medium impact — noticeable improvement |
| 0.5 | Low impact — minor improvement |
| 0.25 | Minimal impact — very small effect |

**Important:** Impact is relative to the *outcome* being optimized (conversion, retention, revenue, engagement), not just user satisfaction.

### Confidence

**Definition:** How confident are you in the Reach and Impact estimates? Express as a percentage:

| Score | Definition |
|-------|-----------|
| 100% | Strong evidence — user research + data + prior experiments |
| 80% | Good evidence — user research or data, but not both |
| 50% | Moderate evidence — directional signals but no hard data |
| 20% | Low evidence — hypothesis based on intuition |

**Rule:** If confidence is below 50%, consider a validation experiment before the full build.

### Effort

**Definition:** Total person-months required across all roles (engineering, design, PM, QA).

- 1 person working for 1 month = 1
- 2 engineers + 0.5 designer for 3 weeks = approximately 1.4
- Use calibrated estimates against historical velocity where possible

**Note:** Effort uses person-months, not story points or arbitrary units. This makes RICE scores comparable across teams with different sprint structures.

## Worked Example

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Saved payment methods | 12,000 | 3 | 80% | 2 | 14,400 |
| Guest checkout | 8,000 | 2 | 100% | 1 | 16,000 |
| Order status push notifications | 50,000 | 0.5 | 80% | 0.5 | 40,000 |
| Bulk listing upload for sellers | 800 | 3 | 50% | 3 | 400 |

**Reading:** Guest checkout and push notifications score much higher than they might feel intuitively — guest checkout has a high confidence that boosts it; push notifications win on Reach despite low Impact per user.

## Effort Estimation Patterns

### T-Shirt Sizing with Person-Month Conversion

| T-Shirt | Person-Months | Characteristics |
|---------|--------------|-----------------|
| XS | 0.25 | Config change, copy update, minor UI tweak |
| S | 0.5–1 | Single-surface change, existing patterns, no new APIs |
| M | 1–2 | Multi-surface, some new backend logic, standard integration |
| L | 3–5 | New subsystem, significant backend work, multiple integrations |
| XL | 6+ | Platform-level change, new data model, cross-team dependencies |

### Dependency-Adjusted Effort

When Feature B requires Feature A first, the total effort for B includes the dependency overhead:
- Add 20–30% for integration work between A and B
- Add sequencing cost: B can't start until A is done, which may delay B by a full sprint

### Risk-Adjusted Estimates

Always provide three estimates:

```
Optimistic: Everything goes smoothly, no surprises
Expected:   Normal velocity, 1-2 minor surprises
Pessimistic: Key dependency is harder than expected, one rework cycle

Expected estimate = (Optimistic + 4×Most Likely + Pessimistic) ÷ 6
```

## Common RICE Mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| Using total users for Reach | Inflates scores for features with narrow real reach | Scope Reach to users who will actually encounter the feature |
| Overconfidence (everyone scores 80%+) | Prioritization feels certain when it isn't | Force calibration: what evidence supports each confidence score? |
| Ignoring second-order effects | Undervalues prerequisite features | Add "prerequisite multiplier" — if A enables B and C, A's effective value includes B and C |
| Effort in story points | Scores aren't comparable across teams | Convert to person-months |
| One-time scoring | Backlog gets stale as evidence accumulates | Re-score after each validation experiment |

## Outcome Modeling

For high-stakes items (large effort, strategic importance), complement RICE with a simple outcome model:

```
Feature: [Name]
Target metric: [e.g., checkout conversion rate]
Current baseline: [e.g., 62%]

Scenario modeling:
  Optimistic: +5pp conversion → +$840K ARR at current volume
  Base case:  +2.5pp conversion → +$420K ARR
  Pessimistic: +1pp conversion → +$168K ARR

Expected value: 0.2 × $840K + 0.6 × $420K + 0.2 × $168K = $453K ARR
Engineering cost: 2 person-months × $15K/month blended = $30K
Expected ROI: 15:1
```

## Best Practices

1. **Score collaboratively** — PM + engineering + design should each estimate effort; take the average or discuss divergence
2. **Calibrate against history** — compare previous estimates to actuals and adjust systematically
3. **Flag low-confidence estimates** — a high RICE score with 20% confidence is a hypothesis, not a priority
4. **Re-score after experiments** — if a validation experiment changes your Impact or Confidence estimate, the ranking changes
5. **RICE is an input, not the output** — the stack rank is a recommendation; human judgment still overrides for strategic, dependency, or constraint reasons
