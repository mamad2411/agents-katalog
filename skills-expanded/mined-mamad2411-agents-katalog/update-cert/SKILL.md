---
name: update-cert
description: Refresh facts on an existing certification JSON when an Issue or routine sweep flags that something changed.
---

# update-cert

## When to use

- An `update-certification` Issue arrives.
- A routine sweep (monthly cron or `make` target) finds a cert with a stale
  `official.fetched_at`.
- A reviewer notices a logistics field is wrong (cost changed, exam
  retired, blueprint refreshed).

## Process

1. **Locate the file** under `data/certs/<vendor>/<cert>.json`.
2. **Re-fetch the official URL** with WebFetch. Compare against the JSON,
   diffing field-by-field:
   - `name`, `abbr`, `vendor.url`
   - `logistics.cost_usd`, `duration_min`, `questions`, `languages`,
     `renewal_years`, `ce_required`, `format`
   - `prerequisites.experience_years`, `recommended_certs`

   **Special attention to `recommended_certs[]`**: this list powers the
   roadmap UI's arrow overlay (prerequisite arrows from this cert, and
   inverse-lookup successor arrows on the prereqs themselves). If the
   vendor adds, removes, or renames a prerequisite, the arrows must follow
   — update the list explicitly rather than leaving stale entries.
3. **Refresh `third_party_evaluations[]`.** For each existing entry, re-fetch
   to confirm the URL still resolves and the `level_hint` still matches
   the evaluator's current page. Add new entries when you find them.
4. **Update `official.fetched_at`** to today's date. Add `note` fields to
   any factor whose evidence has shifted.
5. **Do not rewrite `scoring_factors` casually.** Only change a factor when
   the underlying evidence has changed. Comment on the diff in the PR
   description.
6. **Track availability changes.** If the vendor has paused, retired, or
   announced a future launch, set the top-level `availability` field
   (`paused` / `retired` / `coming-soon`) and a one-line `availability_note`
   quoting the vendor's wording. Reset to `available` (or remove the field)
   once delivery resumes. The roadmap UI surfaces availability as a card
   badge and a banner in the detail panel.
7. **Reset evaluation freshness.** Set `evaluation.computed_at = null` and
   `evaluation.computed_tier = null` so CI's `check_evaluations_fresh.py`
   forces a re-run of `evaluate-roadmap-3-personas`.
7. **Update manifest + validate** (`make manifest`, `make validate`).
8. **Open a PR** with a description that lists each changed field and
   links the evidence.

## Retired or renamed certs

- If the vendor has retired the cert, set
  `evaluation.computed_tier = null` and add a top-level field is **not**
  appropriate (the schema does not allow extra fields). Instead: in the
  PR description, propose moving the file to `data/certs-retired/` (a
  future schema addition) and ask the maintainer.
- If renamed, change `name` and `abbr`; keep the file path so URLs in
  third-party documents still resolve, unless the vendor itself changed.
