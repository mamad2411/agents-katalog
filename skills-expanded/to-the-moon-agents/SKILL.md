# sysdesign: Agent Instructions

> `CLAUDE.md` and `GEMINI.md` are symlinks to this file.

One repo for the whole system-design build guide, a scaled-down influencer-intelligence
pipeline (Defrag's creator watchlist) built up in modules. Personal interview-prep learning
code, internal, never client-facing.

The modules are cumulative layers of a single app, not separate apps, so they live
in one repo that accumulates. Each finished module gets a git tag (`module-1`,
`module-2`, ...) so any milestone is one `git checkout` away.

- **Module 1, data model.** Partitioned Postgres schema, per-partition indexes, a
  read-path materialized view, EXPLAIN drills, and the FastAPI surface over it.
- **Module 2, Celery fan-out.** `POST /runs` fans out one Celery task per influencer (a
  chord), each writing signals through the same `common.signals.insert_signal` upsert the API
  uses, bumping the `runs` row's `done_count`, and publishing a progress delta to a Redis
  channel. The frontend streams progress over **Server-Sent Events** (`GET /runs/{id}/stream`,
  `sse-starlette`), not polling: the endpoint reads the `runs` snapshot from Postgres on
  connect (so a page refresh re-establishes state) then subscribes to Redis for live deltas.
  The chord's fan-in callback runs `REFRESH MATERIALIZED VIEW CONCURRENTLY daily_signal_rollup`
  so the rollup reflects each run the moment it finishes, with a Celery-beat task (every 5 min)
  as a staleness backstop. This is why Module 1 built the matview with a unique index on
  `(influencer_id, day)`, that index is what lets `CONCURRENTLY` refresh without locking
  dashboard readers. Runs have a `demo` mode (synthetic signals, no Apify spend) for watching
  the fan-out and SSE stream cheaply, and a `live` mode (real Apify scrape). The worker lives in
  `services/worker/` (`celery_app.py`, `tasks.py`, `scrape.py`); run it with `moon run worker:dev`.
  Full first-principles walkthrough (Redis's two hats, chord = distributed Promise.all,
  snapshot-then-deltas SSE, debugging with `--pool solo`) in [docs/module-2.md](docs/module-2.md).
- **Module 3, deploy (SHIPPED).** Railway for the API + worker + Redis (next to the
  existing shared AI service), Postgres on Railway with pgvector enabled (it lived on
  Supabase until 2026-09-12; see infra/README.md). Live at
  sysdesign.thedefrag.ai; the infra contract, gotchas, and migration story are in
  [infra/README.md](infra/README.md). Migrations run automatically as the api's
  `preDeployCommand` (a deploy can't ship code ahead of its schema). A planned piece,
  moving the beat backstop to a serverless scheduled function to learn the serverless
  constraints (stateless, wall-clock limits, chunked work re-entered via a durable run
  row), is DEFERRED. It was scoped as a Supabase Edge Function on pg_cron, which no longer
  applies now that Postgres is on Railway; the replacement is likely a Railway cron
  service or a Vercel cron route. The lesson stands either way,
  long unreliable work stays on the queue-backed worker, short scheduled work goes
  serverless.
- **Module 4, AI rating layer (BUILT, semantic cache BUILT in Module 6).** An LLM lands in the write
  path as a new pipeline stage, not a longer task. Each scrape task already knows which
  signals it newly inserted (`insert_signal` returns `inserted`), so it enqueues one
  `rate_signal` Celery job per new row and finishes; ratings drain through the same worker
  pool with their own retries (backoff on `RatingError`), and a slow model call never blocks
  a scrape. The rating is a single structured-output call (relevance to Defrag's AI-research
  thesis, topics, summary, confidence) written idempotently to `signal_ratings` keyed on the
  signal's `content_hash`, deduping on the INPUT hash rather than the model's answer because
  the model is non-deterministic. A beat sweep for unrated signals is the backstop, same
  pattern as the matview refresh; it only sweeps `source = 'instagram'` rows, so the 4000
  seeded drill signals never turn into a surprise model bill. The model call goes through one
  provider-agnostic adapter, `packages/core/common/rating.py`, speaking the OpenAI-compatible chat
  completions shape over raw urllib (a wire format every serving stack clones, the way S3's
  API got cloned by R2 and MinIO), so local dev rates through Ollama in the devcontainer
  (free, offline; `moon run root:ollama-pull` once, then `RATING_MODEL=ollama/llama3.2:1b` is already
  in the compose env; the model must be small and non-thinking, qwen3:4b's <think> preambles
  blow the adapter's 180s timeout on container CPU) and prod rents a hosted model (DeepSeek, a Groq free-tier Llama, Haiku).
  Which model rates a run is data, not deployment config. `POST /runs` takes an optional
  `model` ("provider/model", validated at the door with a 400 via `resolve_model`), the run
  row carries it, and the rating tasks read it; env vars hold only the `RATING_MODEL`
  default and the credentials, secrets never ride in request bodies. With neither set the
  whole layer is inert, which is prod's state until a provider key lands in
  `infra/railway-env.py`. Ratings read back over `GET /ratings` (newest first, optional
  `min_relevance`), which is the surface the Module 5 digest agent will consume. The
  pgvector semantic cache from the original sketch is now built (in Module 6, since it reuses
  that module's embedding pipeline), before paying for a rating call `rate_signal` embeds the
  caption and copies the nearest already-rated neighbor's rating when it's within
  `RATING_CACHE_MAX_DISTANCE` (0.05 cosine, near-duplicate content), tagging the copy
  `cache:<model>`; the layer degrades to a normal model call when no embedding provider is
  configured or the lookup misses. The design rule, **own the
  interface, rent the model**. Self-host where compute is free (your laptop), rent where
  compute is metered (the cloud), and make the code indifferent to which one it's talking
  to. The AWS rebuild that once held this module number was cut to a read-only talk track
  (parent package, `notes/aws-talk-track.md`); the concepts were already built here in
  Celery and the vocabulary mapping is readable. The high-level mental model behind all of
  it (weights, training vs inference, the token loop, memory bandwidth vs compute, CPU vs
  GPU, quantization) lives in [docs/llm-foundations.md](docs/llm-foundations.md).
- **Module 5, Managed Agent capstone.** A scheduled Anthropic Managed Agent (the digest
  bot) runs the daily sweep, pulls the week's rated signals through the deployed API (the
  sandbox reaches Railway over HTTP; start with bash + the OpenAPI spec, graduate to an MCP
  wrapper), clusters themes, compares against last week via a Memory Store mounted at
  `/mnt/memory/`, and writes `digests` rows. Pipeline for volume, agent for judgment; the
  per-signal ratings from Module 4 are what the agent reasons over, and the API is its tool
  surface. Requires the Module 3 deploy, already live (the sandbox can't reach localhost).
  Full control-flow walkthrough (the three channels, vaulted sandbox curl, the fragile
  worker-side custom tool vs the MCP+deployment target, and the Messages-API-to-Managed-
  Agents layer cake, with ASCII diagrams of both the current and target flows) in
  [docs/module-5.md](docs/module-5.md).
- **Module 6, hybrid search (BUILT).** pgvector HNSW + Postgres full-text + Reciprocal Rank
  Fusion over signal content. Two retrieval halves run in parallel, a lexical half (a
  generated `caption_tsv` column with a GIN inverted index, `websearch_to_tsquery` +
  `ts_rank_cd` cover-density ranking) and a semantic half (a `signal_embeddings` table,
  `vector(1536)` behind an HNSW index, cosine `<=>` KNN). RRF fuses the two ranked lists by
  ordinal rank alone (`sum 1/(k+rank)`, k=60), so no score normalization is needed across the
  incomparable `ts_rank` and cosine scales, and a doc both halves surface outranks one either
  found alone. Surfaces as `GET /search?q=` and the `search_signals` MCP tool the digest agent
  can call, both sharing `packages/core/common/search.py` so they can't drift. The whole semantic half is
  inert until keyed, with `EMBEDDING_MODEL` unset, search degrades to lexical-only and says so
  (`"semantic": false`), so it works offline with no provider. The embedding pipeline is its
  own decoupled Celery stage (`embed_signal` + a `sweep_unembedded` beat backstop) mirroring
  Module 4's rating stage, and its embeddings double as the Module 4 semantic-cache key, one
  `signal_embeddings` table, two features. The provider adapter (`packages/core/common/embedding.py`) is the
  same **own the interface, rent the model** urllib shim as the rating adapter, speaking the
  OpenAI-compatible `/v1/embeddings` shape. Full first-principles walkthrough (tsvector/GIN,
  the generated-column immutability trap, HNSW approximate-vs-exact, why RRF fuses by rank, the
  shared-table cache, EXPLAIN drills, interview soundbites) in [docs/module-6.md](docs/module-6.md).
  The same embeddings also power a discovery-side reuse (`packages/core/common/clusters.py`), `get_signal_clusters`
  groups the week's rated posts into emergent themes by cosine proximity (greedy threshold, exact
  distances, a pure testable core like RRF) so the Module 5 digest agent reasons over ~15 themes
  instead of hundreds of raw posts. It's a second MCP tool plus `GET /signal-clusters`, with
  `get_rated_signals` kept as the flat drill-down; embeddings do two jobs, retrieval for search and
  clustering for the digest (pipeline groups, agent judges). Inert-until-keyed holds, `clustered:
  false` when no embeddings back the window and the agent falls back to the flat list. The
  clustering appendix is in [docs/module-6.md](docs/module-6.md).

## Appendix modules

Parked experiments, worth one afternoon each, never on the critical path.

- **Appendix A, self-host the rating model on Railway.** Ollama as a fourth Railway
  service, CPU-only, a 3B quantized model, pointed at by the same rating adapter Module 4
  builds (no code changes, that's the point). The lesson is feeling the wrong economics
  firsthand. Railway has no GPUs, inference is memory-bandwidth bound, so CPU streams maybe
  5-15 tokens/sec while the ~5GB of always-on RAM bills more per month than the API pennies
  it replaces. Stand it up, measure tokens/sec and the RAM line on the bill, write the
  numbers down, tear it down.

## The custom-vs-hosted line

The thread running through modules 3 to 5 is deciding what to run custom and what to rent
hosted, and being able to move a workload across that line without rewriting it. The rating
model swaps between self-hosted Ollama and rented APIs behind one interface (Module 4).
Scheduled work splits between the queue-backed worker we own and serverless we rent (Module
3's deferred Edge Function). The digest bot rents an entire agent runtime (Module 5's
Managed Agent) in the same season Cursor ships hosted background agents; soon every vendor
will have one. The durable skill isn't picking a side, it's keeping the interface yours so
the answer can change per workload as the hosted offerings evolve.

## Layout

A moon + uv-workspace monorepo. One `uv.lock` at the root covers every workspace member,
and moon is the ONE task runner (no Makefile). Tasks live in the project that owns them:
db lifecycle in `packages/core` (it owns the migrations), agent hand-cranks in
`services/managed-agents`, dev servers in `services/*`, and workspace lifecycle (compose up/down,
setup, format, ollama-pull) in the root-level moon project (`moon.yml` at the repo root).
moon is a standalone Rust binary, not a node package. Install it with `brew install moon`
on the host; the dev container and Cursor Cloud VM fetch a pinned release binary in their
own setup. The version is pinned in `.moon/workspace.yml` (`versionConstraint`), so there
is no root `package.json`, no pnpm, and no node in the backend toolchain. The one exception
is `.railway/package.json`. It only holds the Railway IaC SDK that `.railway/railway.ts`
imports, and nothing in the Python workspace touches it.

```
moon.yml          root moon project: workspace lifecycle tasks (root:up, root:setup, ...)
.moon/            moon workspace config (doubles as the .env loader's repo-root marker)
.railway/         Railway IaC: railway.ts (every service's build/run/env) + its own package.json
apps/chat-web/    React chat agent UI (scaffold, Module 7)
services/api/     FastAPI surface (sysdesign-api): api/, tests/, railway.json, openapi.json
services/worker/  Celery worker + beat (sysdesign-worker): worker/, railway.json
services/agent/   Module 7 chat agent, Python (sysdesign-agent): ReAct loop, CLI + SSE server, railway.json
services/agent-ts/  Module 7 chat agent, TypeScript: same contract, native async generators
services/managed-agents/  Module 5 Anthropic Managed Agents: agent.yaml + agentctl.py
packages/core/    shared code (sysdesign-core): common/, db/migrations/, drills/, tests/
packages/task-contract/  task-name constants + send-only Celery client (api->worker contract)
infra/            Railway env-var sync + preview-env scripts
.devcontainer/    reproducible container (its own sibling Postgres at db:5432)
```

Run everything from the repo root. `brew install moon` gets the task runner (once), and
`uv sync --all-packages` installs every workspace member; `uv run --package sysdesign-api ...`
targets one.

## Stack

Postgres 16 with pgvector (Docker), Python 3.13 managed by `uv`, `psql` for the drills,
`dbmate` for migrations, FastAPI for the API surface. The frontend (Next.js) arrives in
Module 2 and talks to the FastAPI service over HTTP.

## Build / Dev

All from the repo root:

```bash
moon run root:setup        # HOST: docker compose up db, then migrate + full seed
moon run core:db-init      # DEV CONTAINER: migrate + full seed (influencers + 4000 drill signals)
moon run core:db-fresh     # DEV CONTAINER: drop db, re-migrate from empty, seed ONLY influencers (no signals)
moon run core:db-empty     # DEV CONTAINER: drop db, re-migrate from empty, seed NOTHING (add influencers via the API)
moon run core:up           # THE schema command: dbmate history, then every pending alembic revision
NAME=X moon run core:revision   # autogenerate an alembic revision by diffing common/models.py vs the db
moon run core:alembic-status    # which alembic revision the db is on, and what's pending
moon run core:alembic-sql       # print the SQL a pending upgrade would run, touching nothing
moon run core:downgrade    # undo the most recent alembic revision
moon run core:migrate      # dbmate only: apply pending packages/core/db/migrations/*.sql (frozen history)
moon run core:status       # dbmate only: which .sql migrations have run vs pending
moon run core:rollback     # dbmate only: undo the most recent .sql migration (its migrate:down)
NAME=X moon run core:new   # dbmate only: scaffold a timestamped .sql migration (rarely what you want now)
moon run core:seed         # full seed: watchlist + 4000 synthetic signals (drill volume)
moon run core:seed-influencers  # just the watchlist, no signals
moon run core:drills       # run packages/core/drills/explain-drills.sql (whole file, smoke test)
moon run api:dev           # run the FastAPI surface (uvicorn, reload) at :8000, docs at /docs
moon run worker:dev        # DEV CONTAINER: Celery worker for Module 2 fan-out jobs (needs Redis + the API)
moon run worker:beat       # DEV CONTAINER: Celery beat, periodic backstops (rollup refresh + unrated sweep)
moon run root:ollama-pull  # DEV CONTAINER: one-time pull of the Module 4 local rating model (llama3.2:1b)
moon run api:openapi       # export the OpenAPI spec to services/api/openapi.json (no db/server needed)
moon run :lint             # every project's ruff check + format check (root covers infra/)
moon run :test             # every project's pytest; integration tests auto-skip when Postgres is down
moon run root:format       # auto-apply ruff's formatter across the whole workspace
moon run root:down         # drop the volume
moon run root:reset        # down then setup
uv run python -m common.seed   # re-seed (idempotent, inserts nothing the second time)
```

The FastAPI app lives in `services/api/api/` (`api.main:app`). Endpoints: `/influencers` (POST a
single creator, POST `/influencers/bulk` for the whole watchlist, both upsert on
instagram_handle; PATCH advances the last_scraped_at watermark), `/sources`, `/signals` (POST
is the idempotent `ON CONFLICT` upsert, content_hash derived server-side; GET requires a
`from`/`to` window so it always prunes), and `/rollup` (reads the matview). To populate real
data, POST `/runs` with `{"mode": "live"}`. That fans out one Celery task per creator and each
worker does the real Apify scrape itself, writing straight to Postgres (`services/worker/worker/scrape.py`)
rather than POSTing back over HTTP. `{"mode": "demo"}` runs the same fan-out with synthetic
signals and no Apify spend. Live mode needs `APIFY_API_KEY` in the repo-root `.env` (gitignored, never commit it).

FastAPI generates the OpenAPI spec automatically (`/openapi.json`, Swagger at `/docs`,
ReDoc at `/redoc`); no separate OpenAPI library. `operationId`s are the handler names
(`list_signals`, `create_signal`) so generated clients read cleanly. `moon run api:openapi` dumps the spec to `services/api/openapi.json`
(introspection only, no db/server), which the Module 2 Next.js frontend codegens a typed
client from.

## Schema layer: SQLAlchemy models plus Alembic

Modules 1 to 6 were written in raw psycopg SQL on purpose. The explicit SQL is the studyable
artifact (partition pruning, ON CONFLICT, index usage all stay visible), and it matched the
dbmate raw-SQL migrations. That choice stops paying once the repo hosts more than one
workload, because every new table then costs hand-written DDL plus hand-written CRUD.

So the schema now has two layers, and they coexist deliberately.

- `packages/core/common/models.py` is the declarative mirror of every table. Alembic diffs it
  against the live database to generate migrations, so a new table is written once here
  instead of twice (model and SQL). `packages/core/common/session.py` supplies the engine,
  the `session_scope()` contextmanager, and a `db_session` FastAPI dependency.
- The dbmate `.sql` files in `packages/core/db/migrations/` are frozen history. They still
  build a database from empty and they're still the record of how Modules 1 to 6 got here.
  Nothing new goes in there.
- `packages/core/db/upgrade.py` runs both, in that order, and is what Railway's
  `preDeployCommand` and CI both call. On an existing database dbmate reports up to date and
  Alembic applies what's new; on a fresh one dbmate builds the world and Alembic's empty
  baseline revision is a no-op. Both halves are idempotent.

Existing psycopg call paths are untouched. Nothing forces a rewrite, and the raw-SQL read
paths in `common/search.py` and friends stay as they are because their SQL is the lesson.
New tables and new query code should use the models.

Two guard rails worth knowing before you touch this. Alembic autogenerate cannot see the
monthly `raw_signals_*` partitions, the `daily_signal_rollup` matview, or either migration
bookkeeping table, so `common/schema_filter.py` hides all four; without that filter the first
generated revision confidently proposes dropping the partitioned data. And
`packages/core/tests/test_orm_schema.py` asserts that autogenerate produces an EMPTY diff
against the live schema, which runs in CI with a real Postgres. If the models and the
migrations drift, the build goes red rather than a later deploy going sideways.

Always read a generated revision before committing it. Autogenerate is a first draft.

To study a single query plan, don't use `moon run core:drills` (it fires the whole file at once).
Open an interactive shell with `psql "$DATABASE_URL"` and paste one drill block at a time.

`DATABASE_URL` defaults to `postgresql://lab:lab@localhost:5432/sysdesign` on the host,
and `db:5432` inside the dev container. dbmate reads it with `?sslmode=disable` appended
for the local no-TLS container.

The dev container (`.devcontainer/compose.yml`) is standalone and runs its own Postgres
with no host port publish, so it never collides with a host-run `moon run root:up` on 5432. Its db
is a separate volume, so seed it once with `moon run core:db-init` (from the repo root) in a container
terminal. Do not add `include: ../docker-compose.yml` back. Compose appends port mappings,
which reintroduces the 5432 collision.

## Git workflow

App tier. ALWAYS a feature branch plus PR. Never commit to `main` directly. Tag each
completed module on `main` (`git tag module-1 && git push origin module-1`). Schema changes
go through Alembic now: edit `packages/core/common/models.py`, run `NAME=... moon run
core:revision`, read the generated file, then `moon run core:up`. Never edit an
already-applied migration, dbmate or Alembic. Write the `downgrade()` body too, so rollback
works.

## The one idempotency sentence

At-least-once delivery is assumed everywhere. Every write is an idempotent upsert keyed
on `(influencer_id, content_hash, captured_at)` via `INSERT ... ON CONFLICT DO NOTHING`,
so reprocessing the same item twice is a no-op. That answers most "what if it runs
twice" and "how do you avoid duplicates" probes.

## Writing style

No em dashes or en dashes as punctuation. Use commas, parens, periods. No prose colons
introducing a list in body text. Use contractions.

## Cursor Cloud specific instructions

The Cloud VM runs the stack natively (no Docker, no `.devcontainer/compose.yml`). Postgres 16
+ pgvector, Redis, `uv`, and `dbmate` are baked into the VM image; `.cursor/environment.json`'s
install step fetches the pinned moon release binary into `$HOME/.local/bin` (arch-matched,
no node). If moon is somehow missing, every task just wraps `uv run ...`/`dbmate ...`, so you
can always call those directly. The code's env defaults
(`DATABASE_URL=postgresql://lab:lab@localhost:5432/sysdesign`, `REDIS_URL=redis://localhost:6379`,
Celery on the same Redis) already point at localhost, so no `.env` or exported URLs are needed
for local dev. The `lab` Postgres role is a superuser (so migrations can `CREATE EXTENSION vector`).

Postgres and Redis are system services that do NOT auto-start on boot. Start them once per session
before running anything (the seeded `sysdesign` db persists in the image, so you usually don't need
to re-seed):

```bash
sudo pg_ctlcluster 16 main start
sudo redis-server /etc/redis/redis.conf --daemonize yes
```

Then run services from the repo root, each in its own terminal, per the moon tasks already
documented above (`moon run api:dev` on :8000, `moon run worker:dev`, optional `moon run
worker:beat`). The DB is already migrated and seeded (5 influencers + 4000 drill signals); use
`moon run core:migrate`/`core:seed` or `core:db-fresh` only if you dropped or emptied it. The fastest end-to-end smoke test is a demo
run (no external keys, no Apify spend), which exercises the Celery chord fan-out and the SSE stream:
`curl -X POST localhost:8000/runs -d '{"mode":"demo","limit":5}'`, then watch
`curl -N localhost:8000/runs/<run_id>/stream`.

Lint with `moon run :lint` (ruff `check` plus `ruff format --check`, config in `pyproject.toml`);
`moon run root:format` auto-applies the formatter. Tests are `moon run :test` (pytest under
`services/api/tests/` and `packages/core/tests/`): unit tests are hermetic, and tests marked
`integration` need a live Postgres and auto-skip when it's unreachable, so `moon run :test` is
green even with no DB up (start Postgres first to actually exercise them). Lint, format check,
and tests all run in CI (`.github/workflows/ci.yml`) on every PR and on merge to main, so run
`moon run root:format` and `moon run :lint` before pushing. "Build" for the Python side is
`uv sync --all-packages` plus `moon run api:openapi` (spec export). The Module 4
rating layer stays inert unless `RATING_MODEL` and a model are provided; local Ollama is a
`.devcontainer` sibling that is not installed on the Cloud VM, so demo runs finish with
`rated_count = 0`, which is expected. The `apps/chat-web/` scaffold has no UI to run yet.
