---
name: new-job
description: This skill should be used when the user wants to add a new company or job to their Excel tracker (List.xlsx). Triggers on phrases like "add [company] to tracker", "I applied to [company]", "track [company]", "save [company] for later", "add [company] [role]", "new application at [company]".
---

# Add New Job to Tracker

Add a new row to `List.xlsx` (Sheet1) with the bundled script. Do not write ad hoc openpyxl code.

## Column layout
- A: Company name
- B: Role title
- C: Role link (job posting URL, without tracking redirects; `/thanks` pages are fine)
- D: Status
- E: HR contact (leave empty; use the update-hr skill)
- F: Comments (optional)

## Status values
- `done` = applied (default)
- `In progress` = ONLY when a callback/response was received
- `Rejected` = only when logging a rejection for a job that was never tracked

## Steps
1. Get the company name (required), role title and job URL. If the user only pasted a link, fetch the page (or the ATS public API: Ashby/Lever/Greenhouse) to get company and role.
2. Run from the project root (`claude-job-agent/`):
   ```
   python .claude/skills/new-job/scripts/add_job.py --company "Company" --role "Role" --url "https://..." [--status done] [--comment "..."]
   ```
3. Handle the result:
   - `ADDED: row N` (exit 0) → confirm company, role, status and row to the user.
   - `DUPLICATE` (exit 2) → the same job URL is already tracked; tell the user the existing row, do not add.
   - `COMPANY EXISTS` (exit 3) → show the existing rows. If it's a different role, re-run with `--force`.
   - `ERROR` (exit 1) → e.g. Excel has the file open; ask the user to close it and retry.

The script takes the shared tracker lock, backs up List.xlsx to `backups/` before writing, and matches URLs ignoring `www`, query strings, trailing slashes and `/thanks` or `/application` suffixes.

## 4. Same-day outreach (her rule 2026-11-23: cold email reaches people faster than the application itself)
Right after `ADDED` with status `done` (she applied), don't wait for the weekly HR agent:
1. **Earlier contacts at this company?** If other rows of the company have col E contacts, they were copied to
   the new row (weekly-hr-agent `tracker.copy_hr_contacts`; run it now if the new row's col E is still empty).
   Tell her who is there and who has an email. Someone emailed less than 3 months ago is not emailed again.
2. **Otherwise run `/find-contacts` for this job straight away** (treg first while its balance is above $0.50):
   the recruiter AND the hiring manager of the job description's team, written to col E.
3. **Draft the follow-up with `/send-outreach`** for those contacts and show it to her. She approves, a test
   send goes to her first, then the real send. Never send without her OK.
Skip step 4 only for status `Rejected` / `In progress`, or when she says "just add it".
