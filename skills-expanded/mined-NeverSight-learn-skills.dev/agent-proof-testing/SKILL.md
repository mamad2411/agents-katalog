---
name: agent-proof-testing
description: Write clean, behavior-focused unit/integration tests that remain trustworthy when code is written or modified by agents (prevents “test weakening”, enforces invariants, and adds CI guardrails).
allowed-tools: runSubagent read_file grep_search file_search runTests run_in_terminal
---

# Agent-proof testing for Freelancerino

This skill helps you write tests that validate **real behavior and integration** (not just “green CI”) when an agent is implementing or modifying code.

The core problem: agents (and humans) sometimes “fix” failing tests by **loosening assertions**, **re-recording snapshots**, **over-mocking**, or **editing fixtures** until the test no longer protects the behavior.

## When to use

Use this skill when you are:

- adding tests in an **existing codebase** and want to avoid brittle tests or free passes
- writing tests for **code that doesn’t exist yet** (tests-as-spec)
- reviewing an agent PR where tests changed and you need to detect weakening
- adding CI/PR rules to make test integrity enforceable

## Non-negotiable principles

1. **Tests are a spec.** Changing assertions is a spec change.
2. **Prefer invariants over implementation details.** Assert “must always be true” properties.
3. **Integration beats over-mocking.** Mock only at true boundaries you don’t own.
4. **Determinism is mandatory.** Control time/random/locale/tz/order.
5. **Make cheating expensive.** Use contracts, invariants, and (selective) mutation testing.

## Step-by-step workflow (existing code)

### 1) Start by pinning the intended behavior

Write a short “executable spec” at the top of the test file:

- **Given**: preconditions (workspace/user/locale/time)
- **When**: action under test
- **Then**: expected result + side effects + invariants
- **And not**: at least one explicit negative constraint

Then translate that into tests.

### 2) Pick the right test level

- **Pure domain logic**: unit tests + property tests (fast)
- **DB logic**: integration tests against a real database (or transactional harness)
- **App seams** (Server Actions / Route Handlers): black-box tests through the public boundary

Avoid writing tests against private helpers that don’t represent your contract.

### 3) Add invariants that are hard to weaken

Add an `Invariants` section in the test file that asserts properties like:

- money stays in **integer cents**; totals equal sum(items)
- tenant isolation: no cross-`workspace_id` reads/writes
- idempotence: normalization twice equals once
- ordering stability: deterministic ordering for lists

Invariants reduce the chance an agent “loosens” one expectation and gets away with it.

### 4) Choose fakes over mocks

For most dependencies, prefer **small fakes** (in-memory / deterministic implementations):

- `Clock` (controls time)
- deterministic id generator
- in-memory storage adapter for most tests

Mocking is acceptable at true external boundaries (payments, third-party APIs), but pair it with a **contract test** (see below).

### 5) If you use snapshots/goldens, make them reviewable and scoped

Snapshots are code. Treat them like code.

Rules:

- snapshot only stable, intentional representations (e.g., normalized JSON view-model)
- normalize volatile fields (timestamps, random IDs, environment paths)
- keep goldens small and feature-scoped (one concern per file)
- never bulk re-record without an explicit “mechanical change” explanation

## Step-by-step workflow (tests for code that doesn’t exist yet)

When an agent will implement the production code later, tests must remove ambiguity.

### 1) Declare the public contract first

Define:

- the module entrypoint(s) and function signatures
- result/error shapes (prefer typed unions)
- what counts as validation vs domain errors
- dependency ports (db/clock/idGen/etc.)

### 2) Use table-driven tests for branching behavior

Create a scenario table:

- columns: inputs, expected outputs, expected error codes/messages
- rows: happy path + edge cases + negative cases

Table tests make “creative interpretation” difficult.

### 3) Add property-based tests (invariants)

Write 3–8 properties per unit:

- idempotence (normalizers)
- permutation invariance (totals don’t depend on item order)
- additivity (sum(items) = total)
- isolation (workspace A never sees workspace B)

### 4) Add at least one boundary integration test

Even if the core logic is unit-tested, add one end-to-end-ish test at the system boundary you care about (DB + auth + locale/time).

## “Agent-resistant” PR review checklist

Use this whenever tests were changed in a PR.

### If tests were modified

- [ ] The PR explains **why** tests changed (spec change vs test bug vs flaky fix).
- [ ] Assertions did not get quietly less specific (`toBe` → `toBeTruthy`, exact → regex/contains) without a compensating stronger check.
- [ ] No tests were deleted/disabled/skipped without a replacement test of equivalent intent.
- [ ] Tests are deterministic (time/random/locale/tz/order controlled).

### If snapshots/goldens changed

- [ ] Diff is small and reviewed; not a “re-record everything”.
- [ ] Snapshot scope is narrow; volatile fields are normalized/mocked.
- [ ] CI does not auto-update snapshots.

### If integration seams changed

- [ ] A contract test exists (or was updated) to prevent mock drift.
- [ ] Provider/consumer verification is in CI for important contracts.

## CI/PR guardrails (recommended)

These guardrails prevent “make tests pass by weakening tests”.

1. **Protected main**: require PRs, required checks, approvals.
2. **CODEOWNERS for tests**: require test-owner review for `tests/**` and `**/*.test.ts`.
3. **Diff heuristics**: fail CI on `it.only`, `describe.skip`, mass snapshot updates, or test-only changes without justification.
4. **Coverage gates**: modest threshold first, then ratchet.
5. **Mutation testing (selective)**: run nightly or on critical folders; surviving mutants indicate weak tests.

## Multi-subagent research workflow (how to work safely)

When you’re unsure how to test something, use multiple sub-agents with different roles and then reconcile results:

1. **Codebase investigator**: find existing patterns/helpers in `tests/` and similar modules.
2. **Spec extractor**: derive acceptance criteria from PRD/README/docs.
3. **Adversary**: list ways a naive test could be weakened while still passing.
4. **Test designer**: propose invariants + integration boundary tests.
5. **Reviewer**: apply the PR checklist to the proposed tests.

Only after that, write tests.

## Repo-specific notes (Freelancerino)

- Tenancy: every DB query/mutation must scope by `workspace_id`.
- Money: integer cents + currency.
- Time: UTC.

For deeper guidance, see:

- `.github/skills/security-strict/SKILL.md` (auth/tenancy/security)
- `.github/skills/drizzle-tenant-queries/SKILL.md` (workspace scoping)
- `.github/skills/bun-workflow/SKILL.md` (how to run tests/lint/typecheck)

## Validation

- Run unit/integration tests.
- If you touched DB logic, ensure tenant isolation tests exist for the changed behavior.
- If you changed goldens/snapshots, review diffs like code.

## References

- Agent Skills spec: https://agentskills.io/specification
- Jest snapshot testing guidance (snapshots are code; review diffs)
- Contract testing (consumer-driven contracts)
- Mutation testing (StrykerJS)
