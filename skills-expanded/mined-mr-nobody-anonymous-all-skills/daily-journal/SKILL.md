---
name: daily-journal
description: Create a concise daily journal with events, reflection, lessons, and tomorrow's priorities.
category: productivity
aliases:
- journal
- daily
- reflection
- gratitude
- intention
- mood
triggers:
- Daily journal
- Reflect on today
- What did I do today
- Morning prompt
- Evening wrap
keywords:
- journal
- daily
- reflection
- gratitude
- mood
- intention
- win
- lesson
- log
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- daily-journal
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- daily
- gratitude
- journal
- productivity
- reflection
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

# Daily Journal

## Purpose
Run a short, structured **daily check-in** that helps the user notice what mattered,
what worked, and what to carry into tomorrow. The skill is intentionally lightweight:
three prompts in, three blocks out, no scoring, no streak pressure.

## When to Use
- The user wants a morning intention prompt
- The user wants an evening wrap-up
- The user wants to start journaling but has no template

## When NOT to Use
- The user is in acute distress (route to support)
- The user wants long-form memoir writing (different skill)

## Capabilities
- Three-mode operation: `morning`, `midday`, `evening`
- Prompts that are open enough to feel easy, specific enough to be useful
- A template that survives a 90-second answer
- Optional append to a vault (see `obsidian-sync`)
- Track wins (â‰¤ 3), friction (â‰¤ 3), one lesson, one intention

## Inputs
- `mode` (morning | midday | evening)
- Optional `append_to` (path to a daily-note file or vault)
- Optional `template` (custom prompts; default is shipped)

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
- None required
- Optional: filesystem append, `obsidian-sync`

## Examples
**User:** "Start my morning journal."
**Response:** "1. Intention? 2. Win for today? 3. What will you protect?"

**User:** "Wrap up today."
**Response:** "Wins? Friction? Lesson? Intention for tomorrow?" — and writes a
markdown file `daily/2026-02-09.md`.

## Safety
- Never log mood/energy to a third party
- Honor a "private" flag (no write, output only to chat)
- Do not pressure the user to write long answers
- If distress appears, suggest a break and a support contact

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
