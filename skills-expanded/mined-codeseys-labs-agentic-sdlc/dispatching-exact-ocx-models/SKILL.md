---
name: dispatching-exact-ocx-models
description: >-
  Fires at the spawn boundary — after model-tier-rightsizing has chosen an exact OCX route,
  before the worker starts — when that conductor-selected route must be injected into an
  Agent or Workflow worker, especially for generated ocx agent types, namespaced provider
  IDs, or tool surfaces whose compatibility needs checking. Also fires on the symptom of a
  generated `ocx-*` agent or namespaced provider ID whose post-run identity is unverified.
  Not for choosing a tier or evaluating candidates; use model-tier-rightsizing first.
---

# Dispatching exact OCX models

Load `model-tier-rightsizing` first. This skill consumes its resolved `RuntimeAssignment`; it does
not choose a preferred model or make an unresolved route dispatchable.

## Preconditions

Require `resolution_state: resolved`, an exact model ID, explicit effort and context form, compatible
tools, immutable injection evidence, and a known post-run receipt path. An inherited/default model,
prompt prose, alias, missing injection support, incompatible tool surface, or absent receipt stops
before spawn.

Require the route/class cell to be qualified too, and ask that question BEFORE the assignment is
written rather than here: `route_qualification.py admit` in `model-tier-rightsizing` derives one
`admit-dispatch`/`refuse-dispatch` verdict over recorded evidence for one exact route and one task
class. A resolved assignment is not qualification evidence — the receipt carries no task class, so
it cannot express the question — and a refusal returns one `SeedProposal` instead of a dispatch.
Its `cell-quarantined` refusal is the standing consequence of the identity-mismatch and
default-provider-fallthrough events the verification step below detects: record the quarantine that
`quarantine_required` names, because a detected misroute that leaves the cell dispatchable will be
dispatched again.

## Select the real injection surface

- **generated `ocx-*` Agent types:** the agent definition owns the exact route. Its public `model`
  argument is a placeholder and may be ignored. Use only the generated type whose pinned route
  exactly matches the assignment; never put another ID in the prompt or placeholder and claim it
  was selected.
- **Workflow `agent()` calls:** every `agent()` call carries the assignment's exact `model` and `effort`.
  Do not inherit either. The context request must use the adapter's supported request form;
  prose such as “use 1m” is not injection.
- **Namespaced provider IDs:** preserve the full ID, for example
  `muse/muse-spark-1.2-contributor`. Never strip the provider prefix or replace it with a nominal
  family name.

Choose an agent type/tool set compatible with the route before dispatch. Muse tool names must be
at most 64 characters; remove unnecessary model-visible tools and avoid structured-output tooling
when that extra tool is incompatible. Do not broaden permissions merely to retain a convenient
agent type.

**A namespaced ID's provider prefix is checked against the LIVE catalog before dispatch, not after.**
The gateway does not fail closed on a prefix it does not serve: its router computes the prefix, finds
no provider of that name, discards that result, and forwards the model string verbatim to whichever
provider is DEFAULT — so the request is attempted and billed against the wrong upstream, and the
attribution the verification step below reads records the selected provider rather than the requested
one. Reading `routeKind: "default-provider"` afterwards is therefore detection of a charge already
incurred, not prevention. Before dispatching a namespaced ID, confirm its prefix appears in the
running gateway's own `GET /v1/models` (`ccodex models`, or `ccodex status` for configured-vs-live);
a prefix that is configured but absent from that catalog is not published and routes to the default
provider exactly as an unknown one does. If the catalog cannot be read, the prefix is unverified —
return one SeedProposal, not a dispatch. A bare, un-prefixed ID is not subject to this check: those
take the router's own vendor-pattern and native-passthrough paths and need no catalog row.
`ccodex launch --model` enforces this refusal itself; a dispatch that reaches the gateway by any
other path carries the check as the caller's obligation.

## Verify, then admit

After the call, correlate the concrete request with adapter readback or gateway attribution and
compare observed provider/model to the assignment. Requested identity is not readback; neither a
prompt echo nor a response-body model label proves the route. Record effective effort/context only
when independently exposed, otherwise mark them unavailable rather than copying requested values.

On the OCX gateway the attribution surface is `ocx observe logs --jsonl`, correlated by
`requestId`: `resolvedModel`, `provider`, `status`, and `routeDecision.routeKind`/`.selected` are
the fields that carry identity, and `routeKind: "default-provider"` means the router did not
recognize the target — an alarm, not a route. Those fields were re-verified against opencodex
`2.28.0`. Two refusals are not identity evidence and must not be recorded as provider faults: an
HTTP 413 whose error type is `input_admission_refused` (new in 2.28.0, absent from a live 2.11.1
gateway) is opencodex's own input-admission preflight (estimated input above the route ceiling
× 2.5) refusing locally before any provider request — other 413s exist locally and upstream, so
match the error type, not the bare status — and a configured-but-unsynced provider
is served by the DEFAULT provider instead of failing closed. Both stop the dispatch.

If identity is ambiguous, mismatched, or uncorrelated, discard the result and stop or use the
assignment's predeclared fallback. **No verified receipt, no dispatch** means no result may enter the
production handoff as if the assignment ran.

## Output

Return the bounded worker artifact plus its verified receipt, or one refusal/SeedProposal naming
the missing injection, compatibility, or receipt capability. Never silently substitute a model.

## References

Read only what is needed:

- `references/ccodex-ocx-configuration.md`: configuring ccodex and the ocx gateway — the two
  configuration planes, provider onboarding order (restart is the publish step), liveness
  verification, the silent default-provider misroute, reasoning-token headroom for probe turns,
  OpenRouter upstream pinning, attribution reading, launch refusals, cheap test models, and the
  agent/operator authority boundaries. Read when the task is configuring or onboarding rather
  than dispatching.

## Admission rationale

This skill clears all four admission gates: its description selects exact dispatch rather than tier
choice; its recurring share justifies one small row; exact OCX routes and both dispatch surfaces
exist now; and it is task-shaped rather than always-on. It clears all five promotion signals:
**Recurs; needs sequencing; has repeated failure modes; has stable input/output; benefits from
explicit handoff**.
