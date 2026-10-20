---
name: tailwindcss-4-quality
description: Helps agents review, debug, audit, and verify Tailwind CSS 4 class usage, source detection, build integration, accessibility states, responsive behavior, and migration regressions.
license: MIT
compatibility: Requires Python 3 for the optional audit and hook scripts.
---

# Tailwind CSS 4 Quality Skill

Use this skill for Tailwind CSS 4 review, debugging, build verification, class detection, responsive checks, accessibility-state checks, and safe command auditing.

## When to Use

- A Tailwind utility class is missing from the generated CSS.
- A build fails after Tailwind setup or migration.
- A UI change needs review for class hygiene, accessibility, responsive behavior, or design consistency.
- The agent is about to run commands that might use Tailwind CSS 3 setup patterns.
- The project needs a lightweight Tailwind CSS 4 audit.

## Workflows

- `workflows/tailwindcss-4-review-workflow.md`: use for PR-style review of Tailwind UI/CSS changes.
- `workflows/tailwindcss-4-debug-build-workflow.md`: use for build failures, missing classes, or generated CSS issues.

## Resources

- `resources/review-checklist.md`: review checklist for Tailwind CSS 4 changes.
- `resources/class-detection-checklist.md`: debugging checklist for class detection problems.

## Scripts

Scripts live inside this skill folder by design.

- `scripts/tailwindcss-4-command-guard.py`: used by the plugin hook to block or ask about unsafe Tailwind commands.
- `scripts/tailwindcss-4-project-audit.py`: manual audit for common Tailwind CSS 4 setup and migration issues.
- `scripts/tailwindcss-4-ui-quality-hook.py`: hook/manual helper that flags extreme class blocks, repeated class blocks, responsive-risk UI changes, and possible color-only or missing-focus state patterns.

Before running a script, run it with `--help`.

## Operating Guidance

- Prefer project-provided build, lint, format, type-check, and test commands.
- If no scripts exist, inspect package manager and tool config before inventing commands.
- Use audit scripts as helpers, not as substitutes for reading relevant files.
- Treat hook findings as review prompts, not automatic proof of defects.
- Do not auto-fix by deleting legacy config unless the migration workflow has accounted for every legacy behavior.
