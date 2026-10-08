# Stillhouse — Claude Code project notes

Open-source distillery management for Canadian craft distillers. See
[`README.md`](README.md) for the user-facing overview and the stages
table tracking what's shipped.

## Layout

```
proto/                 .proto source of truth (Buf)
backend/
  cmd/server/          binary entrypoint
  cmd/seed/            bootstrap tenant + admin
  cmd/mcp-token/       recovery-path API-token issuer (UI is preferred)
  internal/audit/      audit-log writer
  internal/auth/       Argon2id password hashing
  internal/config/     env config
  internal/db/         pgx pool, migrations, sqlc queries + generated
  internal/distilling/ mass → sugar → ethanol → LAA projection math
  internal/excise/     Canadian excise duty rates
  internal/genpb/      generated Go from .proto (do not hand-edit)
  internal/mcp/        Model Context Protocol server (mounted at /mcp)
  internal/rpc/        ConnectRPC service implementations
  internal/server/     HTTP server, session middleware, static embed
  internal/tenantdb/   WithTenantTx — opens a tx, sets RLS GUC
web/                   React + TS + Vite frontend; generated TS client in src/gen/
deploy/                Dockerfile + compose
```

## Build / test / lint

The Makefile works (stage 156 fixed the `SHELL` line that broke every
recipe needing a real shell). `make help` lists the targets. The direct
commands, for when you want one step rather than a target:

```sh
# Codegen
cd proto && buf generate --template buf.gen.yaml      # Go stubs
cd proto && buf generate --template buf.gen.web.yaml  # TS client
cd backend && sqlc generate                            # SQL → Go

# Backend
cd backend && go vet ./...
cd backend && go build ./...
cd backend && go test ./...

# DB-backed tests need one DSN — the superuser one. The pool the code
# under test runs through is derived from it with SET ROLE stillhouse_app
# (internal/testdb), so the tests exercise RLS the way production does.
#
# One run at a time: the suite owns the database while it runs. Two
# concurrent runs against one database collide and fail somewhere
# unrelated to the cause.
cd backend && STILLHOUSE_INTEGRATION_TEST_ADMIN_DSN=\
  "postgres://stillhouse:stillhouse@localhost:5432/stillhouse?sslmode=disable" \
  go test ./...

# Frontend
cd web && npm run lint
cd web && npm run build

# Dev DB (postgres in a container, bind-mounted to .data/postgres)
podman compose -f deploy/compose.yaml up -d postgres
migrate -path backend/internal/db/migrations \
  -database "postgres://stillhouse:stillhouse@localhost:5432/stillhouse?sslmode=disable" up
cd backend && DATABASE_URL=... go run ./cmd/seed

# Nuke + reset dev DB (compose down -v doesn't, bind mount survives)
podman compose -f deploy/compose.yaml down
podman unshare rm -rf .data/postgres
podman compose -f deploy/compose.yaml up -d postgres
```

## Container build + ship

Set your registry in a gitignored `local.mk` (`REGISTRY := ...`) rather
than editing the Makefile, then:

```sh
make image-push        # builds, tags short-SHA + :latest, pushes both
```

Or by hand:

```sh
SHA=$(git rev-parse --short HEAD)
podman build -f deploy/Dockerfile \
    -t $REGISTRY/stillhouse:$SHA \
    -t $REGISTRY/stillhouse:latest .
podman push $REGISTRY/stillhouse:$SHA
podman push $REGISTRY/stillhouse:latest
```

**Deployment is not automated.** Whoever runs the host pulls and restarts
themselves — ping them with the new tag and stop. Site-specific values
(registry hostname, LAN IP, data dir) are deliberately not in this repo.

## Conventions

- **Stage commits.** Every shipped feature is a single commit titled
  `stage N: <terse one-liner>`. Add a row to the README stages table
  in the same commit, and delete the item's line from `PLAN.md` if the
  stage closes one. Not every stage does — QA and review passes tend to
  fix things nobody had written down yet, and those get added to the
  README table without ever having had a plan line.
  Cross-reference related stages in the body (`see also stage 109`).
- **Web UI first.** Any operator-facing operation (token mgmt,
  invites, audit export, B266 generation, etc.) goes in the web UI,
  not a CLI. CLIs are reserved for bootstrap (`cmd/seed`,
  `cmd/server`), migrations, and recovery (`cmd/mcp-token`).
- **Canada-only framing.** LAA not proof gallons. B266 not 5110.40.
  Bulk / packaged not in-bond / tax-determined. Province-coded
  excise stamps as a first-class concept. Never reference TTB /
  DSP / 5110-series in shipped code, docs, or UI.
- **B266 scope.** B266 tracks alcohol (bulk + packaged + duty). Mash
  and fermentation are pre-alcohol — useful operational data, not
  on the B266 critical path.
- **Auth is dual-mode.** ConnectRPC interceptor accepts either an
  scs session cookie (browser) or `Authorization: Bearer sh_…`
  (MCP + scripts). Both resolve to a sqlcgen.User attached to the
  ctx via `rpc.WithUser`.
- **RLS enforcement.** Server runs as `stillhouse_app` (non-super).
  Migrations + seed run as `stillhouse` (super). `WithTenantTx` sets
  `app.current_tenant_id` before queries.
- **Proto generation drift.** Generated code in `internal/genpb/` and
  `web/src/gen/` is committed. After editing a `.proto`, regenerate
  both before committing. The Dockerfile regenerates the web client
  during the image build, so a generated-code drift between commit
  and Docker build will fail loudly.
- **Strength is a 20 °C quantity.** Never store or compare a strength
  without knowing its temperature. Gauging paths funnel through
  `rpc.resolveStrength`, which records whether a figure was determined
  from a hydrometer indication, corrected for volume only, or left
  uncorrected. **The tables are operator-supplied, never shipped** —
  Crown material, non-commercial reproduction only. The server reads
  whatever `STILLHOUSE_ALCOHOLOMETRIC_TABLES` points at (CRA ZIP, the
  ALC_TAB.TXT inside it, or a directory holding either) and degrades
  gracefully when it's absent: only the correction paths refuse, with
  `failed_precondition`. Tests need `ALC_TAB=/path/to/lc_tb.zip` and skip
  without it; the expected SHA-256 is pinned in the package test.
- **Cite the curriculum, or say you can't.** Domain constants in
  `internal/mashing` carry the CIBD passage they came from on the
  constant itself. Where the curriculum has no figure (oat
  gelatinisation, say), the code returns "unknown" and the UI says so —
  never interpolate a plausible-looking number into operator guidance.
- **Don't `gofmt -w` a whole directory.** Several files under
  `internal/rpc/` aren't gofmt-clean; formatting them sweeps unrelated
  churn into a stage commit. Format the specific files you edited.
- **Figures on the wire.** Every float leaving Stillhouse is stated to
  six decimal places by `internal/wire`, applied once at the boundary:
  a ConnectRPC interceptor for the API, and inside `jsonResult` /
  `jsonResultRaw` for MCP, which calls the service impls directly and so
  never sees an interceptor. Nothing stored or computed is rounded — six
  places is below anything a distillery measures and above every
  artefact of the arithmetic (QA finding F17, closed in stage 175). Do
  not add per-field rounding at conversion sites; that is the habit the
  one rule replaced. Display rounding — the coarser, domain-specific
  kind — still lives in `web/src/lib/format.ts`.

## MCP server

Stillhouse embeds an MCP server at `/mcp` (Streamable HTTP). Reuses
the same RPC service implementations as the web UI, so RLS, audit,
and role gating behave identically. See `backend/internal/mcp/` and
README's MCP section.

When `mcp__stillhouse__*` tools are loaded in a Claude Code session,
prefer them for QA + reads + supported writes. Tools intentionally
cover only the "operator with wet hands" surface; back-office writes
(production gauge, bottling, removal, B266 gen) stay in the web UI.

## QA pattern

Drive the live system end-to-end against real seeded data, not just
unit tests. Direct ConnectRPC via curl is in scope for seeding when
the MCP surface is too narrow. File findings as you go with severity
(P0–P3). Bundle fixes into a tight single-purpose stage. The bottling
LAA-conservation P0 (stage 109) was found this way — a unit test
wouldn't have surfaced it.

## What to read first

- `README.md` — user-facing overview + stages table
- `PLAN.md` — the open backlog, by track and severity. Items carry track
  IDs (`A1`, `D3`), not stage numbers; a stage number is assigned when the
  item ships, and its line in PLAN.md is deleted in the same commit.
- `proto/stillhouse/v1/*.proto` — the API surface, well-commented
- `backend/internal/rpc/bottling.go` (LAA conservation), `barrel.go`
  (maturation + regauge), `b266.go` (period generation) — the
  load-bearing math
- `backend/internal/alcoholometry/` — CRA Canadian Alcoholometric
  Tables 1980; every strength/volume lands at 20 °C through here
- `backend/internal/mashing/` — cereal gelatinisation, amylase windows,
  strike temperature, conversion efficiency (CIBD-sourced, cited inline)
- `backend/internal/distilling/` — projection math (whisky spine)
- `backend/internal/mcp/` — MCP tool registrations
- `web/src/pages/RecipeDetailPage.tsx` — the most feature-dense page
  (gin recipe development, sensory bench, version compare)
