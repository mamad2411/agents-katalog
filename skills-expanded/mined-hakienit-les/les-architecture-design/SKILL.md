---
name: les-architecture-design
description: Design or deepen a module boundary when ownership, coupling, or interface shape materially affects the change.
invocation: model
maturity: stable
route: architecture
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/architecture.md","../../policies/rules/technical-decisions.md","../../policies/rules/file-organization.md"]
---

# Architecture Design

## Invoke

Inherit `../les-bootstrap/SKILL.md` and architecture policy.

## Inputs

Boundary concern, consumers, constraints, and current design.

## Procedure

1. Identify ownership and public contract. Done when: the boundary has one purpose.
2. Compare the smallest viable seams. Done when: trade-offs are explicit.
3. Record the chosen interface and verification. Done when: consumers can use it.

## Output

Boundary decision, contract, and evidence plan.

## Guardrails

Do not add speculative layers or select project-owned tools.

## Verification

Show the design preserves required consumers or flag `PENDING_USER_ACTION`.

Bootstrap LES. Map owners, callers, invariants, and dependency direction; compare
the smallest viable boundary options and choose one with a reversal path. Output
the interface and project decision needed for implementation. Stop before editing
until durable tradeoffs are approved; verify every dependency has one clear owner.
