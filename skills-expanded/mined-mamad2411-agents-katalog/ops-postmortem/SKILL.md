---
name: ops-postmortem
description: "Produce evidence-based timelines and concrete follow-up work. Use to reconstruct an actual incident; decision-premortem analyzes hypothetical failure."
---

# ops-postmortem

Produce evidence-based timelines and concrete follow-up work.

## Choose this workflow

Use to reconstruct an actual incident; decision-premortem analyzes hypothetical failure.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; incident evidence, timeline, impacts, actions, and intended audience.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `telemetry.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Evidence-based learning and follow-up design; no blame assignment or external publication.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Reconcile timestamps, observations and impact evidence.
2. Separate the trigger from contributing conditions, and document detection and recovery gaps.
3. Tie each preventive or detective action to a documented gap, with a measurable outcome.

## Technical method

- **Inspect:** Collect timestamped events, impact evidence, hypotheses, interventions and unresolved gaps.
- **Method:** Separate trigger, contributing conditions and detection/recovery failures; derive follow-ups from demonstrated mechanisms.
- **Avoid misdiagnosis:** Invented certainty, blame or assigned owners hides uncertainty and cannot support useful prevention.
- **Check the result:** Link each action to a causal mechanism and observable success condition, preserving unknown impact/root cause where evidence is incomplete.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).


## Decision branches

- **When root cause or impact remains unknown:** Preserve the uncertainty and propose a discriminating follow-up instead of filling the narrative with guesses.

## Deliver and verify

- Postmortem with evidence-linked timeline, impact, causal factors, response gaps and measurable follow-up actions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Unknown root cause remains explicit; each proposed action addresses a documented failure mechanism.

## Stop and recover

- Do not invent owners, impact counts, or consensus. Sending the report or creating external action tickets requires explicit instructions.

## Example requests

- **Normal (plan):** Write an evidence-based postmortem without inventing impact counts or owners.
- **Edge (plan):** Write a postmortem where deployment timing correlates with failure but causation is unproven.
- **Blocked (inspect):** Draft from partial logs without inventing customers affected, owners or consensus.
