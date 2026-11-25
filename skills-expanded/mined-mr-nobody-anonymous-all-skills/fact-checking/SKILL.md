---
name: fact-checking
description: Verify a claim by checking primary sources, looking for authoritative confirmation, and rating confidence.
category: research
aliases:
- verify
- fact-check
- claim-verification
triggers:
- is this true
- verify this
- fact check
- check this claim
- is this accurate
keywords:
- fact
- check
- verify
- 'true'
- claim
- accuracy
- source
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- check
- checking
- fact
- research
- verify
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

# Fact Checking

## Purpose

Take a claim, find authoritative sources, and rate the claim's confidence. Be honest about
uncertainty.

## When to Use

- User wants to verify a specific claim
- User is reviewing an article / essay
- User wants to challenge a statement

## When NOT to Use

- The user wants open-ended research (route to `web-research`)
- The claim is a value judgment, not factual

## Capabilities

- Locate authoritative sources
- Triangulate across sources
- Rate confidence (well-supported, plausible, contested, unsupported, false)

## Inputs

- The claim (quote or paraphrase)
- Domain context

## Workflow

1. **State the claim precisely.** Note its domain.
2. **Identify authoritative sources.** What kind of source would settle this?
3. **Search and check.** Run targeted searches.
4. **Triangulate.** Confirm across multiple sources where possible.
5. **Rate confidence.**
   - **True / well-supported** — multiple authoritative sources agree
   - **Plausible** — partial support, plausible but not confirmed
   - **Contested** — credible sources disagree
   - **Unsupported** — no good sources found
   - **False** — authoritative sources contradict

## Safety

- Don't assert beyond what sources support
- Be explicit about confidence levels

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `web-research`
- `source-verification`

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "is this true"; "verify this"; "fact check".
