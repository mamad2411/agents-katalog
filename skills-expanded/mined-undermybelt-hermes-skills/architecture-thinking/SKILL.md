---
name: architecture-thinking
description: Use when a user needs architecture-first framing before implementation, wants to turn requirements into constraints, quality attributes, trade-offs, C4 views, or ADRs, or wants a guided architecture learning path from the awesome-architecture knowledge base.
---

# Architecture Thinking

Use the `awesome-architecture` tutorial as a pre-implementation architecture lens. Stay at the architecture level by default; do not collapse into framework or library picks unless the user explicitly asks.

## Source Of Truth

- Local source repo: `~/.hermes/external-repos/awesome-architecture`
- Tutorial map: `references/tutorial-map.md`

## When To Use

- `架构思维`, `系统设计基础`, `架构教程`
- `质量属性`, `架构取舍`, `一致性`, `可用性`, `成本`
- `C4`, `架构图`, `ADR`, `架构演进`
- New-system design before implementation starts

For concrete system classes, route to `comm/arch/general-system-templates` or `comm/arch/ai-system-templates`.

## Workflow

1. Restate the goal, constraints, scale assumptions, and failure budget.
2. Pick the smallest relevant chapters from `references/tutorial-map.md`.
3. Structure the answer as:
   - problem shape
   - constraints
   - quality attributes
   - candidate architecture shape
   - trade-offs
   - evolution triggers
4. If the user is talking about diagrams, switch to the C4 lens from chapter 03.
5. If the decision should be durable, end with a short ADR stub:
   - Context
   - Decision
   - Consequences

## Guardrails

- Default to architecture reasoning, not stack shopping.
- Explain why a shape fits before describing how to build it.
- Use the repo's language of constraints, quality attributes, and trade-offs.

## References

- `references/tutorial-map.md`

