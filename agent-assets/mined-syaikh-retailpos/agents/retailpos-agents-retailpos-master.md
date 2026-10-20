# Development Commands

## Codebase Investigation & Semantic Index

This project uses a semantic codebase index at `.opencode/index`, use semantic tools provided as much as possible. The current working tree is always the source of truth.

### Tool selection

| Tool | When to use |
|------|-------------|
| `codebase_context` | Default starting point for feature-level, architectural, or cross-module questions |
| `codebase_peek` | Conceptual area is known, but exact files/symbols are not |
| `implementation_lookup` | Symbol name is known, locate its authoritative definition |
| `codebase_search` | Need actual source content for known files/symbols/concepts |
| `semble.search` | Second opinion from the independent Semble index when `codebase_search` misses or returns doc-heavy noise; strongest on frontend/Svelte, where the Go-weighted index underperforms. Discards paths under `docs/`, `*.md`, and `database/migrations/` when judging whether a hit is real code. Reached inside `execute` as `tools.semble["search"]` |
| `call_graph` | Understand callers or callees of a known symbol |
| `call_graph_path` | Investigate end-to-end execution path between two points |
| `find_similar` | Before creating new implementation, check for existing patterns; matches against a pasted snippet |
| `semble.find_related` | Similarity from the Semble index, keyed off a `file:line` you already have — use when there is no snippet to match against, e.g. locating near-duplicates of a known implementation for the duplication review track. Inside `execute`: `tools.semble["find_related"]` |
| `code_communities` | Module boundaries, architecture, coupling, hub symbols |
| `codebase_edit_context` | Before modifying a known implementation, get bounded context |
| `architecture_context` | Repository-scale orientation first: module responsibilities, boundaries, and recent Git activity before focused retrieval or planning |
| `index_status` / `index_health_check` | Index readiness, provider/model compatibility, pending migrations, and stale-entry cleanup — check before diagnosing a miss as a stale index |
| `pr_impact` | Assess blast radius of a branch or planned change |

**Quick rules:** For known symbols, start with `implementation_lookup`. For exact text, use `grep`. For new features, add `find_similar` → `code_communities` before implementing. When a semantic search comes back thin, cross-check with `semble.search` before falling back to `grep`. When you have a location but no snippet, use `semble.find_related` instead of `find_similar`.

### Incremental indexing

- Prefer incremental indexing for small changes. Full re-index only when index is missing/corrupt, large portion changed, or major refactoring.
- Do not repeatedly re-index because a query returned no result — first consider whether the query is vague, wrong tool selected, or target outside index.
- **Never run `index_codebase` with `force=true`, or `/index force` (equivalent shorthand: `/reindex`), on your own initiative.** A full re-index is expensive and the user runs it themselves. If the index is stale or a symbol you just wrote is not found, say so and let the user re-index; fall back to `grep`/`Read` in the meantime rather than triggering a rebuild.
- Other plugin slash commands: `/status` (readiness/provider metadata), `/search`, `/peek`, `/find`, `/definition`, `/call-graph`, `/pr-impact`, `/visualize`.

### Known index limitations

- **A duplicated symbol name must be disambiguated by file.** `call_graph`, `call_graph_path`, and the `symbol`/`from`/`to` arguments of `codebase_context`/`codebase_edit_context` resolve Go **methods** by name (overloads included — `CreateSale` returns its `method_declaration` candidates), but a name found in several files comes back as `Ambiguous symbol`. Pass `filePath` / `fromFilePath` / `toFilePath`, or retrieve one overload with `implementation_lookup`/`codebase_peek` and enumerate callers with `grep -rn '<method>' internal`.
- **`pr_impact` diffs the branch against its base**, so it reports zero changed files for uncommitted work. Commit or stash first, or run it on a branch.

## Environment Configuration

All configuration variables and their defaults live in `.env.example` (and the code fallbacks in `internal/config` / `internal/middleware`). Copy `.env.example` to `.env` and adjust as needed. Non-obvious gotchas:

- `DATABASE_URL`, when set, replaces all `DB_*` parameters (`cmd/server/main.go:89`) and carries its own `sslmode`, so `DB_SSLMODE` is ignored. `DB_HOST` is only required when it is unset.
- **Required:** `JWT_SECRET` (256-bit, generate with `openssl rand -hex 32`) — the server panics at startup if missing. `JWT_SECRET_REFRESH` defaults to a derived value.
- `.env.example` deliberately ships looser login/refresh rate limiters (`60/60`, `120/120`) so E2E runs do not hit 429 — do not read those as the shipped defaults (`5/5`, `10/10`), and do not copy them to a deployment.
- `VITE_PRINT_AGENT_URL` is a build-time override naming **one** print agent for **every** register. **Leave unset for a multi-register shop** — each register must find the agent on its own PC (the frontend falls back to `http://localhost:9123`). Only set it for development (frontend and agent on different machines) or a kiosk with a server-hosted print agent. See `docs/guides/print-agent-production.md`.

## Timezone Handling

**All queries must use Asia/Jakarta timezone** (data stored in UTC, Jakarta midnight = UTC 07:00).

- Backend: `time.ParseInLocation("2006-01-02", dateStr, jakartaLoc)`
- Frontend: `getTodayInJakarta()` and `getDateNDaysAgoInJakarta()` utilities

## Analytical Data Consideration

Analytical queries are served from materialized views pre-aggregated in Jakarta time, refreshed via `refresh_sales_mv()`:
- `mv_hourly_sales` — period comparisons and hourly chart
- `mv_daily_sales` — daily chart, dual-period chart, available years
- `mv_dashboard_totals` — live dashboard stats

`report.RefreshCoordinator` (`internal/report/refresh_coordinator.go`) refreshes once at startup and then at each Jakarta hour (`:00`) boundary. The `sale.created` listener only invalidates dashboard caches and never triggers a refresh. Refresh failures are retried with exponential backoff (`REPORT_REFRESH_DEBOUNCE` is base retry delay).

**Only completed hours/days are displayed.** The in-progress hour is never surfaced, even if a mid-hour refresh wrote a partial bucket. This invariant is enforced in: `report.getRealtimeRanges`, `Repository.GetHourlySales`, and frontend `chart-config.ts` / `data-fetching.ts`.

## Git Commit Policy
Never auto-commit. User will request commits explicitly.

## Linting & CI (GitHub Actions)

New/edited code must pass all linters on the next CI run. Load the `lint-code` skill for backend (golangci-lint, go vet, gofmt -s) and frontend (ESLint, Prettier, svelte-check) rules, depguard import boundaries, and the verified Svelte 5 `$effect` bare-read fix patterns.

**All validation — formatting, linting, type-checking, testing, building, and security scanning — runs in GitHub CI** (`.github/workflows/ci.yml`, triggered on pushes to `main` and on pull requests). **Do not run these locally, and do not execute lint, type-check, build, or test commands without being asked** — if the user wants to verify something, provide the exact command and let them run it themselves. For rapid iteration during development, only run the specific package or file you are changing.

E2E tests run in a separate workflow (`.github/workflows/e2e.yml`) with sharded Playwright tests against a full stack (PostgreSQL, backend, frontend, print-agent).

### Security Toolchain

Beyond govulncheck and CodeQL, CI enforces first-party SAST and secret detection (design: `docs/adr/ADR_Security_Toolchain.md`):

- **gosec** runs inside golangci-lint (enabled in `.golangci.yaml`). New/edited Go code must be gosec-clean; `//nolint:gosec` requires an inline justification. Never "fix" a finding by excluding a path or downgrading the rule.
- **gitleaks** runs as the `Secrets: Gitleaks` CI job (full history, `fetch-depth: 0`) and as an optional pre-commit hook (`.pre-commit-config.yaml`; install with `pre-commit install`).
- **Fuzzing** runs in `.github/workflows/fuzz.yml` (`Fuzz (Scheduled)`) — weekly + `workflow_dispatch`, non-blocking, `-fuzztime 5m` **per target**. `scripts/list_fuzz_targets.py` discovers every `func Fuzz*` in the repo (including the second module under `tools/print-agent`) and the `discover` job fans out one parallel job per target, so adding a `Fuzz*` test to a parser/validator/calculation package needs no workflow edit. The run fails loudly when zero targets exist, so a broken discovery step cannot pass green.
  - A target must always be run with a matching `-run` filter: `go -C <module> test -run='^FuzzX$' -fuzz='^FuzzX$' -fuzztime 5m <pkg>`. Without `-run` the coordinator also executes the package's regular tests, which need the database the next bullet skips.
  - A fuzz worker and coordinator re-run `TestMain`, so a package with a database-backed `TestMain` must skip DB setup in fuzz mode via `shared.FuzzTestMode()` (`internal/shared/fuzz.go`) or workers contend on `RunMigrations`/`TruncateTestData` and die with "fuzzing process terminated ... EOF". Skipping the database also lets these targets fuzz in CI without a PostgreSQL service.
  - Keep fuzz targets panic-free rather than `t.Skip`-guarded: a `t.Skip` stops the fuzzing engine. Guard non-fuzzable inputs (NaN, out-of-range) with an early `return` and document why.

### E2E Testing Conventions (Playwright, `tests/e2e/`)

- **Behavior tests** (`*-api.spec.ts`) assert against API via `api-driver.ts`. **UI tests** (`*.spec.ts`) keep only genuine UI behavior (labels, navigation, validation messages).
- **`apiAs(request, role)`** returns authenticated `ApiDriver` for seeded roles (`superadmin`/`admin`/`manager`/`cashier`). Returns `ApiResult = { status, ok, body, headers }`.
- **Token rule (critical):** Do not reuse `request` fixture from `beforeAll` inside `test` bodies. Recreate `ApiDriver` per test via `beforeEach`.
- **Login rate-limited** (5/min per IP). Use `getToken(request, role)` / `apiAs` — tokens cached on disk in `fixtures.ts`. Bump `TOKEN_CACHE_VERSION` after backend restart with new `JWT_SECRET`.
- **Browser navigation:** Use explicit `page.goto(\`${FRONTEND_BASE}/...\`)`. Use `waitForAppReady(page)` (not `networkidle`).
- **POS/cart scenarios:** Use `pos-api.ts` helpers for shift/cart flows; raw `apiAs` for entity/CRUD specs.
- **Run from repo root** (`npx playwright test` / `npm run test:e2e`), never from `tests/e2e/`.

## Running Server

```bash
go run cmd/server/main.go
```

A local `.env` is loaded automatically (dev only; production is skipped). The
loader uses `godotenv.Load`, so variables already exported in the shell always
win and `.env` only fills gaps. No `set -a; source .env` needed.

Two consequences worth knowing:

- `ENV` is read from the process environment **before** `.env` is loaded, so
  putting `ENV=production` in `.env` will not disable the loader. Export it in
  the shell for that.
- Settings are cached on startup (`config.Load` is `sync.Once`-guarded), so
  editing `.env` requires a restart.

## Utilities

- `scripts/kill-port.sh <port>` — force-kill process holding a TCP port. Useful when `go run` child keeps port occupied (killing the parent `go run` PID does NOT free the port).
- `scripts/audit-store-fk-orphans.sh [--database NAME]` — read-only preflight for `059_store_fk_integrity.sql`; reports `store_id` orphans (exit 1 = blockers). Safe against production.

## Seeding Dummy Data

```bash
./seed-dev.sh [flags]
```

| Flag | Description |
|------|-------------|
| `-products=N` | Number of products (4500-5000, random if 0; if 0 and DB has products, reuses existing) |
| `-days=N` | Days to generate (0 = interactive prompt) |
| `-categories=N` | Number of categories (65-100, random if 0) |
| `-stores=N` | Number of stores to generate (random 20-40 if 0) |
| `-warehouses=N` | Warehouses per store (default 1) |
| `-storage-zones=N` | Storage zones per warehouse (default 4) |
| `-storage-racks=N` | Racks per storage zone (default 5) |
| `-stock-opnames=N` | Stock opname sessions to inject (0 = auto ~1/month) |
| `-suppliers=N` | Number of suppliers (random 10-15 if 0) |
| `-consignment=N` | Consignment suppliers (0 = auto, 10-20% of suppliers) |
| `-truncate=false` | Skip truncating existing data |

Re-seeding (`-truncate=false`) continues document sequences and reuses existing products/suppliers/pricing rules, adding new transactions without key collisions. The seeder preserves `must_change_password` on the six system accounts (the e2e workflow unflags its own test users instead).

`seed-dev.sh` is **not** a reset. It truncates 43 tables (`cmd/dummy/main.go`) but preserves `users` (ids, `store_id`, `must_change_password`) and never touches `roles`, `permissions`, `role_permissions`, or `app_settings`; `cart_sessions`, `cash_movements`, the four `import_*` tables, and `dead_letter_events` survive it entirely.

## Resetting the Dev Database to Fresh-Install State

```bash
./scripts/reset-dev-db.sh [flags]   # or: make db-fresh
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip the interactive `RESET` confirmation |
| `--keep-uploads` | Do not clear `uploads/logos/` |
| `--reseed` | Run `./seed-dev.sh` afterwards (**not** a fresh install — the seeder recreates `stores`/`payment_methods`/`customer_groups` with new ids, so `stores(id=1)` and `customers(id=1)` drift off the baseline invariant) |

Re-migrating cannot achieve this: `000_baseline.sql` is purely additive, so replaying it over a drifted database leaves every extra store, user, role, grant, and sale in place. The script drops and recreates the database and replays the migrations a fresh deployment would.

**Dev only.** The script hard-refuses (no override) on `ENV=production`, a non-`localhost` `DB_HOST`, a `DB_NAME` other than `retail_pos`, or a port served by a container other than `postgres-dev`. The container-identity check is skipped with a warning when `podman` is not on `PATH`; the other three guards still apply.

After a reset it prints the manual steps it cannot perform (restart the backend, clear browser site data, delete the Playwright token cache). Design rationale: `docs/design/dev-db-fresh-install-reset-plan.md`.

## Deployment

### Migration Ordering

Migrations must be applied **before** deploying a new server binary. Permission codes are seeded in dot notation by `000_baseline.sql`; there is no startup validation of codes — a mismatch surfaces as permission failures at request time, not at boot.

- Per-migration purpose: read the header comment of each `database/migrations/*.sql` file; design history is in `docs/design/squash-v1-baseline-plan.md`.
- **New migrations continue from the highest existing number (currently `066`, next `067_*.sql`).** Any new permission code and its grants must also be added to `000_baseline.sql` — it is the authoritative fresh-install seed, and `internal/permissions` baseline tests require every registered code to have a baseline row and grant.
- The 32 migrations squashed into the baseline (`000_squash.sql` + `001`–`007` + `031`–`053`) are preserved in `database/migrations/archive/pre-squash-migrations.tar.gz`.

`000_baseline.sql` is generated, not hand-written: it was produced from a `pg_dump` of a fully-migrated reference database and normalised so that it replays on an empty database, on a database that already went through the legacy chain, and on every re-run. Anything it does not cover (timestamps, random-salt credential hashes, materialised-view contents) is deliberately excluded rather than frozen into the file.

### Migration Replay Contract

All three non-test runners apply **every** file in `database/migrations/*.sql` (lexical order, `psql -v ON_ERROR_STOP=1`) on every run — no ledger check:

| Runner | Reads `schema_migrations` | Writes it |
|--------|---------------------------|-----------|
| `deploy/podman-deploy.sh:542-557` | no | yes, per file (`:555-556`) |
| `.github/workflows/ci.yml:375-393` | no | no |
| `.github/workflows/e2e.yml:62-66` | no | no |
| `internal/shared/testdb.go:46-117` | **yes** (`:64`, `:70-79`, `:92`) | yes (`:75`, `:112`) |

Consequences:

- **Every migration must be permanently re-runnable.** Use `IF NOT EXISTS` / `ON CONFLICT DO NOTHING` / `DROP … IF EXISTS`. One statement that fails on a second run aborts the loop.
- **`000_baseline.sql` self-registers as its last statement and deletes the rows of the 32 migrations it replaced.** The ledger therefore holds **one row per migration file**, not one row. The deletion is scoped to an explicit filename list, so migrations added later keep their own entries.
- **`testdb.go` is the one ledger-aware runner, and it short-circuits three ways.** It returns early when the row count already equals the file count (`:66`), and — critically — when the ledger is empty but the schema is *not*, it writes every filename and returns without applying anything (`:70-79`). That second path is why a migration file which only an already-migrated database needs (see `060`'s own header comment) cannot be exercised through `testdb.go` alone. Per file it skips anything already recorded (`:92`).
- **Never make a runner skip by filename.** The baseline is amended in place, so skipping would freeze old content in prod while CI/e2e (empty ledger) keep replaying — the two would diverge invisibly.
- **Guarded DDL skips silently when the object already exists.** `ADD COLUMN IF NOT EXISTS x INTEGER REFERENCES parent(id)` adds neither column nor FK if the column pre-exists.
- **`database/migrations/archive/001_create_tables.sql` is the only file containing `DROP TABLE … CASCADE`.** Never execute it (or any archived file) against an existing DB: dropping `products`/`stores`/`categories`/`users` cascades away inbound FKs on tables it does not recreate, and the guarded DDL that follows never restores them.

## Filesystem Convention

Non-code files follow this organization:

```
docs/
├── adr/          — Architecture/Business decision records
├── design/       — Technical design docs, specs, feature references
├── prd/          — Product requirement documents
├── guides/       — End-user documentation and manuals
├── reviews/      — Design/product reviews, feasibility analyses
├── reports/      — Implementation/status/progress summaries
├── roadmap/      — Upcoming features roadmap
├── audits/       — Security, architecture, UI/UX, RBAC audits
├── archive/      — Outdated implementation plans
├── archived-plans/ — AI agent planning documents
├── examples/     — Pre-filled import/export templates
└── exported-sample/ — Exported dashboard/report samples
```

- Root-level kept: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `LICENSE`
- SQL schema: `database/migrations/` (seed data consolidated into `000_baseline.sql`)
- `docs/docs.go`, `docs/swagger.*` — swag-generated OpenAPI artifacts (do not move)
