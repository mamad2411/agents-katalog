---
name: incident-rca
description: Structured production incident triage using a four-phase workflow (hypothesis → reproduce → isolate → fix + verify) with service-context gathering and a durable RCA summary artifact.
---

> All `docs/` paths in this skill refer to the plugin-level `docs/` directory (`../../docs/` relative to this file), not a `docs/` directory inside this skill folder.

## Purpose

Use this skill when a developer or on-call responder needs a structured process for triaging a **production incident** — a live alert, service degradation, SLA breach, or customer-impacting failure — and driving it from symptom through root cause to verified fix.

This skill is **not** for general-purpose debugging. For bugs discovered during development, test failures, or non-production issues, use `debug` instead. `incident-rca` is specifically designed for situations where a production system is actively degraded: it adds a service-context gathering phase (metrics, logs, traces, deployment history) before hypothesis formation, and it produces a durable RCA summary artifact suitable for post-incident review.

Persistent team, squad, or fleet-style long-lived orchestration is out of scope for this skill. Use a separate orchestration layer if persistent coordination is needed.

## When to Use It

Activate when the developer or on-call engineer describes a live production problem:

- "we have a 5xx spike on the payments endpoint"
- "the service is returning errors after today's deploy"
- "customers are reporting timeouts on checkout"
- "our SLA dashboard is red — latency exceeded P99 targets"
- "PagerDuty alert: error rate on /api/orders above threshold"

Also activate when:

- a monitoring system has fired an alert tied to a production service;
- a deployment has been correlated with degraded behavior;
- the issue involves multiple services, logs, metrics, or traces that need systematic collection;
- a post-incident RCA document is expected as an output.

Do **not** activate for:

- local test failures or development-time bugs (use `debug`);
- architecture health reviews (use `arch-review`);
- proactive test generation (use `e2e-tests`).

## Project-Specific Inputs

Before you start, identify:

- the affected service or endpoint and the alerting signal (error rate, latency, HTTP status codes);
- where to find production observability data (log aggregator, metrics dashboard, tracing system, deployment history);
- the repository's validation commands for running the test suite;
- a safe reproduction environment (staging, canary, local) — or confirm that none exists;
- `max-failed-hypotheses` — number of failed hypotheses before narrowing scope (default: **3**);
- where durable RCA artifacts should live (default: `.agent/rca-summary.md`).

If any critical inputs are missing, ask the developer before proceeding.

## Default Roles

Use separate roles for:

- a **scout** that gathers service context — recent deployments, log excerpts, metric anomalies, trace data, and recent commits touching the affected area;
- an **implementer** that forms hypotheses, attempts reproduction, isolates the root cause, and implements the fix;
- a **reviewer** that validates root-cause logic, fix correctness, and regression safety.

The scout produces a factual context brief of the incident: what is failing, what changed recently, what the observability data shows. The implementer and reviewer consume this brief independently.

### Model Selection

Resolve the active model for each role using this priority chain:

1. **Project config** — look for the runtime-specific config file in the current project root:
   - Copilot CLI: `.copilot/models.yaml`
   - Claude Code: `.claude/models.yaml`

   Read the `implementer`, `reviewer`, and `scout` keys directly. If a key is absent, fall back to the baked-in default for that role.

2. **Session cache** — if models were already confirmed earlier in this session,
   reuse them without asking again.
3. **Baked-in defaults** — if neither config file nor session cache exists, use
   the tier defaults below silently without prompting. Create project model config
   only when the developer wants persistent overrides.

#### Default model tiers

Defaults are **tiers, not pinned versions** — resolve each tier to the latest model of that tier available in the active runtime. In Claude Code, pass the tier alias to the Agent tool (`haiku`, `sonnet`, `opus`) — aliases are the only values it accepts, so Claude Code always runs the tier's latest model. Pinning an exact model version via `models.yaml` is a Copilot CLI capability (`.copilot/models.yaml` only).

| Role        | Claude Code                          | Copilot CLI                      | Effort |
|-------------|--------------------------------------|----------------------------------|--------|
| Implementer | `sonnet` (latest Sonnet)             | latest Claude Sonnet             | high   |
| Reviewer    | `opus` (latest Opus)                 | latest GPT or latest Claude Opus | high   |
| Scout       | built-in `Explore` agent, or `haiku` | latest Claude Haiku              | low    |

See `docs/model-selection.md` in this plugin for the full role matrix, per-role effort guidance, and the premium-tier (Fable) opt-in policy, and `docs/models-config-template.md` for ready-to-copy config templates.

## Workflow

### Phase 1 — Hypothesis

Run a scout pass to gather the **factual context brief** for the incident:

- symptom description (error type, affected endpoint, user impact);
- recent deployment history (commits deployed in the last 24 hours, migration events);
- error logs (exact error messages, stack traces, log timestamps);
- metric anomalies (latency spikes, error-rate increases, throughput drops, correlated with deployment or config changes);
- affected services and their dependency graph;
- recent configuration or infrastructure changes.

Using the gathered context, list candidate root causes ranked by likelihood. Present the ranked list to the developer and confirm the most likely hypothesis to investigate first.

**Gate: Hypothesis confirmed**

- PASS — developer confirms a hypothesis to investigate.
- FAIL — no plausible hypothesis can be formed from available context. Emit a partial RCA and stop.

Write `.agent/SESSION.md` with `current-phase: "hypothesis"` after this phase completes.

### Phase 2 — Reproduce

Attempt to reproduce the failure in a safe environment (staging, canary, or local).

1. Replicate the conditions identified in the hypothesis (deploy state, data state, request pattern).
2. Confirm the symptom appears in the reproduction environment.
3. If **no reproduction environment exists**: declare **degraded mode** — proceed with static analysis only. Mark the gate as PARTIAL and record the limitation in the RCA artifact.
4. If reproduction fails despite a valid environment: record the attempt in `## Failed Hypotheses` and return to Phase 1 for the next hypothesis.

**Gate: Reproduction**

- PASS — failure reproduced in a safe environment.
- PARTIAL — no reproduction environment available; proceeding in degraded mode (static analysis only).
- FAIL — reproduction failed after exhausting available environments.

Write `.agent/SESSION.md` with `current-phase: "reproduce"` after this phase completes.

### Phase 3 — Isolate

Narrow the failure to a specific component, service, function, or code path.

1. Trace from the symptom inward — follow the error from the entry point through the call chain.
2. Eliminate components that are functioning correctly and record them in `## Failed Hypotheses`.
3. Record evidence at each step: log lines, stack traces, metric anomalies, code paths.
4. If isolation stalls after `max-failed-hypotheses` attempts, apply the rescue policy: narrow scope to the next-largest suspect component and retry.
5. If still stalled after rescue: escalate to the developer with a partial RCA containing all evidence gathered so far.

**Gate: Root cause isolated**

- PASS — root cause narrowed to a specific location with supporting evidence.
- FAIL — isolation failed after rescue attempts. Emit a partial RCA and stop.

Write `.agent/SESSION.md` with `current-phase: "isolate"` after this phase completes.

### Phase 4 — Fix + Verify

1. Propose the fix to the developer before applying. Include:
   - the confirmed root cause (one sentence);
   - the proposed change (files, logic);
   - the test or reproduction check that will validate the fix.
2. Implement the fix.
3. Run the repository's validation suite — all existing tests must pass.
4. Confirm the original reproduction (or the symptom signal, in degraded mode) no longer triggers.
5. Document the fix in the durable RCA summary artifact.

**Gate: Fix verified**

- PASS — validation suite passes AND original symptom is resolved.
- FAIL — fix introduces new failures or does not resolve the symptom. Escalate to developer.

Write `.agent/SESSION.md` with `current-phase: "fix-verified"` after this phase completes.

### Produce the durable RCA summary artifact

At the end of every invocation — whether the workflow completes fully, stops early, or is interrupted — produce a **durable RCA summary** written to the confirmed artifact path. This artifact must contain:

- **Symptom**: what failed, how it was detected, user impact.
- **Hypothesis confirmed**: the root cause that was validated (or the best candidate if unconfirmed).
- **Evidence gathered**: log excerpts, metric data, stack traces, deployment correlation.
- **Fix implemented**: what was changed, file paths, and logic.
- **Validation outcome**: test results, reproduction check result.
- **Open questions / follow-ups**: unresolved threads, recommended hardening steps, monitoring gaps.

"Durable" means written to a repository-appropriate sink — a committed document, a PR comment, or an issue — not only to chat. Chat-only summaries do not satisfy this requirement.

### Update SESSION.md

Write `.agent/SESSION.md` using the full schema defined in `docs/session-md-schema.md`. All five YAML frontmatter fields are required on every write:

- `current-task`: the incident description
- `current-phase`: the current phase name
- `next-action`: what happens next
- `workspace`: the active branch or PR reference
- `last-updated`: current ISO-8601 timestamp

Required sections: `## Decisions`, `## Files Touched`, `## Open Questions`, `## Blockers`, `## Failed Hypotheses`.

Write SESSION.md after each phase gate. If the write fails, log a warning and continue.

## Required Gates

### Phase gates

Each phase must satisfy its specific gate condition (see workflow above) before advancing to the next phase. A failed gate halts forward progress; the skill must either rescue or stop.

### RCA artifact gate

The durable RCA summary artifact must be written to disk at the end of every invocation. If both the primary path and the fallback path (`.agent/rca-summary.md`) fail, the gate fails.

### Verification checklist — RCA complete

Before declaring the incident RCA complete, confirm ALL of the following. Any failing item blocks the "RCA complete" declaration.

- [ ] Hypothesis confirmed with evidence — PASS / FAIL
- [ ] Root cause isolated to specific location — PASS / FAIL
- [ ] Fix implemented and validation suite passes — PASS / FAIL
- [ ] Original symptom resolved (reproduction no longer triggers) — PASS / FAIL
- [ ] Durable RCA summary artifact produced — PASS / FAIL
- [ ] SESSION.md written with correct phase — PASS / FAIL

If any item is FAIL: report the failing item(s) by name, state what must be done to resolve each, and do not advance past the gate.

## Stop Conditions

- Reproduction is impossible and static analysis cannot isolate the root cause — stop, emit a partial RCA with all evidence gathered.
- The fix causes new failures that cannot be resolved without significant scope expansion — stop, escalate to the developer with a partial RCA.
- Incident scope grows to multiple unrelated services — stop, split into separate RCA tracks and emit a partial RCA for the current scope.
- The developer asks to stop.
- All hypotheses exhausted after rescue attempts — stop with a partial RCA.

Before stopping, ensure any partial results are preserved as a durable artifact so work is not lost. A partial RCA must still contain the symptom, evidence gathered, hypotheses attempted, and the reason for stopping.

## Example

### Invocation

```text
Developer (on-call): We're seeing a 5xx spike on /api/payments — started about 2 hours ago
```

### Walkthrough

**Phase 1 — Hypothesis**

The scout gathers the factual context brief:
- Recent deployments: a DB migration (`add_nullable_bank_code`) was deployed 2 hours ago.
- Error logs: `NullPointerException` in `PaymentService.charge()` at line 142, reading `merchant.bankCode`.
- Metrics: latency spike on `/api/payments` correlated exactly with the migration deployment timestamp.
- Affected services: `payment-service` only; upstream `order-service` sees elevated error rates from downstream.

Candidate hypotheses (ranked):
1. DB schema change made `merchant.bankCode` nullable but `PaymentService.charge()` assumes non-null (most likely — correlates with migration timing and NPE location).
2. Migration caused a transient connection-pool exhaustion (less likely — error is NPE, not timeout).

Developer confirms H1 as the primary hypothesis.

**Phase 2 — Reproduce**

Run the migration on staging, then execute a test charge. `PaymentService.charge()` throws the same `NullPointerException`. Reproduction confirmed.

**Phase 3 — Isolate**

Root cause: `PaymentService.charge()` line 142 reads `merchant.bankCode` which is now nullable after the migration. The code path has no null guard. Evidence: stack trace, migration diff, schema before/after comparison.

**Phase 4 — Fix + Verify**

Fix: add a null guard on `merchant.bankCode` in `PaymentService.charge()` (default to the merchant's primary bank code from the accounts table). Add a migration rollback path that restores the NOT NULL constraint with a default value. Run the validation suite — all tests pass. Staging charge succeeds with the fix deployed.

### Durable RCA summary (abbreviated)

```markdown
# RCA — 5xx spike on /api/payments

**Symptom:** 5xx errors on POST /api/payments starting 2025-07-20T14:00Z.
**Hypothesis confirmed:** DB migration `add_nullable_bank_code` made `merchant.bankCode` nullable; `PaymentService.charge()` line 142 has no null guard.
**Evidence:** NullPointerException stack trace, migration timing correlation, staging reproduction.
**Fix:** Null guard + migration rollback path. PR #347.
**Validation:** All tests pass, staging charge succeeds.
**Follow-ups:** Add NOT NULL constraint back with default value; add null-safety lint rule for merchant fields.
```
