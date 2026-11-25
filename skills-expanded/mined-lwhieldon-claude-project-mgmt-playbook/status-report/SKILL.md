---
name: status-report
description: Generate a weekly project status report from a status CSV or free-text notes, with RAG status, accomplishments, upcoming work, risks, and actions. Use when you need a client-ready update from raw project data. Usage - /status-report path/to/status-data.csv
---

# Status Report

Generate a structured weekly status report from project data or a free-text summary. Output is
formatted for direct use in a client email or a PowerPoint status slide.

## Input

`$ARGUMENTS` is either:

- the path to a `status-data.csv` (see `sample-projects/acme-data-warehouse/status-data.csv` for
  the expected columns), or
- a short free-text description of the week: accomplishments, blockers, upcoming work, open issues.

Optionally reference last week's report for a comparison view. If nothing was given, ask.

## Steps

1. Read the data. If it is a CSV, read every row, not just the last one. The trend is the story.
2. Check budget burn against percent complete. If burn is ahead of completion by more than a few
   points, say so explicitly. This is the most common early warning a status report hides.
3. Propose a RAG rating with the reasoning that led to it. The rating is a proposal. The delivery
   lead confirms or overrules it; never present it as settled.
4. Draft the report below. Compare the figures you were given; do not extrapolate from them. A
   cost at completion, a percentage over budget, or a revised go-live date is a forecast, and a
   forecast is a commitment the delivery lead makes, not the report. If the data points to one,
   say so to the delivery lead in a note outside the report and leave the report's figures as
   given.

## Output

**Overall Status:** [🔴 Red / 🟡 Amber / 🟢 Green]: one-sentence rationale

**Accomplishments This Week:**
- 3 to 5 bullet points tied to specific deliverables or milestones

**Upcoming (Next 2 Weeks):**
- 3 to 5 bullet points with target dates

**Risks & Issues:**
| Risk/Issue | Severity | Owner | Mitigation / Status |
|---|---|---|---|

**Action Items:**
| Action | Owner | Due Date | Priority |
|---|---|---|---|

*Drafted with Claude Code on YYYY-MM-DD; reviewed by [NAME]*

Use professional, direct consulting language. No filler sentences. If data is missing or
ambiguous, flag it explicitly with `[NEEDS INPUT]` rather than guessing. An invented number that
reaches a client is worse than a blank.

## Example Output

**Overall Status:** 🟡 Amber. Sprint 4 velocity is 15% below plan due to delayed UAT environment setup; mitigation plan in progress.

**Accomplishments This Week:**
- Completed data migration scripts for Orders and Inventory modules
- Delivered revised data mapping document to client for sign-off
- Onboarded two new client SMEs to the UAT process

**Action Items:**
| Action | Owner | Due Date | Priority |
|---|---|---|---|
| Finalize UAT environment configuration | Dev Lead | Fri May 10 | High |
| Client sign-off on data mapping document | Client PM | Wed May 8 | High |
