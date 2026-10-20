# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **polyglot** library shipping decorators for caching, tracking, and queue emission in two languages — Node/TypeScript (`node/`, npm: `@montionugera/server-decorator`) and Python (`python/`, PyPI: `server-decorator`) — kept in lockstep behind a shared wire-format contract (`contracts/`). Both packages publish together under one semver tag (Decision #2). The published artifact lives in `node/` and `python/`; the repo root is a workspace, not a package — its `package.json` only proxies scripts.

A third lane, **Go** (`go/`, module `github.com/montionugera/node-server-decorator/v2`, root `go.mod`, Go 1.22+, stdlib only), ships a full suite, not just the IR producer: `go/entity` (EntitySpec IR builder + struct-tag parser, byte-identical to the Node/Python `entity` packages), `go/openapi` (OpenAPI 3.1 generator), `go/dto` (runtime DTO validation + struct codegen), `go/core` (cache key, `Cache`, `EmitOnSuccess`, `Retry`, `CircuitBreakerWrapper`, `RateLimit`) with sub-packages `go/core/coalesce` (batch loader, multi-tier L1/L2/L3), `go/core/distlock` (Redis distributed lock, plus the try-or-skip `Manager` interface with in-memory and no-op managers) and `go/core/tracing` (W3C trace context + spans), `go/http` (package `httpserver`: REST routes on `http.ServeMux`, RFC 9457 problems, scope auth), `go/sse` (broadcaster with `Last-Event-ID` replay and keyed channels), `go/adapter/gqlloader` (request-scoped GraphQL loader registry), the CLIs `go/cmd/gen-entity-spec` and `go/cmd/gen-dto`, and `go/internal/example` fixtures. `go/adapter/gin` is a **separate module** with its own `go.mod`, and `go/adapter/pgxlock` (PostgreSQL advisory-lock `Manager` on pgx v5, which does not import the root module) is the second one; these two are the only places a third-party dependency is allowed, and `go test ./go/...` from the root covers neither. See `go/README.md`.

A fourth lane, **Nim** (`nim/`, nimble package `server_decorator`, Nim 2.2.12), ships the `entity` IR producer (a `restful` block macro + field pragmas — the decorator ergonomics Go could not offer) **and** the OpenAPI generator (`server_decorator/gen_openapi`), both byte-identical to the Node/Python twins; see `nim/README.md`.

**Before changing anything non-trivial, read `DECISIONS.md`** — it holds the 12 locked decisions (plus D-A…D-D, N1…N4) that constrain the design. Revisit any item only via a new ADR under `docs/adr/`.

## High-level architecture

Three layers, in dependency order:

1. **`contracts/`** — source of truth for the wire format. JSON Schemas (`schemas/`), algorithm specs (`rules/cache-key.md`, `rules/topic-naming.md`, `rules/tracking-key.md`, `rules/cache-adapter.md`, `rules/rest-conventions.md`), golden fixtures, and a `VERSION` file. CI asserts `contracts/VERSION`, `node/packages/core/src/_contract.ts`, and `python/packages/core/src/server_decorator/_contract.py` all agree. `contracts/schemas/entity-spec.schema.json` and `contracts/fixtures/entity-spec.*.json` are the same kind of source-of-truth for the entity-spec IR layer described below.
2. **`node/` and `python/`** — pnpm/uv workspace roots, each holding a `packages/core` reference implementation (ADR 0006) plus the entity-spec layer:
   - **`entity` packages** (`node/packages/entity` = `@montionugera/entity-spec`, `python/packages/entity` = `server-decorator-entity`) — declarative decorators (`@Restful`/`@action`/field markers in Node, `@restful`/`@action`/field markers in Python) that emit the language-neutral **EntitySpec IR**, validated byte-identical across languages against `contracts/schemas/entity-spec.schema.json`.
   - **`gen-*` packages** (`node/packages/gen-zod` = `@montionugera/entity-spec-gen-zod`, `python/packages/gen_pydantic` = `server-decorator-gen-pydantic`) — compile an EntitySpec IR into `create`/`update`/`read`/action-input DTO validators (zod / pydantic v2), applying the same include/exclude rules (`readonly` excluded from create, `writeonly` excluded from read, nested obj/list fields filtered recursively) in both languages.
   - **Layering rule: `entity` → `gen-*` → adapters.** `entity` packages depend on nothing else in this repo; `gen-*` packages depend only on their language's `entity` package (never the other language, never `core`); nothing here yet consumes a `gen-*` package as an "adapter" (HTTP/RPC wiring is P2+ scope) — don't introduce a reverse or cross-language import.
   - Each exposes a `tracking` / `cache` / `EmitOnSuccess`(Node) or `emit_on_success`(Python) decorator from `packages/core`. Python additionally has class-form variants (`tracking_class`, `cache_class`, `emit_on_success_class`) that walk only `vars(cls)` (never the MRO — N2) and apply the method form to public methods (Decision #4).
3. **`interop/`** — Node↔Python end-to-end tests via Redis Streams (`docker compose up -d redis` then run the `scenarios/*/run.sh`). Only matched-adapter round-trips are in scope; BullMQ-aware Python consumers are deferred to v2.1+.

Queue routing on the Node side: `@EmitOnSuccess` → `globalQueueRegistry` → adapter (`BullMQAdapter` / `RabbitMQAdapter` / `KafkaAdapter` / `InMemoryQueueAdapter`). Topics auto-generate from `ClassName.methodName`; an explicit `topic:` overrides, and a queue's `defaultTopic` is the fallback. See `node/packages/core/README.md` for the priority order.

`CACHE_MISS` is a sentinel (`Symbol.for('server-decorator.cache.miss')` in Node, a module singleton in Python — D-B) that `CacheAdapter.get` returns for absent keys, so `null`/`0`/`""`/`false` can be cached as legitimate values. Custom adapters must update from the v1.x "return undefined on miss" pattern.

## Common commands

Node lives at `node/packages/core` under a pnpm workspace rooted at `node/`; Python lives at `python/packages/core` under a uv workspace rooted at `python/` (ADR 0006); Nim lives at `nim/` as a single nimble package. Multi-package commands run from the workspace root (`cd node`, `cd python`); single-package commands (a specific test file) need `cd node/packages/core` / `cd python/packages/core`. The root `package.json` has thin proxies:

| Task | Command |
|------|---------|
| Node unit tests + coverage gate (fast) | `cd node && pnpm -r test:unit` (each package's `jest.config.js` holds a `coverageThreshold` on lines: core 98, entity 97, gen-zod 100, gen-openapi 100; plain `test` and `test:e2e` collect no coverage) |
| Node e2e (needs Docker) | `cd node && pnpm -r test:e2e` |
| Backend-specific e2e | `cd node && pnpm -r test:e2e:redis` / `:rabbitmq` / `:kafka` |
| Single Jest test file | `cd node/packages/core && pnpm test -- --testPathPattern=cache.spec` |
| Build Node | `cd node && pnpm -r run build` (outputs `node/packages/core/dist/`) |
| gen-zod tests | `cd node/packages/gen-zod && pnpm test:unit` (builds `entity` first via `pretest:unit`; schemas checked against `contracts/fixtures/entity-spec.cases.json`) |
| Python lint+type+unit + coverage gate | `cd python && bash scripts/check.sh` (runs every package's own `scripts/check.sh`; uses `uv` if present, ruff + ruff format + mypy strict + pytest with `--cov-fail-under=$COV_MIN` on unit tests: core 99, entity 96, gen_openapi 96, gen_pydantic 97) |
| Single pytest | `cd python/packages/core && uv run pytest tests/unit/test_cache.py::test_x -q` |
| gen_pydantic tests | `cd python/packages/gen_pydantic && bash scripts/check.sh` (DTO models checked against `contracts/fixtures/entity-spec.cases.json`) |
| gen-openapi tests | `cd node/packages/gen-openapi && pnpm test:unit` (builds `entity` first via `pretest:unit`) |
| gen_openapi tests | `cd python/packages/gen_openapi && bash scripts/check.sh` |
| Go tests (byte parity, guards, drift gate) | `go test ./go/...` (repo root; stdlib only, no install) |
| Go coverage gate | `bash scripts/check-go-coverage.sh` (runs `go test ./go/...` once with a coverprofile and fails if any package is below its statement threshold, declared at the top of the script; a new package must add an entry; `ci-go.yml` runs this) |
| Go hygiene | `test -z "$(gofmt -l go)" && go vet ./go/...` |
| pgxlock unit tests (nested module, no database) | `cd go/adapter/pgxlock && go vet ./... && go test -race -cover ./...` (`ci-go.yml` and `scripts/contributor-check.sh` run the tests; no coverage gate) |
| pgxlock integration (real Postgres, local only) | `cd go/adapter/pgxlock && PGXLOCK_TEST_DATABASE_URL=postgres://... go test -tags integration ./...` (throwaway database; no CI job runs it) |
| Regenerate Go example IR | `go generate ./go/...` |
| Nim tests (byte parity, cases.json openapi suite, compile-error harness) | `export PATH=$HOME/.nimble/bin:$PATH && cd nim && nimble test` (Nim 2.2.12, stdlib only) |
| Nim hygiene | `cd nim && nimble check && nim check --hints:off src/server_decorator.nim` |
| OpenAPI parity | `bash scripts/check-openapi-parity.sh` (asserts Node, Python and Nim emit byte-identical OpenAPI, equal to `contracts/fixtures/openapi.valid-user.json`) |
| Python integration (Docker) | `cd python/packages/core && uv run pytest -m integration` |
| Contract validation | `bash contracts/scripts/validate.sh` (requires `npm i -g ajv-cli@5`) |
| Entity-spec parity | `bash scripts/check-entity-parity.sh` (asserts Node, Python, Go and Nim `entity` packages emit byte-identical IR, equal to `contracts/fixtures/entity-spec.valid-user.json`) |
| Cross-version assert | `bash scripts/check-versions.sh` (fails if Node, Python, Go, Nim or Rust package versions diverge, including the Rust internal dep versions) |
| Go/Nim install smoke test | `bash scripts/smoke-install-go.sh vX.Y.Z` / `bash scripts/smoke-install-nim.sh vX.Y.Z` (post-tag; the `smoke` job in `ci-node.yml` runs both) |
| Local release gates | `bash scripts/precheck.sh` (Gate 1 of `psrw ship`: shell tests, actionlint, version lockstep, Node build + unit tests; ~1.5-3 min) and `bash scripts/integration.sh` (Gate 2 of `psrw promote`: precheck + Go, Python, contract validation, entity/OpenAPI parity; ~4 min; stages whose toolchain is missing are reported as skipped). Both exit non-zero on any failure and end with one summary line. |
| Lockstep version bump | `bash scripts/bump-version.sh patch\|minor\|major` then commit + `git push --tags` |

Node uses **pnpm** (pinned `pnpm@9.14.2`, `packageManager` field). Python uses **uv** as the dev runner. `package-lock.json` and `yarn.lock` are gitignored on purpose — do not create them.

## Things that will trip you up

- **Don't change `contracts/` without bumping `VERSION`, updating `CHANGELOG.md`, AND patching both `_contract.ts` and `_contract.py`** in the same PR. `ci-contracts.yml` will fail otherwise.
- **Don't break the cache-key algorithm** — it's specified in `contracts/rules/cache-key.md` and Node/Python must match byte-for-byte (modulo the one irreducible whole-number-float JSON quirk documented there). Changing it is a major bump and forces a cache flush on every consumer (see D-A in `MIGRATION.md`).
- **Don't bump versions out-of-lockstep.** Use `scripts/bump-version.sh`, never `pnpm version` alone — it leaves Python behind. Note: `ci-node.yml`'s `publish` job already auto-bumps a patch on every push to `main`, so manual `pnpm version` commands on `main` produce conflicts.
- **Don't reintroduce `@nestjs/event-emitter`.** v2.0.0 swapped it for `eventemitter3` (Decision #8) and dropped `@nestjs/common`/`core`/`rxjs` from deps. `custom-logger.ts` was removed at the same time.
- **`kafkajs` is an optional peer dep** (Decision #9). It's in Node `devDependencies` for tests but consumers must install it themselves. Python equivalent: `pip install server-decorator[kafka]` pulls `aiokafka`.
- **Python is `asyncio` only** (Decision #10). Don't add `trio`/`anyio` shims. Sync `@emit_on_success(use_queue=True)` outside an event loop runs on a module-level single-worker `ThreadPoolExecutor` (`_EMIT_EXECUTOR`, D-C) — don't introduce a second one.
- **Class-form decorators walk `vars(cls)` only**, never the MRO (N2). Inherited methods aren't picked up by design. Skip `_private`, `__dunder__`, and `@property` by default; opt in via `include`/`include_private`/`wrap_properties` (Decision #4, N1 defers `@property` to v1.1+).
- **iCloud-doubled files (`* 2`, `* 2.*`, `* 3*`) are gitignored** (D-D). If you're on a Mac with iCloud Documents on, double-check your tree before committing.
- **npm publishes to two registries**: GitHub Packages (the default — see `.npmrc` and `node/packages/core/package.json` `publishConfig`; needs `GITHUB_TOKEN` in env) and a public mirror on npmjs.com via OIDC trusted publishing (`ci-node.yml`, `continue-on-error`).
- **Rust crates publish to crates.io from the same `publish` job** (`continue-on-error`, like npmjs.com), in dependency order; a tag does not guarantee all five crates reached crates.io at that version. Internal crate deps live in `rust/Cargo.toml` `[workspace.dependencies]` with a `version` next to the `path`; `scripts/bump-version.sh` moves them and refreshes `rust/Cargo.lock`, and `scripts/check-versions.sh` fails if they drift. A crate must not read files outside its own directory at compile time (`include_str!` of `contracts/...`) — `cargo publish` verifies the packaged tarball. That is why `server-decorator-entity` and `-openapi` `exclude` their fixture bins and tests from the tarball. `rust/examples/*` are `publish = false`.
- **The nested Go modules are `.../go/adapter/gin/v2` and `.../go/adapter/pgxlock/v2`** (`/v2` last; mid-path it would resolve inside the root module). Each release tags them `go/adapter/gin/vX.Y.Z` and `go/adapter/pgxlock/vX.Y.Z` next to `vX.Y.Z`, and `go/adapter/gin/go.mod` requires the root module at that same version (`bump-version.sh` rewrites it, `check-versions.sh` asserts it; the local `replace` is for in-repo builds only). Neither may import the root module's `go/internal/...`.
- **`contracts/fixtures/entity-spec.cases.json` is the cross-language validation contract** — it drives both `gen-zod`'s and `gen_pydantic`'s DTO test suites. Changing generator behavior (a new include/exclude rule, a new field type, a validation edge case) requires adding or updating a case there, and both languages must pass it — a change that only updates one language's tests is incomplete.
- **Nim is pinned to 2.2.12** (`ci-nim.yml`, `ci-contracts.yml`, `nim/README.md`); on the maintainer Mac it lives at `~/.nimble/bin` (not on PATH — `export PATH=$HOME/.nimble/bin:$PATH` first; do not use brew/choosenim). The package has zero dependencies: never commit `nimble.lock`. Nested `obj` types must be declared inside the same `restful` block, and `min`/`max` are integer literals even on `float` fields.

## CI workflow gating

`.github/workflows/`:

- `ci-node.yml` — unit + build on every Node/contracts PR; e2e only on `push: main` or PRs with the `run-e2e` label; auto-publishes (Node + Python + Rust crates) on `push: main` touching `node/`, `contracts/`, `go/`, `go.mod`, `nim/` or `rust/` by patch-bumping, pushing back and tagging `vX.Y.Z` plus the Go adapter tags `go/adapter/gin/vX.Y.Z` and `go/adapter/pgxlock/vX.Y.Z` in one atomic push, also writing a `CHANGELOG.md` entry, and a `release` job then creates the GitHub Release with `docs-site.tgz` (the built docs site); a follow-up `smoke` job then installs the Go root module, both Go adapter modules and the Nim package at that tag (fail-closed, re-runnable alone).
- `ci-python.yml` — equivalent for the Python side.
- `ci-go.yml` — gofmt + `go vet ./go/...` + `scripts/check-go-coverage.sh` on every `go/`/`go.mod`/`contracts/` PR and on `push: main`, then `go vet` + `go test` inside the nested modules `go/adapter/gin` and `go/adapter/pgxlock` (unit tests only; no database, no coverage gate).
- `ci-nim.yml` — `nimble check` + `nim check` + `nimble test` on every `nim/`/`contracts/` PR and on `push: main`; Nim parity with the other lanes runs in `ci-contracts.yml`.
- `ci-contracts.yml` — schema/fixture validation + version-match enforcement.
- `ci-interop.yml` — heavy cross-language scenarios; runs on `push: main`, weekly schedule, or PRs with the `run-interop` label.

If you're iterating on Node-only code, the unit lane is the fast feedback loop; e2e is opt-in via the label.
