---
description: Run the complete ATDD cycle from requirements to a verified, spec-compliant, quality-gated implementation — through to PR and review resolution. Spec approval is the only mandatory stop; autonomy after that is chosen at the approval gate.
argument-hint: "<feature or user story to implement> [--auto]"
---

Run the complete ATDD cycle for:

$ARGUMENTS

**Authoritative procedure for every phase: `docs/atdd/workflow.md`.** Read that file before
executing a phase (or when you need the full step list). This command covers **orchestration
only** — subagent choices, gates, and reporting.

Track progress through each phase with the todo/task list.

## Autonomy Mode

This command runs at one of two autonomy levels. **Do not ask which one up front** — the user
has not seen anything yet, and an extra question before Phase 0 is an interruption for nothing.
The choice is made at the spec approval gate, which is the one stop that already exists (Phase 1).

| Mode                | After spec approval                                            |
| ------------------- | -------------------------------------------------------------- |
| **(a) Hands-off**   | Runs through PR creation and review resolution without stopping |
| **(b) Check first** | Stops once before opening the PR, then finishes                  |

If `--auto` appears anywhere in the arguments above, skip the mode question entirely and use
mode (a). Otherwise ask for it as part of spec approval — see Phase 1, step 5.

Whichever mode is chosen, **spec approval is the only mandatory human gate**. Mode (b) adds
exactly one more stop, immediately before the PR. Never introduce a third.

## Hard Constraints

The full list is in `CLAUDE.md` / `AGENTS.md`, already in your context. The two the orchestrator
enforces at a phase boundary:

- **Test-first**: the first files created after spec approval must be **test files**. No DTOs,
  entities, interfaces, services, or repositories before a test file exists. If a missing type
  blocks compilation, add the minimum empty shell — nothing more.
- **Phase 6 blocks Phase 7**: no archive, no PR while any drift is unresolved.

## Cycle

```
Analyze → Spec → [HUMAN GATE] → Tests (Red) → Implement (Green) →
Quality Gates → Refactor → Spec & Doc Sync → Archive → PR → Review
```

## Phase 0 — Project Analysis

**Start here — do not browse files speculatively.**

1. Check for `docs/project-profile.md`. If it exists, read it and treat as authoritative —
   skip detection unless the user asked to re-analyze.
2. If missing: follow `docs/atdd/workflow.md` § Phase 0 and `docs/atdd/project-detection.md`
   in full — this includes reading existing project docs (README, CONTRIBUTING, ARCHITECTURE,
   ADRs, etc.) **before** sampling code.
3. Write the profile to `docs/project-profile.md`. Actually persist the file — do not keep it
   in reasoning. Re-read to verify, then print verbatim:

   > ✓ Wrote `docs/project-profile.md` (Tooling: N rows, Conventions: N rows, Reference
   > Files: N entries). Future sessions will read this instead of re-detecting.

   If the write fails, stop the cycle and tell the user.

4. Greenfield vs. legacy:
   - **Greenfield**: prompt for tooling preferences in a single prompt (required: language,
     test framework, package manager; optional: linter, formatter, structure, CI/CD). Record
     choices in the profile. Do not set up configs yet.
   - **Legacy**: conventions discovery is mandatory. Match all existing conventions exactly.

## Phase 1 — Spec

1. Check `specs/changes/` for an in-flight change covering this work; if found, read it and skip
   to step 4.
2. **Identify the target capability.** List `specs/capabilities/` and pick the domain this change
   modifies, then read its `behavior.feature` and `rules.md` in full. If none fits, this change
   creates a capability — note that; every delta scenario will be `@added`.
3. Parse requirements. Ask at most 3 questions if actor, acceptance criteria, or critical
   error/edge cases are unclear. Then invoke the **spec-writer** subagent with the full context.
   It produces the change folder `specs/changes/<name>/` — `proposal.md`, `delta.feature`,
   `delta-rules.md`, and `tasks.md`.
4. Show the user the delta, grouped by operation (added / modified / removed / renamed) so the
   shape of the change reads at a glance.
5. **MANDATORY GATE — ask for approval and autonomy level together**, in one message. If
   `--auto` was passed, ask only the approval half and proceed in mode (a).

   > Do these specs look correct? Any adjustments before I generate tests?
   >
   > And after approval, should I:
   > **[a]** run hands-off through implementation, quality gates, PR and review, or
   > **[b]** check with you once before opening the PR?

6. **Wait for explicit approval.** Iterate on the spec until approved. If the user approves the
   spec without answering the mode question, default to **(b)** — the more cautious reading of
   an ambiguous answer — and say which mode you are using before continuing.
7. Record the chosen mode. Everything from here runs uninterrupted until the mode's stopping
   point (mode (a): none; mode (b): before the PR).

## Phase 2 — Acceptance Tests (Red)

**Order: test file first, everything else second.** See `docs/atdd/workflow.md` § Phase 2.

1. Write the test file first, using the profile's framework and conventions. One test per
   scenario. Each body throws a "not implemented" error. Header:
   `// Spec: specs/capabilities/<domain>/behavior.feature`.
2. Add minimum empty shells only if needed for compilation (no fields, no logic).
3. Run the **test command** (not the build command). Every test must fail for the right
   reason (not compile/import errors).
4. **Quality gate**: print the test runner output. Report: _"X scenarios, all red ✓"_.

## Phase 3 — Implementation (Green)

**Step 0 — Convention sync (mandatory before any production file is created or edited):**

a. Re-read `docs/project-profile.md` — `Conventions`, `Reference Files`, `Anti-patterns`.
b. Open at least one reference file from the same layer you are about to write.
c. **State explicitly which conventions you will follow.** This statement is required output.
d. If `docs/project-profile.md` is missing, stop and run Phase 0 first.

Then implement in priority order: `@smoke` → `@happy-path` → `@edge-case` → `@error`. Minimum
code per scenario, mirror the profile, run the full test suite after each scenario, never
modify tests. Full procedure: `docs/atdd/workflow.md` § Phase 3.

## Phase 4 — Quality Gates

Run lint, format, typecheck, build, test. Iterate until all pass (max 3 fix attempts per gate,
re-run all gates after each fix). Reference: `docs/atdd/quality-gates.md`. **Quality gate**:
report the gate results table. Do not proceed until all available gates pass.

## Phase 5 — Refactor

Only with tests green. One focused change at a time; run tests after each. Stop when clean —
no speculative abstractions. **Quality gate**: re-run all gates after refactoring.

## Phase 6 — Spec & Doc Sync (Hard Gate)

**Blocking.** Do not proceed with any unresolved drift — repair in-phase. This gate blocks the
PR in both modes.

**6a. Spec compliance.** Invoke the **spec-reviewer** subagent to validate implementation
against the spec and produce a drift report.

**6b. Spec drift repair.** Classify each flagged item **ADDED / MODIFIED / REMOVED** before
touching a file. ADDED and MODIFIED: update the `.feature` or `-spec.md` → add/adjust a test →
re-run the full suite. A **REMOVED** item is a spec weakening — never apply it under "match the
code":

- **Mode (b)**: stop on that item, show what the spec promises versus what the code does, and ask
  whether to narrow the spec or fix the code. Keep repairing other items meanwhile.
- **Mode (a)**: do not stop. Preserve the spec — correct the implementation to honor it. Stop
  only if honoring it is genuinely impossible. Hands-off never authorizes narrowing the spec.

Full procedure: `docs/atdd/workflow.md` § Phase 6b.

**6c. Documentation sync.** Walk the `Sources consulted` list in `docs/project-profile.md`.
For every doc listed there that could describe the changed behavior, update it or mark ⏭️
with reason. Work through: README → CONTRIBUTING → ARCHITECTURE → ADRs → style guides /
runbooks → `docs/project-profile.md` → any other consulted doc. Do not skip sources silently.

**6d. Final verification.** Re-run the suite and all quality gates, then produce the **Spec & Doc
Sync report** — the format is defined in `/verify-spec-coverage`, which owns this gate. Every row
must be ✅ or an explicit ⏭️ with a reason, and the Spec Weakenings table must be empty or fully
resolved, before Phase 7 runs.

## Phase 7 — Archive & Merge

The change is built and verified; now it becomes part of the truth. Merge the delta into the
capability, then move the change folder to `specs/changes/archive/<YYYY-MM-DD>-<name>/`. This
runs **before** the PR so the merged capability and the archived change ship together.

**Run `/archive-change` and follow it in full** — it owns the preflight checks, the merge rules,
and the guardrails. Orchestration note: a preflight failure is a hard stop in both autonomy
modes; report it and do not proceed to the PR.

Then re-run the test suite — spec files changed, not code, so it must still be green.

## Phase 8 — Create PR

**Mode (a):** proceed automatically. Do not ask.
**Mode (b):** this is the one additional stop. Show the branch name, commit message, and PR
title you intend to use, and ask: _"Ready to push and open the PR?"_ Then proceed on approval.

**Run `/create-pull-request`** — it owns the branch, commit, push, and PR-body procedure. Record
the PR number and URL for Phase 9.

## Phase 9 — Review + Address Comments

**Mode (a):** run automatically.
**Mode (b):** run automatically as well — the mode (b) stop was Phase 8. Do not stop again.

Poll for the review every 60 seconds, up to 5 minutes
(`gh pr view <number> --json reviews,comments`). If one arrives, **run
`/address-review-comments`** — it owns the triage rules and the spec-first protocol for behavior
changes.

If no review lands within the timeout, do not block. Report:

> "PR created at `<URL>`. The review has been requested but has not yet completed.
> When the review is ready, run `/address-review-comments <PR-number>`."

## Completion Summary

End every run with this table:

| Phase           | Artifact                         | Status                         |
| --------------- | -------------------------------- | ------------------------------ |
| Analysis        | Project profile                  | ✅ <language>, <framework>     |
| Capability      | `specs/capabilities/<domain>/`        | ✅ Targeted / ✨ Created       |
| Spec            | delta merged into the capability      | ✅ N scenarios (A:n M:n R:n)   |
| Tests           | `<test-file-path>`               | ✅ Red → Green (N scenarios)   |
| Implementation  | `<src-file-path(s)>`             | ✅ Implemented                 |
| Quality Gates   | lint/format/typecheck/build/test | ✅ All passed                  |
| Spec & Doc Sync | Spec / all consulted docs        | ✅ In sync (drift repaired)    |
| Archive         | `specs/changes/archive/<date>-<name>/` | ✅ Merged into capability      |
| PR              | `feat/<name>` #N                 | ✅ Created                     |
| Review          | Comments addressed               | ✅ Done / ⏳ Awaiting review   |

Name the autonomy mode used in the line above the table, e.g.
_"Ran in mode (a) — hands-off after spec approval."_
