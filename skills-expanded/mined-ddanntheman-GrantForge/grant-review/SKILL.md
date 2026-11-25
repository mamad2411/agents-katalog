---
name: grant-review
description: >
  Pre-submission review of a grant application. This skill should be used when
  the user says "review the application", "score our draft", "are we ready to
  submit", "run the compliance check", or when drafting is complete for a grant
  in the pipeline. Runs a compliance audit and a mock-scorer pass, and produces
  the requirements-to-response compliance matrix.
version: 0.1.0
---

# Grant Review

Two independent passes, run in this order, plus a traceability deliverable.
Do not soften findings; a hard review here is cheaper than a rejection.

## Pass 1 — Compliance audit

Work through `requirements.md` mechanically. For every requirement, verify
against the actual draft files (not from memory):

- Every required narrative section exists and answers its verbatim prompt.
- Every limit respected: pages, words, characters (count them), font,
  margins, spacing, file naming, file format.
- Every required attachment present or explicitly tracked as pending with
  an owner and date.
- Every "must/shall" statement in the announcement satisfied.
- Budget totals within award range; match requirement met; budget
  narrative matches workbook.
- All statistics carry citations that appear in `research/evidence.md`.

Any failure is a **blocker**. List blockers first, plainly.

## Pass 2 — Mock scorer

Adopt the persona of a tired reviewer on their fourteenth application of
the day, scoring strictly against the funder's published rubric (or a
standard rubric — need 25 / design 30 / capacity 20 / evaluation 15 /
budget 10 — if none was published).

For each scored criterion: assign points with a one-paragraph justification
written as a reviewer comment, quote the weakest passage, and state the
single change that would most raise the score. Score honestly against the
likely field of applicants, not against effort. Then report: total score,
the three highest-leverage revisions, and a judgment — "fund", "fundable
with revisions", or "not competitive as written" — with the reason.

Also run the house-style humanization check across the full application:
any surviving AI tells, banned phrases, or unsourced numbers get flagged
as revision items.

## Deliverable — Compliance matrix (`final/compliance-matrix.xlsx`)

A traceability table, one row per requirement: `Requirement (verbatim) |
Source (page/section of announcement) | Where addressed (document, section,
page) | Status (met / partial / missing) | Notes`. This doubles as the
user's final pre-submission checklist and, for federal grants, a defensible
record of diligence.

## After the review

Present blockers, then scores, then the revision list ranked by point
impact. Offer to apply the revisions via grant-draft. When all blockers
clear and the user accepts the score, move final documents to `final/`,
update `tracker.md` to `ready to submit`, and remind the user of the
submission mechanism and deadline from the requirements matrix, including
portal registration lead times.
