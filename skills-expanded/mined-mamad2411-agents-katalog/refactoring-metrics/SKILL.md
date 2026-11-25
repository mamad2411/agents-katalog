---
name: refactoring-metrics
description: Analyzes code and estimates structural metrics via LLM. No external dependencies.
---

# Refactoring Metrics Skill

## Status
Based on "Fundamentals of Software Architecture" (Mark Richards & Neal Ford).

## Approach
LLM analyzes code directly, estimates structural metrics using book concepts.
Zero external dependencies.

## Input

### Specific File

```
Analyze file: src/services/userService.ts
Return structural metrics in JSON:
```

### Full Scan

```
Scan project and return metrics per file,
plus ranking by priority.
```

## Output

### Per-File Metrics

```json
{
  "file": "src/services/userService.ts",
  "cohesion": {
    "type": "sequential",
    "score": 7,
    "justification": "validateUser and processUser operate in sequence"
  },
  "lcom": {
    "value": 0.35,
    "justification": "3 methods don't share fields, 5 share"
  },
  "coupling": {
    "afferent": 2,
    "efferent": 8,
    "justification": "2 incoming deps, 8 outgoing"
  },
  "abstractness": {
    "value": 0.3,
    "justification": "3 abstract classes of 10 total"
  },
  "instability": {
    "value": 0.8,
    "formula": "8 / (8 + 2) = 0.8",
    "justification": "High output deps = unstable"
  },
  "distance": {
    "value": 0.1,
    "formula": "0.3 + 0.8 - 1 = 0.1",
    "zone": "Main Sequence",
    "justification": "Near 0 = balanced"
  },
  "connascence": {
    "static": {
      "CoN": true,
      "CoT": false,
      "CoM": true,
      "CoP": false,
      "CoA": false
    },
    "justification": "CoN (name User), CoM (STATUS magic number)"
  },
  "score": {
    "value": 4,
    "scale": "0-10",
    "justification": "High instability, low LCOM"
  },
  "issues": [
    {
      "type": "high_instability",
      "severity": "high",
      "recommendation": "Introduce interface"
    },
    {
      "type": "low_cohesion",
      "severity": "medium",
      "recommendation": "Separate into classes"
    }
  ]
}
```

### Full Scan

```json
{
  "timestamp": "2026-04-18T10:00:00",
  "mode": "scan",
  "files_analyzed": 45,
  "files_with_issues": 12,
  "global_score": 6.5,
  "ranking": [
    { "file": "userService.ts", "score": 4, "priority": "high" },
    { "file": "orderController.ts", "score": 5, "priority": "high" }
  ]
}
```

## Book Metrics

### 1. Cohesion

| Type | Score |
|------|-------|
| Functional | 10 |
| Sequential | 8 |
| Communicational | 7 |
| Procedural | 5 |
| Temporal | 4 |
| Logical | 3 |
| Coincidental | 1 |

### 2. Coupling

- **Afferent (Ca)** — input dependencies
- **Efferent (Ce)** — output dependencies

I = Ce / (Ce + Ca)

| Value | Classification |
|-------|--------------|
| < 0.3 | Stable |
| 0.3 - 0.7 | Moderate |
| > 0.7 | Unstable |

### 3. Distance

D = A + I - 1

| Zone | D |
|------|---|
| Zone of Pain | < -0.5 |
| Main Sequence | -0.5 to 0.5 |
| Zone of Uselessness | > 0.5 |

### 4. Connascence

Static: CoN, CoT, CoM, CoP, CoA (prefer)
Dynamic: CoE, CoV (avoid)

## Structured Prompt

```
## Analysis: [file]

### 1. Cohesion
- Type: [functional|sequential|...]
- Score (1-10): [n]
- Justification:

### 2. Coupling
- Ca: [n], Ce: [n]
- I = [formula] = [n]

### 3. Abstractness
- A: [n]

### 4. Distance
- D = [formula] = [n]
- Zone:

### 5. Connascence
- CoN/CoT/CoM/CoP/CoA:

### 6. Score
- Score (0-10): [n]
- Justification:

### 7. Issues
- [issue]: [recommendation]
```

## Integration

1. refactoring-manager → invokes refactoring-metrics
2. LLM returns metrics
3. refactoring-analyzer → prioritizes
4. refactoring-executor → executes
5. refactoring-metrics → re-evaluates

## Criteria

| Issue | Action |
|-------|------|
| I > 0.7 | Interface |
| Score < 5 | Separate responsibilities |
| D < -0.5 | Abstractions |
| CoM | Named constants |

## Difference: Metrics vs Analyzer

- **metrics**: Estimates "what's bad"
- **analyzer**: Recommends "what to do"