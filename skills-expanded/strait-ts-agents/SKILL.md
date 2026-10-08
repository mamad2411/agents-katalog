# AGENTS.md

Operating guide for contributors and AI agents working on this repository.

**Read this document before making any change.** When instructions
conflict, use this priority order:

1. Direct user request
2. Repository conventions in this file
3. Existing code patterns
4. Personal preference

---

## What this project is

- **Project**: Strait TypeScript SDK
- **Package**: `@strait/ts`
- **Language**: TypeScript (strict mode)
- **Runtime**: Bun (test runner, scripts) / Node.js (consumers)
- **Compiler**: tsgo (`@typescript/native-preview`)
- **Linter**: Biome + ultracite
- **Build**: tsup (dual ESM + CJS) → `dist/`

The SDK has four pillars:

1. **Generated typed client** for the Strait REST API (273+ operations across 31 domains).
2. **Authoring DSL** — `defineJob`, `defineWorkflow`, `defineDag`, `defineAgent`.
3. **Serve handler** — HTTPS push receiver with HMAC verification + framework adapters.
4. **Worker package** — long-lived gRPC bidi-stream worker.

For internals, see the topic deep-dives under [`docs/`](./docs/).

---

## Ecosystem

| Component | Language | Repository |
|-----------|----------|------------|
| **Platform** (server) | Go | [strait-dev/strait](https://github.com/strait-dev/strait) |
| **CLI** | Go | [strait-dev/cli](https://github.com/strait-dev/cli) |
| **MCP server** | TypeScript | [strait-dev/mcp](https://github.com/strait-dev/mcp) |
| **TypeScript SDK** (this) | TypeScript | [strait-dev/strait-ts](https://github.com/strait-dev/strait-ts) |
| **Python SDK** | Python | [strait-dev/strait-python](https://github.com/strait-dev/strait-python) |
| **Go SDK** | Go | [strait-dev/strait-go](https://github.com/strait-dev/strait-go) |
| **Ruby SDK** | Ruby | [strait-dev/strait-ruby](https://github.com/strait-dev/strait-ruby) |
| **Rust SDK** | Rust | [strait-dev/strait-rust](https://github.com/strait-dev/strait-rust) |
| **Docs** | MDX | [strait-dev/docs](https://github.com/strait-dev/docs) |

- Website: <https://strait.dev>
- Docs: <https://docs.strait.dev>
- API reference: <https://api.strait.dev/reference/openapi.json>

---

## Topic deep-dives

| Doc | When to read |
| -- | -- |
| [`docs/architecture.md`](./docs/architecture.md) | Layering, request lifecycle, dual API surfaces, error/tracing model. |
| [`docs/authoring.md`](./docs/authoring.md) | `defineJob` / `defineWorkflow` / `defineAgent`, `RunContext`, execution modes. |
| [`docs/schema-adapters.md`](./docs/schema-adapters.md) | Bringing your own validator (Zod, Effect Schema, Standard Schema, custom). |
| [`docs/serve.md`](./docs/serve.md) | HTTPS push handler, HMAC verification, framework adapters. |
| [`docs/worker.md`](./docs/worker.md) | gRPC worker, dispatch, reconnect, OTel hooks. |
| [`docs/contracts.md`](./docs/contracts.md) | OpenAPI codegen pipeline, regen workflow, strict mode. |
| [`docs/release.md`](./docs/release.md) | Release process, changesets, versioning policy. |

---

## Local setup

```bash
bun install
bun run run-all                  # format + lint + typecheck
bun test                         # SDK tests
cd packages/react && bun test    # React tests
```

Always run `bun install` after a `git pull` or branch switch — the lock file
may have changed. (`bun test` does not run the `pretest` install hook; only
`bun run test` does.)

Opt-in live integration tests need the local Docker stack up (REST/SSE on
`:8080`, gRPC on `:50051`): `STRAIT_TEST_INTEGRATION=1 bun test test/integration`.

Frequent commands:

| Goal | Command |
| -- | -- |
| Build | `bun run build` (tsup → `dist/`) |
| Typecheck | `bun run typecheck` (tsgo) |
| Lint | `bun run lint` (biome) |
| Test | `bun test` |
| Regen contracts | `bun run generate:contracts` |
| Regen proto stubs | `bun run generate:proto` |
| Bench | `bun run bench` |
| API docs | `bun run docs` (TypeDoc → `docs/api/`) |

---

## Engineering rules (non-negotiable)

- **No emojis** in code, comments, logs, docs, or commits.
- **Never edit `_generated/` files by hand** — change the generator.
- **Conventional commits**: `type(scope): summary` (feat / fix / chore / docs / refactor / test / build).
- **No `Co-Authored-By` lines, no AI attribution** in commits or PRs.
- **PR descriptions** describe what was actually worked on — substantive,
  not boilerplate.
- **Effect** is used internally for runtime validation, error handling,
  and the HTTP client. Public surfaces are Promise-based; consumers
  should not need to import Effect.
- **Schema adapters** bridge external validators to the SDK's internal
  `SchemaAdapter` interface — see [`docs/schema-adapters.md`](./docs/schema-adapters.md).
- **`src/domains/index.ts`** must re-export every domain from the
  generated contracts.

---

## Validation before merge

```bash
bun run run-all                          # format + lint + typecheck
bun test
cd packages/react && bun test && cd -
bun run build && node dist/index.js      # raw Node ESM resolution
bun pack --dry-run                       # confirm tarball contents
```

For changes touching contracts:

```bash
bun run generate:contracts && git diff src/internal
STRICT_OPENAPI=1 bun run generate:contracts   # CI-style strict prune
```

---

## DOs and DON'Ts

### DO
- Write tests alongside any new behaviour.
- Prefer editing existing files over creating new ones.
- Use `Effect.withSpan` for any new operation that hits the wire.
- Add a `defineJob`-level example to `examples/` when adding a
  user-visible feature.
- File a follow-up issue rather than expanding the scope of a PR.

### DON'T
- Don't add features, refactors, or abstractions beyond what the task
  requires.
- Don't introduce backwards-compatibility hacks (renamed `_unused`,
  `// removed` comments, dead re-exports). If something is unused,
  delete it.
- Don't write multi-paragraph docstrings or planning files.
- Don't bypass safety checks (`--no-verify`, `--no-gpg-sign`) — fix the
  underlying issue.

---

## Definition of done

A change is done when:

1. The new behaviour has tests and they pass.
2. `bun run run-all` is clean.
3. `bun test` (root + `packages/react`) is clean.
4. If the change is user-visible, a changeset is added (`bunx changeset`).
5. If the change touches the public surface, the relevant doc under
   [`docs/`](./docs/) is updated.

That's it. Ship it.
