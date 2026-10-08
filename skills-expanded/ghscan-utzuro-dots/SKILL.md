---
name: merge-crucible
description: Perform the final, holistic merge-readiness judgment using the master agent's full accumulated context. Use only when explicitly asked for the Merge Crucible or as the final gate after a Loop plan is complete; never use for individual tasks or commits.
disable-model-invocation: true
---

# Merge Crucible

This is the final branch-level judgment. It is the master agent's best work, not a fast commit review.

Perform the entire audit yourself in the current session. Never delegate to workers, subagents, `review-council`, or another model. Retain and use the accumulated conversation, decisions, implementation history, validation evidence, and user intent. Use the highest practical reasoning effort, slow down, and examine second-order effects before reaching a verdict.

Invoke this skill only at genuine merge readiness: explicitly via `/skill:merge-crucible` or once after a Loop plan has no implementation work left. Never invoke it for an individual task or commit.

Do not edit while auditing. Report first. If blockers are fixed afterward, personally rerun every affected audit section before changing the verdict.

## Establish truth

1. Determine the intended merge base from the user's argument or actual branch/upstream metadata. State the exact merge range.
2. Inspect staged, unstaged, untracked, ignored-but-relevant, and committed changes separately. Ensure nothing is hidden by the selected range.
3. Read all applicable `AGENTS.md` files and the complete relevant `PLAN.md`, `SPEC.md`, and `ADR.md` documents.
4. Reconstruct the user's real goal, explicit requirements, decisions, non-goals, guardrails, acceptance criteria, external actions, and acknowledged limitations from both documents and conversation context.
5. Inspect the full diff and commit sequence. Read every changed file in context plus directly related callers, imports, option definitions, generated sources, configuration, documentation, and operational workflows.

## Challenge the work

Review every concern normally covered by product, risk, and design reviewers yourself:

- **Product and behavior:** intended workflows, observable behavior, normal and failure paths, compatibility, usability, surprising outcomes, and whether the result actually solves the user's problem.
- **Production and security risk:** malformed input, partial failure, retries, interruption, concurrency, degraded dependencies, privilege boundaries, secrets, privacy, destructive operations, data loss, migration, rollback, recovery, deployment, boot, and platform differences.
- **Architecture and design:** ownership, boundaries, coupling, duplication, hidden side effects, state flow, naming, maintainability, extension pressure, generated-code boundaries, and consistency with established project patterns.

Go beyond the written plan:

- Identify requirements or acceptance criteria the plan should have included but missed.
- Challenge assumptions that were never validated.
- Look for contradictions between tasks, decisions, code, docs, and actual runtime behavior.
- Consider interactions and cumulative effects across commits that were safe individually but unsafe together.
- Ask what breaks on first install, upgrade, rollback, fresh state, existing state, alternate platform, interrupted execution, and operator error.
- Detect false confidence: lazy evaluation, mocked or synthetic data, checks that reference without forcing, documentation claims unsupported by runtime evidence, and tests that cannot prove the stated property.
- Distinguish true defects from accepted limitations, external prerequisites, and speculative concerns.

## Prove readiness

1. Build a requirement-to-evidence map. For every required outcome, identify implementation and validation evidence. Mark it complete, partial, missing, or contradicted.
2. Inspect prior validation evidence critically; do not accept summaries blindly.
3. Personally run the final checks still needed to determine readiness. Expensive builds and platform checks are appropriate at this one final gate when they materially change confidence.
4. Never claim a command, boot, platform, hardware path, destructive workflow, or external action was validated when it was not. Record the exact limitation and resulting risk.
5. Verify repository hygiene: no accidental secrets, generated payloads, stale artifacts, unintended lock changes, temporary planning files staged for merge, unexplained worktree changes, or unrelated commits.
6. Verify commits and documentation form a coherent, reviewable, operable change with safe commands and realistic recovery guidance.

For long-running, interactive, or multi-service final checks, use tmux when available. Tmux supervises commands only; the master still personally selects, runs, interprets, and reports every check. Use uniquely named panes or sessions, preserve and inspect actual exit status, and capture the output used as evidence. Do not parallelize checks when resource contention, shared state, or ordering could distort results. Stop services and remove sessions after evidence is recorded; if a failed session remains useful, report exact attach and cleanup commands.

## Findings

Report only evidence-backed issues, including plan omissions with a concrete consequence:

```markdown
### [P0-P2] <title>
- Location: `<path>:<line>` or `Plan omission`
- Scenario: <concrete failure or missing requirement>
- Impact: <why merge readiness is affected>
- Evidence: <code, diff, decision, or validation evidence>
- Remedy: <smallest safe correction>
```

P0 and P1 block merge. P2 does not block unless multiple P2 findings combine into material risk.

## Final report

Return:

1. **Merge range and repository state**
2. **Goal and plan assessment** — including missing or flawed plan assumptions
3. **Requirement-to-evidence matrix**
4. **Cross-cutting implications**
5. **Findings** — or `No findings`
6. **Validation performed** — exact commands and results
7. **Unvalidated paths, accepted limitations, and external actions**
8. **Verdict** — exactly one:
   - `READY TO MERGE`
   - `NOT READY TO MERGE`
   - `READY TO MERGE WITH DOCUMENTED LIMITATIONS`

A ready verdict requires no unresolved P0/P1 findings, no required plan work left open, no material cross-commit contradiction, and no readiness claim unsupported by evidence.
