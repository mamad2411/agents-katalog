---
name: cleanup-github-issue
description: Close, delete, or tidy up stale GitHub issues
argument-hint: "[repo]"
related:
  - cleanup-files-in-computer
  - cleanup-files-in-project
  - suggest-next-action
  - run-clean
  - run-cleanup
---

## Goal

Clean up stale, duplicate, or already-resolved issues through the `gh` CLI

## Scope

Use for maintaining the issue backlog

## Execute

### 1. Identify targets

> Goal: Identify targets

1. List open issues with filters
1. Find duplicate or stale issues

### 2. Confirm

> Goal: Confirm

1. Ask the user before closing or deleting
1. Prefer closing over deleting

### 3. Execute

> Goal: Execute

1. Run `gh issue close` or `gh issue delete`
1. Add a closing comment if needed

### 4. Report

> Goal: Report

1. Summarize the issues that were closed/deleted
1. Call `/suggest-next-action`

## Rules

- Never delete issues without explicit user confirmation
- Close with a comment explaining the reason
- Never mass-close without approval

- Use /cleanup-files-in-computer if needed
- Use /cleanup-files-in-project if needed
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Stale issues are closed or deleted
- Backlog is clean with a log trail
