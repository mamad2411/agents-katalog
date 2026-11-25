---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Convert tasks.md into deterministic, import-ready issue artifacts without remote mutation.
---

## Mission
Create an idempotent export that preserves task traceability, dependencies, acceptance checks, and phase grouping.

## Inputs and Outputs
- Read `spec.md`, `plan.md`, `tasks.md`, and repository issue conventions.
- Write `.agents/memory/issues-export.md` plus a summary of skipped/malformed tasks; never create remote issues.

## Protocol
1. Validate task IDs, titles, user-story links, paths, dependencies, priorities, and acceptance text. Report duplicates and malformed rows.
2. Generate one stable issue block per task with deterministic title, labels, phase/milestone, body, dependency links, acceptance checks, and source task ID.
3. Preserve ordering and IDs across reruns; escape markdown safely and avoid secrets or environment-specific URLs.
4. Group by phase and identify dependency cycles, orphan tasks, blocked tasks, and tasks lacking acceptance evidence.
5. Report export counts, skipped items, and import instructions. A remote sync requires separate explicit authorization and provider configuration.

## Completion Gate
Every valid task maps exactly once to an issue block, source links are retained, and malformed/unsafe items are visible rather than silently dropped.

## Guard Rails
Read-only with respect to remote trackers. Do not create, update, close, or delete remote issues from this skill.