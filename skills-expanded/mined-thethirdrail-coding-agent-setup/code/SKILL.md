---
name: code
description: |
  Implement approved plans, refactor, test, prepare commits or PRs, and handle deployment execution.
  Use when implementing a plan, coding a feature, refactoring, creating tests, preparing commits/PRs, or executing deploy/release steps.
---
# Code

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Implementation from plan | `code.md` | Read when executing an approved plan or checklist. |
| Refactoring | `refactor.md` | Read when reducing complexity, large files/functions, or duplication. |
| TDD workflow | `test-developer.md` | Read when tests should drive feature or bug work. |
| Test generation | `test-generator.md` | Read when scaffolding or expanding unit/regression tests. |
| Commit message | `git-commit-generator.md` | Read when generating a conventional commit message from staged changes. |
| Pull request preparation | `pr.md` | Read when preparing PR summary, labels, review state, or merge readiness. |
| Deployment/release | `deploy.md` | Read when rolling out to staging/production or creating release steps. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `code`, `refactor`, `test-developer`, `test-generator`, `git-commit-generator`, `pr`, `deploy`.

Related routers: `quality-repair`, `archive-manager`, `research-docs`.
