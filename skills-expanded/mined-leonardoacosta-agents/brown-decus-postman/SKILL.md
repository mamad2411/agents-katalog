---
name: brown-decus-postman
description: |
  Test the Decus Postman collections against live APIM environments using Newman.
  Covers the two-surface model (Aggregates noauth, Cogitate key-gated), all three
  environments (dev/test/stage), collection generation from the APIM sync pipeline,
  the historical OneDrive transport, and the approved CPC scp replacement. Use when
  the user wants to run Postman tests for decus, smoketest the decus collections,
  check endpoint health for decus, sync collections from the Postman workspace, or
  debug a decus APIM surface through Newman.
---

# Brown Decus Postman Testing

Run Postman/Newman tests for the Decus (WHS-537) satellite APIM surfaces. There are
**two decus surfaces** split by auth model, each with its own collection and per-env
variable file.

## Two-surface model

| Surface | Env | Auth | Path prefix | Subscription key |
|---------|-----|------|-------------|-----------------|
| **Aggregates** | dev | noauth | `/aggregates/` | None (header ignored at APIM) |
| **Aggregates** | test | **key-gated** | `/aggregates/` | Required — `WWW-Authenticate: AzureApiManagementKey` returned (verified 2026-09-17) |
| **Aggregates** | stage | unverified | `/aggregates/` | Likely key-gated same as test |
| **Cogitate** | dev | key-gated | `/cogitate/`, `/decusdirect/` | Pre-filled in committed env file |
| **Cogitate** | test | key-gated | `/cogitate/`, `/decusdirect/` | Pre-filled in committed env file |
| **Cogitate** | stage | key-gated | `/cogitate/`, `/decusdirect/` | Not committed — use `.local.json` overlay |

Both surfaces route through `https://api.{env}.bridgespecialty.com` (Cloudflare-fronted).
The Aggregates surface strips the backend's leading `/api` segment; callers use `/aggregates/<route>`,
not `/aggregates/api/<route>`.

## Quick run

All collections and env files live in the `ws` repo at
`docs/reference/api-testing/postman/decus/`. Clone `ws` first if you do not have it.

```bash
# Aggregates surface - dev (no auth needed):
newman run docs/reference/api-testing/postman/decus/decus-aggregates.postman_collection.json \
  -e docs/reference/api-testing/postman/decus/decus-aggregates.env.dev.json

# Cogitate surface - dev (subscription key pre-filled in env file):
newman run docs/reference/api-testing/postman/decus/decus-cogitate.postman_collection.json \
  -e docs/reference/api-testing/postman/decus/decus-cogitate.env.dev.json

# Scoped to one folder:
newman run docs/reference/api-testing/postman/decus/decus-aggregates.postman_collection.json \
  -e docs/reference/api-testing/postman/decus/decus-aggregates.env.dev.json \
  --folder "GET /Filters"
```

Swap `dev` for `test` or `stage` in both the collection and env file paths (see
[Environment matrix](#environment-matrix)).

## Environment matrix

Each (surface, env) pair has two files: the base collection and the matching
env file. The env file sets `baseUrl` + (for Cogitate) `subscriptionKey`.

| Env | Aggregates env | Cogitate env | baseUrl |
|-----|---------------|--------------|---------|
| dev | `decus-aggregates.env.dev.json` | `decus-cogitate.env.dev.json` | `https://api.dev.bridgespecialty.com` |
| test | `decus-aggregates.env.test.json` | `decus-cogitate.env.test.json` | `https://api.test.bridgespecialty.com` |
| stage | `decus-aggregates.env.stage.json` | `decus-cogitate.env.stage.json` | `https://api.stage.bridgespecialty.com` |

**Production testing is gated.** There is no committed env file for `prod`.
Do not run Postman collections against prod without explicit authorization.

## Per-env v3 collections

The directory also contains per-env collection variants:

```
decus-aggregates-dev-v3.postman_collection.json
decus-aggregates-test-v3.postman_collection.json
decus-aggregates-stage-v3.postman_collection.json
decus-cogitate-dev-v3.postman_collection.json
decus-cogitate-test-v3.postman_collection.json
decus-cogitate-stage-v3.postman_collection.json
```

These are Postman v3 protocol collections generated from the Postman workspace.
The combined `*.postman_collection.json` files (without env in the name) are
the canonical source-of-truth copies from the APIM sync pipeline. Either works;
the v3 variants may carry richer examples.

## Key security rules

1. **Cogitate DEV keys are pre-filled** in the committed env files. Do NOT
   share the env files outside Brown & Brown — they carry live subscription keys.
2. **Stage/prod keys are never committed.** Use a gitignored
   `decus-cogitate.env.{env}.local.json` overlay and point Newman at the overlay.
3. **Never run against prod** without explicit operator authorization.

## Collection sources and transport

The Decus collections are maintained in Leo's Postman workspace, split from a
combined `decus.postman_collection.json` on 2026-07-16 via
`scripts/bin/split-decus-postman-collection`.

The collections were historically synced to `Postman Collections/decus/` in
Leo's personal OneDrive via a delegated Microsoft Graph token
(`scripts/bin/postman-onedrive-sync`, `systemd` timer every 15 min).
The historical reference is at
`docs/reference/identity/postman-onedrive-sync.md`.

**Current approved transport:** a pipeline-driven CPC `scp` transfer from the
DecusDirect APIM sync job, immediately after APIM publish. This is a tactical
replacement — it removes the personal `systemd` timer but does not settle the
final security/distribution model.

## Troubleshooting

### 401 / 403 Unauthorized
- **Aggregates dev:** should never 401. The surface is `subscriptionRequired:false`.
  A 401 means the backend itself is rejecting the request — check the backend
  health, not the collection.
- **Aggregates test/stage:** the test APIM returns `WWW-Authenticate:
  AzureApiManagementKey` (verified 2026-09-17). The test/stage Aggregates
  surfaces are actually key-gated despite `subscriptionRequired:false` in bicep —
  the APIM policy layer may differ per env. Add a `subscriptionKey` variable
  to the env file or a `.local.json` overlay.
- **Cogitate:** ensure the `subscriptionKey` value in the env file matches the
  current APIM subscription key. Pre-filled keys can drift. Check the KV store
  or APIM portal for the current key.

### 404 Not Found
- Verify `baseUrl` is set and the path matches the APIM API definition.
  Aggregates: `/aggregates/<route>` (no `/api` prefix). Cogitate: `/cogitate/<route>`
  or `/decusdirect/<route>`.

### Connection refused / timeout
- The Decus APIM is VNet-internal. Run Newman from a host with VNet
  connectivity (CPC, managed pool agent, or Tailscale-connected machine).
  The `ws` repo's `postman-smoke` wrapper handles this transparently.

## Reference

- [API Testing landing page](docs/reference/api-testing/postman/index.md) — Wholesale collection catalog
- [Migration Parity Validator](docs/reference/api-testing/postman/parity-validator.md) — Newman parity harness
- [Decus OneDrive sync history](docs/reference/identity/postman-onedrive-sync.md) — transport decisions
- [Bearer Token Broker](docs/reference/api-testing/postman/BEARER-BROKER-README.md) — delegated JWT auth for the one bearer-gated folder