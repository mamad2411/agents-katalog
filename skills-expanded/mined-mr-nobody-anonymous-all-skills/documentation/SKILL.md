---
name: documentation
description: Write and structure documentation — READMEs, API docs, guides, and reference material.
category: utilities
aliases:
- docs
- readme
- api-docs
triggers:
- write docs for this
- document this API
- write a README
- help me document
keywords:
- document
- docs
- readme
- api
- reference
- guide
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- api
- docs
- document
- documentation
- readme
- utilities
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

# Documentation

## Purpose

Help the user produce documentation that future readers will actually use. Focus on
audience, structure, and accuracy.

## Capabilities

- README structure
- API reference (endpoints, params, errors)
- Tutorial / guide writing
- Doc review and audit

## Source

Custom skill, written for this library.

## Notes

Pairs with `writing`, `markdown`.

## When to Use

Use when the request matches the documented documentation capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

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

Requests that should activate this skill include: "write docs for this"; "document this API"; "write a README".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
