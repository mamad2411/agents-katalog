---
name: text-processing
description: Process text — search, replace, transform, dedupe, slice, and convert between common formats.
category: utilities
aliases:
- text-utils
- string-manipulation
triggers:
- process this text
- find and replace
- clean this text
- transform this
keywords:
- text
- string
- search
- replace
- transform
- slice
- dedupe
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- processing
- replace
- search
- string
- text
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

# Text Processing

## Purpose

Operate on text: search/replace, transformation, deduping, slicing, and format conversion.

## Source

Custom skill, written for this library.

## Notes

Foundation utility — powers many other skills.

## When to Use

Use when the request matches the documented text-processing capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the text-processing workflow consistently.
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

Requests that should activate this skill include: "process this text"; "find and replace"; "clean this text".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
