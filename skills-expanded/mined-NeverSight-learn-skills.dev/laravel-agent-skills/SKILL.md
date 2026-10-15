---
name: laravel-agent-skills
description: Apply Laravel's official agent-skills guidance for Laravel-native refactoring, official workflow alignment, and starter-kit upgrade tasks.
---

# Laravel Agent Skills

Use this skill when the task should follow Laravel's official agent or skill guidance rather than generic community patterns.

## Goal

Bias work toward official Laravel conventions and official upstream workflows.

## Primary use cases

- Refine recent Laravel code without changing behavior.
- Align naming, structure, and flow with Laravel conventions.
- Review modified code for clarity and maintainability.
- Pull specific upstream improvements from a Laravel starter kit without doing a full rewrite.

## Working rules

- Prefer the Laravel-native solution first.
- Simplify recent code instead of abstracting preemptively.
- Preserve existing behavior unless the user explicitly asks for changes.
- Treat starter-kit sync as selective feature adoption, not a blind version bump.
- Never silently overwrite customized files or manifests during starter-kit upgrade work.
- Re-run focused verification after each meaningful change.

## Starter-kit upgrade guardrails

When the task involves a Laravel starter kit:

- Work feature by feature.
- Keep changes on a dedicated branch.
- Surface customized files instead of auto-merging them.
- Separate lockfile regeneration from feature commits.
- Stop if verification regresses.

## Output expectations

When using this skill, report:

- Which Laravel conventions were enforced.
- Whether the task was simplification, review, or upstream sync.
- Which files are likely customized-risk surfaces.
- What verification was run.
