---
name: decision-reversible
description: "Separate reversible choices from expensive commitments. Use to classify and reduce switching cost; decision-spike tests a specific uncertainty."
---

# decision-reversible

Separate reversible choices from expensive commitments.

## Choose this workflow

Use to classify and reduce switching cost; decision-spike tests a specific uncertainty.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Decisions methods](../../references/packs/decisions.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; candidate decisions, migration constraints, contracts, and timeline.

**Pack prerequisites:** The decision question, constraints, alternatives or permission to identify them, and relevant project evidence. Current vendor claims and prices require current authoritative sources during execution. Scores are decision aids, not facts.

- **Infer from evidence:** Recover hard constraints, the current option, adoption status and stated priorities from the brief and prior decisions.
- **Reasonable default:** Compare feasible options qualitatively when weights were not supplied; make a reversible conditional recommendation when useful.
- **Ask only when needed:** Ask only about a missing constraint or preference that could reverse the recommendation; do not demand a complete scoring questionnaire.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Reversibility, lock-in, exit cost, and staged commitment.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Inventory persisted data, external promises, dependency adoption, switching mechanisms and operational costs.
2. Classify reversibility with evidence, distinguishing rollback of code from reversal of consequences, and design a cheaper experiment with a usable exit.

## Technical method

- **Inspect:** Identify persisted data, external promises, migrations, lock-in and rollback dependencies.
- **Method:** Describe reversal steps, time, retained artifacts and irreversible consequences separately from changing a feature flag.
- **Avoid misdiagnosis:** A reversible code change may already have sent messages or transformed data irreversibly.
- **Check the result:** Walk reversal after partial adoption and identify what the previous version can no longer read or undo.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Decisions worked example](../../references/examples/decisions.md).


## Decision branches

- **When a configuration toggle has irreversible downstream effects:** Classify those effects separately and design a bounded trial with cleanup or reconciliation.

## Deliver and verify

- Decision map with reversibility dimensions, reversal steps, exit cost assumptions, dependencies, commitment checkpoints and the experiment boundary.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A simple config toggle with irreversible downstream data effects is not marked freely reversible; a trial has a usable exit path.

## Stop and recover

- Avoid unsupported effort estimates. Unknown contractual constraints remain explicit dependencies.

## Example requests

- **Normal (plan):** Identify irreversible commitments in this storage-provider decision.
- **Edge (plan):** Assess a feature flag that sends customer emails.
- **Blocked (inspect):** Assess reversibility with unknown contract terms; identify the missing constraint.
