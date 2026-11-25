---
name: Story Point Estimator
description: Planning poker estimation with domain-aware complexity factors — Fibonacci scales for planning and fine-grained scales for coding tasks
version: 1.0.0
trigger: story-point-estimator
---

# Story Point Estimator

## Purpose

Estimate story points for tasks with awareness of domain-specific complexity factors. Uses calibrated scales for both planning (Fibonacci) and coding (fine-grained) estimation.

## Baseline

**1 SP = simple authenticated API** (key→value, secured, tested, deployed, documented)

This is the universal reference point. Every estimate is relative to this baseline.

## Scales

### Planning Scale (Fibonacci)
Use for feature planning, sprint sizing, roadmap estimation.

```
1, 2, 3, 5, 8, 13, 21...
```

**Break any item > 13 SP** into smaller pieces.

| SP | Examples |
|----|----------|
| 1 | Simple CRUD endpoint, env var config, docs page |
| 2 | Endpoint with validation + error handling |
| 3 | Feature with 2-3 interacting components |
| 5 | Feature touching 4+ files, needs integration testing |
| 8 | Cross-system feature with API contracts |
| 13 | Multi-service feature with migration + rollback plan |
| 21 | Epic-level work (break this down) |

### Coding Scale (Fine-Grained)
Use for implementation tasks within a sprint.

```
0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1, 2, 3, 5
```

**Break any item > 5 SP** into smaller pieces.

| SP | Examples |
|----|----------|
| 0.05 | Rename variable, fix typo, update constant |
| 0.1 | Add a field, update a test, config change |
| 0.2 | New utility function with test |
| 0.3 | Component with props + basic logic |
| 0.5 | Feature slice with tests (happy path) |
| 0.8 | Feature with edge cases + error handling |
| 1 | Full feature equivalent to baseline API |
| 2 | Feature with integration points |
| 3 | Feature with complex state or concurrency |
| 5 | Multi-component feature (break this down) |

## Complexity Adjustment Factors

Apply these to the base estimate:

| Factor | Adjustment | When |
|--------|-----------|------|
| Multi-system coordination | +1-2 SP | Feature spans >1 service/repo |
| Compliance/legal | +1 SP | HIPAA, GDPR, FTC, SOC2 |
| Integration complexity | +1-3 SP | Third-party APIs, payment, auth |
| Data migration | +1-2 SP | Schema changes with existing data |
| Performance-critical | +1 SP | Latency SLAs, high-throughput |
| Unfamiliar domain | +1 SP | Team has no prior experience |
| Seasonal/time-pressure | +0.5 SP | Hard deadline increases coordination |

## Estimation Process

### Step 1: Identify Domain
What kind of system? (API, frontend, data pipeline, infrastructure, etc.)

### Step 2: Decompose
Break into components. List each piece.

### Step 3: Base Estimate
Estimate each component relative to the 1 SP baseline.

### Step 4: Apply Adjustments
Add complexity factors that apply.

### Step 5: Sanity Check
- Does the total feel right compared to similar past work?
- Is anything > threshold? (13 for planning, 5 for coding) → break it down.
- What's the confidence level? (High/Medium/Low)

### Step 6: Output

```markdown
## Story Point Estimate: [X] SP

**Task**: [Description]

### Breakdown
| Component | SP | Notes |
|-----------|----|----|
| [Component 1] | [X] | [Brief justification] |
| [Component 2] | [X] | |
| ... | | |

**Base Total**: [X] SP

### Complexity Adjustments
| Factor | Adjustment | Reason |
|--------|-----------|--------|
| [Factor] | +[X] SP | [Why it applies] |

**Final Estimate**: [X] SP

### Risk & Confidence
- **Confidence**: [High/Medium/Low]
- **Risk**: [What could blow the estimate]
- **Recommendation**: [Spike? Prototype? Break down further?]
```

## Rules

1. **Never use time estimates** — always story points
2. **Always show your work** — breakdown + adjustments
3. **Flag uncertainty** — if confidence is Low, recommend a spike
4. **Round to scale values** — don't invent numbers (no "4 SP" on Fibonacci)
5. **Compare to baseline** — "is this really 8x harder than a simple API?"
6. **Break large items** — >13 (planning) or >5 (coding) must be decomposed

## Anti-Patterns

- Estimating without decomposition
- Using time ("this is a 2-day task") instead of complexity
- Anchoring to the first number someone says
- Estimating things you don't understand (spike first)
- Padding estimates with "buffer" instead of identifying specific risks

## Integration

This skill is called by:
- Planners (during sprint planning)
- Implementation coordinators (during task breakdown)
- Requirements analysts (during scope validation)

All QPLAN, QNEW, and implementation outputs should include SP estimates.
