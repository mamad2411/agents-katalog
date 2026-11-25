---
name: ether-tdd
description: Use before writing any implementation code in a project under this repo's ether harness (`.ether/changes/<id>/`) — apply and verify phases both require it. Mandatory, not conditional on the target already having a test suite — if it has none, this is how one gets started. Red-green-refactor, own harness, no dependency on superpowers, no network calls.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Ether TDD

ether's own test-first discipline. Every write to `.ether/changes/`
implementation files invokes this skill first — `ether-phase-dag`'s
apply/verify phases require it unconditionally.

## Workflow

1. **Red.** Before touching implementation code, write a test that encodes
   the behavior `tasks.md`/the acceptance criteria describe. Run it. It
   must fail, and fail for the expected reason (missing function, wrong
   assertion) — not a typo or import error. If it passes before any
   implementation exists, the test isn't testing the right thing; fix the
   test first.

2. **Green.** Write the minimum implementation that makes the test pass.
   No extra scope, no anticipatory abstraction — just enough to turn red
   green. Run the full suite, not just the new test, to confirm nothing
   else broke.

3. **Refactor.** With the suite green, clean up (naming, duplication,
   structure) if warranted. Re-run the suite after every refactor step. If
   nothing needs cleaning up, skip this step — it's not mandatory the way
   red/green are.

4. **Verify pass (regression check).** Before marking `apply`/`verify`
   done, re-run the *entire* target suite from a clean state (not just the
   file you touched). This is what separates "I wrote a test" from "the
   change is actually proven" — a paired test file that exists and once
   passed isn't the same as a suite that passes now.

## Non-negotiables

- No implementation line gets written before its failing test exists.
  Writing code first and backfilling a test after is not TDD — it defeats
  the purpose of using the test to pin down expected behavior first.
- No skipping this for "trivial" changes, "the repo has no test suite
  yet", or "there's no time" — those are exactly the cases most likely to
  regress silently later. If the target repo genuinely has no test
  runner/framework set up, standing one up is part of the task, not an
  excuse to skip it.
- No asserting `true`/placeholder tests to satisfy a file-existence gate
  (`ether phase done apply`). That gate checks that a paired test file
  exists and the suite exits 0 — it cannot tell a real assertion from a
  stub. This skill is what keeps that honest; a stub test that always
  passes is a violation even though no hook will catch it directly.
- If the target repo has its own testing conventions (a specific
  framework, fixture pattern, naming scheme), follow those — this skill
  governs the red-green-refactor *order*, not which test framework to use.

## Where this is invoked from

- `ether-phase-dag` — apply and verify phases, before any write to
  `.ether/changes/<id>/` implementation files.
- Any bounded fix delegated to a builder-style subagent that touches
  implementation code.

## Offline note

Nothing here needs network access — the gate is local `.ether/state.db`
+ local file checks, and the test suite you run is whatever runs locally
in the target project. Fits ether's no-network-calls constraint as-is.
