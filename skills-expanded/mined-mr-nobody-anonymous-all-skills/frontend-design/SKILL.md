---
name: frontend-design
description: Design and implement frontend interfaces — HTML, CSS, layouts, and visual design for the web.
category: design
aliases:
- html-css
- web-design
- landing-page
triggers:
- design this landing page
- style this page
- frontend design
- layout this
- CSS for this
keywords:
- frontend
- html
- css
- layout
- design
- landing
- page
- style
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- css
- design
- frontend
- html
- layout
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

# Frontend Design

## Purpose

Design and implement frontend pages — semantic HTML, accessible CSS, responsive layouts,
and component composition.

## When to Use

- User wants to design a page / landing
- User wants CSS / layout help
- User wants to translate a design into code

## Source

Custom skill, written for this library.

## Notes

Pairs with `ui-ux`, `accessibility`, `frontend` (development).

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the frontend-design workflow consistently.
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

Requests that should activate this skill include: "design this landing page"; "style this page"; "frontend design".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
