---
name: repo-frontend-ux-state-review
description: Reviews frontend user flows for loading, empty, error, disabled, pending, retry, offline, unauthorized, validation, optimistic, and success states. Use when changing forms, data fetching, navigation, async actions, or user-facing flows.
---


# Repository Frontend UX State Review

Use this skill when UI behavior depends on data, permissions, network state, async actions, or user input.

## Review Areas

- loading states
- empty states
- error states
- validation states
- disabled and pending states
- success and confirmation states
- retry behavior
- offline or degraded network behavior
- unauthorized and permission-denied states
- optimistic updates and rollback
- destructive action confirmation

## Required Behavior

- Avoid leaving users without feedback during async work.
- Make errors actionable where possible.
- Keep validation messages specific.
- Prevent duplicate submissions.
- Preserve user input across recoverable errors.
- Clearly distinguish unavailable, unauthorized, empty, and loading states.

## Workflow

Use `workflows/ux-state-review-workflow.md`.

## Resource

Use `resources/ux-state-checklist.md`.

