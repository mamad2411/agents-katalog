---
name: excel-to-deck-evidence-map
description: >-
  Map workbook evidence into a defensible deck. Use when slide claims must trace to workbook
  tabs, cells, source files, assumptions, and review status.
---

# Excel-to-Deck Evidence Map

Execute this workflow as written. Ask for missing inputs in the sequence it specifies, pause
when it says to wait, and preserve any stated output format and guardrails. Treat external
actions as drafts unless the user explicitly authorizes the action.

## Context
## Prompt 4: Excel-To-Deck Evidence Map
## Job
Map every slide claim back to workbook tabs, cells, source files, assumptions, and review status.
## Use When
- A workbook becomes a board deck, QBR, investor update, campaign report, or client presentation.
- You need to review a deck without reverse-engineering the spreadsheet.
- Multiple source files or assumptions feed the final story.

You are creating an evidence map between spreadsheet-backed analysis and a PowerPoint deck.
For every proposed or existing slide claim, create a table with:
- Slide number
- Claim headline
- Workbook tab(s)
- Cell ranges, tables, named outputs, or formulas used
- Source file IDs behind the workbook data
- Calculation or transformation used
- Assumptions involved
- Date range
- Owner or source authority
- Review status: verified / needs review / unsupported / conflicting
- Speaker-note text needed
- Notes for the reviewer
Then run an evidence gap review. Flag:
- Claims with no source
- Numbers with no date
- Charts with unclear data
- Assumptions presented as facts
- Workbook outputs that do not tie to raw data
- Slides where speaker notes do not explain the evidence
- Claims that rely on stale or superseded sources
- Conflicts that require human judgment
Rules:
- If a slide claim cannot be traced, mark it unsupported.
- If a number depends on an assumption, name the assumption.
- If two sources disagree, preserve the conflict instead of choosing silently.
- If the deck uses a chart, map the chart to the exact data behind it.

## Source

Source: [Prompt 4: Excel-To-Deck Evidence Map](https://app.notion.com/p/80177baa0fe346a59a88ee82f3c5903b)
