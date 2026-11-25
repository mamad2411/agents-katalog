---
name: botkits-transcript-healthcheck
description: >-
  Needs Grok Bot. Use when auditing Grok Bot fleet transcripts for user friction, proposing new
  skills/bots/routines from repeated corrections, or running the standing
  transcript-healthcheck routine.
compatibility: Needs Grok Bot (reads Grok Bot fleet transcripts).
---
# Transcript healthcheck

Read recent bot transcripts, find where the user had to fight the bot, and propose a skill, bot, or routine only where the evidence repeats. Build nothing until the user picks.

## When

- The standing `transcript-healthcheck` routine fires (default weekday mornings).
- The user asks for a friction audit or "what should we automate?".
- First run after import: ask once what cadence they want, then create or update the `transcript-healthcheck` routine. Don't re-ask.

## Scope

- Window: the last 24 hours unless the routine or user says otherwise.
- Files: `/home/box/agent-data/agent-transcripts/<agentId>/<agentId>.jsonl`. Skip `sand-subagent-*` folders. Sort by modification time, not by folder name.
- Names: `/home/box/agent-data/agents/<agentId>/profile.json`.

Say the window and the number of bots out loud before reading.

## Read

Split the transcript files across parallel subagents; keep only their findings in the main thread. Each subagent returns, per bot that had user messages in the window:

- the user's goals, in a line
- friction, with a short quote and rough timestamp
- what the bot did versus what the user wanted
- a candidate fix (skill, bot, or routine) or `none`

Signs of friction: "no", "stop", "wrong", "I said", "undo", sarcasm; the same instruction given twice; the user doing work the bot should own; the bot asking a question it could have answered by trying; a thread the user abandons mid-task.

Bots with no user messages are skipped. Finding nothing is a valid result.

## Sort before proposing

Group the friction into a few named failure types across all bots (for example "forgets formatting rule", "asks instead of acting", "wrong account"). Count each. Propose only for types that show up more than once, or once with real cost (a wrong send, lost work). A one-off annoyance goes in the notes, not the proposals.

## Report

- Summary: up to five bullets.
- Proposals, biggest first, each tagged `skill`, `bot`, or `routine`, with its count and one quoted line as evidence.
- Bots with nothing to report, on one line.

On a scheduled run with nothing to propose, send nothing at all. Offer to build only after the user picks. Never create agents, skills, or routines from the report alone.

## Inspired by

- [Lauren Tan (@poteto), dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2) (marketplace template; no reuse license shown, so no text is copied). Does well: a weekday friction scan that stays quiet and waits for the user to choose. Missing: the listing doesn't say how to read transcripts or when evidence is strong enough.
- [Lauren Tan, pstack recall](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/recall/SKILL.md) (MIT). Does well: lock the window first, fan transcripts out to subagents, sort by real modification time, and lead with a short capsule. Missing: built to rebuild one person's working context, not to find friction across a fleet.
- [Hamel Husain, A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/). Does well: error analysis (read real logs, categorize failures, then fix the biggest categories). Missing: written for product teams with eval tooling, not a self-auditing bot.

## What this version adds

- A grouping and counting step, so proposals rest on repeated failures, not single quotes.
- A cost exception for one-off failures that were expensive.
- Full silence on empty scheduled runs.
