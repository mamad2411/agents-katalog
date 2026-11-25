---
name: summarization
description: Summarize long content — articles, documents, transcripts — at various lengths and for various audiences.
category: utilities
aliases:
- summary
- tldr
- abstract
triggers:
- summarize this
- tldr
- give me the summary
- shorten this
keywords:
- summarize
- summary
- tldr
- abstract
- shorten
- condense
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- abstract
- summarization
- summarize
- summary
- tldr
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

# Summarization

## Purpose

Produce useful summaries at the right length and angle for the user. Different audiences and
purposes need different summaries.

## Capabilities

- One-line TL;DR
- 3-bullet summary
- Section-by-section summary
- Audience-specific summary (executive vs. technical)
- Key quotes extraction

## Safety

- Summarize, don't fabricate
- Preserve uncertainty

## Source

Custom skill, written for this library.

## Notes

Pairs with `pdf`, `docx`, `web-extraction`, `deep-research`.

## When to Use

Use when the request matches the documented summarization capability or its declared triggers.

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

Requests that should activate this skill include: "summarize this"; "tldr"; "give me the summary".
