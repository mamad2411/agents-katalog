---
name: hyperplan
description: "[OMCP] Adversarial 5-member planning skill that runs cross-critique rounds and hands the surviving insights to the planner agent"
orchestrates-agents: "code-simplifier, test-engineer, research, architect, analyst, planner"
argument-hint: "<planning request>"
level: 4
---

# [OMCP] Hyperplan — Adversarial Multi-Agent Planning

> **MANDATORY:** First action when this skill loads — say "HYPERPLAN MODE ENABLED!" so the user knows orchestration started.

**Hyperplan = `/omcp:plan --adversarial`. The procedure lives in the plan skill.**

Hyperplan is a shorthand alias for `/omcp:plan --adversarial`. The full 7-phase adversarial procedure — the 5-member roster (skeptic/validator/researcher/architect/creative), their hostile system prompts, the 3 cross-critique rounds, the Phase 5 insight distillation, and the **mandatory** Phase 6 planner handoff — is defined once in `skills/plan/SKILL.md` under **Adversarial mode (`--adversarial`)**. Follow that procedure.

## Agent orchestration

You (the orchestrator) become the **Lead** of a 5-member adversarial team mapped to existing custom agents:

```text
skeptic     → code-simplifier
validator   → test-engineer
researcher  → research
architect   → architect
creative    → analyst
```

The five members attack each other's findings ruthlessly; you distill only the **defensible insights** that survive and **mandatorily** hand them to the `planner` agent for executable plan formalization. **The Phase 6 planner handoff is non-negotiable** — skipping it turns this back into vanilla orchestration. The Lead distills in Phase 5 but does NOT write the plan itself.

## When to use

- "hyperplan", "hpp", "/omcp:hyperplan"
- "adversarial plan", "hostile planning", "cross-critique plan"
- Planning that needs maximum rigor and surfacing of weak assumptions, blind
  spots, and over-engineering before any code is written.

## When not to use

- Trivial or single-file tasks (use `/omcp:plan` or direct execution).
- Pure exploration without a planning deliverable (use `/omcp:trace` or
  `explore`).
- When the user already has a vetted plan (use `/omcp:autopilot` or
  `/omcp:ralph` to execute it).
