---
name: ai-native-prd-architect
description: Use when turning a feature idea into an implementation-ready PRD with traceable REQ IDs, acceptance criteria, NFRs, risks, data model, and task slices for /agileteam Phase 0.
---

# AI-native PRD Architect

Produce a buildable, testable PRD without filling gaps by guessing.

## Workflow
1. Restate the goal and target repository.
2. Create stable `REQ-###` identifiers.
3. Define scope, non-goals, actors, data model, interfaces, constraints, NFRs, security/privacy risks, rollout and rollback notes.
4. Write Given/When/Then acceptance criteria for every REQ.
5. Build a traceability matrix with `REQ`, `test`, `task`, `evidence`, `wired-in-prod?`, and `evidence-class` columns.
6. Mark unknowns explicitly as `MISSING`, `OPEN QUESTION`, `ASSUMPTION`, or `BLOCKER`.

## Hard rules
- Never close a missing requirement through plausibility. Ask the user or call `brainstorming`.
- Every task must trace back to at least one REQ.
- Every REQ must have at least one machine-checkable acceptance signal.

