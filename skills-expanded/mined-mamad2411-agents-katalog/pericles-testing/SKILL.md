---
name: pericles-testing
version: 2026.05.0
description: >
  How testing works in Pericles — Vitest configuration, what to test by layer (tool,
  handler, scorer, security), and how the scorers double as eval gates. Use this
  WHENEVER you write a test, add coverage to a new module, or wire CI. Encodes the
  Vitest config from .claude/rules/12-testing.md, the layered test matrix, the rule
  that consequential paths must have security/tenant tests, and the current-state
  caveat that backend test script is not yet wired.
doctrine_refs: [§11; Ops §1; Security Spec §7]
depends_on: [pericles-evals-scorers, pericles-security-threat-model, pericles-functional-agent, pericles-execution-node]
last_reconciled: 2026-05-28
---

# Pericles Testing (build skill)

Tests in Pericles serve two jobs: catching regressions like any codebase, and gating the
LLM-bearing parts (eval scorers, lifecycle promotion). The framework is **Vitest** — set
up in `.claude/rules/12-testing.md` with concrete coverage thresholds — but the backend
`test` script is currently a placeholder (`"echo ... && exit 1"`), so wiring CI is a
needed step.

## When to use this skill

Writing a unit/integration test; deciding what to cover for a new tool/handler/Skill;
wiring `npm test` into CI; designing the security test suite for tenant isolation,
prompt-injection, or egress.

## Vitest config (from the rule)

`vitest.config.ts`: `globals: true`, env `node` for backend / `jsdom` for frontend,
include `**/*.{test,spec}.{ts,tsx}`, exclude `node_modules`, `dist`, `.mastra`;
`testTimeout: 10000`. **Coverage thresholds (v8 provider):** statements 80, branches 75,
functions 80, lines 80. Treat these as the bar, not the aspiration.

Current state: `backend/package.json#scripts.test` is a placeholder. Adding a real
`vitest` script + a CI step is on the path to enforceable coverage.

## Test layers (what to put where)

- **Unit (tool)** — every Mastra tool (`pericles-mastra-tool`): input-schema validation
  pass/fail, `organization_id` required, timeout/UA on external calls (mock fetch),
  output-schema shape. Mock the network; never hit live feeds.
- **Unit (handler)** — every workflow node handler (`pericles-execution-node`): trial
  vs run mode behavior (`NotificationHandler` simulates in trial), `ExecutionLog`
  written, error path writes a FAILED execution.
- **Unit (scorer)** — every scorer has reference cases pinned to a rubric
  (`pericles-evals-scorers`); these are also the lifecycle eval gates.
- **Integration (pipeline)** — the monitoring pipeline (`pericles-monitoring-pipeline`):
  dedup is stable across cycles, geo + risk-type filters honor org context, a feed
  failure logs and the cycle continues.
- **Integration (workflow)** — a `Workflow` runs end-to-end through handlers with the
  expected `ExecutionLog` trail.
- **Security** — the highest-leverage tests in Pericles:
  - Tenant isolation: a query without `organization_id` errors; cross-tenant access
    fails for every guarantee in `pericles-tenant-isolation`.
  - Prompt injection: a poisoned customer doc / feed item does not become instructions;
    output stays schema-valid (`pericles-prompts`).
  - Egress allowlist: a Custom Skill attempting non-allowlisted egress fails closed
    (`pericles-mcp-layer`, `pericles-custom-skill`).
- **Frontend** — component tests (`jsdom`) for `components/ui` primitives; persona-
  framing tests that assert data-scope enforcement (e.g. financial impact hidden from a
  Stakeholder).

## Eval scorers as a gate (lifecycle integration)

A `published` Skill needs `eval_criteria` (`pericles-skill-authoring`). The standard
promotion gate: every scorer above its threshold, no scorer regressing >5% vs the prior
version. Eval runs in CI gate the promotion, not just the merge.

## What this forbids

A new tool/handler/scorer landing without tests at its layer; integration tests that hit
live feeds; consequential paths shipping without tenant-isolation and (where applicable)
injection/egress tests; LLM-graded scorers without a pinned rubric; coverage below the
thresholds for new code.

## Verification

Vitest runs locally and in CI; the four coverage thresholds are enforced; every Mastra
tool, every workflow handler, and every scorer has unit tests; the security suite
includes tenant-isolation + injection + egress cases; eval scorers gate Skill
promotion.

## Existing standards (read alongside)

`.claude/rules/12-testing.md` (Vitest config); `backend/src/mastra/scorers/monitoring-scorer.ts`
(3 existing scorers as reference); `pericles-evals-scorers`,
`pericles-security-threat-model`.

## Open questions

- Adding the actual `vitest` script to `backend/package.json` + `frontend/package.json`
  + the CI step — a one-PR fix, but currently undone.
- Whether `test/setup.ts` should provision a per-test-suite Postgres (testcontainers)
  for integration tests — sequence with `pericles-dev-environment`.

## Changelog

- 2026.05.0 — Initial draft from `.claude/rules/12-testing.md`; flagged the missing
  `npm test` wiring; layered the test matrix to the build skills.
