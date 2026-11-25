---
name: decision-spike
description: "Design or run a bounded experiment to resolve uncertainty. Use for a bounded experiment resolving a decision; build creates production behavior."
---

# decision-spike

Design or run a bounded experiment to resolve uncertainty.

## Choose this workflow

Use for a bounded experiment resolving a decision; build creates production behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Decisions methods](../../references/packs/decisions.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; uncertainty, competing hypotheses, success criteria, time/compute budget, and scratch scope. Running the spike uses apply mode within that budget.

**Pack prerequisites:** The decision question, constraints, alternatives or permission to identify them, and relevant project evidence. Current vendor claims and prices require current authoritative sources during execution. Scores are decision aids, not facts.

- **Infer from evidence:** Recover hard constraints, the current option, adoption status and stated priorities from the brief and prior decisions.
- **Reasonable default:** Without a stated budget, propose a time box and stop rule before any run.
- **Ask only when needed:** Ask only about a missing constraint or preference that could reverse the recommendation; do not demand a complete scoring questionnaire.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Design or explicitly run a disposable experiment; no production integration disguised as a spike.

Inspect/plan: design the experiment; save requested artifacts only. Apply: build and run the disposable prototype or measurement only in an isolated artifact location outside product source, within the declared time, compute and data budget. Production integration, shared services and paid resources require their resolved target and existing session authorization.

## Execute

1. Name the decision the spike will inform and the uncertainty that could change it. Define a representative workload/sample and an observable acceptance/rejection criterion before building.
2. Set a time/compute/data budget, isolated artifact location and stop rule. Choose the smallest prototype or measurement that can distinguish the alternatives; avoid building production scaffolding that does not test the hypothesis.
3. In apply mode, run within the budget and record raw observations, versions and deviations from the plan. Preserve failures and resource-limit outcomes; do not change the success threshold after seeing the result.
4. Classify supported, rejected or inconclusive. Explain the implication for the original decision and the limits of the sample; prototype success does not establish production readiness.

## Technical method

- **Inspect:** Identify one uncertainty, representative input, budget and rejection condition.
- **Method:** Run the smallest experiment that separates alternatives; retain failure evidence and mark prototype shortcuts.
- **Avoid misdiagnosis:** Building a polished prototype can consume the budget without testing the disputed assumption.
- **Check the result:** Apply the predeclared criterion to raw observations, including an inconclusive outcome when the sample cannot distinguish options.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Decisions worked example](../../references/examples/decisions.md).


## Decision branches

- **When budget expires without separation:** Preserve measurements and report inconclusive, including what a larger experiment would need.

## Deliver and verify

- Experiment protocol or results with hypotheses, resource cap, observations, reusable evidence and the decision implication.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The test can reject a hypothesis; reaching the budget yields an inconclusive result rather than endless expansion.

## Stop and recover

- Paid resources require budget authorization. Keep prototype quality and production readiness clearly distinct.

## Example requests

- **Normal (plan):** Design a two-hour local spike to test whether our current search index is sufficient.
- **Edge (apply):** Test whether streaming reduces perceived latency without building the full product.
- **Blocked (inspect):** Design a spike without available hardware; do not fabricate benchmark results.
