---
name: bulk-api-partial-success
description: >
  Design and test bulk APIs with partial success semantics: per-item results, atomic vs
  best-effort modes, idempotency keys, error envelopes, ordering, limits, and client
  retry rules. Use when batch endpoints, bulk create/update, multi-status responses,
  or partial failure UX for owned APIs — not for abusing unbounded bulk endpoints.
---

# Bulk API Partial Success

## Scope And Authorization

- **In scope:** APIs and clients you own or are authorized to change/test.
- **Out of scope:** Flooding third-party bulk endpoints; using bulk for authz bypass beyond RoE.
- Partial success increases authz complexity — test cross-tenant item IDs carefully (authorized).
- Redact PII in bulk payloads from logs.
- Pair with `code-quality-standards`, IDOR skills for authz, and rate-limit skills for abuse.

## When To Use

- Designing `POST /resources:batch` or `PATCH` multi-item endpoints.
- Clients need independent per-item success/failure instead of all-or-nothing only.
- Migrating slow N+1 client loops into one bulk call safely.
- Defining HTTP status: 200 vs 207 vs 400 when mixed outcomes occur.
- Fixing ambiguous bulk error responses that break retries.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GraphQL batching attacks | GraphQL security skills |
| Generic REST style | `api-recon-and-docs` / API design skills |
| Rate limit / abuse | rate-limit skills |
| Transactional DB design only | `database-migration-safety` / data skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mode | Semantics | Use when |
| --- | --- | --- |
| Atomic | All succeed or all roll back | Strong consistency required |
| Best-effort partial | Independent items; mix OK | Large imports, email fanout |
| Stop-on-first-error | Prefix applied | Rare; document clearly |
| Async bulk | Job ID + poll/webhook | Long-running imports |

**Response shape goals:** stable item index/key, error code, retryable flag, server idempotency replay.

## Workflow

### 1. Confirm scope and success criteria

1. Record operations (create/update/delete), max batch size, auth model, SLA.
2. Success: documented semantics; clients can retry safely; authz per item; metrics for partial rates.
3. Choose HTTP convention and stick to it across APIs.

### 2. Choose semantics and status codes

| Outcome | Recommended HTTP | Body |
| --- | --- | --- |
| All success | 200 (or 201 for all creates) | results[] all ok |
| Mixed | **207 Multi-Status** or **200** with explicit `errorCount` (pick one org-wide) | per-item status |
| All fail validation | 400 | per-item or top-level errors |
| Authn failure | 401 | no partial apply |
| Entire batch not authorized | 403 | none applied |
| Oversize batch | 413 or 400 | no apply |

1. Document whether partial apply commits independently (separate transactions per item).
2. Atomic mode: single transaction; return 4xx without side effects on failure.

### 3. Design envelope

```json
{
  "batchId": "01J...",
  "mode": "partial",
  "results": [
    {
      "index": 0,
      "clientKey": "row-1",
      "status": "success",
      "httpStatus": 201,
      "resourceId": "res_123"
    },
    {
      "index": 1,
      "clientKey": "row-2",
      "status": "error",
      "httpStatus": 409,
      "error": {
        "code": "conflict",
        "message": "duplicate external_id",
        "retryable": false
      }
    }
  ],
  "summary": { "total": 2, "succeeded": 1, "failed": 1 }
}
```

1. `clientKey` / idempotency key **per item** for safe retries.
2. Stable `code` enum for clients; human `message` optional and non-PII.
3. Include server-generated `batchId` for support traces.

### 4. Implement server rules

1. **Authz per item** — never authorize once for whole batch using first item’s tenant.
2. Cap `max_items` (e.g. 100) and payload bytes; document.
3. Time budget: soft timeout → mark remaining as `error`/`timeout` retryable **without** double-apply (use idempotency).
4. Ordering: specify parallel vs sequential; if sequential, define dependency limitations (usually disallow inter-item deps).
5. Validation: schema-validate all items first optional precheck mode vs stream apply — document.

```text
# Pseudocode
for item in items:
  if not authz(user, item): results.append(403); continue
  try apply_idempotent(item.key, item): results.append(201)
  except Conflict: results.append(409, retryable=false)
  except Transient: results.append(503, retryable=true)
```

### 5. Client retry rules

| Item error | Client action |
| --- | --- |
| `retryable: true` | Retry item or sub-batch with same idempotency key |
| `retryable: false` | Fix payload; do not blind retry |
| HTTP 429 on batch | Backoff whole batch |
| Network drop mid-batch | Re-send with same per-item keys; server dedupe |

1. Clients should not assume atomicity in partial mode.
2. UI: show per-row errors; allow retry failed subset only.

### 6. Verify with tests

```bash
# Contract tests (example sketch)
# 1) mixed validation
# 2) cross-tenant ID in one item → only that item 403, others succeed if mode partial
# 3) replay same idempotency keys → no duplicate resources
# 4) oversize → rejected
pytest tests/test_bulk_api.py -q
```

1. Load test max batch size p99 latency.
2. Authz matrix: user A items + user B id → isolated failure.
3. Observability: `bulk_items_total{status}`, `bulk_partial_batches_total`.

### 7. Hand off

1. OpenAPI: document mode, limits, envelope, status policy.
2. Runbook: how support interprets `batchId`.
3. Apply `code-quality-standards`; consider `json-schema-design` for envelope schemas.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Semantics | Explicit partial vs atomic flag | Undocumented half-apply |
| Authz | Per item | One check for entire payload |
| HTTP | Consistent 207/200 policy | Random 500 on first item fail after others committed |
| Idempotency | Per-item keys | Retry creates duplicates |
| Errors | Machine codes + retryable | Free-text only |
| Limits | Hard max items | Unbounded 10k row silent timeout |

## Output Checklist

- [ ] Mode (atomic/partial/async) chosen and documented
- [ ] Status code policy written
- [ ] Response envelope with per-item results
- [ ] Per-item authz and idempotency implemented
- [ ] Max size limits enforced
- [ ] Client retry guidance published
- [ ] Tests for mixed, authz, idempotent replay
- [ ] Metrics/logs with batchId (redacted payloads)
- [ ] OpenAPI updated
- [ ] `code-quality-standards` applied

## Rules

- Never hide partial commits behind a single false “success”.
- Authorize every item in the caller’s tenant/context.
- Idempotency is mandatory if clients retry partial failures.
- Authorized load testing only; prevent bulk abuse with authn + rate limits.
- Focus this skill on bulk semantics; deep IDOR testing uses IDOR skills.
