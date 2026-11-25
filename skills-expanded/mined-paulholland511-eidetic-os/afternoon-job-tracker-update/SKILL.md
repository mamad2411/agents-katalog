---
name: afternoon-job-tracker-update
description: Afternoon email scan for job-application updates — catches later emails and updates the tracker spreadsheet.
---

Check your inbox for job-application updates since the morning scan and update
the job tracker spreadsheet. This is the afternoon check (e.g. 2pm on weekdays).

> Placeholders: `{{USER_EMAIL}}` = your address, `{{JOB_TRACKER_PATH}}` = path to
> your tracker `.xlsx` (keep OUTSIDE the repo — personal data), `{{WATCHLIST}}` =
> comma-separated companies/recruiters you're tracking.

**Step 1 — Search email** using your connected email MCP/tools:
- Search threads from the last 6 hours matching: interview OR shortlist OR application OR rejected OR offer OR "next stage" OR "moving forward" OR "pleased to" OR any name in `{{WATCHLIST}}`
- Also search common recruiter senders, subject:application newer_than:6h
- Read full thread content for anything that looks like an application confirmation, rejection, interview request, or status update

**Step 2 — Classify each email** as one of:
- NEW APPLICATION → add new row, status "Applied"
- REJECTION → status "Rejected", add date + reason
- INTERVIEW → status "Interview" / "2nd Interview", add details
- SHORTLIST → status "Shortlisted", add details
- STATUS UPDATE → update notes only
- IGNORE → job alerts, recommendations, newsletters (skip)

**Step 3 — Update spreadsheet** at `{{JOB_TRACKER_PATH}}`:
- Use `openpyxl` to load, modify, and save
- For new applications: add a row with Date, Source, Company, Role, Status, Notes
- For status changes: find the matching row and update Status and Notes
- Preserve all existing formatting

**Step 4 — Report** what was found and updated.

**Watchlist:** Track the companies/recruiters in `{{WATCHLIST}}` and surface
related updates at the top of the report.

**Constraints:**
- This is an automated run. Do not ask questions — make reasonable choices.
- If unsure whether an email is a new application or just a recommendation, err on the side of adding it.
- The tracker file holds personal data — never commit or transmit it.
