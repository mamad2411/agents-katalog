---
name: implementing-linear-issue
description: Use when asked to implement, fix, build, or work on an existing Linear issue in this repository, and coding should stop before PR creation
argument-hint: "[issue-id]"
---

# Implementing Linear Issues

## Overview

Implement an existing Linear issue, but stop before PR creation. This skill owns the local implementation phase: branch/worktree setup, issue/code/spec/design discovery, pre-implementation routing, plan approval, TDD implementation, checkpoint commits, local verification, independent subagent quality gates, Linear implementation updates, and a final local commit.

## When to Use

- User asks to implement, fix, build, or work on a Linear issue.
- The issue already exists and needs repository changes.
- Do not use for issue drafting, PR raising, merge, closeout, or cleanup.

## Workflow

### Phase 1: Setup (always runs)

| Step | Requirement |
|---|---|
| 1 | Read the Linear issue to retrieve `gitBranchName` from the issue metadata |
| 2 | Create or checkout the worktree at `../worktrees/<branchName>` using `./scripts/worktree.sh <branchName>` from the repo root |
| 3 | Stop immediately if branch or worktree setup fails |

### Phase 2: Discovery (always runs)

| Step | Check | Output or stop |
|---|---|---|
| 4 | Read Linear description, comments, attachments, labels, and linked documents | Issue context |
| 5 | Identify the Linear team | Team-scoped User Flow rule |
| 6 | For Studio, Roadmap, and Utilities issues, find the issue's User Flow label | Stop if missing |
| 7 | For Studio, Roadmap, and Utilities issues, require exact folder `docs/functional/<User Flow label>/` | Stop if missing |
| 8 | For Studio, Roadmap, and Utilities issues, read the matching functional spec before clarification, planning, or coding | Functional spec path |
| 8a | For Studio, Roadmap, and Utilities issues, check whether the change affects end-user UI labels, workflows, or visible behavior; if so, user guide updates are part of implementation scope | User guide obligation |
| 9 | Search the codebase before user clarification | Relevant files and behavior |
| 10 | Search `docs/design/` by issue key, User Flow label, feature name, domain terms, and linked-document titles | Related design docs, or `not_applicable` |
| 11 | Search `docs/plan/` before creating a new plan | Existing plan path, or new plan needed |

For Studio, Roadmap, and Utilities issues, the User Flow label and functional-spec folder are hard prerequisites. Do not plan, code, or work around either gap. For other teams, do not fail solely because no User Flow label or functional spec exists; record functional spec as `not_applicable`.

| Design-doc situation | Action |
|---|---|
| Referenced related design doc exists | Read it before implementation planning |
| Referenced related design doc is missing | Treat as a context gap and route through design handoff |
| No related design doc after search | Record `not_applicable` in the plan and Linear updates |

### Phase 3: Routing Decision (pick one path)

After discovery, evaluate the conditions below. **The first matching condition wins** — do not evaluate further rows.

| Priority | Condition | Next skill |
|---|---|---|
| 1 | User explicitly asks to brainstorm, think through approach, or explore options; OR discovery reveals 2+ viable implementation strategies, delivery approaches, architectural paths, or technology choices with no chosen path — examples: push vs. queue-based delivery, REST vs. GraphQL, sync vs. async processing | `superpowers:brainstorming` |
| 2 | Functional behavior or product flow is missing, stale, or disputed between the issue and the user flow doc | `authoring-functional-spec` |
| 3 | Bug report, unexplained defect, reproduction failure, flaky behavior, regression, or unexpected test result | `superpowers:systematic-debugging` |
| 4 | Durable architecture, data model, cross-service flow, security, migration, permissions, auditability, API/module boundary, or UI interaction contract is not covered | `authoring-design-spec` |
| 5 | Issue asks to simplify, untangle, modularize, split, consolidate, or replace existing code without behavior change | `superpowers:writing-plans` |
| 6 | Non-bug implementation or multi-module change is ready after hard gates and discovery; OR complex bug fix after debugging — use `superpowers:writing-tests` for test scenario planning, then `superpowers:writing-plans` for implementation sequencing | `superpowers:writing-tests`, then `superpowers:writing-plans` |
| 7 | Simple confirmed single-module bug fix with root cause isolated and fix direction confirmed by user | Phase 4 (skip step 9) |

After the invoked skill completes, proceed to Phase 4. Paths 1-4 return to this routing table for re-evaluation before implementation. After brainstorming selects an approach, re-evaluate: if the issue is now a multi-module implementation with a chosen path, it matches priority 6 (`superpowers:writing-tests` then `superpowers:writing-plans`). After debugging isolates a root cause, re-evaluate: if the fix is multi-module, it matches priority 6; if single-module and confirmed, it matches priority 7.

### Phase 4: Execution

| Step | Requirement |
|---|---|
| 9 | If a plan was created, route to `superpowers:subagent-driven-development` when it has 2+ tasks with no shared files and no ordering dependency; otherwise implement sequentially using `references/implementation-quality.md` |
| 9a | Read existing tests before changing or adding tests for the affected modules |
| 9b | For Studio, Roadmap, and Utilities issues, after quality gates pass and before handoff, compare as-built behavior against the functional spec; if they diverge, route to `authoring-functional-spec` to reconcile |
| 10 | Update Linear with source traceability and AC status using `references/linear-update-and-handoff.md` |
| 11 | Run required validation and all required independent subagent quality gates before handoff. These always include changed-area validation, affected skill evals, code review (`superpowers:requesting-code-review`), simplification review (`superpowers:code-simplifier`), test coverage review (`superpowers:requesting-code-review`), acceptance-criteria review, and AI PR review preview (`ai-pr-review-guide` dry-run on the local diff) |
| 12 | Use `superpowers:receiving-code-review` before applying any quality-gate, human, or external review feedback. If the AI PR review preview verdict is NOT READY, present its findings to the user with a fix-vs-reject proposal, apply the user's decision, and re-run the preview. Stop the loop on `READY TO MERGE` or when every remaining finding is user-rejected with recorded justification. Cap the loop at 5 review turns total (the first run counts as turn 1); if turn 5 still leaves accepted findings open, stop and report them instead of continuing |
| 13 | Check off only completed acceptance criteria in the main Linear requirements section |
| 14 | Post a final Linear implementation note that references the functional spec, related design documents, related implementation plan, verification, review outcomes, and remaining risks |
| 15 | Create the final implementation commit and leave the worktree clean |
| 16 | Stop with a clean worktree and hand off to `raising-linear-pr`; do not push or create a PR |

## Required References

| Reference | When to load |
|---|---|
| [`references/implementation-quality.md`](references/implementation-quality.md) | During Phase 4 execution and quality gates |
| [`references/linear-update-and-handoff.md`](references/linear-update-and-handoff.md) | During Phase 4 Linear updates |
| [`references/refactor-planning.md`](references/refactor-planning.md) | When routing path 6 (refactor) is selected |
| [`references/interface-design.md`](references/interface-design.md) | When routing path 4 (design spec) is selected |

## Branch and Worktree

- Always create or reuse the issue branch and worktree before implementation work starts, regardless of issue size.
- Do not make code changes in the main checkout.
- Do not inspect or edit target files from the main checkout once branch/worktree setup begins.
- If branch creation or worktree creation fails, stop immediately and report the exact failing command.

## Linear Status

- Stop on `Done`, `Cancelled`, or `Duplicate`.
- Move `Todo` to `In Progress` and assign to `me`.
- Move `In Review` back to `In Progress` before continuing.

## Stop Conditions

- branch or worktree setup fails
- User Flow label is missing from a Studio, Roadmap, or Utilities Linear issue
- `docs/functional/<User Flow label>/` is missing for a Studio, Roadmap, or Utilities Linear issue
- permanent file deletion or new external dependency is needed
- unresolved architecture, product, security, data, migration, or interface fork
- unresolved error after two attempts
- required local or independent subagent quality gate still fails after retry
- required changes exceed issue scope

## Common Mistakes

- Coding before branch/worktree setup and source discovery are complete.
- Skipping functional spec, design doc, or implementation-plan context.
- Treating bug fixes as normal implementation before root cause and fix direction are confirmed.
- Asking ad hoc clarification questions when brainstorming, design, debugging, or planning handoff applies.
- Skipping user guide updates when end-user visible behavior changes.
- Changing tests without reading existing tests first.
- Skipping functional spec reconciliation for Studio, Roadmap, or Utilities issues when as-built behavior diverges.
- Pushing, creating a PR, moving to `In Review`, merging, or cleaning up from this phase.

## Boundary

Do not push, create or update a PR, move the issue to `In Review`, merge, close, or remove the worktree. The next skill is `raising-linear-pr`.
