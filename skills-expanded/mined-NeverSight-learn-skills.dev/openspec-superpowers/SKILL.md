---
name: openspec-superpowers
description: Use when a repo uses OpenSpec and a requested change may affect product behavior, especially when the user asks to combine OpenSpec with Superpowers, run spec-driven development, create proposals/designs/specs/tasks, implement feature or bugfix work under process discipline, or ship a PR tied to an OpenSpec change.
---

# OpenSpec Superpowers

## Overview

Coordinate OpenSpec as the product-change record with Superpowers as the engineering discipline. Keep this skill as the traffic controller: load the concrete skills it names, then follow their instructions instead of duplicating them here.

## Core Rule

Use OpenSpec to define and track what changes. Use Superpowers to decide how to discover, plan, implement, debug, review, and verify the work.

## Required Skills

This is a coordinator skill, not a standalone workflow. Before using it for real work, confirm these skills are installed and discoverable:

- `openspec-workflow`
- `using-superpowers`
- `brainstorming`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`

If any required skill is unavailable, tell the user which prerequisite is missing and ask them to install it before continuing. Continue with a high-level outline only if the user explicitly asks for a degraded, non-executing guide.

If this skill conflicts with a directly invoked skill, follow the more specific skill for its domain:

- `openspec-workflow` owns OpenSpec artifact format, change lifecycle, and archive/PR conventions.
- Superpowers skills own process gates such as brainstorming, TDD, debugging, code review, and verification.

## Workflow

1. Load `using-superpowers` first when available. Let it determine which Superpowers process skills apply.
2. Decide whether OpenSpec is required:
   - Use OpenSpec for features, bug fixes, behavior changes, migrations, breaking changes, refactors that alter behavior, or any request involving OpenSpec artifacts.
   - Skip OpenSpec for typo fixes, README-only edits, examples, dependency bumps, CI configuration, or other supplementary changes unless the user explicitly asks for OpenSpec.
3. If the need or shape of the change is unclear, load `brainstorming`, `problem-statement`, `user-story`, or `prd-development` before creating OpenSpec artifacts.
4. Load `openspec-workflow` and follow it for:
   - change naming
   - `proposal.md`
   - `design.md`
   - `specs/*/spec.md`
   - `tasks.md`
   - OpenSpec validation and status checks
   - PR body text that includes the exact OpenSpec change name
5. During implementation, load the relevant Superpowers discipline before editing:
   - `test-driven-development` for features, bug fixes, refactors, and behavior changes
   - `systematic-debugging` for failures or unexpected behavior
   - `receiving-code-review` when acting on review feedback
   - `requesting-code-review` for substantial completed work when review is available
6. Before claiming completion, load `verification-before-completion` and run concrete verification commands.
7. When work is ready to integrate, load `finishing-a-development-branch` if branch, commit, PR, merge, or cleanup decisions are needed.

## Implementation Delegation

Prefer the implementation path required by `openspec-workflow`. If a required delegate, CLI, or subagent mechanism is unavailable or disallowed in the current platform, continue locally with the same artifact, TDD, debugging, review, and verification gates. State the deviation briefly in the final report.

Do not let delegation replace judgment. The current agent remains responsible for reconciling OpenSpec artifacts, applying review feedback, validating behavior, and explaining what shipped.

## Status Updates

When the workflow is longer than a trivial change, maintain a visible checklist that includes:

- discovery / framing
- OpenSpec artifacts
- implementation
- tests and verification
- branch / PR / archive follow-through

Update the checklist as work progresses. Keep user-facing updates short and concrete.

## Final Report

Include:

- OpenSpec change name, if one was created
- artifacts created or updated
- implementation summary
- verification commands and outcomes
- any intentional deviations from `openspec-workflow` or Superpowers skill instructions
