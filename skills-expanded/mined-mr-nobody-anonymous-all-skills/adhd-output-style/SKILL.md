---
name: adhd-output-style
description: Format agent responses to be ADHD-friendly (concise, scannable, bottom-line upfront, zero fluff, heavy visual chunking).
category: productivity
aliases:
- bluf
- adhd-format
- chunked-output
- concise-format
triggers:
- format for ADHD
- give me the bottom line first
- BLUF format
- make this scannable
- ADHD output style
keywords:
- adhd
- bluf
- format
- concise
- chunking
- scannable
- brevity
- bullet
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- adhd-formatting
- visual-chunking
- bluf-synthesis
inputs:
- text
- task
- response
outputs:
- scannable_response
- action_checklist
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- adhd
- bluf
- concise
- format
- output
- productivity
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

# ADHD Output Style

## Purpose
Formats all agent communication to match ADHD cognitive workflows by enforcing concise, scannable, zero-fluff responses with the bottom-line upfront and high-visibility visual chunking.

## When to Use
- User explicitly requests ADHD-friendly or concise formatting.
- User is experiencing cognitive fatigue, decision paralysis, or overwhelm.
- Complex information needs to be scanned quickly without parsing large walls of prose.
- Generating action plans, next steps, or status summaries.

## When NOT to Use
- When the user explicitly requests long-form narrative prose, creative storytelling, or philosophical essays.
- Formal legal, regulatory, or compliance filings that mandate specific boilerplate wording.

## Capabilities
- **Bottom-Line Upfront (BLUF)**: Deliver the direct answer or action item in the very first sentence.
- **Visual Chunking**: Strictly limit paragraphs to 2–3 sentences with bullet points and bold anchors.
- **Fluff Elimination**: Strip pleasantries, conversational filler, and rhetorical repetition.
- **Action Verbs**: Format task checklists starting with concrete, single-word action verbs.

## Inputs
- `text` (required) — Content or task instructions to format.
- `urgency` (optional) — High/medium/low priority flag for visual highlighting.
- `checklist_mode` (optional) — Boolean indicating if tasks should render as interactive Markdown checkboxes.

## Workflow
1. Identify the core insight, answer, or immediate next action.
2. Formulate the BLUF sentence and place it at the very top.
3. Decompose secondary supporting details into concise bullet points (max 3 items per section).
4. Highlight critical terms, deadlines, and parameters using bold text.
5. Provide a numbered or checkbox action list with clear, imperative verbs.

## Tools
- No external tools required; pure formatting and cognitive structuring.

## Examples
- "Give me the bottom line first on our deployment status."
- "Format this project plan in an ADHD-friendly style."
- "Make this error log scannable with zero fluff."

## Safety
- Never omit critical safety warnings, security precautions, or data-loss risks in the pursuit of brevity.
- Clearly call out any destructive implications before presenting abbreviated command snippets.

## Source
Custom skill maintained in this library following open Agent Skills standards.

## Notes
Works synergistically with `productivity.unlazy` and `productivity.adhd-task-breakdown` to move users from inertia into immediate execution.
