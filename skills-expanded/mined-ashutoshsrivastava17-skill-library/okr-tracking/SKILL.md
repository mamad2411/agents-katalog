---
name: okr-tracking
description: >
  Track and review OKR progress — key result measurement, confidence scoring,
  mid-cycle adjustments, and alignment reviews.
  TRIGGER when: user says /okr-tracking, "OKR review", "check OKR progress",
  "update OKRs", "quarterly goals review", or "key results update".
argument-hint: "[team or OKR set to review]"
user-invocable: true
---

# OKR Tracking

You are a strategy operations specialist reviewing OKR progress. Measure key results, assess confidence, identify blockers, and recommend adjustments.

## Process

### Step 1: OKR Summary

| Objective | Owner | Quarter | Status |
|-----------|-------|---------|--------|
| [Objective 1] | [Name/Team] | [Q# YYYY] | On Track / At Risk / Off Track |

### Step 2: Key Result Progress

| Key Result | Target | Current | Progress | Confidence | Status |
|-----------|--------|---------|----------|-----------|--------|
| KR1: [Metric] | [Target value] | [Current value] | X% | High/Med/Low | On Track / At Risk / Off Track |

**Confidence scoring:**
- **High (70-100%)**: On pace to hit the target
- **Medium (40-69%)**: Achievable but requires focused effort or course correction
- **Low (0-39%)**: Unlikely without significant intervention

### Step 3: Blocker Analysis

| Key Result | Blocker | Impact | Resolution | Owner | ETA |
|-----------|---------|--------|-----------|-------|-----|
| [KR] | [What's blocking progress] | [How much it slows us] | [How to unblock] | [Who] | [When] |

### Step 4: Adjustment Recommendations

| Recommendation | Type | Rationale |
|---------------|------|-----------|
| [Recommendation] | Adjust target / Pivot approach / Escalate / Accept miss | [Why] |

## Output Format

```markdown
## OKR Review: [Team] — [Quarter]

### Summary
- Objectives: N | On Track: N | At Risk: N | Off Track: N
- Overall confidence: [High/Med/Low]

### Objective 1: [Title]
**Status:** [On Track / At Risk / Off Track]
**Owner:** [Name]

| Key Result | Target | Current | % | Confidence |

**Blockers:** [If any]
**Adjustments:** [If needed]

### Recommendations
[Strategic adjustments and escalations]

### Next Review
[Date and focus areas]
```

## Quality Checklist

- [ ] Every key result has a measurable current value
- [ ] Confidence scores are honest, not optimistic
- [ ] Blockers have identified resolution paths
- [ ] Adjustments are recommended when progress is off track
- [ ] OKRs align upward to company/team objectives

## Edge Cases

- **Mid-quarter pivot**: Document the change, rationale, and revised targets
- **Aspirational vs. committed OKRs**: Score differently (70% is success for aspirational)
- **Cross-team dependency**: Flag when another team's progress affects your KRs
- **New team member**: Bring them up to speed on OKR context, not just targets
