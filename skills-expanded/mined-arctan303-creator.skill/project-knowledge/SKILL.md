---
name: project-knowledge
description: Maintain current project knowledge, capture explicit design and release conventions during ordinary work, reconcile superseded decisions, and retire obsolete tasks without losing historical evidence. Use for scoped knowledge upkeep or authorized documentation cleanup, not for inventing product decisions or changing global workflow policy.
---

# Project knowledge

## Purpose

Keep the project's current state, effective expectations and active work easy to recover. Capture useful project conventions from ordinary collaboration without requiring a separate “remember this” request. Preserve one authoritative home for each rule and the evidence for changes.

## Trigger

- The user states or corrects a project design, development or release convention during an authorized task.
- Implemented or verified work changes the relevant current-state entry, limitation or task status.
- A capability or decision is replaced or removed, affecting current documentation or unfinished work.
- The user requests repository orientation, documentation reconciliation, cleanup or migration. Orientation is read-only unless editing is also authorized.

Do not run a repository-wide sweep on every turn. Update only the affected scope at meaningful decisions, handoffs or milestones. A transient tool failure belongs in the task; a workflow defect belongs to `self-evolver`. New product choices still belong to the product/design skills.

## Required context

- Repository instructions, working-tree changes and the user's effective scope, authorization and restrictions.
- Registered entrypoints in `.creator/docs-state.json`, or verified equivalent README, MANUAL or PROJECT-CONTEXT files.
- The affected current rules, relevant active tasks and evidence; historical material only when needed to resolve a replacement or source.
- The user's actual statement or a stable task/decision reference. Distinguish it from an inference and from observed implementation.

## Workflow

1. Identify the narrow knowledge change and its existing owner. Reuse Design-Principles, Design-Brief, Development-Release or their equivalents; do not create a universal memory file containing copies of them.
2. Classify the information as an explicit project convention, a verified project fact, an inferred candidate, or a task-specific authorization/constraint. Preserve its scope and source. Clear project conventions can be captured immediately; frequency is not a prerequisite. Inferences remain candidates and do not become user decisions through repetition or silence.
3. Reconcile current clauses in place, including affected references and exceptions. Record what replaces or withdraws the old clause. Retain the original historical outcome and unknowns; do not merely append an opposite rule.
4. For affected tasks, decide current applicability separately from historical implementation, validation, review and release. Removed capabilities close obsolete validation obligations as retired, not passed. For partial replacement, retain the still-effective outcomes and obligations with their actual evidence.
5. Update verified current facts and relevant active-plan links after implementation or verification. Keep unimplemented requirements explicit. Use a small entrypoint/index with links; keep detailed decisions, commands and evidence in their existing homes.
6. At an authorized cleanup or milestone, consolidate only the affected material, preserve unique evidence and repair navigation. Do not delete a document because it is old, large or unreferenced. Do not alter concurrent work, sibling projects or global preferences without scope authorization.
   For design-library adaptation, follow the [shared procedure](../../../.creator/references/design-adaptation.md): reconcile chosen decisions into existing project owners, retain local exceptions and provenance, and keep unadopted or newer library material from becoming runtime policy. Design-brief-builder owns unresolved design choices; this skill owns knowledge reconciliation.
7. Check relevant structure and links, then review the meaning of the changes: no invented decisions, resurrected retired tasks, lost live requirements or inflated evidence. Follow the user's language and the existing document's language. Briefly report the actual update and any material uncertainty.

## Output

- Updated authoritative project documents and lightweight navigation, only where necessary.
- Traceable sources, applicability, replacement/exception relationships and evidence boundaries for affected rules or tasks.
- Concise handoff with what changed, what is current, remaining live work and checks actually performed. No-change orientation may return only the findings.

## Stop or escalate

- A conflict cannot be resolved without choosing new user-visible behavior: retain the uncertainty and involve the product/design skill; continue independent authorized work.
- A convention's broader scope is only inferred: keep it a candidate. Do not promote project preferences across repositories or into global workflow rules without authorization.
- Read-only scope, unknown document ownership or concurrent changes prevent a safe edit: preserve the material and explain the specific gap.
- Never persist secrets or unnecessary personal data. Remembering a release procedure does not authorize the next release, production migration or other external action.

## References

Read [stage-contract.md](references/stage-contract.md) for classification, retirement and examples. The shared [project knowledge reference](../../../.creator/references/project-knowledge.md) describes document ownership and checker declarations. Apply the [workflow contract](../../../.creator/references/workflow-contract.md) within the current task's scope.
