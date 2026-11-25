---
name: to-docs
description: Analyze decisions made during implementation, review, or design work and distinguish project-wide guidance from route-specific fixes, already-documented rules, and premature patterns. Use when the user asks which lessons or decisions deserve inclusion in project documentation, wants to review proposed guidelines before approving documentation changes, or asks to update project guidance from recent work.
---

# To Docs

Turn recent work into durable guidance without treating the session as a changelog.

## Phase 1: Propose

Do not edit project documentation during this phase.

1. Read the repository instructions and the existing documents that could own the guidance. Distinguish committed guidance from uncommitted documentation drafts; do not treat a draft as approved policy merely because it exists in the worktree.
2. Use the conversation or user-specified work as the authoritative scope. Reconstruct its material decisions from the discussion, relevant code, and focused diffs. Include implicit decisions revealed by rejected alternatives or later corrections. Treat unrelated dirty-worktree changes as out of scope, and use diffs as evidence rather than as a backlog of decisions to document.
3. Evaluate each decision instead of merely classifying it. Ask:
   - Would this guide work on another resource or page?
   - Does it express an intended invariant rather than describe the current implementation?
   - Would a future coding agent make a materially better choice by knowing it?
   - Can its scope, exceptions, and failure cases be stated clearly?
   - Is it supported by repeated use or strong design reasoning rather than one accidental example?
   - Is it already documented adequately?
   - Does it contradict existing guidance, lint rules, tests, or shared modules?
4. Test candidate rules against counterexamples. Reject or narrow rules that become semantically wrong outside the original case.
5. Classify each material decision as one of:
   - **Document**: durable, general guidance.
   - **Refine existing guidance**: already present but incomplete, misleading, or contradicted by the new decision.
   - **Already covered**: requires no documentation change.
   - **Keep local**: resource, route, copy, naming, or implementation detail.
   - **Defer**: plausible pattern without enough evidence to make it a project rule.
6. Present only the meaningful results. For every proposed documentation change include:
   - the generalized rule;
   - why it deserves project-wide status;
   - its scope and exceptions;
   - the document that should own it;
   - contradictions or related enforcement that must be updated with it.
7. Explicitly list important decisions rejected from project documentation and explain why.
8. End by requesting approval of the proposal. Do not edit documentation until the user explicitly approves it.

If the decision history is unavailable or the requested scope cannot be separated reliably from unrelated work, state that limitation and ask for the missing fixed point or decision context instead of inferring policy from the whole worktree.

Prefer modifying an existing authoritative document over creating a new one. Avoid duplicating the same rule across documents; put the complete rule in one owner and use short cross-references elsewhere.

## Phase 2: Apply after approval

After explicit approval:

1. Invoke `writing-for-agents` and apply its writing discipline throughout this
   phase. If it is unavailable, stop and ask the user to install it with
   `npx skills@latest add mattpocock/skills --skill writing-for-agents`.
2. Re-read every affected document before editing it.
3. Apply only the approved rules and preserve the repository's terminology and language requirements.
4. Reconcile the full documentation set: remove obsolete guidance, resolve contradictions, and update cross-references.
5. Update enforcement when the documented policy is mechanically checked, such as lint configuration, shared modules, or tests. Do not leave documentation and enforcement disagreeing.
6. Keep resource-specific examples illustrative; do not turn their names, routes, fields, or query parameters into universal policy.
7. Run checks proportional to the changed documentation and enforcement. Report checks not run.
8. Summarize the durable rules written, their owning documents, and any approved follow-up work still needed in code.

## Quality bar

A useful guideline tells a future agent what to choose, why, where it applies, and when not to apply it. Reject rules that only restate the final code, encode personal preference without a project invariant, or prescribe a mechanism where a semantic rule would age better.
