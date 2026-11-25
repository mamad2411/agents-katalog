---
name: slack-synthesizer
description: Summarize Slack threads into decisions, evidence, disagreements, and action items.
category: utilities
aliases:
- slack
- thread
triggers:
- Summarize this Slack thread
- What was decided in this channel
- Extract action items from Slack
- Slack summary
keywords:
- slack
- summary
- thread
- decision
- action-items
- channel
dependencies:
- optional:slack-access
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- slack-synthesizer
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- decision
- slack
- summary
- synthesizer
- thread
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

# Slack Synthesizer

## Purpose
Summarize Slack threads and channels into structured information: decisions made,
key evidence and arguments, disagreements noted, and action items with owners.
The skill helps users catch up on conversations without reading everything.

## When to Use
- The user wants to catch up on a Slack channel
- A thread needs to be summarized for someone who missed it
- Extracting action items from a discussion
- Identifying decisions made in a channel

## When NOT to Use
- Real-time conversation monitoring (use Slack's built-in features)
- Accessing private channels without authorization
- Archiving or storing Slack data beyond the session

## Capabilities
- Fetch thread messages with context
- Identify key speakers and their positions
- Extract decisions (explicit or implicit)
- Surface disagreements or open questions
- Extract action items with owners
- Generate summaries in multiple formats (brief, detailed, bullet)

## Inputs
- `source` (required) — channel ID, thread URL, or message IDs
- `format` (optional) — one of: brief, detailed, bullet-points
- `focus` (optional) — decisions, actions, disagreements, or all

## Workflow
1. **Fetch** — Retrieve messages from specified source
2. **Analyze** — Identify speakers, sentiment, and structure
3. **Extract** — Find decisions, actions, and key points
4. **Synthesize** — Generate coherent summary
5. **Format** — Output in requested format

## Tools
- Slack API (with appropriate read scopes)
- Thread/message access permissions

## Examples
**User:** "Summarize the decisions from #project-alpha this week"
**Response:**
```

## Safety
- Respect channel privacy settings
- Never store Slack data beyond the session
- Only access channels the user has permission for
- Flag sensitive content without disclosing details

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
