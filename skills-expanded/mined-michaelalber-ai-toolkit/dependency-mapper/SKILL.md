---
name: dependency-mapper
audience: professional
description: Coupling visualization with Robert C. Martin stability metrics — makes architectural decisions visible as dependency patterns. Use when analyzing module dependencies, detecting circular references, visualizing coupling, or assessing architectural health through Robert C. Martin stability metrics.
---

# Dependency Mapper

> "The dependencies between packages must not form cycles. If there is a cycle in the dependency structure, you have a problem that must be broken."
> -- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*

## Core Philosophy

Architecture is not what you draw on a whiteboard — it is the dependency structure in your code. This skill makes that structure visible and measurable. Using Robert C. Martin's package coupling metrics (Ca, Ce, I, A, D), you learn to see dependency patterns as architectural decisions and recognize when those decisions have drifted from intent.

Every `import`, `using`, `require`, or `#include` is an architectural vote. Most developers have a mental model that diverges significantly from reality. This skill closes that gap with numbers.

**What this skill is:** A coaching framework for reading dependency structure as architecture, computing Martin's metrics, and acting on the patterns they reveal.

**What this skill is not:** An automated refactoring tool. It shows the truth of your dependency structure; you decide what to do.

**Non-Negotiable Constraints:**
1. **Measure before judging** — compute Ca, Ce, I, A and D from the actual import statements; never estimate, and state the scope when only a subset is scanned
2. **The code is the architecture** — report the dependency graph as it is, not as the documentation says it should be
3. **Cycles are urgent** — every cycle is reported as a structural defect, not deferred debt
4. **Instability is not a verdict** — I = 1.0 is correct for leaf and UI modules; flag Stable Dependencies / Stable Abstractions violations and D > 0.3, not high I alone
5. **The user decides** — show the structure and the options; do not refactor

## Workflow: CACR Interaction Loop

**CHALLENGE → ATTEMPT → COMPARE → REFLECT**, then next module or project.

### Phase 1: Challenge

Enumerate the top-level modules/packages. Ask the user: "Before I compute metrics, sketch the dependency directions, predict which module has highest/lowest I, and predict whether any cycles exist. This is about building intuition, not speed."

### Phase 2: Attempt

User provides predictions about dependency structure, coupling, and problem areas. Coach does NOT correct yet — ask clarifying questions, record predictions for comparison, encourage reasoning.

### Phase 3: Compare

Scan source for import/dependency statements. Build the dependency graph. Compute Ca, Ce, I, A, D per module. Detect cycles. Present results alongside predictions.

### Phase 4: Reflect

Guide the user through: where predictions matched reality, where they diverged, which SDP violations are intentional vs. accidental, which one dependency to change first, and which cycle is most urgent to break.

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Anti-Patterns, Error Recovery, Stack-Specific Guidance. Deeper detail: `references/visualization-patterns.md`.

## State Block

```
<dependency-state>
mode: scan | analyze | predict | reflect
project_path: [absolute path to project root]
language: [primary language detected]
modules_analyzed: [count]
circular_deps_found: [count of cycles]
instability_violations: [count of SDP violations]
main_sequence_distance: [average D across all modules]
last_action: [what was just completed]
next_action: [what should happen next]
</dependency-state>
```

## Output Templates

### Metrics Table

```markdown
## Package Coupling Metrics: [Project Name]

| Module | Ca | Ce | I     | A     | D     | Zone |
|--------|----|----|-------|-------|-------|------|
| Core   | 8  | 1  | 0.111 | 0.750 | 0.139 | --   |
| Data   | 3  | 4  | 0.571 | 0.200 | 0.229 | --   |
| Web    | 0  | 6  | 1.000 | 0.000 | 0.000 | --   |
| Shared | 6  | 5  | 0.455 | 0.100 | 0.445 | Pain |

**Formulas:**
- Ca: Afferent Coupling (incoming dependencies — how many depend on this)
- Ce: Efferent Coupling (outgoing dependencies — how many this depends on)
- I: Instability = Ce / (Ca + Ce), range [0,1]; 0=stable, 1=unstable
- A: Abstractness = abstract types / total types, range [0,1]
- D: Distance from Main Sequence = |A + I − 1|, range [0,1]; 0=ideal
- Zone: "Pain" = low I AND low A (stable+concrete); "Useless" = high I AND high A
```

### Dependency Scan Report

```markdown
## Dependency Scan: [Project Name]
**Language**: [language] | **Modules**: [count] | **Cycles detected**: [N]

### Raw Dependencies
[ModuleA] --> [ModuleB]
[ModuleA] --> [ModuleC]
...

### Circular Dependencies
Cycle 1: [A] → [B] → [C] → [A] — impact: independent deployment impossible, changes cascade
Breaking strategies: (1) Extract interface from A into shared abstractions, (2) Merge tightly-coupled modules, (3) Replace back-edge with event mechanism

### SDP Violations
| Depender | I(depender) | Dependee | I(dependee) | Delta |
|----------|-------------|----------|-------------|-------|
| Data | 0.571 | Shared | 0.455 | 0.116 |

Delta > 0.3 = high priority; < 0.1 may be acceptable depending on context.
```

Full templates (Main Sequence Chart, Violation List, Refactoring Suggestions): `references/coupling-metrics.md`.

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| **architecture-review** | Use dependency-mapper metrics as quantitative input; metrics provide evidence for architectural concerns |
| **pattern-tradeoff-analyzer** | When coupling patterns are revealed, use this skill to evaluate whether a design pattern would improve structure |
| **architecture-journal** | Record metric trends and refactoring decisions for longitudinal tracking |
| **technical-debt-assessor** | SDP violations, cycles, and Zone of Pain modules feed directly into technical debt assessment |
| **technical-debt-assessor** | When breaking a cycle or fixing an SDP violation, use this skill to evaluate the refactoring approach |
