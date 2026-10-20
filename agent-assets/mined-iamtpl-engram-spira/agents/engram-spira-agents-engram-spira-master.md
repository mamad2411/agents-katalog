# AGENTS.md — engram-spira

Canonical agent instructions for this repository. Tool-agnostic; `CLAUDE.md` imports this file.

**Engram Spira** is an AI-powered spaced-repetition flashcard app: Bun workspaces monorepo, ElysiaJS + Drizzle + Postgres/pgvector API, SolidJS + Vite SPA, Google Gemini for card generation and embeddings.

---

## 0. Performance first

Performance is the product's competitive edge and a hard requirement for every change, not a polish step. Before you claim done, you must be able to say how many SQL statements and HTTP round trips your change adds or removes, and every new query must be proven by an `EXPLAIN` test to use an index. Rules, budgets and the measurement recipe live in [docs/agents/performance.md](docs/agents/performance.md); the non-negotiables are:

- One set-based SQL statement per aggregate. No query in a loop. Every list has a `LIMIT`.
- Every new `WHERE` / `JOIN` / `ORDER BY` column is backed by an index and covered by an `EXPLAIN` test under a forced plan.
- Retention is computed only by `fsrs_retrievability()` in SQL, never per card in JavaScript.
- Frontend: parallel queries, prefetch on intent, optimistic `setQueryData` instead of broad `invalidateQueries`, deliberate `staleTime`.
- A PR that touches a query carries its `EXPLAIN (ANALYZE, BUFFERS)` before/after.

## 1. Never trust the prose — verify the number

`README.md`, `docs/srs/`, `docs/project_report.md`, `docs/ui/design.md`, `docs/c4/`, `docs/erd/` and every file in `docs/dev_prompt/` were last updated 2026-03-21 or earlier and are **stale by 20+ commits**. They disagree with the code on module counts, table counts, test counts, Gemini model names, ports, algorithm constants and feature availability. Never cite a count from them. Re-derive it:

| Fact | Command | Truth today |
|---|---|---|
| API modules | `ls -d apps/api/src/modules/*/ \| wc -l` | **16** |
| Postgres tables | `grep -rho 'pgTable(' apps/api/src/db/schema/ \| wc -l` | **26** |
| HTTP routes | `grep -rhE '^\s*\.(get\|post\|put\|patch\|delete)\(' apps/api/src/modules/*/*.routes.ts \| wc -l` | **100** + `GET /health` = **101** |
| SQL migrations | `ls apps/api/src/db/migrations/*.sql \| wc -l` | **30** (`0000`–`0029`) |
| API tests | `cd apps/api && bun test` | **703** in 78 files — all pass |
| Web tests | `cd apps/web && bun test` | **104** in 18 files, all pass |
| Web routes | `apps/web/src/app.tsx` | **13** `<Route>` |

Re-measured 2026-09-09. The table drifts fast, in both directions — the FSRS-only migration *removed* 4 tables and 3 routes and cut ~57 tests (SM-2, replay tooling and the legacy retention estimators are gone) two commits after a 12-table jump added them. Re-derive before trusting any of these, including this row.

Toolchain: Bun 1.3.10, TypeScript 5.9.3, Node 22.22.2. Ports: API 3001, Vite dev 3002, Vite preview 4173, Postgres **5435** (host) → 5432 (container), Structurizr 8080.

## 2. The red baseline — do not mistake it for your regression

Capture this before you change anything so you can prove you did not add to it. As of 2026-09-09 the baseline is **fully green** — the name stays as a reminder that it has flipped red → green → red before and will again.

- **`bun run typecheck` PASSES (exit 0).** Both `@engram/api` and `@engram/web` are clean. **CI is green.** The 22-error Eden Treaty path-inference collapse this section used to describe (blamed on untyped handlers in `experience.routes.ts`) no longer reproduces — that file has since been refactored to an injectable-services pattern. Re-verify with `bun run typecheck` before trusting this.
- **0 API tests fail**, of 703 across 78 files. Three long-standing failures were fixed on 2026-09-08 and must not come back: the `experience` fixture time bomb (`__tests__/helpers/fixtures.ts` now derives `now/past/future` from `Date.now()`), two `fsrs-live.postgres.test.ts` cases that seeded parameter revisions with a baked `retired_at` older than the column-default `created_at` (violating `chk_fsrs_parameter_revisions_timestamps` once the real clock passed the baked date — they now pin `created_at`/`activated_at` explicitly), and the `fsrs-only.migration.test.ts` FK-index introspection query's ambiguous `table_name` (rewritten against `pg_catalog`). The previously-documented `config-ai.test.ts` mock-leak from `kg.service.test.ts` is also gone.
- **The Postgres-backed suites need the dev database up** (`docker compose up -d`): `fsrs-*.postgres.test.ts` each create and drop a disposable database via `TEST_POSTGRES_ADMIN_URL` (default `postgresql://postgres:postgrespassword@localhost:5435/postgres`). Without it they fail with connection errors that are not a regression.

See [docs/agents/known-issues.md](docs/agents/known-issues.md) for the full list and which are safe to fix.

## 3. Non-negotiable rules

Violating any of these breaks the build, the types, the database, reactivity, or auth scoping.

**Errors & responses**

1. Throw an `AppError` subclass from `apps/api/src/shared/errors.ts`; never `set.status` for a failure and never return an `{ error }` object from a service. The single `onError` in `apps/api/src/index.ts:145` is the only place module code produces error status codes — the sole exceptions are `/health`'s own `503` (`index.ts:179`) and the five `elysia-rate-limit` plugins, which return a hand-built 429 `Response`. Available: `UnauthorizedError` 401, `ForbiddenError` 403, `NotFoundError` 404, `ConflictError` 409, `PayloadTooLargeError` 413, `ValidationError` 422, `TooManyRequestsError` 429. No subclass produces 400.
2. Every error body stays exactly `{ error: string }`. `getApiError()` in `apps/web/src/api/client.ts` depends on that single-key shape.
3. `new NotFoundError('Deck')` takes a resource **noun** — the class appends `" not found"`.

**Auth & authorization**

4. Authorize inside the **service**, never the route: take `userId` as an explicit parameter and scope every query by it. Decks/cards use the denormalized `decks.user_id`; folders/classes traverse `folders.class_id → classes.user_id`.
5. For anything the caller does not own, throw `NotFoundError('<Resource>')` — never `ForbiddenError`, never 403, never an empty result. Existence must not leak.
6. `.use(requireAuth)` position is load-bearing: the derive is `{ as: 'scoped' }`, so **only routes chained after it are authenticated**. Adding a route above that line in `auth.routes.ts:148` or `users.routes.ts:21` silently ships an unauthenticated endpoint. `.guard()` is never used in this codebase.

**Database**

7. Never add `card_field_values.embedding` (or any vector column) to the Drizzle schema and never write vectors through Drizzle. Use raw `pgClient` tagged templates for writes and ``db.execute(sql`…`)`` for reads. Build literals from `number[]` as ``[${vec.join(',')}]``, bind them, cast `::vector`, and keep the dimension at exactly **768**.
8. Before `db:generate` / `db:push`: drizzle-kit's baseline is snapshot **0017** (16 tables, pre-FSRS). Generated SQL will duplicate `fsrs_user_params` / `dismissed_suggestions` / `users.email_*` / the `study_progress` FSRS columns, and re-emit `DROP INDEX "idx_sdl_user_date"` — without `IF EXISTS`, so it errors against an already-migrated database. Read and prune every generated statement by hand. **`db:push` is the dangerous one**: it diffs the *live* DB, so it also proposes dropping `card_field_values.embedding` and its HNSW index, and it never creates the `vector` extension or the 3 partial indexes. (`db:generate` does *not* touch `embedding` — snapshot 0017 predates that column, so drizzle-kit is blind to it.) Migration `0029` **dropped** `study_progress`, `review_logs`, `fsrs_user_params` and `fsrs_migration_runs` plus `users.srs_algorithm` — do not go hunting for them, and note that the 0017 baseline predates all four, so drizzle-kit will happily re-create them if you do not prune its output.
9. `db:reset` is **not** a database reset: `drizzle-kit drop` interactively deletes a migration *file* + its snapshot + its journal entry. Never run `db:push`/`db:reset` against data you care about. `db:migrate` is the default.
10. A new table goes in its own file under `apps/api/src/db/schema/` and **must** export both the table and its `<name>Relations` from `schema/index.ts` — `drizzle.config.ts` reads only that barrel, so an unexported table is invisible to drizzle-kit and gets dropped by push.
11. Hand-written migrations are named `NNNN_snake_case_purpose.sql` with a `_journal.json` entry whose `when` is **strictly greater** than the previous entry's. Migration `0015` violates this and is permanently skipped. Make every statement idempotent; never `CREATE INDEX CONCURRENTLY` (the whole batch runs in one transaction).

**Study / SRS**

12. Route **every** review through `fsrsLiveService.reviewBatch` (`study.service.ts:16`, built over `fsrs-live.postgres.ts`). Never write `fsrs_card_states` / `fsrs_review_events` directly: the repository does the whole batch in **one serializable transaction** with `FOR UPDATE` locks, per-`requestId` idempotency, the `study_daily_logs` roll-up and a retry on serialization failure. There is **no SM-2 and no `users.srs_algorithm`** — no algorithm dispatch, no per-user params table; parameters live in `fsrs_parameter_revisions` and rotate through `fsrsLiveService.rotateParameters`. Scheduling policy on top of ts-fsrs: intervals are hard-capped at `FSRS_MAX_INTERVAL_DAYS = 365` (`fsrs.engine.ts`; a tail-risk guard — it does not shorten sub-year intervals), client `reviewedAt` is **never** a reason to reject a grade (trusted only within 24 h before `receivedAt`, otherwise replaced by `receivedAt`, then clamped up to `card.last_reviewed_at`), `study_daily_logs` follow the server's `receivedAt`, and `learnedCards` means review state with stability ≥ 21 days. The `/study` rate limit is per **user**, not per IP (`study-rate-limit.ts`). On the web, every grade goes through `createReviewOutbox` (`study-review-outbox.ts`) and the in-session queue is refetched only via `refetchQueue()` (`study-mode.tsx`), which hides the card UI, awaits `settle()`, then rewinds.
13. Never compute a day boundary from a bare `new Date()` in a service. Read the offset once via `getTimezoneOffsetMinutes(headers)` in the routes file and pass it as a trailing `tzOffset = 0` parameter. The API process must run with `TZ=UTC`.

**Config**

14. Read config only through `ENV` (`apps/api/src/config/env.ts`). Adding a variable means **four** edits: `env.ts` (with an inline default), `apps/api/.env.example`, and **both** ENV mock blocks in `apps/api/__tests__/preload.ts`. Only `DATABASE_URL` is in `REQUIRED_VARS`. Frontend config is separate: `VITE_API_URL`.
15. Any custom request header a route reads must be added to `allowedHeaders` in the `cors()` call at `apps/api/src/index.ts:135` (currently `Content-Type`, `Authorization`, `x-timezone-offset`) or the browser preflight rejects it.
16. `.unref()` every `setInterval` in a long-lived module (see `index.ts:285,302`).

**Frontend (SolidJS)**

17. **Never destructure or alias props.** Type as `Component<Props>` and read `props.x`, or peel keys with `splitProps` when spreading. Zero files in `apps/web` destructure props today.
18. No React idioms: no `useState`/`useEffect`/`useMemo`/`useRef`, no `className`, no `htmlFor`, no `onChange` for text input (use `onInput`), no `key` prop, no early `return` to change rendering. Use `class`, `for`, `<Show>`/`<For>` (`<Index>` only for focus-stable inputs), and pair every listener/timer/observer with `onCleanup`.
19. Any reactive primitive created at **module scope** must be wrapped in `createRoot` (see `theme.store.ts:43`). A bare `createSignal` is fine; `createEffect`/`createQuery` is not.
20. Build new shell surfaces in `apps/web/src/components/app-shell/` — `app.tsx:69` renders it via `protect()`. `components/layout/{header,sidebar,mobile-nav}.tsx` and `layout/sidebar/*` have **zero importers** and must not gain features. Only `layout/page-shell.tsx` is live.
21. Style with Tailwind utilities and the semantic tokens in `apps/web/src/app.css` `@theme`. Never hardcode hex in a component; add a token plus its `.dark` override. There is no `tailwind.config.*` — `app.css` is the entire config and the only source of truth for design tokens (`docs/ui/design.md` is superseded).

**Cross-boundary coupling**

22. `apps/web/src/api/client.ts:2` imports `App` from `../../../api/src/index` and `apps/web/src/lib/experience-api.ts` imports `experience.types.ts` by relative path. Do not move/rename `apps/api/src/index.ts`, do not delete `export type App`, and do not move `experience.types.ts` — each breaks the web typecheck with no API-side error.
23. `.gitignore` ignores exactly `/skills` (root-anchored — the vendored `ui-ux-pro-max` clone). `docs/superpowers/` is **tracked** since 2026-09-08: design specs go in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and implementation plans in `docs/superpowers/plans/`. **`.agents/skills/` is intentionally trackable**: that is where project skill packs (`elysiajs`, `solid-js-best-practices`) live, versioned via `scripts/skills-update.ts` / `skills-lock.json` — run `bun run skills:update` after adding or editing one. Do not widen `/skills` back into a bare `skills` pattern; that previously hid `.agents/skills/` too (see git history). Confirm any new path with `git check-ignore -v <path>` before writing a doc.

**Raw SQL through `pgClient`**

27. `db/index.ts` hands the **same** postgres.js client to `drizzle()`, and the drizzle driver mutates it: timestamp/date parsers **and** serializers, plus the `json`/`jsonb` serializers, become identity functions. So through `pgClient` (tagged template or `.unsafe()`): a bound `Date` throws `Received an instance of Date`, a bound object for `$n::jsonb` throws `Received an instance of Object`, and `timestamptz` columns come back as **text**, not `Date`. Tests that open their own `postgres()` client see none of this, which is how it reached production. Use `apps/api/src/db/pg-codecs.ts`: `bindTimestamp(date)` for `$n::timestamptz`, `bindJson(value)` with the placeholder cast **`$n::text::jsonb`** (a bare `::jsonb` corrupts the value on a pristine client), and `timestampFromRow(row.x, name)` before treating a column as a `Date`. Any new `*.postgres.test.ts` must also exercise the repository through a client wrapped with `drizzle()` — see `drizzleWrappedSql` in `fsrs-deck-reads.postgres.test.ts`. For canonical FSRS reads, compose the shared fragment vocabulary in `apps/api/src/modules/study/fsrs-sql.ts` (`fsrsStateJoin`, `fsrsDue`, `fsrsAtRisk`, `fsrsRetrievability`, `fsrsAsOf`) instead of re-spelling the join, and expose each statement as an exported `*Sql()` builder returning `SQL` so tests can execute and `EXPLAIN` it — see [docs/agents/performance.md](docs/agents/performance.md).

**Testing**

24. Run API tests **only** from `apps/api` (`cd apps/api && bun test`). `bunfig.toml`'s preload is CWD-relative; a root run silently drops 15 tests with `Missing required environment variable: DATABASE_URL`. Web tests: `cd apps/web && bun test` — no `test` script exists in `apps/web`.
25. Put every `mock.module` at file top **before** the subject import. Never `mock.module` a shared app module (`src/config/ai`, `src/db`) — Bun's registry is process-global and this already breaks `config-ai.test.ts`. Prefer the injectable-loaders pattern the `experience` module uses over the DB mock for new code.
26. Never bake an absolute date into a fixture whose past/future-ness matters — derive from `Date.now()`.

## 4. Before you claim done

Run all three and compare against the §2 baseline. CI runs **only** `bun run typecheck` — no tests, no lint, no build, no migrations.

```bash
bun run typecheck          # expect: exit 0
cd apps/api && bun test    # expect: 703 pass / 0 fail (dev Postgres up)
cd apps/web && bun test    # expect: 104 pass
```

Both tsconfigs typecheck their test files, so a type error in a test breaks CI.

There is **no linter, formatter, or git hook** in this repo. Match surrounding style by eye: 2-space indent, single quotes, semicolons, trailing commas in multiline literals. Do not add eslint/prettier/biome as a drive-by change.

## 5. Local setup

```bash
bun install
docker compose up -d                      # starts ONLY `db` (structurizr is behind --profile docs)
cp apps/api/.env.example apps/api/.env    # then fix GEMINI_EMBEDDING_MODEL — see below
bun run db:migrate && bun run db:seed
bun run dev                               # api :3001, web :3002, + browser-extension watcher
```

Seeded login: `test@example.com` / `password123`. `apps/api/.env.example:17` sets `GEMINI_EMBEDDING_MODEL=gemini-embedding-2-preview`, but the code default is **`gemini-embedding-001`** — copying the example silently switches models. `DATABASE_URL` is validated for *presence* only, so the API boots against a dead database and then floods `CONNECT_TIMEOUT localhost:5435`.

## 6. Where to read next

Load only what your task touches. Each file is self-contained.

| Task | File |
|---|---|
| Performance rules, budgets, EXPLAIN gate | [docs/agents/performance.md](docs/agents/performance.md) |
| Orientation, monorepo map, request lifecycle | [docs/agents/orientation.md](docs/agents/orientation.md) |
| Adding/changing an API module, error & auth contracts | [docs/agents/api-conventions.md](docs/agents/api-conventions.md) |
| Finding an endpoint's exact shape | [docs/agents/endpoints.md](docs/agents/endpoints.md) |
| Schema, migrations, pgvector | [docs/agents/database.md](docs/agents/database.md) |
| FSRS scheduling, review, streaks, retention | [docs/agents/srs-study.md](docs/agents/srs-study.md) |
| Gemini generation, embeddings, search, knowledge graph | [docs/agents/ai-search.md](docs/agents/ai-search.md) |
| Command-center aggregate (BFF) layer | [docs/agents/experience-bff.md](docs/agents/experience-bff.md) |
| SolidJS, app shell, stores, design tokens | [docs/agents/frontend.md](docs/agents/frontend.md) |
| Writing tests, mocking strategy | [docs/agents/testing.md](docs/agents/testing.md) |
| Scripts, CI, env vars, docs pipeline | [docs/agents/tooling-ci.md](docs/agents/tooling-ci.md) |
| Known defects, red baseline, dead code | [docs/agents/known-issues.md](docs/agents/known-issues.md) |

Index and stale-doc blacklist: [docs/agents/README.md](docs/agents/README.md).
