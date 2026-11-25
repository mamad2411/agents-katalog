---
name: quality-loop
description: >-
  use this when a shipped product needs an honest feature inventory
  and test pass — discover every user-facing feature from the code,
  generate and run cases, fix defects, regress, loop until the sheet
  is complete
license: MIT
metadata:
  portability: portable
---
# quality-loop

Inventory what the **code actually does**, then test, fix, and regress
until the sheet is complete. Expected behaviour comes from implementation,
not from docs or memory.

This loop will not fit one smart-zone session. Write the sheet to disk
and come back. Do not ingest the whole tree into chat.

Docs describe shipped behavior. Aspirational product copy is not a row.


## When

- A shipped product needs an honest feature inventory and test pass.
- A plan or diff needs a P0/P1/P2 read → use review instead (a shipped product
  audit is quality-loop, not review).
- Orientation in an unfamiliar codebase → use learn-codebase instead.

## Before you start

- Confirm cwd is the named product before editing. Wrong repo is a stop.

## Artifact (source of truth)

One canonical spreadsheet, **outside** the product as living docs.
Default: sibling workspace `<repo>-qa/features.csv` (xlsx is fine).
Do not commit a living sheet into the app repo. Code stays primary.

Required columns — keep these names:

| Feature ID | Feature Name | User Story | Expected Behaviour | Edge Cases | Test Cases | Current Status | Defect Count | Severity | Notes | Last Tested Date |

Status values: `undiscovered` | `documented` | `tests-written` | `tested` | `failing` | `fixed` | `waived` | `regressed`.
Severity: `critical` | `high` | `medium` | `low`.
IDs: `F-001`, `D-001`, sequential, never reused.

Update the sheet the moment a fact changes. The sheet is the handoff.

## Phase 1 — Feature discovery

Inventory from surfaces, not from a dump of every file:

- routes / screens / navigation
- user-facing workflows and business processes
- API endpoints the product exposes or calls
- configuration options that change behaviour
- permissions, empty states, error states, background jobs

For each feature write: unique Feature ID, name, user story, expected
behaviour **from the code**, edge cases, validation rules, dependencies,
assumptions. Status = `documented`.

Exit: every identifiable user-facing feature, screen, route, workflow,
and API is a row. No "we'll add it later."

If the surface list is large, finish one surface per session, then
handoff. The next session starts from the sheet, not the old transcript.

## Phase 2 — Test generation

For every row, add cases covering:

- happy path
- error path
- boundary conditions
- invalid input
- permission / security
- performance where it can break the journey
- mobile / responsive if the product has a UI

Each feature gets at least one complete suite. Major journeys get an
end-to-end case that crosses features. Status = `tests-written`.

Prefer runnable checks the repo already has (unit, e2e, API). Write
missing cases as steps in the sheet first; automate only a case you
have executed by hand once.

## Phase 3 — Execution

Run every case. On failure record immediately:

- Defect ID, Feature ID
- reproduction steps
- expected result / actual result
- severity
- root-cause hypothesis

Bump Defect Count and Severity on the feature row. Status = `failing`
or `tested`. Last Tested Date = today.

No fake eval. No hash embeddings. No template output labeled as model
output. An eval that does not run the production path does not count.
Generated-but-unrun cases stay `tests-written`, not `tested`.

Exit: every case executed, every defect documented. Do not skip a
case because the fix "looks obvious."

## Phase 4 — Remediation

For each open defect: smallest safe fix, verify locally, update status.

Focus: functional breaks, UX friction, workflow / navigation gaps,
validation errors, accessibility, error messaging, data integrity,
performance bottlenecks.

Waive only with an explicit Notes reason. Waived ≠ fixed.

Exit: every defect `fixed` or `waived`.

If a fix is a multi-session feature, graduate that defect to **to-spec**
(destination spec + vertical tickets) and keep the sheet row pointed at
the ticket. Do not grow a living SPEC.md in the app repo.

## Phase 5 — Regression

Re-run every case and every major end-to-end journey. Status =
`regressed` only after the rerun. New failures become new Defect IDs.

Exit: all tests pass; no open `critical` or `high`; no broken journey.

## Phase 6 — Recursive loop

Repeat 1 → 2 → 3 → 4 → 5 until all of these are true:

- no undiscovered feature
- no failing test
- no open critical or high defect
- no unresolved UX issue you logged
- no incomplete user journey

After each iteration write, next to the sheet:

1. Coverage summary
2. Features tested
3. Defects found
4. Defects fixed
5. Remaining risks
6. Confidence score (0–100%)

Never declare completion unless the exit list is satisfied. A high
confidence score with open highs is a lie — fix the sheet first.

## Anti-patterns

- Dumping the repo into context and calling that discovery.
- Treating README / Figma / memory as expected behaviour when the code differs.
- Committing the living sheet into the product tree as source of truth.
- Declaring done after one pass with rows still `documented`.
- Fixing without a Defect ID on the sheet.
- Running the whole loop as one `/goal` on the sheet — that is the spec trap.
  Work one phase, or one surface, per session.
- Counting an unrun generated case as evidence.

## Related

learn-codebase (orientation only; this skill owns the inventory) ·
to-spec (graduate a fat defect) · ralph-loop (sheet rows as a queue) ·
handoff (phase / session boundary) · compact (same-session implement→QA)
