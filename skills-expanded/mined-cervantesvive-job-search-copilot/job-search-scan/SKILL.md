---
name: job-search-scan
description: Scans configured job boards and/or company career pages for new roles matching the user's target profile and adds matches to the tracker's Leads list. Triggers on scheduled runs ("run the job-search-scan skill's job-board mode / company-page mode"), and on-demand requests like "scan for new jobs", "check job boards now", "check company career pages", or "any new leads?".
---

# Job search scan

Read `${CLAUDE_PLUGIN_ROOT}/shared/conventions.md` first. Then read
`profile.md`, `search-config.md`, `tracker-data.md`, and `network.md` (if it
exists) from project memory. If `tracker-data.md` doesn't exist, this
project hasn't been set up yet — tell the user to run setup first (say "set
up my job search") and stop.

Run **job-board mode**, **company-page mode**, or both, based on what the
caller asked for. A scheduled trigger says which one explicitly. A manual
request like "scan for new jobs" with no mode specified runs both.

## Job-board mode

For each entry in `search-config.md`'s `job_boards`:

- If it's a specific saved-search URL, fetch it and read the listed roles.
- Otherwise, search mode: use web search with the board name, the target
  role titles and level from `profile.md`, and the target locations —
  e.g. `site:linkedin.com/jobs "Engineering Manager" Bay Area`. Prefer
  recent postings (last 1-2 weeks) when the source shows dates.

Keep only postings that plausibly match the target profile (role/level,
location or remote fit, not an obvious mismatch on seniority). When in
doubt, err toward including it with an honest `fitNotes` rather than
guessing it away.

## Company-page mode

Work through `search-config.md`'s `companies` list in rotating batches so
the whole list gets covered every 10-14 days at the configured cadence
rather than everyone getting re-checked every run:

- Start at `rotation_index`. Order high-priority companies first, then
  medium, then low, wrapping back to the start once you pass the end of the
  list.
- Batch size: enough to cycle the full list in ~10-14 days at this scan's
  cadence. Default to 25 if that's not calculable (e.g. `list length ÷
  (12 days ÷ cadence_days)`, minimum 10, maximum 60).
- For each company in the batch: if `career_page_url` is set, fetch it and
  look for open roles matching the target profile. If not set, or the fetch
  fails, search for it (e.g. `"[Company]" careers engineering manager`) and,
  if found, add the URL to that company's `search-config.md` entry so future
  runs can fetch it directly.
- After the batch, update `rotation_index` to just past the last company you
  checked (wrapping to `0` if you reached the end).

## Adding matches

For every new match, in either mode: dedupe against `applications` and
`leads` already in `tracker-data.md` (company + role, case-insensitive) —
skip if already present. Otherwise build a `leads` entry per the schema in
`shared/conventions.md`: `source` is the board name or `"career page scan"`,
`fitNotes` is one honest sentence on why it matches (or a caveat if it's a
stretch), and `knowSomeone` is set from `network.md` if any current
connection's company matches (name + their title, else leave empty).

Write the new `leads` entries and bumped `lastUpdated` straight to
`tracker-data.md` — this is the step that must succeed for the scan to count
as done. Then run the sync procedure from `shared/conventions.md` to update
the webpage view (best-effort; see that section for how to handle it
failing — it's not this skill's problem to solve). Update `search-config.md`
if `rotation_index` or any `career_page_url` changed — do this regardless of
whether the webpage sync succeeded, since it's independent.

## Summary

End with a short plain-language reply: how many boards/companies were
checked, how many new leads were added (list company + role for each, and
call out anything with a `knowSomeone` match), and nothing else if nothing
new was found ("Checked N companies, nothing new this time — I'll pick up
where I left off next run.").
