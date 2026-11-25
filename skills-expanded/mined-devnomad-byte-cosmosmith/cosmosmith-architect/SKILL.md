---
name: cosmosmith-architect
description: Design architecture, boundaries, data flow, reliability, security, and integration strategy for a Cosmosmith proposal. Use after proposal/design drafting, before frontend/backend implementation, or when a technical decision needs current official docs or architecture review.
---

# Cosmosmith Architect

## Purpose

Convert product intent into a small, buildable, evolvable technical design.

## Workflow

1. Read `proposal.md`, `design.md`, `task.md`, and relevant code.
2. Use web research for current framework, platform, security, or integration docs.
3. Define module/service boundaries, data flow, interfaces, persistence, and failure modes.
4. Identify risks that need subagent review: security, scale, data loss, cost, or migration.
5. Update the architecture section of `design.md` or write `docs/cosmosmith/architecture.md`.
6. Publish or update frontend, backend, QA, and DevOps tasks in `task.md`.

## Standards

- Prefer boring, proven technology unless novelty is part of the product value.
- Use Alibaba/P3C-style discipline for Java/backend conventions when applicable.
- Use OWASP-style thinking for web security.
- Keep deployability and observability in the design from the start.

## Completion

Stop when implementers have clear boundaries, interfaces, risks, and verification hooks.

