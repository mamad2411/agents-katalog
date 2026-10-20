---
name: decision-buy-build
description: "Compare building, buying, and integrating a solution. Use for vendor versus internal capability decisions; research verifies current vendor claims."
---

# decision-buy-build

Compare building, buying, and integrating a solution.

## Choose this workflow

Use for vendor versus internal capability decisions; research verifies current vendor claims.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Decisions methods](../../references/packs/decisions.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; capability, team capacity, compliance/integration constraints, volume, and budget.

**Pack prerequisites:** The decision question, constraints, alternatives or permission to identify them, and relevant project evidence. Current vendor claims and prices require current authoritative sources during execution. Scores are decision aids, not facts.

- **Infer from evidence:** Recover hard constraints, the current option, adoption status and stated priorities from the brief and prior decisions.
- **Reasonable default:** Compare feasible options qualitatively when weights were not supplied; make a reversible conditional recommendation when useful.
- **Ask only when needed:** Ask only about a missing constraint or preference that could reverse the recommendation; do not demand a complete scoring questionnaire.

Declared evidence requirements: `project.read`, `web.research`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Build, buy, and hybrid options across initial and ongoing ownership.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. State the usage horizon and include the current workaround as an option; verify current vendor capabilities when relevant.
2. Compare fit, integration, operations, staffing, maintenance, migration, exit/export, failure ownership and total-cost assumptions.

## Technical method

- **Inspect:** Establish functional requirements, integration surfaces, support burden, data export and verified pricing terms.
- **Method:** Compare lifecycle scenarios including maintenance, incident response, migration and exit; retain uncertainty ranges instead of invented estimates.
- **Avoid misdiagnosis:** Vendor feature lists do not prove compatibility with the actual identity, offline or data-residency requirements.
- **Check the result:** Validate the decisive integration with a bounded example and compare exit costs as well as the happy-path purchase.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Decisions worked example](../../references/examples/decisions.md).


## Decision branches

- **When a vendor lacks a hard requirement or usable export:** Exclude it or state the explicit compromise before calculating weighted convenience.

## Deliver and verify

- Fit/gap matrix, cost model inputs and assumptions, ownership burden, recommendation, and a validation and exit plan.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Maintenance and migration effort appear alongside subscription cost; a vendor missing a hard feature is excluded.

## Stop and recover

- No purchases or account creation. Do not convert speculative usage into precise budget claims.

## Example requests

- **Normal (plan):** Compare building and buying organization authentication with future SSO.
- **Edge (plan):** Compare buying search with building it when private indexing is required.
- **Blocked (inspect):** Assess buy versus build with no price quote; keep uncertain costs as ranges.
