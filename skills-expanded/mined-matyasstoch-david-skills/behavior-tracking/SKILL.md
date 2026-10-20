---
name: behavior-tracking
description: Use only when David explicitly says "track my behavior in this conversation" or clearly asks to log, track, or analyze his behavior in the current conversation. This skill logs each of David's messages to a local behavior database, records decisions with follow-up questions, updates local notes when useful, and surfaces patterns when asked.
---

# Behavior Tracking

Activate this skill only after an explicit opt-in request from David. Do not use it by default.

Once activated, keep it active for the rest of the conversation until David tells you to stop.

## Message Logging

After every message from David, silently log an entry to the configured local behavior database in the `messages` table.

Capture:
- `timestamp`
- `message_type` — instruction, question, brainstorming, decision, overthinking, venting
- `topic` — short label
- `sentiment` — high focus, frustrated, scattered, calm, excited, etc.
- `task_name` — specific task if relevant, otherwise `null`
- `task_status` — started, in_progress, completed, abandoned, otherwise `null`
- `duration_minutes` — only if David explicitly mentions it
- `note` — any useful insight

## Insights

When David asks for insights, query the configured local behavior database and surface patterns, trends, and observations.

## Decisions

When David makes a decision, log it to the `decisions` table in the same database.

Before logging a decision, ask 2-3 short follow-up questions to extract:
- `chosen_task`
- `why`
- `rejected_alternatives`
- `context`
- `outcome`
- `duration_minutes`

## Notes Folder

After each message, scan for useful signals of taste, judgment, reasoning, or recurring patterns. If something is worth keeping, silently update the relevant markdown file in the configured local notes folder.

Guidelines:
- Organize by topic
- Synthesize patterns over time
- Do not dump raw quotes unless they are necessary
