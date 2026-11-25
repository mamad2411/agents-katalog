---
name: reviewing-github-pr
description: Use when a user asks to review an existing GitHub PR end-to-end, including PR checkout, scope framing, acceptance-criteria verification, draft review preparation, and gated posting of a GitHub PR review event.
argument-hint: "[pr-url|pr-number|branch]"
disable-model-invocation: true
---

# Reviewing PRs

Review an already-open GitHub PR from the PR outward. This skill is read-mostly until the final GitHub PR review event, which requires explicit user approval before posting.

## When to Use

- The user wants a review of an existing PR rather than PR creation or merge.
- The review needs GitHub, Linear, design-doc, implementation-plan, or functional-spec context.
- The review should verify unchecked acceptance criteria before deciding whether to approve.

Do not use this skill for:

- creating the PR in the first place
- implementing code changes
- merging the PR
- closing the Linear issue after merge

## Core Framing Model

Always separate these three questions:

### PR Claim

What the PR says it does.

Source this only from:

- the PR body
- the actual code changes

### Required Scope

What the PR is supposed to do.

Source this from:

- the linked Linear issue
- Linear acceptance criteria
- related functional specs
- linked design documents
- linked implementation plans
- attached or linked documents reachable from the Linear issue

### Implemented Scope

What the code actually does.

Source this from:

- changed files
- tests added or changed
- docs updated in the PR
- behavior implied directly by the diff

The review decision depends on the gaps between `PR Claim`, `Required Scope`, and `Implemented Scope`.

## Workflow

1. Resolve the PR, look for PR-body `Fixes` references such as `VD-1234`, `VU-1234`, `AD-1234`, or a similar 2–3 letter prefix plus number, and create a temporary sibling review worktree. Use the referenced issue key as the default Linear lookup input, then resolve it through MCP. See [`references/pr-resolution.md`](references/pr-resolution.md).
2. Gather context from the PR body, code changes, Linear, and repo docs. See [`references/context-gathering.md`](references/context-gathering.md).
3. Verify unchecked acceptance criteria from Linear and unchecked PR-body task-list items. See [`references/ac-verification.md`](references/ac-verification.md).
4. Run the review decision flow, including code review and simplification review. See [`references/review-decision.md`](references/review-decision.md).
5. Draft the GitHub PR review event, present it to the user, and wait for explicit user approval before posting. See [`references/github-review-posting.md`](references/github-review-posting.md).
6. Clean up the temporary review worktree. See [`references/worktree-cleanup.md`](references/worktree-cleanup.md).

## Hard Gates

- Never treat Linear alone as the source of what the PR claims to do.
- Never silently guess uncertain document or spec mapping; ask once and proceed from the answer.
- Never check off a Linear or PR acceptance criterion without code or test evidence.
- Never proceed to approval while any relevant acceptance criterion remains open or unproven.
- Never post a GitHub PR review event without explicit user approval.
- Never leave the temporary review worktree behind on a successful run.

## Acceptance Criteria Handling

- Treat unchecked PR-body task-list items as PR-side acceptance criteria.
- Treat linked Linear acceptance criteria as part of the review contract when a linked Linear issue is present.
- If any acceptance criterion remains open, ambiguous, blocked, or unproven, stop the approval path and draft blocker-oriented next steps instead of approving.

## Outcome Types

The proposed GitHub review event must be one of:

- `APPROVE`
- `REQUEST_CHANGES`
- plain `COMMENT`

If the PR is badly mis-scoped, the drafted review may recommend closing it rather than trying to force it through review.
