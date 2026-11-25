---
name: adhd-task-breakdown
description: Turn overwhelming work into ADHD-friendly, visible, short, immediately actionable steps.
category: productivity
aliases:
- adhd
- task-decomposition
- breakdown
- chunk-down
triggers:
- Break this down
- I don't know where to start
- This feels too big
- ADHD task
- Help me start this project
- Too overwhelming
keywords:
- adhd
- overwhelm
- task
- chunk
- decompose
- planning
- executive
- function
- friction
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- adhd-task-breakdown
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
- adhd
- breakdown
- chunk
- overwhelm
- productivity
- task
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

# Adhd Task Breakdown

## Purpose
Turn a large, fuzzy, or overwhelming project into a sequenced set of small, well-defined
steps that someone with executive-function challenges can actually start. The skill
prioritizes the *first* step being so small it is impossible to refuse.

## When to Use
Activate when the user:

- Has a project that feels too big, too vague, or too long
- Asks "where do I even start?"
- Mentions ADHD, overwhelm, getting stuck, or paralysis
- Provides a goal but no path

## When NOT to Use
- The user is in acute distress (route to support)
- The task is already a single, small action (just do it)
- The user needs a value decision first (route to `decision-making`)

## Capabilities
- Decompose a goal into phases, then chunks, then 2-minute actions
- Surface hidden decision points the user did not realize they needed to make
- Estimate a realistic order of magnitude for each chunk
- Flag likely friction points (waiting on others, ambiguous specs, environment setup)
- Suggest a "minimum viable first run" path that proves the approach

## Inputs
- The goal or project (one to several sentences)
- Known constraints (deadline, people involved, tech stack)
- Past attempts (optional but helpful)

## Workflow
1. **Restate the goal** in one sentence. Confirm with the user.
2. **Identify phases** — 3 to 7 high-level stages, in order.
3. **For each phase, list 3 to 7 chunks.** Each chunk should be finishable in one
   sitting (15 to 90 minutes).
4. **For the first chunk, list 1 to 3 starter actions**, each â‰¤ 2 minutes.
5. **Mark decision points** with `?` and the trade-off.
6. **Mark waiting states** with `â€¦` (waiting on person X, deployment, review).
7. **Output a numbered list**, not a paragraph.

## Tools
- None required. Pure structured text.

## Examples
**User:** "I need to launch a SaaS by next quarter."
**Response:**

> 1. Decide pricing tier shape (?)
> 2. Set up a single landing page (one 30-minute chunk)
>    - Open the page template
>    - Paste the headline
> 3. Wire up Stripe (waiting on account verification â€¦)
> 4. â€¦

**User:** "I can't start my thesis."
**Response:**

> 1. Pick the *one* claim you will defend (?)
> 2. Find three sources that disagree with it (one 45-minute chunk)
>    - Open the library search
>    - Save three PDFs to a folder
> 3. Write a 200-word summary of the disagreement (next chunk)
> 4. â€¦

## Safety
- Do not diagnose ADHD or other conditions
- Do not promise productivity; offer structure
- If the user reports acute paralysis or distress, recommend professional support

## Source
Auto-generated from openclawskills.net description. Cross-references the existing
`unlazy` and `focus` skills in this library.

## Notes
Maintained as part of canonical productivity category.
