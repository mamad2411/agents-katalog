---
name: aoa-checkpoint-closeout-bridge
description: "Carry provisional checkpoint hints into a reviewed session closeout: harvest, progression, quest-promotion, and branch handoff. Use to collect bounded hints or execute after the current session artifact is closed and reviewed. Do not use mid-session for final judgment, without reviewed evidence, as a hidden playbook runner, or to write owner truth."
---

# aoa-checkpoint-closeout-bridge

## Intent

Preserve the existing checkpoint-closeout capability while its durable
scenario remains an `aoa-playbooks` playbook without an executable MCP owner.
Checkpoint hints remain provisional; the bridge makes every downstream skill
selection, evidence reread, state transition, and stop explicit.

## Trigger boundary

Use one mode:

- `collect`: record bounded checkpoint hints for later review without emitting
  harvest, progression, quest, or owner verdicts
- `execute`: carry one closed, explicitly reviewed artifact through the
  ordered closeout stages and return a session-local execution report

Do not use when the evidence is live, unreviewed, unbounded, or cross-session
identity cannot be separated; when the request is only a recap; or when a
mechanical checkpoint packet is being treated as proof, memory, progression,
quest, playbook, or owner truth.

## Inputs and outputs

Read `references/contract.yaml` first.

- `collect` consumes `checkpoint-focus-input` and returns
  `provisional-checkpoint-focus`
- `execute` consumes `reviewed-checkpoint-closeout-input` and returns
  `checkpoint-closeout-execution-report`

All outputs remain session-local. A caller may request an explicit local note
or report path, but this skill never writes an owner repository, durable
memory, quest state, progression state, proof surface, playbook, KAG, or stats
surface.

## Procedure

1. Select exactly one mode.
2. For `collect`, read `references/collect.md` to EOF and stop after the
   provisional focus packet.
3. For `execute`, read `references/execute.md` to EOF.
4. Before starting `execute`, require one closed and explicitly reviewed
   artifact plus its current-session boundary. Otherwise return
   `blocked_unreviewed_evidence` without loading downstream skills.
5. Load the exact available `aoa-session-harvest` and
   `aoa-session-progression-lift` bundles before their first nodes. Missing,
   ambiguous, or owner-unresolvable dependencies return
   `blocked_missing_capability`; do not replace them with generic reasoning or
   retired skill names.
6. Preflight each required owner dependency serially. In particular, obey the
   progression bundle's same-bundle source-handle -> manifest -> owner-model
   source-return gate with one completed tool turn per gate. Never substitute
   the profile root, `.system`, or a sibling skill directory for its exact
   handle. A manifest read batched with an owner document is a failed
   preflight, not a successful load.
7. Execute one node completely before selecting the next node. For each node:
   use one tool turn to load only that node's exact procedure; await it; use a
   later tool turn to reopen only the primary reviewed artifact; await it;
   then start, produce, and verify the typed output. Never preload several mode
   procedures or batch evidence rereads for several nodes.
8. Record the procedure-load and primary-evidence action references on that
   node. Earlier reads, cached context, checkpoint hints, another node's read,
   or a final assertion do not satisfy this requirement. Shared tool batches
   across nodes make every affected node
   `unverified_nonserial_node_execution`.
9. Record `selected`, `loaded`,
   `started`, `produced`, `verified`, and `completed`, or the exact
   `blocked`, `failed`, `skipped`, `deferred`, or `handed-off` terminal state.
   A node without its observable primary-evidence reread must terminate as
   `unverified_missing_evidence_reread`, never `verified` or `completed`.
10. Stop after the session-local execution report and explicit owner
   handoffs. Do not continue automatically into owner acceptance or writes.

## Contracts

- preserve the dependency order: donor extraction/classification before
  progression; progression before quest-promotion judgment
- reread the primary reviewed artifact before every executed stage; checkpoint
  notes, generated packets, previous node outputs, and remembered content only
  narrow attention
- treat every `classify[*]` instance and `closeout.report` as its own stage;
  each executed instance requires its own post-selection, pre-start reread
- treat each downstream skill mode as a separate selection and typed node, not
  as an implicit multi-mode invocation
- do not parallelize DAG nodes merely because their source artifact is the
  same; the observable order is part of the checkpoint capability
- allow skipped, deferred, stopped, and no-candidate outcomes; the DAG shape
  never forces a positive verdict
- keep the `aoa-playbooks` checkpoint-closeout route as scenario authority;
  this transitional skill does not claim playbook runtime execution
- keep techniques as optional provenance only, never runtime dependencies

## Verification

- verify review/closure and current-session identity before downstream load
- disposition every checkpoint hint as accepted, rejected, stale,
  cross-session, contaminated, or unresolved
- verify every produced node output against its loaded skill contract
- confirm stage order, observable evidence-read action refs, effects, terminal
  states, and owner handoffs are visible in the report
- compare every report claim with the actual node action record; never report
  a reread, load, tool call, effect, or verification that did not occur
- reject a run whose dependency gate or node reads were parallelized across
  phases, even if the final prose and action refs look plausible
- confirm no downstream owner surface changed and no mechanical artifact was
  narrated as reviewed judgment
