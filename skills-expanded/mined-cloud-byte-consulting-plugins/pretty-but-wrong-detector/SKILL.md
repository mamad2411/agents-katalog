---
name: pretty-but-wrong-detector
description: >-
  Audit polished files for unsupported claims. Use before sharing an AI-generated or heavily
  revised workbook or presentation that looks finished but may be unsafe.
---

# Pretty-But-Wrong Detector

Execute this workflow as written. Ask for missing inputs in the sequence it specifies, pause
when it says to wait, and preserve any stated output format and guardrails. Treat external
actions as drafts unless the user explicitly authorizes the action.

## Context
## Prompt 5: Pretty-But-Wrong Detector
## Job
Catch polished but unsafe Office outputs before they get forwarded.
## Use When
- The deck or workbook looks finished.
- You are tempted to share it.
- The artifact was generated or heavily revised by AI.
- A busy person might trust it because it looks clean.

Read this deck or workbook as a skeptical reviewer who suspects every claim and every number.
For each slide or sheet, identify:
- Claims without source attribution
- Numbers without a date or source
- Charts whose underlying data is not traceable
- Formulas inconsistent across parallel rows or columns
- Formulas that point to fixed cells when they should roll forward
- Hardcoded outputs where formulas are expected
- Outputs that do not change when assumptions change
- Assumptions presented as facts
- Stale or mixed date ranges
- Brand/template drift
- Low-contrast or unreadable charts
- Overcrowded slides
- Broken narrative logic
- Missing speaker-note evidence
- Items requiring human judgment
Produce a written list of every issue found. Do not fix anything. Just enumerate.
Rank each issue as:
- Must fix before sharing
- Should fix before important review
- Polish
End with a final readiness verdict:
- Not ready
- Ready with limitations
- Ready to share
Do not mark it ready if any must-fix issue remains.

## Source

Source: [Prompt 5: Pretty-But-Wrong Detector](https://app.notion.com/p/2ec4bcb3dced483789c7b1edd51c43c6)
