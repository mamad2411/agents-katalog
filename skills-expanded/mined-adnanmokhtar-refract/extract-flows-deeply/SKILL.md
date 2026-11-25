---
name: extract-flows-deeply
description: Round-two deep extraction of business-critical and admin/internal flows — traces ≥5 representative flows end-to-end (trigger → entry → ordered steps → side effects → error paths → idempotency). Used by /setup-project Phase 2.9 in REFINE mode to upgrade round-one flow detection from "the app does checkout" to a precise step-by-step narration with file:line for every step.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-flows-deeply

## Purpose

A flow is a *user-meaningful* sequence (signup, checkout, refund, file upload, nightly batch). Round-one Phase 2 doesn't enumerate flows — it detects entry-point shapes (HTTP routes, queue listeners). Round-two follows individual flows from trigger to final side effect.

The output is what enables an agent working on a related task to say "I see — to add a discount to checkout, I need to insert a step between `cart.validated` and `payment.charged`, and the discount must be reflected in the receipt event published at the end."

## Premise

- Real source is the truth. Walk each flow's call graph end-to-end — entry handler, every middleware in the chain, every called function down to DB / external / queue / cache boundaries — before recording a step.
- Every step cites `<file:function:line>` resolved at the current commit; every side effect is read from the actual method body, not inferred from class names.
- Error paths are walked the same way as happy paths — they reveal where recovery / retry / silent-fail lives.
- Empty extraction is honest — a flow with `idempotency: none` is a finding (not a gap); a `[REFINE-WEAK: flows-coverage]` flag is a valid output when <5 flows trace.
- Fabrication — inferring an external-vendor call from a class name (e.g., guessing payment-provider use from an `EmailService`), asserting a transaction boundary that isn't in code, mixing two flows that share a middle — produces a runbook the team will trust and follow incorrectly.

## Mechanical halt

- Hand-wave in flow output — `etc.`, `...`, `the usual middleware`, `appears to be transactional`, a `steps:` entry without `<file:function:line>`, an `error_paths:` entry without `raised_at:` + `caught_at:`, a flow whose call graph wasn't actually walked — REFUSE to write the YAML.
- Re-trace and regenerate the flow OR downgrade it to `[REFINE-WEAK: flows-coverage]`.
- If <5 flows are traceable, write `<NOT-DETECTED: flows: <N> below threshold 5: <reason>>` per the WEAK gate.
- Never average across surfaces — HTTP, queue, and scheduled handlers behave differently and each gets its own traced row.

## When to use

- `/setup-project --refine` Phase 2.9 — extract ≥3 business-critical flows + ≥2 admin/internal flows.

## Where the output lands

- **Default destination: `ai/business-flows.md`.** The traces written to `_refine-extract.md` § Flows are enriched into the round-one flow catalog by Phase 4.7-DEEP — each matching flow's `Happy path` / `Invariants` / `Failure modes` gains `file:function:line` steps, per-step side effects, error paths, idempotency, and transaction boundary; a traced flow with no round-one match is appended as a new catalog entry. This is the load-bearing file feature-work agents read (Tier 2: "New feature → `ai/business-flows.md`").
- **Secondary, opt-in: `ai/runbooks/<flow>.md`** — only when explicitly requested via `--refine --include-runbooks`. Runbooks are the operational long-form; `ai/business-flows.md` is the always-on default and is never gated behind the flag.

## Inputs

- `flow_count` (default: 5; min 5 for STRONG).
- `flow_hints` (optional) — user-provided list of flow names. If present, prioritize these over auto-discovery.
- `output_section` — section path (default: `## Flows`).

## Procedure

### Step 1 — Pick flows to trace

Auto-discover sources for flow candidates (combine and dedupe):

1. **Lifecycle events from Phase 2.7** — every event that has ≥2 emitters or is consumed by ≥1 handler is a flow.
2. **README.md / CONTRIBUTING.md / docs/** — search for headings matching `## How <X> works`, `## <Verb>ing <noun>`, `## End-to-end`, `### Flow`, `## Lifecycle`.
3. **Test file names** — the project's e2e / integration test naming convention (e.g., `*_e2e.<test-ext>`, `*_integration_test.<test-ext>`, `test_<flow>_flow.<test-ext>`, `<Flow>IntegrationTest.<ext>`). The flow name is often in the filename.
4. **Observability / monitoring config** — if accessible, transactions named `<verb>.<noun>` in the project's APM tool are critical user paths.
5. **High-coverage endpoints / consumers** — heuristic: top 10 by coverage % or git churn.

**Record which of the five fired, in the output header** — `discovery_sources: [lifecycle-events, tests]`
plus `discovery_sources_absent: [docs, apm, coverage]`. Source 4 carries an explicit escape clause
("if accessible") and sources 2 and 5 fail silently on a repo with no docs and no coverage report, so
without this line a run that found candidates from one source is indistinguishable from one that
checked all five. Those are different confidence levels in the flow list, and the next run needs to
know which of the two it is looking at before deciding whether re-running is worth anything.

A candidate list built from a single source is not WEAK — it is narrow, and narrowness has a
direction: tests-only discovery finds what is tested, APM-only finds what is slow, docs-only finds
what someone wrote up. Naming the source names the bias.

Pick:

- 3+ business-critical (user-facing) flows.
- 2+ admin/internal flows (`bulk-import`, `nightly-rebuild-stats`, `daily-reconciliation`, `cleanup-stale-sessions`).

If the codebase is too small for 5 distinct flows, lower the count and flag `[REFINE-WEAK: flows-coverage]` in the output.

### Step 2 — Trace each flow

For each picked flow:

1. **Trigger**: HTTP request? scheduled job (cron)? queue message? user action? webhook?
2. **Entry point**: file:line of the handler function.
3. **Ordered steps**: walk the call graph (re-use the procedure from `extract-architecture-deeply` Step 4). Record each step as one line: `<file:function:line> — <1-sentence what it does>`.
4. **Side effects** at each step:
   - DB writes (entity, operation: insert/update/delete, transactional?).
   - External calls (vendor, endpoint, sync/async).
   - Queue publishes (topic, payload-shape one-liner).
   - Cache writes/invalidations.
   - File writes (where, format).
   - Email / SMS / webhook / notification sends.
5. **Error paths**: at each step, what exceptions are raised + where they're caught + what response/state results.
6. **Idempotency mechanism**:
   - Idempotency key from request header? client-generated UUID? deterministic hash of payload?
   - DB unique constraint guarding double-write?
   - Outbox-pattern + at-least-once consumer?
   - **Or no idempotency mechanism** — if so, record `idempotency: NONE` (this is itself an important finding for round-two perf/reliability artifacts).
7. **Concurrency mode**: are steps sequential? batched? parallel? Cross-reference with Phase 2 Step 15 concurrency-primitive detection.
8. **Total side-effect surface**: sum at the end — "1 invoice row, N ledger rows, 1 outbox event, 1 payment-provider charge call, 0 emails."

### Step 3 — Output

Write to `.claude/_refine-extract.md` under `## Flows`:

```yaml
extraction_date: <YYYY-MM-DD>
flow_count: <N>
strong_signals: ["business-flows", "admin-flows", "idempotency", "side-effects"]

flows:
  - name: <verb-noun e.g. checkout, signup, refund>
    classification: <business-critical|admin-internal>
    trigger: <HTTP POST /api/checkout | cron `0 2 * * *` | queue `orders.created`>
    entry_point: <file:line>
    middleware_chain: [<list of file:line>]
    steps:
      - file: <file:function:line>
        does: <1-sentence>
        side_effects: [<list>]
      # ... ordered
    error_paths:
      - condition: <e.g. payment-declined>
        raised_at: <file:line>
        caught_at: <file:line>
        response: <e.g. 402 + customer email>
    idempotency: <key-mechanism|unique-constraint|outbox|none>
    transaction_boundary: <file:line of the project's transaction primitive (e.g., `BEGIN ... COMMIT`, `transaction { ... }`, framework-equivalent), or "no explicit boundary">
    total_side_effects:
      db_writes: { Invoice: 1, LedgerEntry: 5 }
      external_calls: [<list>]
      queue_publishes: [<list>]
      emails_sent: <N>
    concurrency: <sequential|batched|parallel|mixed>
    notes: |
      <2-3 lines on what's surprising / notable about this flow,
       e.g. "Payment-provider call is BEFORE DB write — payment success without DB persist
       requires manual reconciliation. See ADR-0034.">
  # repeat per flow
```

## Quality gate

- **STRONG**: ≥ 5 flows total, each with all fields populated, ≥ 3 business-critical.
- **WEAK**: < 5 flows OR several flows have empty `steps` (couldn't trace through call graph).

## Anti-patterns

- **Tracing only the happy path** — error paths often reveal more about the architecture (where is recovery? does the system retry? does it fail loudly or silently?).
- **Stopping at the controller** — controllers usually delegate; the flow is in the service + repository.
- **Mixing two flows** — if `POST /api/checkout` calls `BillingService.create_invoice` AND `BillingService.create_invoice` is ALSO called from `POST /api/recurring-charge/run`, those are TWO flows that share a middle. Trace each independently.
- **Inferring side effects from class name** — read the actual method body. A class called `EmailService` may also write to the database.
- **Calling absence-of-idempotency a bug** — sometimes it's intentional. Record the absence; let the user decide whether it's a finding or a feature.
