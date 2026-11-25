---
name: competitive-analysis
description: Analyze competitors — features, positioning, pricing, strengths, weaknesses — to inform product strategy.
category: research
aliases:
- competitors
- market-scan
- competitor-research
triggers:
- analyze competitors
- competitive landscape
- what are competitors doing
- market scan
keywords:
- competitor
- competitive
- market
- landscape
- comparison
- positioning
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- analysis
- competitive
- competitor
- landscape
- market
- research
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

# Competitive Analysis

## Purpose

Help the user understand their competitive landscape: who the competitors are, what they
offer, how they're positioned, and where the user's product fits.

## When to Use

- User is launching or repositioning a product
- User wants a market scan
- User is making a strategic decision

## Capabilities

- Identify direct / indirect competitors
- Compare features, pricing, positioning
- Surface gaps and opportunities

## Source

Custom skill, written for this library.

## Notes

Pairs with `web-research`, `deep-research`.

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

Requests that should activate this skill include: "analyze competitors"; "competitive landscape"; "what are competitors doing".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
