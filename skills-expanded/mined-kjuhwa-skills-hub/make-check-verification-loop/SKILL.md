---
name: make-check-verification-loop
description: Single make check command that runs typecheck + TS tests + Go tests + Playwright E2E for agents and CI, only starting services that aren't already running.
category: devops
version: 1.0.0
tags: [makefile, verification, ci, agent-workflow, playwright]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Monorepo with TS + Go + E2E verification needs.
- AI agents or CI workflows that need one command with a boolean verdict.

## Steps

1. Makefile target delegates to a shell script for complex logic:
   ```makefile
   check:
       $(REQUIRE_ENV)
       @ENV_FILE="$(ENV_FILE)" bash scripts/check.sh
   ```
2. `scripts/check.sh` stages:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   # Stage 1: TS typecheck (fastest, most common failure)
   pnpm typecheck

   # Stage 2: TS unit tests
   pnpm test

   # Stage 3: Go tests (requires DB)
   bash scripts/ensure-postgres.sh "$ENV_FILE"
   (cd server && go run ./cmd/migrate up)
   (cd server && go test ./...)

   # Stage 4: E2E (requires running services)
   if ! curl -sf "http://localhost:${PORT:-8080}/health" > /dev/null; then
       echo "==> Starting services for E2E..."
       trap 'kill 0' EXIT
       (cd server && go run ./cmd/server) &
       pnpm dev:web &
       # wait for health, then proceed
   fi
   pnpm exec playwright test
   ```
3. Each stage exits on failure — set -e short-circuits. Subsequent stages run only if previous pass.
4. Quick per-stage targets so agents can iterate narrowly:
   - `pnpm typecheck` — TS only
   - `pnpm test` — TS unit tests
   - `make test` — Go tests
   - `pnpm exec playwright test` — E2E

## Example

Agent workflow:
```
1. Write code
2. Run pnpm typecheck   (fast feedback for TS changes)
3. Iterate if needed
4. Run make check       (full verify)
5. Iterate if needed
6. Ready
```

## Caveats

- `make check` is slow (~1-2 min first time). Encourage narrow iteration with per-stage commands and keep `make check` for final verification.
- If services are already running, don't restart them — wastes time and disconnects active clients.
- Failures in E2E often indicate frontend + backend skew; don't fix by pinning versions, fix by running migrations first then E2E.
