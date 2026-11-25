---
name: decision-premortem
description: "Assume a proposal failed and identify plausible causes. Use to analyze plausible future failure of a proposal; challenge tests its current assumptions and ops-postmortem reconstructs an actual incident."
---

# decision-premortem

Assume a proposal failed and identify plausible causes.

## Choose this workflow

Use to analyze plausible future failure of a proposal; challenge tests its current assumptions and ops-postmortem reconstructs an actual incident.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Decisions methods](../../references/packs/decisions.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; proposal, success definition, operating context, and time horizon.

**Pack prerequisites:** The decision question, constraints, alternatives or permission to identify them, and relevant project evidence. Current vendor claims and prices require current authoritative sources during execution. Scores are decision aids, not facts.

- **Infer from evidence:** Recover hard constraints, the current option, adoption status and stated priorities from the brief and prior decisions.
- **Reasonable default:** State the failure definition and time horizon as assumptions before listing causes.
- **Ask only when needed:** Ask only about a missing constraint or preference that could reverse the recommendation; do not demand a complete scoring questionnaire.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Plausible reasons the proposal could fail and preventive actions.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Assume a concrete failed outcome and work backward through design choices and contributing conditions to realistic causal chains.
2. Rank the chains by impact and likelihood, identify an observable early warning signal for each, and propose proportionate mitigations.

## Technical method

- **Inspect:** Inspect dependency assumptions, operational ownership, adoption constraints and failure recovery.
- **Method:** Build a plausible trigger-to-impact chain for each material failure, then identify an early signal and an intervention that breaks that chain.
- **Avoid misdiagnosis:** Generic risks with no mechanism or observable warning cannot guide implementation.
- **Check the result:** Test whether each mitigation addresses its stated mechanism and whether a responder could detect the signal in time.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Decisions worked example](../../references/examples/decisions.md).


## Decision branches

- **When a risk cannot be connected to this proposal:** Remove the generic warning and focus on mechanisms supported by context.

## Deliver and verify

- Failure chains with early signal, mitigation, response and residual uncertainty, plus untested assumptions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Risks connect to specific proposal choices; a mitigation includes a detectable signal or concrete action.

## Stop and recover

- Do not present hypothetical failures as observed incidents or pad the report with generic catastrophes unrelated to the design.

## Example requests

- **Normal (plan):** Identify plausible ways the migration plan could fail and early warning signs.
- **Edge (plan):** Premortem a rollout whose rollback cannot undo generated data.
- **Blocked (inspect):** Analyze hypothetical failure without treating it as an observed incident.
