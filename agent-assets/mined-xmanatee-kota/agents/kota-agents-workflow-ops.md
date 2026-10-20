# Workflow Ops Module

This module owns the `kota workflow` CLI surface, its `kota automation` authoring
alias, and the workflow HTTP API routes.

## Internal Structure

- `runs/` — Run inspection: list, show, diff, export, cost, stats, step-inspect, follow, logs, history.
- `definitions/` — Definition inspection and validation: definitions, definition-log, deps, validate.
- `execution/` — Execution and control: run, dry-run, trigger, triggers, control, gc.
- `routes/` — HTTP API: route wiring and handlers for `/api/workflow/*`.

Shared utilities (`utils.ts`, `definitions-source.ts`) stay at the module root.

## Boundaries

- No change to command names, flags, aliases, or output without updating docs.
- `workflow show` renders the client detail directly, including tags and the
  supplied delivery and continuation state. Missing delivery displays as
  unavailable. Local clients derive delivery at the evidence boundary;
  `--step` retains full artifact output under canonical run authority.
- Retry eligibility comes from durable runtime state, not step-result status:
  successful steps may still have a retained integration failure. CLI and HTTP
  clients submit retry intent to the same admission owner.
- `workflow logs --follow` discovers agent streams before their terminal step
  results exist and continues through active integration. Timestamped repair
  activity and the durable publication wait describe different states; a quiet
  stream alone does not establish a stall while publication is waiting.
- Do not add a second automation client namespace. Operator-facing labels may
  say automation or hook, but commands and clients still route through the
  workflow contract and workflow run store.
- The module's live UI source owns run/automation projection and controls;
  related approval, question, and session reads remain typed client calls.
- Tests are co-located with the code they cover inside each subdomain.
- HTTP routes are contributed via `routes/routes.ts` using handlers in the same subdirectory.
- `workflow resume` changes dispatch pause only. The explicit `--retry-agent`
  option clears a corrected quality/output pause; provider and authentication
  incidents remain parked until their recorded recovery horizon elapses.
  Status and resume output report the effective pause reason; resuming an
  operator pause cannot override the automatic quota admission hold.
- Material canary quality regressions use the agent-only quality-pause control.
  They persist in the selected scope's backoff authority and leave deterministic
  workflow dispatch available until an explicit agent retry. That retry clears
  only that scope's quality pause and preserves any provider reset horizon that
  is still active there.
- workflow exec is the eval-harness subprocess boundary. Its paired
  --agent-harness / --agent-model override may also carry --agent-effort and
  validated --agent-options JSON (maxTurns, harnessOptions, modelOutputTokenLimits) so
  model-matrix runs execute the requested runtime facts instead of merely
  labelling the result. Standalone execution is limited to positively
  identified eval-harness roots; canonical execution uses the scoped daemon
  workflow client and fails closed when daemon authority is unavailable.

## KotaClient Surface

The `workflow` namespace contract lives in `client.ts` (`WorkflowClient` and
result/option types). Core owns canonical queued-run and wire-trigger assembly.
`localClient(ctx)` and `daemonClient(link)` factories in `index.ts` realize
the contract; `buildWorkflowDaemonHandler(link)` is the daemon-side factory
that routes the namespace methods through the typed
`DaemonTransport`. Trigger event, schema, payload, run id, and eligibility must
have identical semantics on both paths. Client tests own request selection, response reshaping, and typed domain errors
through controlled transport ports. Route tests own proxy fallback, retrigger
handoff, and artifact/SSE projection; daemon-control and workflow runtime tests
own authorization, admission, durable pause, cancellation, and retained recovery.
CLI tests retain parsing and operator guidance; dry-run decision cases also check
their rendering. Trial isolation uses the real runtime, and simulation composes
existing preview owners without reproducing coordinator semantics.
