---
name: mcp-control-plane-integrate
description: Integrates a hosted or trusted service with MCP control-plane auth, entitlements, and usage consume. Use when wiring quotas, API keys, billable operations, or adding a product ID to the control plane.
---

# Integrate with Control Plane

## Prerequisites

- Control plane running (`ADMIN_TOKEN` ≥32 chars, SQLite path, bind `127.0.0.1` locally)
- Product ID already in `products` in `src/store.js` (or add it + tests + README in the same change)

**Note:** `mcp-security-guard` paid Team/threat-feed today uses **mcp-security-cloud** (`cloud.ts` / `team.ts`), not this consume API. Use this skill for family-wide quota backends or a deliberate future unification — do not redirect security-guard cloud traffic here by accident.

## Admin bootstrap

```http
POST /v1/admin/accounts
Authorization: Bearer <ADMIN_TOKEN>
{ "accountId": "customer-1" }

POST /v1/admin/keys
{ "accountId": "customer-1" }
→ { "key": "mcp_…", "keyId": "<sha256>" }   # raw key shown once

PUT /v1/admin/plan
{ "accountId": "customer-1", "plan": "paid" }  # admin only — not payment proof
```

## Customer billable path

```http
GET /v1/entitlements
Authorization: Bearer mcp_…

POST /v1/usage/consume
{ "product": "api-guardian", "requestId": "scan-123", "units": 1 }
```

| Status | Meaning | Action |
| --- | --- | --- |
| 200 | allowed (or duplicate same units) | Proceed |
| 429 | over quota | Do not run billable work |
| 409 | requestId reused with different units | New requestId or fix units |
| 401 | bad/revoked key | Fail closed |

## Checklist when adding a product ID

- [ ] Append ID to `products` in `store.js`
- [ ] Extend tests for consume/entitlements
- [ ] Update control-plane README product list
- [ ] Document consume call site in the hosted service (not in bypassable local MVP unless hosted)

## Do not

- Send report bodies, source, or DB credentials to control-plane
- Implement refunds/Stripe in ad-hoc form without webhook verification
- Share SQLite over NFS or expose admin routes publicly
