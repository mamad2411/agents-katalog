---
name: scoring
description: "100-point scoring protocol. Use when score-based evaluation is needed for any feedback, review, or QA."
---

# Scoring Protocol

## Rules
- All feedback is scored on a 100-point scale, in 1-point increments
- Provide specific deduction reasons per item
- Never give a perfect score without justification — always include rationale

## Scoring Format

```
### Score: {total}/100

| Item | Score | Deduction Reason |
|------|-------|-----------------|
| {item1} | {score}/{max} | {specific reason or "None"} |
| {item2} | {score}/{max} | {specific reason or "None"} |
| ... | ... | ... |
```

## Severity Criteria
- 90-100: Ready to merge immediately
- 80-89: Merge after minor fixes
- 70-79: Fixes required, re-review needed
- 60-69: Significant rework needed, one revision opportunity then failure if below 70
- Below 60: Immediate failure, redesign required

## Examples
"Spec completeness 85/100 — Missing error handling scenarios(-10), undefined edge cases(-5)"
"QA overall 79/100 — Integration tests uncovered(-8), 3 instances of `any` type(-6), unclear error messages(-7)"
