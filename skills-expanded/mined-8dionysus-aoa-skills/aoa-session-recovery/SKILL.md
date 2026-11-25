---
name: aoa-session-recovery
description: Diagnose a reviewed recurring session/workflow failure, or carry one bounded owner repair through checkpoint, rollback, and real health verification. Use for reviewed contamination, drift, repeated route/tool failure, or an established diagnosis ready for repair. Do not use on live evidence, for vague self-improvement, or to call a proposed or merely executed change verified.
---

# aoa-session-recovery

## Intent

Recover from recurring session or workflow failure without collapsing symptom,
diagnosis, proposed change, executed change, and verified health into one claim.

## Trigger boundary

Use this skill when:

- a closed, explicitly reviewed evidence packet needs diagnosis; or
- a reviewed diagnosis is ready for one bounded repair cycle at its real owner

Do not use this skill when:

- evidence is live, raw, unreviewed, or only a frustration note
- there is no diagnosis for repair, the target owner is unknown, or the route is
  a broad playbook-scale rollout
- the requested action would bypass approval, checkpoint, rollback, or owner law

## Inputs

- one reviewed evidence packet or reviewed diagnosis, with refs, target and
  durable owners, constraints, execution request, approval posture, available
  bindings, checkpoint/rollback anchors, and known health surfaces

## Outputs

- exactly one typed result from `references/contract.yaml`: either a
  `session-diagnosis` or `repair-cycle-result`, with evidence refs, claim and
  execution posture, actual effects, health evidence, uncertainty, and stop line

## Procedure

| Mode | Use when | Reference |
|---|---|---|
| `diagnose` | Reviewed symptoms exist but causes, drift class, or owner are unresolved. | `references/diagnose.md` |
| `repair` | A reviewed diagnosis exists and one bounded repair can be prepared, executed, verified, blocked, or handed off honestly. | `references/repair.md` |

### Mode: diagnose

Read and follow `references/diagnose.md`.

### Mode: repair

Read and follow `references/repair.md`.

1. Read `references/contract.yaml` and only the selected mode reference to EOF.
2. Execute exactly one mode. A diagnosis may hand off to a later repair, but an
   invocation must not manufacture a diagnosis and immediately mutate from it.
3. Preserve the strongest posture actually proved. `prepared`, `executing`,
   `executed`, and `verified` are different states.

## Contracts

- reviewed session evidence is input, not durable memory or owner truth
- diagnosis is read-only; repair acts only through the target owner's available
  tool or repository binding and within the user's authorization
- a repair that changes state requires approval posture, pre-change checkpoint,
  executable rollback, bounded retries, post-change health checks, and cleanup
- execution success is not health verification; only observed checks support
  `verified`, and failed checks trigger rollback or an explicit blocked state
- technique records may explain lineage but are not runtime dependencies

## Risks and anti-patterns

- self-confirming diagnosis or assigning settled blame from one symptom
- a packet-only response when authorized bounded repair was requested and the
  owner binding is available
- changing multiple owners, retrying without a limit, or inventing a validator
  as temporary scaffolding
- reporting a preview, diff, command exit, or green unrelated check as health

## Verification

- trace diagnosis claims and repair decisions to reviewed evidence or diagnosis
- compare pre/post health on the affected surface and record commands or refs
- confirm actual effects, rollback status, cleanup, remaining uncertainty, and
  whether the target owner accepted or still owns the next handoff

## Adaptation points

Sessions provide reviewed evidence. Target owners provide mutation, checkpoint,
validation, rollback, approval, and durable-policy contracts.
