---
name: complexity-calculator
description: >-
  Centralized complexity calculation for EPCI workflows. Evaluates feature complexity
  based on files, LOC, dependencies, and risk factors. Returns categorization
  (TINY/SMALL/STANDARD/LARGE) with confidence score and recommended workflow.
  Use when: /brief, /decompose, /quick, /debug, /ralph-exec need complexity evaluation.
  Not for: Runtime performance analysis, code quality metrics.
allowed-tools: [Read, Glob, Grep]
---

# Complexity Calculator

## Overview

Skill centralisé pour le calcul de complexité des features EPCI. Évalue la complexité
en utilisant une formule pondérée et retourne une catégorisation avec score de confiance.

**Utilisé par:** `/brief`, `/quick`, `/decompose`, `/debug`, `/ralph-exec`, `/epci`

## Configuration

| Element | Value |
|---------|-------|
| **Model** | Haiku (fast evaluation) |
| **Max files scan** | 50 |
| **Cache** | Session-scoped |

## Scoring Formula

```
score = (files_norm × 0.30) + (loc_norm × 0.30) + (deps_norm × 0.20) + (risk_factor × 0.20)
```

### Normalization

| Metric | Min | Max | Normalization |
|--------|-----|-----|---------------|
| **files** | 1 | 20 | `min(files, 20) / 20` |
| **loc** | 0 | 2000 | `min(loc, 2000) / 2000` |
| **deps** | 0 | 15 | `min(deps, 15) / 15` |
| **risk** | 0.0 | 1.0 | Direct (see Risk Factors) |

## Risk Factors

| Factor | Weight | Detection |
|--------|--------|-----------|
| **Security patterns** | +0.30 | `**/auth/**`, `**/security/**`, `**/payment/**` |
| **Database migration** | +0.25 | `**/migrations/**`, schema changes |
| **Breaking API** | +0.25 | API endpoint modification, contract changes |
| **Multi-service** | +0.20 | Cross-service dependencies |
| **No tests** | +0.15 | Test coverage < 30% for affected files |
| **Legacy code** | +0.10 | Files > 500 LOC without recent changes |

**Max cumulative risk:** 1.0 (capped)

## Category Mapping

| Score Range | Category | Workflow | Description |
|-------------|----------|----------|-------------|
| 0.00 - 0.20 | **TINY** | `/quick --autonomous` | 1 file, < 50 LOC, no risk |
| 0.21 - 0.40 | **SMALL** | `/quick` | 2-3 files, < 200 LOC, low risk |
| 0.41 - 0.70 | **STANDARD** | `/epci` | 4-10 files, tests required |
| 0.71 - 1.00 | **LARGE** | `/epci --large` | 10+ files, architecture impact |

## Invocation

### Input Format

```yaml
complexity_request:
  brief: "{brief_text}"
  files_impacted: [{path: "...", action: "Create|Modify|Delete"}]
  exploration_results:
    stack: "{stack_info}"
    patterns: ["Repository", "Service", ...]
    risks: ["risk1", "risk2", ...]
```

### Output Format

```yaml
complexity_result:
  category: "TINY|SMALL|STANDARD|LARGE"
  score: 0.42
  confidence: 0.85
  breakdown:
    files_norm: 0.15
    loc_norm: 0.20
    deps_norm: 0.10
    risk_factor: 0.25
  flags_recommended: ["--think", "--uc"]
  workflow_command: "/epci"
  reasoning: "4 fichiers impactés, patterns auth détectés"
  warnings: ["Security patterns detected", "No existing tests"]
```

## Integration Examples

### In /brief (Step 3)

```markdown
### Step 3.1: Complexity Evaluation

**Skill**: `complexity-calculator`

Invoke with exploration results:
- Files impacted from @Explore
- Stack and patterns detected
- Risks identified

Use output to determine:
- Category for routing
- Flags to recommend
- Warnings to display in breakpoint
```

### In /quick (Phase E)

```markdown
### [E] EXPLORE Phase

After @Explore completes:
1. Invoke complexity-calculator
2. IF category > SMALL → Escalate to /epci
3. Store category for resume final
```

### In /decompose

```markdown
### Sub-spec Estimation

For each sub-spec generated:
1. Invoke complexity-calculator per spec
2. Aggregate for total effort
3. Use for parallelization planning
```

## Calibration Integration

Le skill s'intègre avec `project-memory` pour calibration continue:

```yaml
# .project-memory/calibration/complexity.yaml
predictions:
  - predicted: "SMALL"
    actual: "STANDARD"
    feature_slug: "auth-oauth"
    date: "2025-01-15"
calibration_factor: 1.15  # Slightly underestimates
```

**Usage:** Appliquer `calibration_factor` au score final si historique disponible.

## Thresholds Configuration

Les seuils peuvent être ajustés via `.project-memory/settings.yaml`:

```yaml
complexity:
  thresholds:
    tiny_max: 0.20
    small_max: 0.40
    standard_max: 0.70
  weights:
    files: 0.30
    loc: 0.30
    deps: 0.20
    risk: 0.20
```

## Quick Reference Tables

### Files → Category (simplified)

| Files | Category (sans risque) |
|-------|------------------------|
| 1 | TINY |
| 2-3 | SMALL |
| 4-10 | STANDARD |
| 10+ | LARGE |

### LOC → Category (simplified)

| LOC | Category (sans risque) |
|-----|------------------------|
| < 50 | TINY |
| 50-200 | SMALL |
| 200-1000 | STANDARD |
| 1000+ | LARGE |

### Risk Elevation

| Base Category | + Risk > 0.3 | + Risk > 0.5 |
|---------------|--------------|--------------|
| TINY | → SMALL | → STANDARD |
| SMALL | → STANDARD | → STANDARD |
| STANDARD | → STANDARD | → LARGE |
| LARGE | → LARGE | → LARGE |

## Error Handling

| Situation | Action |
|-----------|--------|
| Missing exploration data | Use file count only, set confidence = 0.5 |
| Partial scan (timeout) | Mark as UNKNOWN, suggest `--think-hard` |
| No files detected | Return TINY with warning |
| All files high-risk | Cap at LARGE, add security warning |

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Ignoring risk factors | Underestimation | Always include risk in calculation |
| Hardcoding thresholds | No calibration | Use configurable thresholds |
| Skipping for TINY | Hidden complexity | Always evaluate |
| Manual override without logging | Lost calibration data | Log all overrides |

## See Also

| Related | Description |
|---------|-------------|
| `project-memory` | Calibration storage |
| `breakpoint-display` | Display complexity in breakpoints |
| `/brief` | Primary consumer |
| `/quick` | Escalation decision |
| `/decompose` | Sub-spec estimation |
