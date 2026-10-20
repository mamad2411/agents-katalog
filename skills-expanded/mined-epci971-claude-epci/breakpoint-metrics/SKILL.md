---
name: breakpoint-metrics
description: >-
  Calculates complexity metrics and generates enriched breakpoint displays for EPCI workflow.
  Auto-invoke when: /epci reaches BP1 (post-Phase 1) or BP2 (post-Phase 2) breakpoints,
  or when complexity scoring is needed for STANDARD/LARGE features.
  Do NOT load for: /epci-quick (no formal breakpoints), /epci-spike (different output),
  or non-EPCI workflows. Use compact format when context >75%.
---

# Breakpoint Metrics

## Overview

Provides complexity scoring, time estimation, and enriched breakpoint display templates
for EPCI Phase 1 and Phase 2 breakpoints.

## Complexity Scoring Algorithm

### Formula

```
score = (files × 0.3) + (loc × 0.3) + (deps × 0.2) + (risk × 0.2)
```

Where:
- **files**: Normalized file count (files / 20, capped at 1.0)
- **loc**: Normalized LOC estimate (loc / 2000, capped at 1.0)
- **deps**: Normalized dependency count (deps / 10, capped at 1.0)
- **risk**: Risk factor (0.0 = none, 0.5 = medium, 1.0 = high)

### Score Interpretation

| Score Range | Category | Display |
|-------------|----------|---------|
| 0.00 - 0.20 | TINY | `TINY (score: X.XX)` |
| 0.21 - 0.40 | SMALL | `SMALL (score: X.XX)` |
| 0.41 - 0.70 | STANDARD | `STANDARD (score: X.XX)` |
| 0.71 - 1.00 | LARGE | `LARGE (score: X.XX)` |

### Example Calculations

**TINY Example** (1 file, 30 LOC, 0 deps, no risk):
```
score = (1/20 × 0.3) + (30/2000 × 0.3) + (0/10 × 0.2) + (0.0 × 0.2)
      = 0.015 + 0.0045 + 0 + 0 = 0.02 → TINY
```

**STANDARD Example** (7 files, 500 LOC, 4 deps, medium risk):
```
score = (7/20 × 0.3) + (500/2000 × 0.3) + (4/10 × 0.2) + (0.5 × 0.2)
      = 0.105 + 0.075 + 0.08 + 0.1 = 0.36 → SMALL (borderline STANDARD)
```

**LARGE Example** (15 files, 1500 LOC, 8 deps, high risk):
```
score = (15/20 × 0.3) + (1500/2000 × 0.3) + (8/10 × 0.2) + (1.0 × 0.2)
      = 0.225 + 0.225 + 0.16 + 0.2 = 0.81 → LARGE
```

## Time Estimation

### Heuristic Table

| Category | Base Time | Per-File Adjustment | Total Range |
|----------|-----------|---------------------|-------------|
| TINY | 15 min | - | ~15 min |
| SMALL | 45 min | +5 min/file | 45 min - 1h |
| STANDARD | 2h | +15 min/file | 2h - 4h |
| LARGE | 6h | +30 min/file | 6h+ |

### Display Format

- TINY/SMALL: `~Xmin` or `~Xh`
- STANDARD: `~Xh` or `~XhYm`
- LARGE: `~Xh+`

## Risk Assessment

### Risk Factors

| Factor | Risk Level | Value |
|--------|------------|-------|
| No breaking changes, isolated scope | None | 0.0 |
| Minor API changes, limited scope | Low | 0.25 |
| Breaking changes possible, medium scope | Medium | 0.5 |
| Architecture changes, security impact | High | 0.75 |
| Critical system changes, data migration | Critical | 1.0 |

### Risk Display

| Level | Display |
|-------|---------|
| None | `Risque: Faible` |
| Low | `Risque: Faible` |
| Medium | `Risque: Moyen (description)` |
| High | `Risque: Élevé (description)` |
| Critical | `Risque: Critique (description)` |

## Breakpoint Templates

### BP1 Template (Post-Phase 1)

See: `templates/bp1-template.md`

Displays:
- Complexity score and category
- Files impacted count
- Time estimate
- Risk level
- @plan-validator verdict
- Preview of Phase 2 tasks (3-5 first)
- Feature Document link
- Interactive options

### BP2 Template (Post-Phase 2)

See: `templates/bp2-template.md`

Displays:
- Task completion ratio
- Test results summary
- Coverage percentage (if available)
- @code-reviewer verdict
- @security-auditor verdict (if invoked)
- @qa-reviewer verdict (if invoked)
- Preview of Phase 3 actions
- Feature Document link
- Interactive options

## Integration

### Usage in /epci

```markdown
## After Phase 1 completion:
1. Calculate complexity score from plan data
2. Generate BP1 using template
3. Wait for user confirmation

## After Phase 2 completion:
1. Collect task completion and test results
2. Aggregate agent verdicts
3. Generate BP2 using template
4. Wait for user confirmation
```

### Data Collection Points

**For BP1:**
- Files from §2 Implementation Plan
- LOC estimate from task breakdown
- Dependencies from risk analysis
- Risk from identified risks

**For BP2:**
- Tasks completed from §3 Progress
- Test results from test execution
- Agent verdicts from review reports
