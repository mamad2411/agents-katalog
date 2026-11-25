---
name: meeting-notes
description: Structure meeting transcripts into organized notes with action items, decisions, and key points. Use when processing meeting recordings or creating meeting summaries.
version: 1.0.0
---

# Meeting Notes

## Overview

Transforms raw meeting transcripts or recordings into structured, actionable meeting notes.

## Instructions

When processing meeting content:

1. **Extract metadata**: Date, attendees, meeting type
2. **Identify key discussions**: Main topics covered
3. **Capture decisions**: What was decided and by whom
4. **List action items**: Task, owner, deadline
5. **Note follow-ups**: Items for future meetings

## Output Format

```markdown
# Meeting Notes: [Topic]

**Date:** YYYY-MM-DD
**Attendees:** Names
**Duration:** X minutes

## Summary
Brief 2-3 sentence overview of the meeting.

## Key Discussion Points
- Topic 1: Summary of discussion
- Topic 2: Summary of discussion

## Decisions Made
1. [Decision] - Decided by [Person]
2. [Decision] - Decided by [Person]

## Action Items
| Task | Owner | Due Date | Status |
|------|-------|----------|--------|
| Task description | Name | Date | Pending |

## Follow-up Items
- Items to discuss in next meeting

## Next Meeting
Date/time if scheduled
```

## Examples

### Example: Process Transcript

**Input:**
Raw meeting transcript with multiple speakers

**Output:**
Structured notes following the format above with clear attribution

## Guidelines

### Do
- Keep summaries concise (2-3 sentences max)
- Attribute decisions to specific people
- Include owners and deadlines for all action items
- Flag unclear items for clarification
- Use consistent formatting throughout

### Don't
- Include verbatim transcript in notes
- Leave action items without owners
- Skip the summary section
- Omit attendee names from notes
