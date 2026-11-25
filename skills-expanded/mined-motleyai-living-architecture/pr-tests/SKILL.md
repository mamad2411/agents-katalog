---
name: pr-tests
description: Stage 2 of 4 of the /la:pr flow — write the full failing test suite for the agreed plan (TDD-first), then Codex-review the tests against the plan. Normally dispatched by /la:pr; if the /la:pr context (BRANCH, CHANGE_ID, OPENSPEC, tracker issue) is not already loaded in this session, invoke the la:pr skill instead.
---

**Stage 2 of 4 of the `/la:pr` flow.** Prerequisite: `/la:pr` has run in this
session, preflight included, and established `BRANCH`, `CHANGE_ID`, `OPENSPEC`, and the full tracker
issue (body + comments), if there is one. If any of that is missing, invoke the `la:pr` skill
instead — it rehydrates and dispatches back here. The `/la:pr` stopping policy
applies throughout this stage.

Before writing anything, recover the durable plan from `pr-plan`:
- `OPENSPEC=1` — read the whole change folder
  `openspec/changes/<CHANGE_ID>/` (proposal, design, tasks, delta specs).
- `OPENSPEC=0` — the finalized plan is a comment on the tracker issue.

## Step 1 — Write the tests first

TDD-first: land the **full**
test suite for the agreed plan before writing any implementation. Tests
should fail for the right reason (feature missing), not for setup reasons.
Run the tests in the `/la:pr` local test scope to confirm that.

If `OPENSPEC=1`, derive the test cases from the delta scenarios in
`openspec/changes/<CHANGE_ID>/specs/<capability>/spec.md`: every
`#### Scenario:` needs at least one covering test.

When writing tests, follow the `la:concise-comments` skill: no design essays,
ticket-ID-on-every-line, or code-restating comments; docstrings to a line.
Rationale belongs in the spec / PR description / the tracker issue — not in
code — so verbose comments never get written in the first place.

## Step 2 — Codex review of the tests against the plan

**Codex follows `reviewers.codex`.** If `la-config get reviewers.codex` prints `false`, skip this step. Otherwise, if the Codex MCP server (`mcp__codex__codex`) is not available, STOP and tell me: this repo requires Codex reviews, so never skip one silently.

Hand both the plan (from `pr-plan`, post-discussion) and the new tests
to `mcp__codex__codex` and ask it to verify that the tests faithfully cover
the plan: every behavior in the plan has at least one test, edge cases
discussed during the plan review are exercised, and no test asserts behavior
that contradicts the plan. Codex should not modify files.

Bring the findings back to me. Adjust the tests (add, remove, or fix) based
on what we agree on before writing implementation.

If `OPENSPEC=1`, "the plan" includes the delta specs: verify every ADDED/MODIFIED
requirement and each of its scenarios has a covering test.

## Step 3 — Commit the changed files

Once the tests are finalized (Step 2 findings resolved), `git add` every file
this stage created or changed — by specific named path — then commit them. This
is the full set: new test modules and their fixtures/helpers, plus any file this
stage only **modified** (a flipped existing test, a reworded docstring, an
amended golden file, an approved plan/spec edit). Per the `/la:pr`
"commit at the end of every stage" rule, do this **without asking**. Rules that
still hold:

- NEVER `git add -A` / `git add .` / `git add tests/` — only specific named
  paths. Listing several named paths in one `git add` command is fine; a bulk
  add (all files, `.`, or a directory) is not.
- Do NOT push — the first push happens in `pr-implement`.

## Step 4 — Hard stop

> **🛑 HARD STOP (reset point 2 of 3) — before implementation.** The finalized
> failing tests, and every other file this stage created or changed, are
> committed. Say we're at reset point 2 and STOP — do not start implementing.
> I'll `/clear` and re-invoke `/la:pr`, which will detect and run `pr-implement`.
