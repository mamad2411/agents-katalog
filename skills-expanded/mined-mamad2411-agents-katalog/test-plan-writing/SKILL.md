---
name: test-plan-writing
description: Teaches how to derive a test plan directly from a PRD's Given/When/Then acceptance criteria, with edge/negative/regression coverage, risk-based prioritization, and clear exit criteria. Use whenever a QA agent (qa-engineer-web, qa-engineer-mobile, or qa-engineer-api) must plan testing for an issue before executing it.
---

# Test Plan Writing

A test plan is how you prove an issue meets its acceptance criteria — not a wish list of everything you could check. It is derived from the PRD, traceable back to it, and posted as an issue comment **before** you run a single test. If there is no PRD comment with acceptance criteria, the issue is not ready for QA; comment saying so and stop.

## Step 1 — Trace every acceptance criterion to a test case

Open the PRD comment (added by product-manager during `phase=product-definition`). Each user story has acceptance criteria in Given/When/Then form. For **every** criterion, write at least one test case whose expected result is that criterion, quoted **verbatim**.

Verbatim traceability is the point: a reviewer must be able to line up each criterion against a test case with no interpretation. Do not paraphrase "Given a logged-in user with an empty cart" into "user has no items" — copy it. If a criterion is too vague to test (no observable outcome), that is a PRD gap: comment on the issue, tag product-manager, and treat it as `Blocked` rather than inventing the expectation yourself.

## Step 2 — Add the cases the PRD didn't spell out

Acceptance criteria describe the happy path. Bugs live at the edges. Add:

- **Boundaries**: min/max lengths, 0 / 1 / n items, first/last page, date rollovers, numeric limits and off-by-one around them.
- **Empty & max inputs**: empty strings, empty lists, whitespace-only, maximum field sizes, oversized uploads.
- **Negative cases**: invalid input, wrong types, malformed payloads, unauthorized actor, expired session — assert the *specified* rejection, not just "it fails".
- **Concurrency**: two writers on the same record, double-submit, race on a limited resource (last seat, last stock unit).
- **Permissions**: each role that touches the feature — allowed roles succeed, denied roles are refused as specified.

## Step 3 — Scope the regression

List existing flows this change can plausibly break (shared components, shared endpoints, shared tables). Pull the impacted set from the diff and its dependents, not guesswork. Name them explicitly in the plan so the regression run is auditable. See the `regression-strategy` skill for selection method.

## Step 4 — Prioritize by risk

Order execution so that **what breaks worst runs first**. Rank each area by (likelihood it's broken) × (blast radius if it is). Money paths, auth, data-integrity, and anything on a `critical`-flow list go to the top. If time runs out, it must run out on the low-risk tail, never on checkout or login.

## Test case format

Every case uses these fields:

```
- id:            TC-<issue>-<n>
  criterion:     <verbatim acceptance criterion, or "edge/negative/regression: <what>">
  preconditions: <state/data/role required before step 1>
  steps:         <numbered, deterministic, no "etc.">
  expected:      <single observable outcome>
  evidence:      <what to capture as proof: screenshot, log line, response body, recording>
```

`evidence` is not optional — every case names the artifact that will prove pass/fail, because "Done" requires evidence in comments.

## Exit criteria

State them in the plan so "done testing" is not a judgment call:

- Every acceptance criterion has a passing test case with attached evidence.
- All planned edge/negative/regression cases executed (pass, or filed as a bug).
- **No open `urgent` or `high` bugs** linked to the issue.
- Any deferred `low`-priority bugs are filed and explicitly acknowledged, not silently dropped.

## Anti-patterns

- Testing only the happy path because the PRD only described the happy path.
- Paraphrasing acceptance criteria so traceability breaks.
- A plan with no `evidence` column — unprovable results.
- Running low-risk cosmetic checks before the money path.
- Writing the plan *after* testing to match what you happened to do.

## Final step (do this every time)

1. Post the completed plan as a comment on the issue **before executing**.
2. Execute in risk order, attaching evidence per case as you go.
3. File any failures as bugs via the `bug-report-standards` skill, linked to this issue, with the correct `urgent`/`high`/`low` priority.
4. Only when exit criteria are met, move the issue toward `Done` (with QA evidence in comments) per the Definition of Done.
