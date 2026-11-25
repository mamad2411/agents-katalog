---
name: delivery-audit
description: "Asynchronously audits completed top-level delivery tasks using one fixed native CLI Graph. Use for the automatic post-delivery metadata handoff and when maintaining this audit skill; never audit an audit, subtask, status check, or metadata-only episode."
---

# Delivery audit

Activation verified 2026-10-14 on Windows Fleet: classified whole-TODO
Graph/Pair completion -> final COMPLETE Hub `record-session` -> native audit
-> Office. The controller supports STOP and does not block product closeout.
Unclassified/ambiguous tasks and `record-handoff` alone remain outside this
automatic path. Never add a manual audit command to ordinary closeout.

## Trigger and result

- The canonical closeout gateway enqueues exactly one audit after a top-level
  `delivery` or `repair` with outcome `COMPLETED`. It sends typed packet v1
  metadata to the existing runner; it does not ask the agent to start a second
  planner or scheduler.
- `audit`, `audit-review`, `subtask`, `status`, and `metadata-only` packets do
  not trigger another audit. Worker, scout, reviewer, and integrator records
  belong in the parent packet. A worker node does not delegate its assigned
  leaf again.
- Enqueue is asynchronous. The delivered product and its existing acceptance
  stay complete while the audit runs, waits for quota, or fails. Never make a
  user wait for the graph or treat an enqueue receipt as an audit result.
- Follow the fixed graph, metadata boundary, and receipt rules in
  [integration.md](references/integration.md). The typed delegation rule is in
  [delegation.md](references/delegation.md).

## Fixed audit graph

Run the installed native `todo_graph.py` once for this fixed DAG:

1. One mandatory history scout uses the installed deterministic economic gate
   to select bounded, sanitized prior task-audit records. It never scans source
   repositories or raw transcripts.
2. `execution-audit` checks outcome, evidence coverage, and execution
   efficiency together. It does not repeat product acceptance or UAT. Use one
   native maker and one independent reviewer.
3. `recurrence-audit` compares the current accepted report with the bounded
   prior records, preserving denominators and unknowns. Use one native maker
   and one independent reviewer.

Use real installed CLI profiles and receipts, with K/W execution where
qualified and a reviewer from a different provider lineage. A different CLI
name alone is not independent review. The graph and reviewer topology are
fixed; do not add a planner call, polling council, nested graph, permanent
second orchestrator, or arbitrary minimum agent count.

## Delegation and recurrence

- A capable M/D parent plans once, then assigns each well-scoped eligible
  subtask to a qualified K/W CLI when such a subtask exists. Keep the parent
  responsible for integration and the credential, irreversible, owner-model,
  or hard-uncertainty decision. Record a real exception when it applies; do not
  hide discretion behind "delegate if needed".
- A declaration, planned task count, profile path, or agent name is not proof.
  Only a verified native completed child-maker receipt establishes delegated
  execution. No fixed number of children is required. See
  [delegation.md](references/delegation.md).
- Keep one-off and task-specific findings in the audit report. Route only a
  confirmed systemic stack issue from an accepted recurrence report to the
  existing RSI Helpdesk. Historical records alone never reopen a resolved
  ticket. Dispatch uses validated enums and opaque evidence references, never
  free model prose.
- Unknown, ambiguous, transient-provider, and quota-reset evidence stays
  unknown or transient. Never invent availability or cost, switch to a paid
  API, or block the completed product because the audit cannot run.

## Delivery lead-time and ceremony telemetry

Passively monitor delivery efficiency using `scripts/delivery_audit_metrics.py`
without creating new mandatory per-task ceremony files:
- Computes `lead_time_s`, `model_exec_s`, `review_s`, `check_s`, `ceremony_s`,
  and `ceremony_ratio = round(ceremony_s / max(lead_time_s, 1.0), 4)` from existing
  `state.json` and `telemetry.jsonl`.
- Flags `high_ceremony_alert=True` when `ceremony_ratio > 0.25` as a diagnostic
  heuristic, never an acceptance gate or proof of wasted work. Unattributed wall
  time may be counted as ceremony; overlapping durations and missing data distort
  the ratio (zero also does not establish process health). Change a process only
  for a concrete cause and task impact, not a threshold or synthetic benchmark.
  Do not add a measurement step to ordinary sessions.
- Choose S/M/L from the actual task and dependencies, preserving required review:
  - **S**: inline TODO for simple responses and local fixes.
  - **M**: single `todo_pair.py` maker/reviewer pair without graph scheduler overhead.
  - **L**: parallel `todo_graph.py` reserved for genuine multi-task dependency DAGs.
- Benchmark trace profiles via `python scripts/delivery_audit_metrics.py benchmark`.

## Privacy and safety

Use only the bounded typed packet described in [integration.md](references/integration.md).
Reject unknown fields and invalid evidence before durable enqueue or model,
Office, or RSI dispatch. Do not read source text, code, command strings, raw
stderr, mail, secrets, URLs, restricted customer data, or unbounded history.
Model output is untrusted; only schema-valid findings grounded in opaque
evidence IDs can be reported or routed.

This skill does not authorize deployment, production changes, credential or
permission changes, deletion, or real Helpdesk/Office effects during tests.
