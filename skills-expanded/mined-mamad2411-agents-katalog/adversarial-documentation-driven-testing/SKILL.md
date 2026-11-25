---
name: adversarial-documentation-driven-testing
description: >-
  Build documentation-traceable unit, integration, contract, and end-to-end testing
  with adversarial loops that identify weak tests, broken frontend-backend linkage,
  API drift, undocumented functionality, and documentation defects.
version: 1.2.0
triggers:
  - improve test coverage
  - expand test suite
  - test all features
  - test documented functionality
  - frontend backend integration testing
  - end-to-end coverage
  - adversarial testing
  - QA audit
  - regression testing
  - contract testing
  - documentation drift
---

# Adversarial Documentation-Driven Testing Skill

## Purpose

Use this skill when asked to audit, design, implement, improve, or validate software testing across a codebase—especially when the request includes frontend/backend linkage, UI controls and settings, documented feature coverage, end-to-end workflows, quality gates, or concern that code coverage is superficial.

This skill produces evidence-based behavioral coverage rather than relying only on line coverage.

## Distribution (master → every workspace)

This skill is **generic**. It is not tied to a product, org, or Makefile layout.

| Layer | Path | Role |
| :--- | :--- | :--- |
| **Master** | The versioned `SKILL.md` you edit (this file in git) | Source of truth |
| **User (global)** | `~/.cursor/skills/adversarial-documentation-driven-testing` | Cursor loads this in **every** project. Must be a **symlink** to master so edits apply immediately. |
| **User `/test`** | `~/.cursor/commands/test.md` | Generic `/test` for any repo |
| **User `/coverage`** | `~/.cursor/commands/coverage.md` | Statement / branch / condition table + 80% loop |
| **Project overlay** | `.cursor/commands/test.md`, `.cursor/rules/`, `Makefile` | Product-specific commands only |

**Do not copy** this skill into each repo as a second master. Copies go stale. Prefer:

```bash
# global (any future project, including ones that never heard of webtools)
ln -sfn /path/to/this/skill/dir ~/.cursor/skills/adversarial-documentation-driven-testing
```

In a multi-repo suite that already mounts this tree as `shared/`, project `.cursor/skills/adversarial-documentation-driven-testing` should also be a **relative symlink** to `shared/skills/adversarial-documentation-driven-testing`.

Refresh links:

```bash
bash scripts/install_adversarial_workflow.sh          # suite + ~/.cursor symlinks
bash scripts/install_adversarial_workflow.sh --user-only
```

### Local commands (discover, do not assume)

From the **open repo root**, use whichever exist:

```bash
make adversarial-preflight || make test || true
make coverage-snapshot     # statement / branch / condition table; /test loops to 80%+
```

If those targets are missing, use the repo’s documented test entry (`pytest`, `npm test`, `./test.sh`, …) **after** applying the workflow in this skill. Product-specific inventory paths belong in the **project** `/test` command, not in this skill.

## Primary Outcome

Establish a verifiable chain for every supported documented capability:

Documentation claim → Implementation → Frontend interaction → Backend contract → Backend effect → Persisted or emitted state → User-visible result → Automated tests

A capability is not complete unless the relevant links in this chain are documented and tested.

## When to Use

Activate this skill when the task involves one or more of:

- Increasing unit, integration, contract, component, or end-to-end test coverage.
- Testing every product feature, tab, tool, control, setting, route, or workflow.
- Verifying frontend controls actually control backend behavior.
- Auditing frontend/backend integration, API request correctness, configuration propagation, or state synchronization.
- Reconciling README files, PRDs, user guides, API documentation, and implementation.
- Detecting documentation drift, obsolete documentation, undocumented features, or unimplemented promises.
- Adding adversarial, mutation, fault-injection, permission, tenancy, persistence, or lifecycle testing.
- Establishing CI quality gates for coverage, workflow verification, API contracts, and test stability.
- Investigating weak, flaky, mock-heavy, skipped, or superficially high-coverage test suites.

## Do Not Use

Do not use this skill when the task is limited to:

- A simple spelling or wording change in a test.
- A single isolated test fix with no feature, integration, or coverage implications.
- Purely cosmetic test refactoring that does not affect test behavior, reliability, maintainability, or coverage.

For a narrow request, use the relevant portions of this skill rather than forcing a full repository audit.

## Required Mindset

Assume initially that:

- Raw coverage may overstate real behavioral protection.
- Existing mocks may accept incorrect requests and hide integration defects.
- User interface controls may update local state without changing backend behavior.
- Backend endpoints may exist but lack a reachable, documented UI workflow.
- Documentation may contain stale, ambiguous, incomplete, or unsupported claims.
- Happy-path coverage may omit security, permissions, tenancy, persistence, asynchronous failure, timing, and state-sync defects.
- Existing tests may be brittle, flaky, implementation-coupled, or too weak to detect meaningful regressions.

Require proof rather than inference.

## Inputs to Collect

Before making coverage claims, collect:

- Repository structure and test tooling.
- Existing coverage configuration and reports.
- Frontend route, component, view, tab, modal, control, and setting inventory.
- API-client, schema, service, event, job, queue, storage, and state-management inventory.
- Product, user, developer, API, deployment, security, configuration, upgrade, and release documentation.
- Current CI workflows, test quality gates, skipped tests, quarantined tests, retries, and flaky-test reports.
- Feature flags, role models, authorization rules, tenant/workspace boundaries, and environment configuration.
- Recent defects, regressions, incidents, TODOs, FIXMEs, deprecations, and known limitations.

## Workflow

### Phase 1: Inventory Documentation

1. Locate all documentation sources.
2. Extract each explicit feature claim, workflow, role rule, setting, default, prerequisite, supported input, output, error behavior, and limitation.
3. Normalize claims into uniquely identifiable features or behaviors.
4. Classify each as user-facing, backend-only, internal, public API, operational, security-sensitive, or deprecated.
5. Flag vague or contradictory claims for clarification.

Documentation sources include:

- PRDs, design documents, ADRs, and architecture documents.
- README files, user guides, tutorials, and examples.
- API specifications, SDK documentation, schemas, and CLI help.
- Configuration files, environment variable references, Helm values, and deployment guides.
- Release notes, changelogs, upgrade guides, deprecation notices, and known issues.
- Security, authorization, audit, data, queue, event, and operational documentation.

### Phase 2: Build Traceability

Create a traceability matrix with at least these fields:

| Field | Description |
|---|---|
| Documentation source | File, URL, section, or source identifier |
| Feature claim | Exact supported behavior being tested |
| User / actor | Role, tenant, workspace, entitlement, or system actor |
| Frontend surface | Route, screen, tab, panel, modal, or component |
| Control / setting | Specific user interaction or configuration value |
| Input / default | Allowed values, default, validation, and prerequisites |
| Backend contract | API route, event, job, schema, command, or subscription |
| Backend effect | Service behavior, mutation, output, side effect, or job |
| Persistence | Database, cache, preference, local state, queue, or event |
| Observable result | Final UI state, API response, audit event, or persisted record |
| Tests | Unit, component, integration, contract, end-to-end, adversarial |
| Status | Coverage and implementation classification |
| Evidence | Test IDs, report links, commit, defect, or decision record |
| Risk | Impact, residual gap, owner, due date |

Use the traceability matrix to discover:

- Documented behavior without code.
- Code without supported documentation.
- UI controls without backend linkage.
- Backend capabilities without UI reachability.
- Settings not persisted or not applied.
- Missing tests, weak tests, and missing error-state tests.
- Missing role, permission, flag, tenant, workspace, or lifecycle coverage.

**Webtools suite canonical artifacts:**

| Artifact | Path |
|---|---|
| Linkage inventory | `tests/contracts/linkage-inventory.json` |
| Exclusions / risk register | `tests/contracts/linkage-exclusions.json` |
| Human matrix | `docs/FE_BE_TRACEABILITY_MATRIX.md` |
| Program index | `docs/ADVERSARIAL_TEST_PROGRAM.md` |
| Adversary log | `docs/ADVERSARY_FINDINGS.md` |
| Drift report | `docs/DOCUMENTATION_DRIFT_REPORT.md` |
| Preflight script | `scripts/adversarial_test_preflight.py` |

### Phase 3: Map Implementation

Map each feature to:

- Frontend routes, views, components, tabs, controls, state, and actions.
- API clients, serializers, validators, request handlers, streams, and subscriptions.
- Backend controllers, services, jobs, queues, events, persistence, caching, authorization, and configuration.
- Runtime dependencies, feature flags, environment variables, defaults, and failure modes.
- Existing tests and current coverage metrics.

Verify every user interaction follows the expected path:

UI action → client state → request/event → service/job → state change → response/event → visible UI result

### Phase 4: Close Test Gaps

Use the following test-layer allocation:

| Layer | Primary responsibility |
|---|---|
| Unit | Logic, validation, state transitions, serialization, permissions, defaults, branch/condition coverage |
| Component | Local UI behavior, rendering, accessibility, user interactions, state changes |
| Integration | UI-to-client-to-service interactions, realistic request/response handling, persistence boundaries |
| Contract | Schema compatibility, consumer/provider expectations, versioning, event correctness |
| End-to-end | Real documented user workflow and actual UI-to-backend outcome |
| Adversarial | Falsification, fault injection, mutation testing, permission bypass attempts, lifecycle disruption |

Implement tests for all applicable scenarios:

- Default and happy-path behavior.
- Empty and first-use states.
- Valid, invalid, malformed, missing, and boundary input.
- Validation failures and user feedback.
- Loading, slow response, timeout, cancellation, retry, and recovery.
- Backend business-rule, dependency, and internal-service failures.
- Network failure, reconnect, duplicate delivery, stale response, and out-of-order events.
- Unauthorized, forbidden, session expiry, role switch, tenant/workspace boundary, feature flag, and environment restriction.
- Persisted setting changes, cache invalidation, rehydration, refresh, navigation, restart, logout/login, and reconnect.
- Concurrent requests, duplicate actions, race conditions, conflicts, idempotency, rollback, and multi-tab behavior.
- Accessibility and keyboard workflows.
- Responsive/platform-specific behavior where supported.
- Migration, compatibility, upgrade, downgrade, and deprecation behavior where documented.
- Regressions for every discovered defect.

### Phase 5: Test Frontend-to-Backend Linkage

For every control or setting that can affect runtime behavior:

1. Verify the control is visible only when it should be.
2. Verify the default state matches the documented/default backend behavior.
3. Verify user action creates the intended frontend state transition.
4. Verify the exact API or event contract:
   - Method
   - Route
   - Path parameters
   - Query parameters
   - Headers
   - Body schema
   - Enum values
   - Default values
   - Serialization
   - Correlation and idempotency metadata
5. Verify backend receipt and processing.
6. Verify persisted state, asynchronous job execution, or emitted event.
7. Verify the final user-visible confirmation and recoverable error state.
8. Verify refresh/restart/rehydration behavior when the setting is persistent.
9. Verify tests fail if request propagation or backend effect is intentionally removed.

Do not accept a simple mocked-function-called assertion as evidence of a working backend linkage.

Shared Playwright helpers: `tests/lib/fe-be-linkage.mjs`

### Phase 6: Run Adversary Loops

For every claimed-covered feature, run the following loop:

1. Select a feature or risk cluster.
2. Read documentation, code, traceability entries, API contracts, existing tests, coverage reports, and historical defects.
3. Form a falsifiable hypothesis about a missing linkage, weak assertion, unsupported document claim, security bypass, race, persistence issue, or contract mismatch.
4. Create an adversarial test, fault injection, schema perturbation, or controlled implementation mutation.
5. Confirm the adversarial check fails when behavior is intentionally broken.
6. Classify the finding:
   - Confirmed defect
   - Missing coverage
   - Weak test
   - Contract drift
   - Documentation drift
   - Unsupported documented capability
   - False hypothesis
7. Remediate implementation, tests, contract, or documentation.
8. Add a regression test that fails against pre-fix behavior.
9. Re-run affected test layers and coverage analysis.
10. Record evidence and residual risk in the traceability matrix.

Use techniques such as:

- Corrupting request fields, defaults, enum values, serialization, and endpoint selection.
- Rejecting, delaying, omitting, duplicating, reordering, or corrupting API responses and event messages.
- Taking services, jobs, queues, subscriptions, or storage dependencies offline.
- Simulating network loss, timeouts, retries, cancellation, reconnects, and partial failure.
- Changing role, tenant, workspace, flag, environment, or permission state mid-workflow.
- Removing, corrupting, externally updating, or downgrading persisted configuration.
- Refreshing, navigating away, opening a second tab, and submitting concurrent actions.
- Attempting direct routes, deep links, unauthorized API calls, and keyboard-only workflows.
- Performing mutation testing on critical logic, permissions, validation, state machines, request serialization, and configuration propagation.
- Searching for broad mocks, hidden skips, focus-only tests, suppressed errors, permanent flags, test-only paths, TODOs, FIXMEs, and dead code.

### Phase 7: Enforce Quality Gates

Implement or improve CI gates:

| Gate | Minimum requirement |
|---|---|
| Documentation traceability | Every documented supported feature has a matrix entry |
| Workflow coverage | Every documented user-facing workflow has end-to-end coverage or a time-bound approved exception |
| Control linkage | Every runtime-affecting control/setting proves UI → backend → visible outcome |
| Critical changed code | 100% meaningful line, branch, and condition coverage where practical |
| Contract integrity | API schema and consumer/provider compatibility checks run in CI |
| Permission boundaries | Positive and negative tests for all documented role, tenant, workspace, and entitlement boundaries |
| Test strength | Mutation testing or equivalent adversarial evidence for critical logic |
| Failure behavior | Documented/expected failure modes have automated tests |
| Test health | No unowned skips, focus markers, quarantine entries, flaky failures, or silent retries |
| Documentation drift | Documentation/schema/implementation discrepancies produce a review gate or CI failure |
| Exceptions | Every exception has scope, rationale, owner, compensating control, and expiration date |

Run from the **open repo root** (skip targets that do not exist):

```bash
make check-linkage          # inventory / contract shape, if the repo has one
make adversarial-preflight  # linkage + on-disk test file verification
make coverage-snapshot      # statement / branch / condition table; /test loops to 80%+
make ci                     # that repo’s CI gate
```

### Phase 8: Report Results

Produce:

- Documentation inventory.
- Traceability matrix.
- Frontend-to-backend flow and control map.
- Coverage report: line, function, branch, condition, workflow, control, setting, documented feature, API contract, and mutation coverage.
- Adversary finding log, including hypothesis, test, outcome, defect, remediation, and regression evidence.
- Documentation drift report.
- Defect report with root cause, severity, fix, and associated regression test.
- CI gate report and trend view.
- Exception/risk register.

## Completion Checklist

Before declaring work complete, verify:

- [ ] All documentation sources have been inventoried.
- [ ] Every supported documented feature has traceability evidence.
- [ ] Every runtime-affecting frontend control and setting has verified UI-to-backend behavior.
- [ ] Every documented user workflow has end-to-end coverage or an approved exception.
- [ ] Every critical API/client contract has schema or consumer/provider validation.
- [ ] Critical logic has meaningful branch/condition tests and test-strength validation.
- [ ] Permissions, roles, feature flags, tenants, workspaces, and configuration boundaries are tested positively and negatively.
- [ ] Persistence, refresh, restart, reconnect, and lifecycle behavior are tested where documented.
- [ ] Error handling, recovery, cancellation, timing, concurrency, and race conditions are tested where relevant.
- [ ] Every defect has a regression test.
- [ ] Every adversary finding is fixed, explicitly accepted, or resolved through documentation correction.
- [ ] No skipped, focused, flaky, quarantined, retried, or ignored test lacks an owner and expiration.
- [ ] CI gates prevent regression in critical workflows, contracts, coverage, test strength, and documentation traceability.

## Output Style

When applying this skill:

- Start with the feature/documentation inventory and the highest-risk coverage gaps.
- State assumptions and evidence limitations clearly.
- Prioritize defects that break documented user-facing behavior, frontend/backend linkage, authorization, data integrity, or recoverability.
- Prefer a concise table for traceability and coverage status.
- Link every implementation or documentation change to a concrete test or evidence item.
- Distinguish verified facts, inferred risk, and untested areas.
- Do not claim full coverage without traceable, executable evidence.
