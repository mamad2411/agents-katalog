---
name: meeting-action-extractor
description: Extract decisions, action items, owners, dates, and unresolved questions from meetings.
category: productivity
aliases:
- meeting
- action-items
- decisions
triggers:
- Extract action items from this meeting
- What were the decisions
- Meeting summary
- Parse meeting notes
- Extract follow-ups
keywords:
- meeting
- action-items
- decisions
- summary
- follow-up
- owner
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- meeting-action-extractor
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
- action
- action-items
- decisions
- extractor
- meeting
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

# Meeting Action Extractor

## Purpose
Extract structured information from meeting content: decisions made, action items
with owners and due dates, and unresolved questions. The skill helps teams stay
accountable and ensures nothing falls through the cracks.

## When to Use
- Processing meeting notes or transcripts
- Extracting action items for follow-up
- Creating meeting summaries for stakeholders
- Tracking decisions across meetings

## When NOT to Use
- Real-time meeting transcription (use specialized tools)
- Accessing private meeting content without consent
- Replacing human judgment on ambiguous assignments

## Capabilities
- Parse meeting text, transcripts, or notes
- Identify explicit and implicit decisions
- Extract action items with owners
- Detect due dates and deadlines
- Surface unresolved questions and open issues
- Generate structured output (markdown, JSON, task list)
- Track items across multiple meetings

## Inputs
- `content` (required) — meeting text, transcript, or notes
- `format` (optional) — one of: markdown, json, task-list, full-summary
- `context` (optional) — previous meeting context for tracking

## Workflow
1. **Parse** — Extract structured data from meeting content
2. **Identify** — Find decisions, actions, and questions
3. **Assign** — Match owners where explicitly stated
4. **Structure** — Format output according to request
5. **Validate** — Present for user review and correction

## Tools
- Text parsing and NLP
- Structured output generation

## Examples
**User:** "Extract action items from these meeting notes: [paste notes]"
**Response:**
```

## Safety
- Never assume ownership without explicit mention
- Flag uncertain extractions for human review
- Respect meeting privacy and confidentiality
- Don't store extracted data without consent

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
