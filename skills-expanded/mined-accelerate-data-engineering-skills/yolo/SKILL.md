---
name: yolo
description: >-
  Use when the user wants to go from a feature description to an open PR in one
  uninterrupted flow, asks to yolo a change, says do it all, or requests a
  single-shot create-implement-PR workflow.
argument-hint: "[feature description]"
disable-model-invocation: true
---

# Yolo — Single-Shot Feature Delivery

## Overview

Run the full feature delivery chain — Linear issue creation, implementation, and PR raising — in one invocation. Each phase runs the corresponding skill workflow in full. All quality gates from `implementing-linear-issue` are preserved. The flow stops after the PR is raised; it does not merge or close the issue.

## When to Use

- User says "yolo this", "single shot", "do it all", "full flow", or any equivalent shorthand for the uninterrupted create-implement-PR chain.
- User explicitly asks to go from a feature description to an open PR without manual skill hand-offs.

Do not use when:

- The issue already exists — start from `implementing-linear-issue` directly.
- Implementation is already done — use `raising-linear-pr` directly.
- The user only wants a ticket — use `creating-linear-issue`.

## Quick Reference

| Phase | Skill workflow | Done when |
|---|---|---|
| 1 — Create Issue | `creating-linear-issue` | Issue created and confirmed |
| 2 — Implement | `implementing-linear-issue` | Final commit, clean worktree |
| 3 — Raise PR | `raising-linear-pr` | PR open, issue In Review |

## Implementation

### Phase 1 — Create Issue

Run the full `creating-linear-issue` workflow exactly as specified in that skill.

Classify, dedupe, resolve all four critical fields, confirm with the user, enter plan mode, and create the issue after approval. All rules from `creating-linear-issue` apply without exception.

On success emit: `✅ Issue created (AD-N) — proceeding to implementation.`

**On failure:** Report the exact failure. Nothing has been created; no recovery action is needed. Do not proceed to Phase 2.

---

### Phase 2 — Implement

Run the full `implementing-linear-issue` workflow exactly as specified in that skill, using the issue created in Phase 1.

Create the branch and worktree, plan the implementation, implement in reviewable slices with checkpoint commits, run all required quality gates (code review, simplification review, test coverage review, AC review), update Linear, and create the final implementation commit. All rules from `implementing-linear-issue` apply without exception. Do not push. Do not create a PR.

On success emit: `✅ Implementation complete — proceeding to PR.`

**On failure after Phase 1 succeeded:** Surface the exact failure and provide this recovery instruction:

> Resume with `/engineering-skills:implementing-linear-issue <issue-id>`

Do not proceed to Phase 3.

---

### Phase 3 — Raise PR

Run the full `raising-linear-pr` workflow exactly as specified in that skill.

Rebase onto the default branch, run post-rebase quality gates, push, create the PR with issue-linking, and move the issue to `In Review`. All rules from `raising-linear-pr` apply without exception.

On success emit: `✅ PR raised — awaiting review.`

**On failure after Phase 2 succeeded:** Surface the exact failure and provide this recovery instruction:

> Resume with `/engineering-skills:raising-linear-pr`

---

## Stop Condition

Stop after Phase 3. Do not merge. Do not close the issue. Do not run `closing-linear-issue`.

The next step is human: review and approve the PR, then run `/engineering-skills:closing-linear-issue` after merge.
