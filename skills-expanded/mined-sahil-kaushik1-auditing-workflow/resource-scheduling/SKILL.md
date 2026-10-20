---
name: resource-scheduling
description: >
  Allocate/extract/reallocate reasoning budget across tasks and cycles.
  Used by the Orchestrator to prioritize where reasoning resources go.
---

# Resource Scheduling Skill

## Purpose

Treat model reasoning as a limited resource. This skill provides the framework for
deciding which tasks receive reasoning first, which deserve deep reasoning, and where
the next round of resources should go.

## Three Actions

### 1. Allocate
Split the large audit goal into smaller tasks (via Threat Modeler).
- Critical invariants → Deep reasoning, mandatory verification
- High-value paths → Deep reasoning
- Medium paths → Fast scan, escalate if suspicious
- Low-value areas → Pattern match only

### 2. Extract
Require each task to produce structured output:
- Evidence (code references, trace output)
- Witnesses (concrete attack sequences)
- Counterexamples (values that break assumptions)
- Unresolved questions (what couldn't be determined)
- Assumptions (what the analysis depends on)

### 3. Reallocate
After each cycle, use gap analysis to redirect budget:
- Category 1 (sufficient) → Done, no more budget
- Category 2 (low-value) → Skip
- Category 3 (high-value gaps) → Next cycle's budget goes here

## Priority Scoring

```
score = (invariant_criticality × 0.4) +
        (attack_surface_breadth × 0.3) +
        (complexity_of_path × 0.2) +
        (historical_vulnerability_rate × 0.1)
```

Where:
- `invariant_criticality`: How bad is it if this breaks? (1-5)
- `attack_surface_breadth`: How many ways can an attacker reach this? (1-5)
- `complexity_of_path`: How many steps/contracts involved? (1-5)
- `historical_vulnerability_rate`: How often do bugs of this class appear? (1-5)
