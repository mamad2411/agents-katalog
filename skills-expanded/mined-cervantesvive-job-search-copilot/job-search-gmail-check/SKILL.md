---
name: job-search-gmail-check
description: Scans Gmail for recruiter or company replies tied to the job search and flags ones needing a response, or surfaces new inbound recruiter outreach. Triggers on scheduled runs ("run the job-search-gmail-check skill"), and on-demand requests like "check my email for replies", "any recruiter emails?", or "did anyone get back to me?".
---

# Gmail reply check

Read `${CLAUDE_PLUGIN_ROOT}/shared/conventions.md` first, then
`tracker-data.md` and `gmail-status.md` from project memory.

If `gmail-status.md` says Gmail isn't connected, or the `mcp__Gmail__*` tools
aren't available in this session, tell the user Gmail isn't connected yet and
that they can say "connect Gmail" to set it up (that runs through
`SuggestConnectors` with keywords `["gmail", "email"]`), then stop.

## Search

Read `tracker-data.md` to get the list of companies currently in
`applications` (and recent `leads`). Using `mcp__Gmail__search_threads`, search for messages
newer than `gmail-status.md`'s last-run timestamp, per company, using the
company name and common recruiting-domain patterns (e.g. `from:company.com
OR from:greenhouse.io OR from:lever.co OR from:myworkday.com`, scoped with
the company name in the query too since ATS domains are shared across many
companies). Also do one broader search for generic recruiting language
(`"next steps" OR "interview" OR "schedule a call"`) newer than the last run,
to catch inbound outreach from companies not yet in the tracker.

## Classify each thread

For each relevant thread, read it (`mcp__Gmail__get_thread`) and determine:

- **Needs a reply** — the most recent message is from the company/recruiter
  and the user hasn't responded since.
- **Informational** — rejection, automated confirmation, or the user already
  replied last.
- **New inbound** — from a company not currently in the tracker at all.

## Update the tracker

For threads tied to an existing `applications` entry: append a short,
dated note to that entry's `notes` field, e.g. `"⚠️ [date] Recruiter
followed up, needs a reply"` or `"[date] Rejection received"`, and update
`status` if the thread makes a stage change obvious (e.g. an onsite
invitation → `Onsite`).

For new inbound outreach not tied to any existing entry: add it to `leads`
with `source: "inbound email"` and a `fitNotes` summarizing what the email
said.

Write these changes straight to `tracker-data.md` — that's the step that
must succeed. Then run the sync procedure from `shared/conventions.md` to
update the webpage view (best-effort, same as `job-search-scan`).

Update `gmail-status.md` with the new last-run timestamp regardless of
whether the webpage sync succeeded.

## Summary

End with a short plain-language reply: how many threads needed a reply
(name the company for each — this is the most time-sensitive part, put it
first), anything new inbound, and nothing else if there's nothing to flag.
