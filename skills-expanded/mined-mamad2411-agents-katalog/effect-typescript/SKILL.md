---
name: effect-typescript
description: Use as when TypeScript/Bun code involves meaningful I/O and you are writing, reviewing, or deciding whether to use Effect, especially services, Layers, Config, Schema, typed errors, retries, resources, tests, or Alchemy deployments.
---

# Effect TypeScript

Use Effect deliberately. The most important trigger is meaningful I/O: external APIs, files, databases, queues, workers, CLIs, config, secrets, clocks, subprocesses, network calls, or deployable runtime boundaries. Effect is excellent when that I/O needs typed failures, dependencies, runtime validation, retries, concurrency, resources, and testable boundaries. It is not a default replacement for simple TypeScript.


This skill adapts Effect guidance to darkmatter conventions: use Bun commands instead of pnpm for darkmatter projects, and prefer Alchemy for deployable infrastructure. It carries the upstream `Effect-TS/effect` monorepo as a local submodule at `reference/effect` for current APIs, tests, package layout, docs, and upstream agent instructions.

## Bootstrap

If `effect-solutions` is on in your `$PATH`, install it: `bun add -g effect-solutions@latest`. 

## Guidelines

- Refer to the best practices recommended by the `effect-solutions` CLI when writing effectful code.
- If you need more specific information, there's a local checkout of the effect source in the reference directory.

## When to use

- Meaningful I/O is involved and the work benefits from explicit failure, dependency, resource, retry, validation, or testing boundaries.
- The code already uses Effect and you are adding or reviewing Effect code.
- You are deciding whether a TypeScript/Bun feature should use Effect.
- The task involves external APIs, databases, queues, workers, CLIs, schedules, retries, config, secrets, structured logging, runtime validation, resource cleanup, or concurrent workflows.
- You need typed domain errors rather than unstructured thrown exceptions.
- You need swappable live/test implementations through services and Layers.
- You are deploying TypeScript infrastructure or workers and need Alchemy-aware conventions.

## When NOT to use

- A small one-off script can be obvious plain TypeScript: read one file, transform pure data, write one file, no retries, no injected dependencies, no long-lived resources. Keep this exception genuinely small; if the file starts accumulating schemas, clients, orchestration, retries, or reusable helpers, split it around those boundaries instead of growing a monolith.
- Pure functions, simple data mappers, UI-local state, or tiny glue code do not need Effect wrappers.
- A project has no Effect dependency and the feature does not benefit from typed errors, Layers, resource safety, retries, or observability.
- The team only needs a tactical fix in plain async code. Do not introduce Effect as a drive-by refactor.
- You cannot explain the service/layer/error/testing shape. Stop and design that first instead of sprinkling `Effect.runPromise` calls everywhere.

## Decision Rule

Use Effect when at least two of these are true:

- There are multiple effectful dependencies to compose.
- Failures need to be represented in types and handled by tag.
- Inputs or outputs cross trust boundaries and need `Schema` validation.
- There are retries, timeouts, schedules, or polling.
- There are resources with lifecycle: DB pools, clients, sockets, subscriptions, background fibers.
- Tests need fake services, shared layers, `TestClock`, or deterministic concurrency.
- The runtime is long-lived: worker, server, daemon, queue consumer, scheduled job.

If only one is true, prefer plain TypeScript unless the surrounding codebase already uses Effect.

## Darkmatter Conventions

- Use Bun commands: `bun install`, `bun test`, `bun run <script>`, `bunx <tool>`.
- Translate upstream `pnpm` examples mechanically. Example: `pnpm test file.test.ts` becomes `bun test file.test.ts` when the project uses Bun test, or `bun run test file.test.ts` when test is a package script.
- Prefer Bun runtime packages where relevant, such as `@effect/platform-bun` and `BunRuntime.runMain` for Bun entrypoints.
- Prefer Alchemy for deployable infrastructure. Put infra in `alchemy.run.ts`, create resources with Alchemy, bind them to workers/services, and build up an `Alchemy.Stack`. Refer to the alchemy skill if writing alchemy code or adding new infra code.

## Upstream Reference

Use `reference/effect` or `effect-solutions` CLI when you need current Effect source or examples instead of relying on memory:
- `reference/effect/AGENTS.md` — upstream repository rules, including pnpm validation commands, generated barrels, changesets, and `it.effect` conventions.
- `reference/effect/packages/effect/` — core library source and tests.
- `reference/effect/packages/platform-bun/` and `reference/effect/packages/platform-node/` — runtime/platform examples.
- `reference/effect/packages/vitest/` — Effect-aware Vitest helpers.

If the submodule is missing in a fresh checkout, initialize it before using local references:

```bash
git submodule update --init skills/effect-typescript/reference/effect
```

For darkmatter application work, treat the submodule as read-only and translate upstream pnpm commands to the repo's package manager. For direct upstream Effect contributions, follow `reference/effect/AGENTS.md` exactly; do not apply darkmatter Bun defaults inside the upstream repo.

## JSON Encoding & Decoding

Use `Schema.fromJsonString` to parse JSON strings and validate them with your schema in one step. This combines `JSON.parse` + schema decoding in one step, and `JSON.stringify` + schema encoding for the reverse:

```typescript
import { Effect, Schema } from "effect"

const Row = Schema.Literals(["A", "B", "C", "D", "E", "F", "G", "H"])
const Column = Schema.Literals(["1", "2", "3", "4", "5", "6", "7", "8"])

class Position extends Schema.Class<Position>("Position")({
  row: Row,
  column: Column,
}) {}

class Move extends Schema.Class<Move>("Move")({
  from: Position,
  to: Position,
}) {}

// fromJsonString combines JSON.parse + schema decoding
// MoveFromJson is a schema that takes a JSON string and returns a Move
const MoveFromJson = Schema.fromJsonString(Move)

const program = Effect.gen(function* () {
  // Parse and validate JSON string in one step
  // Use MoveFromJson (not Move) to decode from JSON string
  const jsonString = '{"from":{"row":"A","column":"1"},"to":{"row":"B","column":"2"}}'
  const move = yield* Schema.decodeUnknownEffect(MoveFromJson)(jsonString)

  yield* Effect.log("Decoded move", move)

  // Encode to JSON string in one step (typed as string)
  // Use MoveFromJson (not Move) to encode to JSON string
  const json = yield* Schema.encodeEffect(MoveFromJson)(move)
  return json
})
```