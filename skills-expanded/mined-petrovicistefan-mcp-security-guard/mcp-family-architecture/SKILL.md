---
name: mcp-family-architecture
description: Explains MCP product-family architecture, control-plane vs local tools, security-guard cloud/Team vs control-plane quotas, and product IDs. Use when planning features, billing, hosted paths, or how products relate.
---

# MCP Family Architecture

## Layout & maturity

```
mcp-control-plane     → HTTP accounts/keys/quotas (MVP management API)
mcp-security-guard    → SHIPPED reference: plugin + CLI + GH Action + opt-in cloud/Team
mcp-dependency-doctor → local MVP
mcp-api-guardian      → local MVP
mcp-database-doctor   → local MVP
mcp-cost-optimizer    → local MVP
mcp-seo-auditor       → local MVP
```

Control-plane IDs (`mcp-control-plane/src/store.js`):  
`security-guard` · `dependency-doctor` · `api-guardian` · `database-doctor` · `cost-optimizer` · `seo-auditor`

## Two paid/hosted tracks (do not mix casually)

### A. security-guard cloud (live, product-specific)

- Endpoint default: `https://mcp-security-cloud.petrovicistefan.workers.dev` (override `MCP_SECURITY_API_URL`)
- Key: `MCP_SECURITY_API_KEY` or plugin secure `userConfig` (empty default for Cowork)
- **Threat feed:** `POST /v1/check` — package names/versions + SHA-256 tool/context hashes (+ plugin name/version). Never definitions/paths/secrets. **Fail open.**
- **Team:** org policy sync, fleet inventory (names/versions only, admin gate + consent), approvals, keys/seats, dashboard, email/Slack alerts. Admin mutations are **CLI only**, not MCP tools.
- Free local audit remains complete without any key.

### B. control-plane (family MVP)

- Accounts, hashed API keys (`mcp_…`), entitlements, monthly per-product quotas
- Trusted hosted caller: `GET /v1/entitlements`, `POST /v1/usage/consume`
- Idempotent `requestId`; `429` = no charge; `409` = unit conflict
- Not yet the live security-guard Team/feed backend

## Decision tree

1. Change local free auditing/analysis? → Product repo; keep useful offline.
2. security-guard Team / threat feed / privacy of payloads? → `mcp-security-guard` (`cloud.ts`, `team.ts`, PRIVACY.md).
3. Cross-product account quota API? → `mcp-control-plane`.
4. Unify billing later? → Explicit migration plan; do not silently point security-guard at control-plane consume.

## Anti-patterns

- Treating security-guard like an unpublished 0.1.0 zero-dep MVP
- Locking free local features behind a key
- Sending rich inventory (paths, env, tool text) to cloud
- Exposing Team admin approve/revoke as MCP tools
- Claiming unpaid README prices as live offers for MVP siblings
