---
name: landing-report
description: Produce a read-only landing queue report for branches, PRs, versions, and likely ship order.
---

# Landing Report

Use this skill when the user asks what is ready to land, what might conflict, or what release slot a change should take.

## Workflow

1. Inspect local state:
   - current branch
   - `git status --short`
   - recent commits
   - version or changelog files if present
2. Inspect remote state when available:
   - open PRs
   - branch names
   - CI status
   - version claims
3. Identify:
   - ready work
   - blocked work
   - likely conflicts
   - release/version slots
4. Produce a read-only report with recommended landing order.

## Guardrails

- Do not merge, push, tag, or edit files.
- Do not claim PR state without checking it.
- Call out unavailable GitHub access explicitly.
