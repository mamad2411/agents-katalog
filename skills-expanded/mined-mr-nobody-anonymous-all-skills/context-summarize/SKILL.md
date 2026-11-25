---
name: context-summarize
description: Compress active context into decisions, facts, open questions, and next actions.
category: productivity
aliases:
- context
- meeting-summary
triggers:
- Summarize this
- TL;DR
- Extract the action items
- What are the key points
- Compress this transcript
keywords:
- summarize
- tldr
- context
- notes
- transcript
- meeting
- action
- items
- decisions
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- context-summarize
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
- context
- notes
- productivity
- summarize
- tldr
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

# Context Summarize

## Purpose
Turn a long piece of text (transcript, log, thread, document, video caption) into a
**structured, skimmable summary** that preserves the parts a human will actually act
on: decisions, action items, open questions, risks, and a 3-sentence "what happened".

## When to Use
- The user has a long document and wants the gist
- A meeting transcript needs follow-up actions extracted
- A log dump needs to be triaged
- A research thread (forum, email, Slack) needs the signal pulled out

## When NOT to Use
- The source is private/sensitive and the destination is untrusted
- The source is already short — just read it
- The user wants a literal translation, not a summary

## Capabilities
- 3-sentence "what happened" top line
- Bullet list of **decisions made** (who, what, when)
- Bullet list of **action items** (owner, due date, verb)
- Bullet list of **open questions**
- Bullet list of **risks / blockers**
- 3 to 5 direct **quotes** (verbatim, with attribution)
- Length budget: summary â‰¤ 15% of source length

## Inputs
- The text (inline, file path, or URL)
- `max_words` (default 400)
- `format`: `md|json|bullets` (default `md`)
- Optional `focus`: pull out one of `decisions|actions|questions|risks` only

## Workflow
1. **Read** the source (or fetch if URL, with `Accept` header for plain text).
2. **Segment** by speaker / paragraph / heading.
3. **Extract** decisions, actions, questions, risks with attribution.
4. **Write the 3-sentence top line** with the most important fact first.
5. **Quote** the 3-5 most load-bearing passages verbatim.
6. **Compress** to the length budget; drop examples, repetition, filler.
7. **Output** in the requested format.

## Tools
- None required
- Optional: `whisper` for audio sources (paired with `audio-transcribe`)

## Examples
**User:** "Summarize this 2-hour meeting transcript."
**Response:** 3 sentences on what was decided, 7 action items with owners, 3 open
questions, 2 risks, 4 direct quotes. Total: 380 words.

**User:** "Just the action items."
**Response:** Filtered output. 9 items, each with owner and due date.

## Safety
- Strip PII (emails, phone numbers, IDs) unless the user asks to keep them
- Preserve attribution for direct quotes; never paraphrase a quote
- Honor a "do not store" flag by not writing the summary to disk
- Never include credentials, even if they appear in the source

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
