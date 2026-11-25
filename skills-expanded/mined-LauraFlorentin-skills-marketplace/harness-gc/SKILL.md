---
name: harness-gc
description: Audit and repair stale agent instructions, broken documentation links, inconsistent feature or task state, obsolete plans, invalid architecture rules, and noisy harness configuration. Use for periodic harness maintenance or when agents are confused by repository drift; preserve active work and require confirmation before deletions.
---

# Harness GC

Reduce drift without erasing history or user intent. Begin with a report; apply only supported, scoped fixes.

## Audit

Check:

- repository-map and documentation links resolve;
- instructions match current commands, paths, stack, and contributor workflow;
- duplicated or contradictory rules across instruction files;
- feature, plan, progress, branch, and task-lock state agree;
- completed or abandoned plans are clearly archived rather than silently deleted;
- architecture rules describe real boundaries and their checker still works;
- generated reports and progress logs have a retention policy;
- hook configuration is valid, useful, and non-destructive;
- runtime state and secrets are ignored appropriately;
- harness scripts are syntactically valid and idempotent.

Run read-only project validation to determine whether a supposedly complete feature still works. Do not flip status from passing to failing, or vice versa, without evidence.

## Prioritize

- **P0:** invalid configuration, unsafe automation, or broken instructions that block work.
- **P1:** stale paths, contradictory task state, or incorrect architecture guidance likely to cause defects.
- **P2:** obsolete, duplicated, or overly verbose context.
- **P3:** optional improvements with no current operational impact.

## Repair rules

- Update stale links to current paths when the intended target is clear.
- Consolidate duplicated guidance into one source and link to it.
- Preserve requirements and acceptance criteria; flag product changes for user approval.
- Treat a task lock as owned work. Report a stale candidate and ask before removal.
- Archive useful historical context with a date and reason; do not delete it merely because it is old.
- Prefer a small deterministic validator over additional prose when a rule is mechanically testable.
- Never use GC to stage, commit, stash, reset, revert, or clean the worktree.

## Verify

After approved fixes:

- rerun link, JSON, shell, architecture, and project checks;
- inspect the diff for unrelated changes;
- confirm instruction files remain concise and non-conflicting;
- write a report only if the repository uses persistent GC reports.

Return issue counts by priority, fixes applied, items requiring a user decision, verification results, and recommended next maintenance trigger. Do not manufacture a health score without defined criteria.
