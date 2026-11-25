---
name: frontend
description: Build frontend applications — frameworks, state management, routing, data fetching, and integration with APIs.
category: development
aliases:
- frontend-dev
- web-app
- react-vue-svelte
triggers:
- build a frontend
- frontend dev
- build a web app
- help with react
keywords:
- frontend
- react
- vue
- svelte
- web
- app
- spa
- ssr
- state
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- development
- frontend
- react
- svelte
- vue
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Frontend

## Purpose

Build and reason about frontend applications: framework choice, state management, routing,
data fetching, performance, and accessibility.

## Source

Custom skill, written for this library.

## Notes

Distinguish from `frontend-design` (which is visual). Pairs with `architecture`, `testing`, `accessibility`.

## When to Use

Use when the request matches the documented frontend capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the frontend workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "build a frontend"; "frontend dev"; "build a web app".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
