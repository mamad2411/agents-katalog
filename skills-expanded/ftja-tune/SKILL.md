---
name: ftja-tune
description: Update rubric.md/criteria.json from a conversational statement of a new preference or dealbreaker. Invoke when, in the course of ANY conversation about jobs/career in this project, the user states a new preference, dealbreaker, or pivot ("I'm not interested in traditional PM roles", "drop the onsite-required ones") — proactively offer to add it, don't silently apply it.
---

# FTJA tune

This is the explicit-confirmation half of "self-improving rubric" (see
SPEC.md's Future Vision section for why the implicit/automatic half is
deliberately out of scope). Never edit rubric.md or criteria.json without
the user confirming first.

## When to trigger

The user says something, in passing or directly, that reads as a job-search
preference, dealbreaker, or a scope pivot (e.g. moving from one kind of role
to another). This can happen mid-conversation about something else that
touches on career/roles — you don't need an explicit `/ftja-tune` invocation.

## What to do

1. Read the current `rubric.md` and `criteria.json`.
2. Restate the new signal back to the user in one line and ask: "should I
   add this to the judgment criteria?" Do not just add it.
3. **Check for conflict** against the existing rubric/criteria. If the new
   statement contradicts something already there (e.g. rubric says "remote
   preferred" and the user now says "drop the onsite-required ones" — that's
   not a conflict, that's a tightening; but if it contradicts something like an
   existing dealbreaker being loosened, or two preferences that can't both
   hold), surface the conflict explicitly and ask which one wins. Don't
   silently pick.
4. On confirmation, edit the file (the rubric for narrative criteria,
   `criteria.json` for structured filters — a "no on-site" statement likely
   touches both: an `exclude_keywords` entry AND a rubric Fail criterion,
   ask if unsure which).

   The rubric exists in two forms that must stay the same rubric:
   `rubric-criteria.json` (a list of single criteria, which the user also
   edits in the viewer's Pipeline tab) and `rubric.md` (what the models
   read). If `rubric-criteria.json` exists, make the change there — add an
   entry (`kind`: `pass` / `fail` / `preference`, a `label` that reads on
   its own, the rule as `text`) or reword one, leaving every other entry's
   `id` as it is — then rewrite `rubric.md` from it:

   ```
   (Windows: `venv\Scripts\python` in place of `venv/bin/python`.)
   venv/bin/python -c "import json; from ftja.verdict import save_criteria; d = json.load(open('rubric-criteria.json', encoding='utf-8')); save_criteria('.', d['criteria'], d.get('notes'))"
   ```

   Editing `rubric.md` as text instead would leave the list stale, and the
   user's next save in the Pipeline tab would overwrite your edit. Only
   when `rubric-criteria.json` doesn't exist yet (no run since setup) edit
   `rubric.md` directly.
5. Do not commit: `rubric.md` and `criteria.json` are personal files that
   git ignores on purpose, so they never enter the repository's history.
   Nothing to regenerate — the review server's Pipeline tab reads
   `criteria.json`/`rubric.md` live on every request.
6. Confirm the change back to the user in one line.

## What NOT to do

- Don't infer preferences from behavior (which digest jobs they clicked,
  applied to, etc.) — there's no tracking of that in this version. Only act
  on things the user actually said.
- Don't batch up multiple unrelated changes into one edit — one
  conversational update, one change, confirmed back to the user, so each
  one can be undone on its own.
