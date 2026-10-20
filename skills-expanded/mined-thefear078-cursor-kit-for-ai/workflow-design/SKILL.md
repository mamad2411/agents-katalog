---
name: workflow-design
description: MUST USE for n8n/cron/event workflows — triggers, validation, idempotency, DLQ, approvals. Triggers on automation design, duplicate runs, or silent workflow failures.
---

# Workflow Design

Automations are **distributed transactions** without 2PC. Design: trigger → validate → act → record → notify, with idempotency keys and dead-letter queues — applies to n8n, Temporal, cron, queue workers.

## When This Skill Applies

- New n8n workflow or cron pipeline
- Duplicate charges/emails from retries
- Human approval steps (finance, deploy)
- Event-driven reactions (webhook → multi-step)
- Replacing manual ops with automation

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **F0** | Side effect without idempotency; infinite retry on bad payload | Stop |
| **F1** | No DLQ; secrets in workflow export JSON | Fix pre-prod |
| **F2** | Missing monitoring on failure branch | Sprint |
| **F3** | Layout | Optional |

Cross-ref: `api-integration` for external calls; `bot-scaffold` for chat triggers; `stripe` template for webhook idempotency.

## Phase 0 — Workflow Contract

```markdown
Name: invoice-paid-fulfillment
Trigger: Stripe webhook invoice.paid
Idempotency key: event.id
Success: shipment created + email sent
Failure: DLQ + PagerDuty if money moved
SLA: 5 min p95
```

## Phase 1 — Trigger Hygiene

- [ ] Verify signature (webhook secret) before parse
- [ ] Schema validate payload — reject poison early
- [ ] Dedupe table / Redis SET on event id
- [ ] Cron: distributed lock (Redis) so one runner

```sql
CREATE TABLE processed_events (
  idempotency_key text PRIMARY KEY,
  processed_at timestamptz DEFAULT now()
);
```

## Phase 2 — Step Design

Each step:

| Step | Retry? | Idempotent? | Compensating action? |

External calls use timeouts + circuit breaker (`api-integration`).

n8n specifics (2025–2026):

- Sub-workflows for reuse
- Error workflow global handler
- Credentials in vault — not node plaintext
- Version control: export JSON to git

## Phase 3 — Human-in-the-Loop

- Approval node with timeout and explicit deny path
- Audit log: who approved, payload hash
- Don't hold DB transaction open during human wait — persist state machine

## Phase 4 — Observability

- Log correlation id through all nodes
- Metrics: success, failure by step, latency
- Alert on DLQ depth >0

Cross-ref: `observability`.

## Phase 5 — Testing

- Fixture payloads in repo; dry-run mode flag
- Staging webhook endpoint mirror
- Chaos: kill worker mid-step — rerun must not duplicate

```bash
# n8n CLI if available
n8n export:workflow --id=WORKFLOW_ID --output=./workflows/invoice.json
```

## Output Template

```markdown
## Workflow Design: [name]

**Verdict:** ✅ / 🔶 / ❌

### Diagram
trigger → validate → ... → notify

### Idempotency
- Key:
- Store:

### Failure modes
| Step | Failure | Behavior |

### Security
- Secrets:
- PII:

### Monitoring
- ...
```

## Anti-Patterns

- **Retry forever** on 400 validation error
- **Parallel branches** both charge customer
- **No version control** on n8n — prod edit untracked
- **Synchronous 5min chain** in serverless HTTP handler
- **Email on every partial success** — alert fatigue

## Cross-References

| Skill | Use when |
|-------|----------|
| `api-integration` | HTTP nodes |
| `data-quality` | Output validation |
| `ci-fix` | Export lint in CI |

## Cursor Kit Templates

- `n8n`, `stripe`

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

