---
name: ftja-review
description: Look at pending apply/skip decisions (recorded via the FTJA review server) and propose concrete criteria.json/rubric.md changes for clear-cut reasons. Invoke when the user says "sort out my applications", "review the digest", "update the judgment criteria" — also runs automatically as part of /ftja-run's preflight when pending decisions exist.
---

# FTJA review

This is the feedback loop that closes the gap between "the pipeline judged
this job X" and "the candidate actually decided Y, for reason Z" — turning
real apply/skip decisions into concrete pipeline improvements, the same way
an ad hoc "I don't like this direction" complaint already does today, just systematized.

Decisions are recorded through the review server, not by hand-editing
digest files: tell the user to run `venv/bin/python -m ftja.server`
(Windows: `venv\Scripts\python -m ftja.server`, as for every command below) and
open `http://127.0.0.1:8765` in a browser (Chrome, Edge, or Safari — it's
a local HTTP server, not a static file, so any browser works) if they
haven't already. There they see every job that reached Stage 2 (passed,
review or stage2_fail) with one result per rubric criterion and the JD
quote behind it, and can record two things:

- for the job as a whole, an application status and a reason — each save
  calls `POST /api/decide`, which writes straight into `seen.db` via
  `ftja.state.update_decision`;
- for a single criterion, a disagreement ("it said this was met, but the
  sentence is about engineers building") — the flag on that row
  calls `POST /api/criterion-feedback`.

Nothing for this skill to parse out of a markdown file.

**This skill's steps 2-3 also run automatically inside `/ftja-run`'s
preflight** whenever pending decisions exist and the run is interactive —
that's the main way this logic actually executes day to day. Calling
`/ftja-review` directly is for reviewing on demand without waiting for the
next run.

## 1. Read what's pending

```
venv/bin/python -m ftja.state pending-review
```

Returns every `skipped_fit` decision with a non-empty reason that hasn't
been proposed-and-resolved yet (`decision_review_status IS NULL`). If
empty, there are no whole-job decisions pending.

```
venv/bin/python -m ftja.state pending-feedback
```

Returns every criterion-level disagreement that hasn't been resolved yet:
the job, the criterion id and label, what Stage 2 answered (`result`,
`quote`, `why`) and the user's `comment`. If both lists are empty, tell the
user there's nothing pending and stop.

## 2. Propose concrete changes

This is the step that makes it "learning" rather than just data collection.
For each pending decision, read `criteria.json` and `rubric.md` and judge
whether the reason maps to a concrete change:

- **A concrete, filterable attribute** (an industry, a company type, a
  technology, anything that would show up as a word in the JD) — e.g.
  "I don't want gambling companies" → propose adding `gambling`/`betting`/`casino`/
  `igaming` to `criteria.json`'s `exclude_keywords` (Stage 0, deterministic,
  cheap — filters before any LLM call, not just this one job).
- **A judgment-call nuance** (seniority framing, team structure, company
  stage, "too heavy a process for how they describe it") — propose adding
  or adjusting a line in `rubric.md`'s Fail/Preferences section (Stage 2).
- **Already covered** — if `exclude_keywords`/`rubric.md` already addresses
  this reason and the miss looks like one-off LLM judgment noise rather
  than a real gap, say so and treat it as declined (nothing to change).

A criterion-level disagreement is more specific than a whole-job reason:
it names the rubric line that was misapplied and shows the sentence it was
misapplied to. Read that criterion's text in `rubric.md` next to the quote
and the comment, and propose the wording change that would have produced
the answer the user expected — usually a clarifying clause or a
counter-example in that one line, not a new rule. Group feedback by
criterion id first: several disagreements on the same id are one proposal.
A disagreement with an empty comment still counts as a signal, but only
propose a change from it when the quote makes the problem obvious;
otherwise ask the user what was wrong.

If multiple pending decisions point at the same theme (e.g. three separate
reasons all about company stage), fold them into one proposal rather than
three near-duplicate edits — but still mark every contributing decision in
step 4.

## 3. Confirm before applying

Present all proposed changes as one list — reason(s) that motivated each,
and the exact edit — and wait for explicit approval, same as `/ftja-tune`.
Never edit `criteria.json`/`rubric.md` without that confirmation.

## 4. Resolve every pending decision either way

This is what stops the same reason from being re-proposed every single
`/ftja-run`. For each pending decision from step 1:

- If its reason contributed to an approved change:
  `venv/bin/python -m ftja.state mark-reviewed --job-url "<url>" --status applied`
- If the user declined the proposal it was part of (or step 2 judged it
  already covered / noise):
  `venv/bin/python -m ftja.state mark-reviewed --job-url "<url>" --status declined`

Resolve every criterion-level disagreement from step 1 the same way:

```
venv/bin/python -m ftja.state mark-feedback-reviewed --job-url "<url>" --criterion-id "<id>" --status applied|declined
```

A decision marked either way stays resolved permanently — it only becomes
pending again if the user edits that job's action/reason through the
review server (record_decision resets the status).

Do not commit the edits: `rubric.md` and `criteria.json` are personal files
that git ignores on purpose, so they never enter the repository's history.

`rubric.md` and `rubric-criteria.json` are the same rubric in two forms.
When a change is to one criterion's wording, or adds or removes a
criterion, make it in `rubric-criteria.json` (keep every other id as it
is) and then rewrite `rubric.md` from it:

```
venv/bin/python -c "import json; from ftja.verdict import save_criteria; d = json.load(open('rubric-criteria.json', encoding='utf-8')); save_criteria('.', d['criteria'], d.get('notes'))"
```

If you edited `rubric.md` as text instead, the list is stale and the next
`/ftja-run` rebuilds it in its preflight.

(The review server's Pipeline tab reads `criteria.json`/`rubric.md` live on
every request — nothing to regenerate.)

## 5. Report

Tell the user: how many pending decisions there were, which were applied
vs declined and why, and confirm nothing is left pending.
