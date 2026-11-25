---
name: daily-job-tracker-update
description: Morning email scan for job-application updates — new applications, rejections, interviews, shortlists — and update a tracker spreadsheet.
---

Check your inbox for job-application updates and update the job tracker
spreadsheet. This is the morning check.

> Placeholders: `{{USER_EMAIL}}` = your address, `{{JOB_TRACKER_PATH}}` = path to
> your tracker `.xlsx` (keep this OUTSIDE the repo — it contains personal data),
> `{{WATCHLIST}}` = a comma-separated list of companies/recruiters you're
> tracking (configure per user; do not hardcode).

**Step 1 — Search email** using your connected email MCP/tools:
- Search threads from the last 24 hours matching: interview OR shortlist OR application OR rejected OR offer OR "next stage" OR "moving forward" OR "pleased to" OR any name in `{{WATCHLIST}}`
- Also search common recruiter senders, e.g.: `from:linkedin.com OR from:<your-job-boards>` subject:application newer_than:1d
- Read full thread content for anything that looks like an application confirmation, rejection, interview request, or status update

**Step 2 — Classify each email** as one of:
- NEW APPLICATION: confirmation an application was sent (add new row, status "Applied")
- REJECTION: application declined (status "Rejected", add date + reason to notes)
- INTERVIEW: interview request/scheduling (status "Interview" / "2nd Interview", add details)
- SHORTLIST: shortlisted for next stage (status "Shortlisted", add details)
- STATUS UPDATE: recruiter follow-up or feedback (update notes only)
- IGNORE: job alerts, recommendations, newsletters (skip)

**Step 3 — Update spreadsheet** at `{{JOB_TRACKER_PATH}}`:
- Use `openpyxl` to load, modify, and save
- For new applications: add a row with Date, Source, Company, Role, Status, Notes
- For status changes: find the matching row and update Status and Notes
- Preserve all existing formatting
- Leave any "Closing Date" column blank unless mentioned in the email

**Step 4 — Report** what was found and updated:
- Number of new applications added
- Number of status changes (rejections, interviews, shortlists)
- Any emails that need your attention (interview scheduling, recruiter questions)
- Current totals: X applications, Y active, Z rejected, W interviewing

**Watchlist:** Track the companies/recruiters in `{{WATCHLIST}}`. Surface any
update relating to them at the top of the report.

**Constraints:**
- This is an automated run. Do not ask questions — make reasonable choices.
- If unsure whether an email is a new application or just a recommendation, err on the side of adding it.
- Always preserve existing spreadsheet formatting.
- The tracker file holds personal data — never commit it to the repo or send it anywhere it isn't explicitly meant to go.
