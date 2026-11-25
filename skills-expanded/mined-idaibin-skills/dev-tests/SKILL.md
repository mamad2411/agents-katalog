---
name: dev-tests
description: "Plan risk-based coverage and execute functional acceptance across backend, APIs, pages, UI, business logic and end-to-end journeys. Run existing scoped checks; route source fixes to their owner."
---

# Dev Tests

## Entry Gate

Own a bounded test-coverage and evidence decision for a declared feature, change, or
journey. For existing projects, default to deriving and running cases from current
code, interfaces and available page observations; a complete PRD is not required.
Record conflicts or unverifiable business meanings for later human confirmation,
continue independent checks, and withhold only dependent business verdicts or unsafe
operations. During product/design work, identify risks, testability gaps and provisional
checks without waiting for implementation. Resolve applicable authorities, their
acceptance status, target basis, environment and permission before execution; only
settled business oracles support business-acceptance verdicts; baseline regression
and provisional exploration retain their narrower meaning. Reuse the project test plan and its IDs.
When asked to execute functional acceptance, run the reachable authorized cases; a
checklist alone does not complete the run.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| AI-generated Playwright journeys or test healing apply | [AI E2E acceptance](references/playwright-e2e.md) | Frozen cases, bounded authoring handoff and native-runner evidence |
| Design early checks or reconcile risk-based coverage against contracts | [coverage](references/coverage.md) | Requirement-to-layer matrix and qualified gaps |
| Run existing checks, rerun failures, or choose regression scope | [execution](references/execution.md) | Reproducible scoped runs and evidence-bound outcomes |
| Execute a functional acceptance campaign or resume its case inventory | [functional workflow](references/workflow.md) | Real journeys, correlated results, retest and cleanup |
| API or business-state behavior participates | [API and logic](references/api-and-logic.md) | Wire, business status and independent persistence assertions |
| Pages, UI or clicks participate | [page walkthrough](references/page-walkthrough.md) | Reachability, real interaction and visible outcomes |
| Record functional cases, defects or recovery | [test record](references/test-record.md) | Finite coverage, case evidence and recovery queue |
| Deletion, moves/renames, identifiers, enforcement rules or instructions change | [change preservation](references/change-preservation.md) | Original acceptance, positive controls, consumer regressions and qualified comparison |
| Scoped performance acceptance or before/after comparison participates | [performance measurement](references/performance-measurement.md) | Comparable metrics, protected journeys and qualified verdicts |
| Role isolation, concurrent users or load scenarios apply | [roles and performance](references/roles-and-performance.md) | Authorized scenarios, metric interpretation and comparable measurements |
| Compose a result for review or another owner | [result contract](references/result-contract.md) | Versioned basis, coverage, evidence and handoff |

## Invariants

- Derive visible copy, control and feedback expectations from the original request and accepted Product/UI decisions. Check the rendered failure state for unapproved additions. When pending or unknown writes can reach a subsequent independent action, exercise the sequence: the original write cannot repeat while unresolved, and the independent action remains usable and submits as specified. Verify actual dispatch separately from completion. Candidate specs and green tests supply no approval.

- Product behavior belongs to `product-spec`, visual behavior to `ui-spec`, and wire
  semantics to `api-spec`. Test ambiguity cannot silently decide those contracts.
- Select and run existing project tests within scope. Missing tests, harness changes,
  fixtures requiring source edits, and fixes belong to the matching implementation
  owner. Browser page/DOM mechanics belong to `ops-browser`, desktop-client control
  to `ops-client`, and mobile device/app lifecycle or native UI to `ops-device`.
  These names are handoff targets, not automatic invocation or granted capabilities.
- Read current project commands and their effects before execution. Use isolated test
  state and authorized resources; preserve safety stops, denied routes and scope limits.
  A failure does not authorize another identity, mechanism, or environment to bypass them.
- Preserve `passed`, `failed`, `blocked`, `not-run`, and `excluded` separately. A mock,
  fixture, static check or lower layer proves only its observed boundary, never a real
  integration or complete E2E. Missing access is a blocker, not an exclusion.
- Rebind evidence after requirement, UI, code, configuration or environment changes.
  Reuse unaffected evidence only with an explicit impact rationale; old green results
  cannot approve a new basis by default.
- Select raw observations for the actual assertions and estimate output growth before
  scaling a capture matrix. Follow the [test record](references/test-record.md) for
  evidence sufficiency; storage retention and cleanup remain with the host owner.
- Produce test evidence, not a competing task ledger or a release verdict. `to-task`
  owns durable work reconciliation, `repo-review` the fixed-basis review, and
  `repo-delivery` separately authorized Git actions. No deployment, installation,
  publication, production load, or implicit promotion follows from testing.

- Consolidate delegated case results into the frozen inventory before selecting more
  work. An agent terminal state closes only its assigned execution, not another
  evidence layer or the run verdict.

## Output Map

Return the [result contract](references/result-contract.md): frozen basis and authority
versions, layer matrix, executed checks and evidence, failures and blockers, justified
exclusions, remaining acceptance gaps and smallest owner-specific next action. State
whether a first real E2E was observed and its exact boundary. Never flatten the matrix
into “all tests passed” when required cells remain unresolved.

## Reference Map

- Read [Playwright E2E](references/playwright-e2e.md) only for coordinating generated browser-test acceptance.
- Read [coverage](references/coverage.md) when deriving or reconciling the acceptance matrix.
- Read [execution](references/execution.md) before running checks or making regression claims.
- Read [functional workflow](references/workflow.md) for functional campaigns and resumed case inventories.
- Read [API and logic](references/api-and-logic.md) for network, business status and persistence.
- Read [page walkthrough](references/page-walkthrough.md) for real UI journeys and browser evidence.
- Read [test record](references/test-record.md) for functional plans, defects, coverage and recovery.
- Read [roles and performance](references/roles-and-performance.md) only for relevant multi-user, authorization or performance requirements.
- Read [result contract](references/result-contract.md) when consuming results or returning evidence.
- Read [change preservation](references/change-preservation.md) when code deletion or instruction changes participate.
- Read [performance measurement](references/performance-measurement.md) for scoped comparative performance acceptance.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary execution.
