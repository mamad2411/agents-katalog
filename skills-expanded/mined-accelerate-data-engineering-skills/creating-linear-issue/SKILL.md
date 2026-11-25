---
name: creating-linear-issue
description: >-
  Use when the user asks to create, file, log, open, draft, refine, decompose,
  or turn a request, bug, spike, or follow-up into a Linear issue or Linear
  ticket before work continues.
argument-hint: "[request-or-issue-context]"
---

# Creating Linear Issues

## Overview

Turn a request into a clear Linear issue only after repo discovery, field resolution, source-doc review, user confirmation, and draft approval. Product scope belongs in the issue; implementation sequencing belongs in the later implementation plan.

## When to Use

- User asks to create an issue, file a bug, track a feature, or break down an existing request.
- The request needs Linear metadata, source context, or decomposition before it can be safely filed.
- Do not use for implementation, PR raising, merge, closeout, or cleanup.

## Workflow

| Step | Requirement |
|---|---|
| 1 | Classify the request as `feature`, `bug`, or `spike` |
| 2 | Search the codebase and existing Linear issues before asking the user |
| 3 | Resolve `project`, `milestone`, `assignee`, `cycle`, and any selected-team User Flow requirements using `references/field-resolution.md` |
| 4 | For selected teams, require and read the matching functional spec before issue creation |
| 5 | Search and read related design docs; record `not_applicable` when none are related |
| 6 | Use `superpowers:brainstorming` when a feature is broad, non-trivial, or still has product forks |
| 7 | Use `references/bug-intake.md` for bug issues |
| 8 | Use `references/issue-breakdown.md` when the request is too large for one issue |
| 9 | Confirm resolved fields with the user in one question |
| 10 | Show the issue draft and create/update only after approval |

## Hard Gates

- Do not create an issue without `project`, `milestone`, `assignee`, and `cycle` unless the user explicitly approves an exception.
- For `Studio`, `Roadmap`, and `Utilities`, do not create an issue without one confirmed `User Flow` child label and an exact matching `docs/functional/<User Flow label>/` folder.
- Do not draft while critical fields, functional-spec gates, brainstorming outcomes, bug-intake gaps, or decomposition gaps remain unresolved.
- Do not ask the user for details the codebase, functional spec, design docs, or existing Linear issues already answer.

## Source Context

For selected-team issues:

- read the functional spec before drafting
- search `docs/design/` by User Flow label, feature name, domain terms, and linked-document titles
- cite the functional spec path and related design doc paths in the Linear description for downstream implementation traceability

For other teams:

- skip User Flow resolution entirely
- do not fail solely because a functional spec is absent
- still search codebase and existing Linear issues for scope, duplication, and wording

## Issue Draft

Use `references/issue-drafting.md` for draft structure and approval content.

The issue body must stay product-level:

- no implementation plans
- no file paths, modules, classes, or architecture mechanics except source-doc traceability paths
- literal Markdown only; never escaped `\n` or escaped checkboxes

## Linear Operations

Use available Linear MCP tools for issue, project, milestone, cycle, label, and comment operations. Retry once on tool failure, then stop and report the exact failing step.

Read `references/linear-operations.md` for User Flow child-label lookup mechanics. Query User Flow child labels at workspace scope and filter by parent label; do not hard-code label names.

## Common Mistakes

- Creating before field confirmation or draft approval.
- Filing selected-team issues without a User Flow label and matching functional spec.
- Turning the feature request into an implementation plan.
- Splitting large work by frontend/backend layer instead of user-value slices.
- Filing bugs without expected behavior, actual behavior, reproduction detail, or consistency.

## References

- [`references/field-resolution.md`](references/field-resolution.md) — issue kind, critical fields, selected-team User Flow rule, and confirmation question
- [`references/linear-operations.md`](references/linear-operations.md) — Linear MCP tool policy and User Flow child-label lookup mechanics
- [`references/issue-drafting.md`](references/issue-drafting.md) — draft approval content and issue body template
- [`references/issue-breakdown.md`](references/issue-breakdown.md) — vertical-slice decomposition for large features or parent issues
- [`references/bug-intake.md`](references/bug-intake.md) — bug issue intake checks before drafting
