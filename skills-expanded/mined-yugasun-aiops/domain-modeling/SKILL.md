---
name: domain-modeling
description: Build and sharpen a project's domain model — glossary, ubiquitous language, ADRs. Use when changing the model, not just reading CONTEXT.md.
---

# Domain Modeling

Actively sharpen the domain model: challenge terms, stress-test scenarios, write decisions as they crystallise. Reading `CONTEXT.md` for vocabulary is a one-line habit — this skill is for **changing** the model.

## Where files live

Single context: `CONTEXT.md` + `docs/adr/`. Multi-context: `CONTEXT-MAP.md` points to per-area `CONTEXT.md` and ADRs. Create files lazily when you have something to write. Formats: [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), [ADR-FORMAT.md](./ADR-FORMAT.md).

## During the session

- **Challenge glossary** — call out terms that conflict with `CONTEXT.md`.
- **Sharpen fuzzy language** — propose precise canonical terms.
- **Stress-test with scenarios** — edge cases that force boundary decisions.
- **Cross-check code** — surface contradictions between stated rules and implementation.
- **Cross-check with code graph** — if `graphify-out/graph.json` exists, tell the user "用代码图谱验证模块边界假设" then query module boundaries and dependency density to validate concept boundary assumptions. Use `/code-graph query modules` for the overview and `/code-graph query deps <module>` to verify that proposed domain boundaries align with actual code boundaries.
- **Update CONTEXT.md inline** — one term at a time; glossary only, no implementation detail.

## ADRs — offer only when all three hold

1. Hard to reverse
2. Surprising without context
3. Result of a real trade-off with alternatives

Otherwise skip the ADR.
