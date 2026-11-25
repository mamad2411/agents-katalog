---
name: brainstorming
description: "Compatibility entrypoint for unresolved MEDIUM/LARGE design choices. PM and Technical Architect workflows own the SDD rules; do not load this skill for clear or approved work."
---

# Brainstorming Compatibility Entry

This directory and skill name remain stable for existing installations. The canonical behavior lives in `core-workflow-contract`, `senior-project-expert-workflow`, and `technical-architect-workflow`.

When triggered, resolve only choices that change behavior, contracts, ownership, security, data, UX, or delivery scope:

1. Record the simplest safe interpretation when only one exists.
2. Otherwise present 2-4 concise options with trade-offs through the runtime's native ask UI; PM owns user questions.
3. Lock the chosen direction, non-goals, constraints, blast radius, and decision provenance before the Spec Bundle is written.
4. Do not implement while a route-changing decision remains open.

Return the repository-specific handoff shape; do not repeat general SDD reasoning:

```markdown
## Design Direction Summary
- chosen_directions:
- decision_provenance: user_confirmed | single_reasonable_interpretation | agent_vote_fallback
- non_goals:
- constraints:
- blast_radius:
- ADRs_needed:
- open_questions:
```

Only PM/top-level may ask the user. If native ask is unavailable, follow the fallback and safety boundaries in `core-workflow-contract`; never invent `user_confirmed` or use agent voting for business semantics, security, destructive actions, public contracts, schema, or credentials.
