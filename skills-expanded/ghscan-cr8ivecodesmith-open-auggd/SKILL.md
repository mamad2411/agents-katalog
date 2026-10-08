---
name: oag-spec-template
description: Template and structure for plan/spec.md — the workspace-wide specification document.
compatibility: opencode
---

# Spec Template

Artifact: `<WS>/plan/spec.md`
Type: rewritten as understanding of the feature evolves; not append-only

## Purpose

The spec is the shared contract between exploration, planning, development, and review. It
answers: what are we building, for whom, and under what constraints? It does not describe
how to build it — that belongs in the iteration plan and the implementation.

Keep the spec thin. It is a living reference, not a design document. Iteration plans carry
the implementation detail.

## When to write / update

Write `spec.md` when:
- A new workspace is planned for the first time
- Exploration reveals that the problem statement needs sharpening
- Review or development reveals a constraint or scenario that was missing

Do not rewrite the spec during development to match what was built. If implementation reveals
a spec gap, update the spec and note the discrepancy.

## Template

```markdown
# Spec — <Feature / Work Item Name>

## Status
- Workspace: <workspace-id>
- Updated: <ISO 8601 date>
- Status: draft | active | partial | stable

## Problem
<One short paragraph. Plain language. What problem does this solve and for whom?>

## Goals
- [ ] <goal 1 — observable outcome>
- [ ] <goal 2 — observable outcome>

## Non-goals
- <explicit exclusion with brief rationale>
- <explicit exclusion with brief rationale>

## Users / actors
- <who initiates the interaction>
- <who is affected>

## Core scenarios
Use scenario IDs (S1, S2, ...) for cross-referencing in iterations and reviews.

### S1 — <title>
- Given: <initial context>
- When: <action taken>
- Then: <expected outcome>

### S2 — <title>
- Given:
- When:
- Then:

## Constraints and invariants
- Security: <any security requirements or invariants>
- Data: <data shape, validation, or migration constraints>
- Performance: <performance requirements if any>
- UX / CLI: <interface constraints>
- Compatibility: <backward compatibility or migration requirements>
- Operational: <deployment, configuration, or environment constraints>

## Out of scope
- <explicit exclusion — what this spec does not cover>

## Open questions
- <question — who is responsible for resolving it>

## Notes
<any other relevant context, decisions made, or references>
```

## Writing guidance

**Goals**: write as observable outcomes, not tasks. "Users can list workspaces by number"
not "add list command." Each goal should be verifiable.

**Non-goals**: just as important as goals. An explicit non-goal prevents scope creep during
development and review. If you are unsure whether something is in or out, make it explicit.

**Scenarios**: use Given/When/Then as a thinking tool, not ceremony. The scenario IDs
(S1, S2, ...) are the primary link between spec, iteration plans, and review findings.
Assign IDs once and keep them stable — do not renumber.

**Constraints**: be specific. "Security: API keys must not appear in log output" is useful.
"Security: follow best practices" is not.

**Out of scope**: if exploration surfaced directions that were explicitly rejected, list them
here with a brief reason. This prevents relitigating the same decisions during planning.
