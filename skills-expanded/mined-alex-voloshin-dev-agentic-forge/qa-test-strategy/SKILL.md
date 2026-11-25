---
name: qa-test-strategy
description: Test strategy for a change or feature — risk areas, test levels (unit, integration, e2e, perf, security) and prioritized test cases, via the qa-engineer role, recorded as a test-strategy handoff. Use whenever the ask is what or how to test — a test strategy, a QA or test plan, which levels to test at. Not a work plan (plan), writing the tests (develop), or reviewing code (code-review).
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
---

# QA test strategy (phase workflow)

The test-planning phase: turn a feature, plan, or change into a **test strategy** — the risk
areas, the test levels to cover, and a prioritized case list — by delegating the test-design
judgement to the [`qa-engineer`](../../agents/qa-engineer.md) role, then recording a
`test-strategy` handoff. It plans *what and how to test*; it does not write the tests (that is
`develop`'s QA step). (Design: `docs/architecture/quality-ops.md` in the agentic-forge repository.)

## When to use

When the task is to decide what to test and at which levels for a change/feature — a test plan or
QA strategy, before or alongside building. **Not** for writing/hardening the tests (`develop`),
reviewing already-written code (`code-review`), or assembling a release (`release`).

## Process

1. **Read the inputs.** Load the feature/`plan.md`/`tech-design.md` or the code under change, and
   detect the stack (`python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" stack-detect --repo <repo>`) so the levels and tools match the repo.
2. **Delegate the analysis — plan only.** Fork the `qa-engineer` role (via `Task`) with the
   feature/code and the question "what are the risk areas, the right test levels, and the cases
   that matter?" — and say **plan only: design the strategy and the test list; do not create or
   edit files, do not run the suite**. The role's standing prompt writes and runs tests; this phase
   wants its judgement, not its edits. It brings the test-design expertise; pass it the context,
   not just the prompt.
3. **Synthesize the strategy.** Aggregate into a `test-strategy` handoff artifact (`handoff` type
   `test-strategy`: `type`, `feature`, `status`, `scope`, `risks`, `test_levels`, `cases`), then
   validate it (the read-back below; see
   [handoff.md](../../patterns/handoff.md)). Cover the real risk areas (boundaries, invalid/abusive
   input, concurrency, rounding/precision, failure modes).
   Keep every frontmatter value **data**: a case's `expect` is a list, and why that order is
   right goes in the body — `expect: [h1, h2, n1] — insertion order kept` is a YAML syntax error
   that makes the whole artifact unreadable, and it is the one this skill actually writes.
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type test-strategy` —
   and fix whatever it reports: this reads the file, so it sees the YAML you typed (ADR 0096).
4. **Prioritize.** Order cases so boundaries and error/abuse paths come first; call out the levels
   (unit / integration / e2e / perf / security) the change actually warrants — not a blanket list.
5. **Defects & exploration (in-flow).** When a defect surfaces while planning the strategy, or
   the strategy calls for an unscripted exploratory pass over a risk area, follow
   [references/bug-reports.md](references/bug-reports.md) — the structured bug-report format
   (minimal repro, expected vs actual, evidence, severity rationale) and the charter-driven
   exploratory pass whose findings feed the strategy's risk areas.

## Environment discipline (non-negotiable)

**Never issue mutating requests (`POST`/`PUT`/`PATCH`/`DELETE`) against production while verifying.**
Rate-limited public endpoints are the worst case: each call burns a real quota unit, warms a
production cache keyed by the target, and makes every later assertion on that endpoint
non-reproducible — including CI's. Verify with a read-only request, a local or stubbed environment,
or a recorded fixture. If a live mutation is genuinely required, it needs **explicit human
authorization and a named cleanup step** in the strategy.

## Output

A `test-strategy` handoff: scope, risk areas, the test levels to cover, and a prioritized case
list — the input the `develop` phase (or an engineer) turns into actual tests. No tests are written.

## Definition of done

- The real risk areas are identified (boundaries, invalid/abusive input, concurrency, failure modes).
- More than one test level is covered where warranted; cases are concrete and prioritized (not vague).
- A valid `test-strategy` artifact is produced (non-empty `test_levels`); no test code is written.
