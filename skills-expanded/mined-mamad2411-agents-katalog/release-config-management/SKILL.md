---
name: release-config-management
description: Standardize release & configuration management across chains/environments: deployments/<chainId>.json, env/runtime secrets, ABI/schema versioning, idempotent migrations, and reproducible scripts. Use when touching deploy scripts, env vars, DB migrations, ABI/events, or production setup.
---

# Release & Config Management (Multi-chain + Multi-env)

## When to use
- Any PR touching:
  - deploy scripts or addresses
  - env vars or runtime config
  - ABI/events/schema
  - dbmate migrations / Kysely types
  - production or testnet rollout

## Goal (Definition of Done)
- ✅ Addresses are persisted per chainId in `deployments/<chainId>.json`.
- ✅ Env vars follow `.env.example` and secrets are never committed.
- ✅ DB migrations are idempotent and applied via dbmate.
- ✅ ABI/event schema changes are versioned and coordinated (contracts ↔ indexer ↔ app).
- ✅ Release has a clear “what changed” + upgrade/deploy steps.

## Canonical config layout
- `deployments/<chainId>.json` includes:
  - GAME_ADDRESS and dependencies
  - deploy blockNumber
  - git commit hash
  - timestamp
- `.env.example` contains keys only (no values).
- Runtime secrets are injected at runtime (not build time).

## ABI/schema versioning
On any event/ABI change:
1) regenerate ABI artifacts
2) update Ponder handlers
3) add DB migration (if schema changes)
4) update API/app types
5) replay/reorg sanity tests

## Database migrations (dbmate)
- Migrations must be:
  - forward-only and idempotent
  - reviewed for locks/index impact
- After migrations:
  - regenerate Kysely types (if used)

## Deployment checklist (minimum)
- Contract deploy succeeds in target chainId
- Explorer verification performed (recommended)
- Indexer points to correct RPC + GAME_ADDRESS
- App reads chainId + addresses correctly
- Smoke E2E passes (pay → commit → reveal → draw → claim)

## Anti-patterns (forbidden)
- ❌ Hardcoding addresses in frontend/backend.
- ❌ Committing `.env` or secrets.
- ❌ Changing ABI/events without updating indexer + schema.
- ❌ “Hotfixing” prod env without recording what changed.

## Testing checklist
- Local deploy + smoke (anvil)
- Fork tests for external integrations (when relevant)
- E2E (Playwright) for wallet → checkout → tx
