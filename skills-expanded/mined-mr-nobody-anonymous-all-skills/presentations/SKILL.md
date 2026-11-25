---
name: presentations
description: Design and structure presentations — narrative arc, slide content, visual hierarchy, and delivery notes.
category: design
aliases:
- slide-design
- deck-design
- presentation-design
triggers:
- design a presentation
- structure my talk
- slides for
- presentation outline
keywords:
- presentation
- slides
- deck
- talk
- narrative
- arc
- visual
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- deck
- design
- presentation
- presentations
- slides
- talk
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

# Presentations

## Purpose

Help the user design and structure a presentation. Outline the narrative arc, draft slide
content, and note visual / delivery considerations.

## When to Use

- User has a talk / presentation to give
- User wants feedback on an existing deck
- User wants help structuring ideas for slides

## Capabilities

- Narrative arc (setup → tension → resolution)
- One-idea-per-slide discipline
- Visual hierarchy and layout hints
- Speaker notes

## Source

Custom skill, written for this library.

## Notes

Pairs with `pptx`, `ui-ux`.

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

Requests that should activate this skill include: "design a presentation"; "structure my talk"; "slides for".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
