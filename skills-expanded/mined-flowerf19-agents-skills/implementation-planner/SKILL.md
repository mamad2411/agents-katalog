---
name: implementation-planner
description: Compares designs and plans code changes with Tier 1 guardrails and Tier 2 verification artifacts. Use when asked to plan a feature, choose an architecture, turn a spec into tasks, or plan a complex approved change. Do not use to edit code or execute implementation.
license: MIT
---

# Implementation planner

Compare designs and write an executable plan grounded in live code, Tier 1 guardrails, and Tier 2 verification proof.

**Read-only lock:** Never edit code, tests, config, or dependencies; verify with [check-readonly.sh](../scripts/checks/check-readonly.sh). Write a plan file only when requested or needed for approved work.

## Step 1: Frame the Change

1. State goal, required behavior, constraints, and non-goals.
2. Read the Feature Map (if present; [templates/feature-map.md](../templates/feature-map.md)) and trace the flow from entrypoint to callers, shared types, adapters, and stored state.
3. Require confirmed diagnosis + repro artifact before planning a bug fix.

## Step 2: Resolve Design Questions & Clean Cutover

1. Compare options on correctness, contracts, cost, and testability; recommend one. Keep proposals separate from accepted decisions.
2. Surface missing business rules and scope choices as blocking questions.
3. **Clean cutover inventory:** List callers to migrate, superseded code to delete, approved compatibility exceptions, and any contract or data-migration conflicts.

## Step 3: Write the Plan

Use the project's plan path, or `.agents/plans/<slug>.md`. Require:

- **Goal, scope, non-goals, accepted decisions**, and open blocking questions.
- **Dependency-ordered tasks:** affected modules, prerequisites, and cutover deletions.
- **Tier 1 Guardrails:** exact typecheck, compiler, lint, and hard-ban checks that must exit `0` (plus new rules; [lint-rules/README.md](../lint-rules/README.md)).
- **Verification Artifacts (Definition of Done):** exact Tier 2 live runtime proof (CLI, API, browser/Playwright/CDP, or integration), failure cases, environment, and artifact paths for [templates/verification-artifacts.md](../templates/verification-artifacts.md).
- **Contracts & state** when relevant: interfaces, errors, concurrency, restart, rollback, or migration approvals.

## Step 4: Check and Hand Off

Confirm every task has prerequisites, Tier 1 checks, and Tier 2 runtime proof. A plan with blocking questions is not ready to execute.

**Plan status** (only if the project tracks plan files): `draft` (unapproved), `approved` (ready/active), or `done` (implemented and artifacts verified). Preserve history; do not delete plans without permission.

Return the recommendation or plan path, code references, open questions, and approval status.
