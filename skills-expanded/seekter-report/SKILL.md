---
name: seekter-report
description: Summarise the job search from the markdown tracker - funnel, response rate, what's working, where applications come from, what's pending on the user. Use when the user runs /seekter-report or asks how the search is going, for weekly numbers, or what to change.
---

# /seekter-report — how is the search going

Read-only. Data comes from `applications/` via `scripts/seekter.mjs`, plus `runs/*.md` for per-day source tables.

1. `node scripts/seekter.mjs stats` (all time) and `node scripts/seekter.mjs stats --since <7 days ago>`.
2. `node scripts/seekter.mjs list --since <period start>`, then read the front matter of the rows you need (source, ats, location_fit, fit).
3. Compute, for the period and all time:
   - applications sent, skips, pending hand-offs;
   - replies: interviewing + offer + rejected, as a share of sent; median days from `applied` to the first log line after it;
   - the breakdowns, each one command (`node scripts/seekter.mjs stats --by <field> [--since …] [--min 5]`), which print sent, replies and interviews per group:
     - `source` (freehire, linkedin, board names, manual) and `apply_type` (company form, Easy Apply, email);
     - `ats`, the form system the application went through;
     - `location_fit` (A/B/C). A track with many sends and no replies is a targeting signal;
     - `title` and `seniority`, derived from the role ("Senior Product Designer (Growth)" counts as product designer · senior);
     - `fit` and `resume`, once they are filled: whether the fit score predicts replies is the question the score exists to answer, and the resume type is what the run uploaded;
     - `month`, to see whether the funnel is moving.
   An interview is a record that reached `interviewing` or `offer`, even if it was later rejected or closed. Replies include rejections. Rates are over **decided** applications (a reply, or closed); one still `applied` is "in flight", has its own column and counts in no rate, so a week of fresh sends does not pull a group down. A group with fewer than 5 decided shows `n<5` instead of a rate (`--floor` changes it): quote its counts, not a percentage. With only a handful of interviews, compare groups on replies and say how many interviews there are rather than quoting interview rates;
   - top skip reasons (group the Reason column of `applications/<YYYY-MM>/skipped.md` by its first clause).
4. Every record with `status: pending` is a hand-off (`node scripts/seekter.mjs list --status pending`; also the "Needs you" table in `applications/README.md`): list each with its link and the exact action.
5. Write 3–5 plain observations with the number behind each ("C-track: 14 sent, 0 replies in 3 weeks"). Suggest at most two changes, each tied to a file (`profile/settings.json` query, `profile/profile.md` rule). Don't change them without the user saying yes.

Save as `runs/report-<YYYY-MM-DD>.md` and show the user the short version.
