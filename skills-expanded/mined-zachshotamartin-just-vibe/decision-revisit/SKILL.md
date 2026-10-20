---
name: decision-revisit
description: "Reassess a decision using new constraints or evidence. Use when new evidence may invalidate a recorded choice; decision-adr preserves the resulting decision record."
---

# decision-revisit

Reassess a decision using new constraints or evidence.

## Choose this workflow

Use when new evidence may invalidate a recorded choice; decision-adr preserves the resulting decision record.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Decisions methods](../../references/packs/decisions.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; prior decision record, new evidence, and changed constraints.

**Pack prerequisites:** The decision question, constraints, alternatives or permission to identify them, and relevant project evidence. Current vendor claims and prices require current authoritative sources during execution. Scores are decision aids, not facts.

- **Infer from evidence:** Recover hard constraints, the current option, adoption status and stated priorities from the brief and prior decisions.
- **Reasonable default:** Compare feasible options qualitatively when weights were not supplied; make a reversible conditional recommendation when useful.
- **Ask only when needed:** Ask only about a missing constraint or preference that could reverse the recommendation; do not demand a complete scoring questionnaire.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Reassess a specific choice while preserving its historical rationale.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. If the decision was saved, run decision show NAME and then decision revisit NAME with attributed observations; otherwise reconstruct the rationale and label it as reconstructed.
2. Compare the original assumptions with current facts.
3. Weigh migration costs, disruption and option value, and recommend retaining, modifying or superseding the decision.

## Technical method

- **Inspect:** Read the original premise, accepted status, trigger and new evidence with dates.
- **Method:** Change only conclusions affected by the new premise; compare continuing, adapting and replacing, preserving the original record.
- **Avoid misdiagnosis:** A hindsight rewrite loses the information needed to understand why the earlier choice was reasonable.
- **Check the result:** Show the changed premise, resulting recommendation and migration cost; unchanged conditions should not trigger automatic reversal.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Decisions worked example](../../references/examples/decisions.md).
- The decision was saved with decision save, or the user wants the review recorded: [Decision history](../../references/decision-history.md).

## Decision branches

- **When only preferences or fashion changed:** Retain the decision unless an explicit new priority justifies transition costs.

## Deliver and verify

- Changed-assumption table, alternatives and migration implications, and a retain/change recommendation with the proposed status update and adoption or revisit conditions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- New fashion alone does not invalidate a sound decision; a broken core assumption triggers a concrete alternative analysis.

## Stop and recover

- Do not rewrite history or silently mark a decision superseded without an adoption instruction.

## Example requests

- **Normal (plan):** Reassess the cache decision now that writes occur in two regions.
- **Edge (plan):** Revisit a queue choice after workload ordering requirements change.
- **Blocked (inspect):** Review an old decision without its rationale; distinguish reconstruction from recorded facts.
