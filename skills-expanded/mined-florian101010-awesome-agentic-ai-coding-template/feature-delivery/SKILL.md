---
name: feature-delivery
description: End-to-end feature workflow with planning, implementation, QA, and documentation sync. Use when delivering a new feature or larger enhancement.
disable-model-invocation: true
---

# Feature Delivery

Follow `.agent/workflows/feature-delivery.md` strictly.

Execution requirements:

1. Produce a concise feature brief (goals, non-goals, affected files, risks, acceptance criteria).
2. Implement in minimal, reviewable increments.
3. Run targeted validation for touched flows.
4. Update affected docs and `CHANGELOG.md`.
5. Run pre-commit checks before final handoff.
6. End with a DoD checklist status.

Never skip documentation sync.
