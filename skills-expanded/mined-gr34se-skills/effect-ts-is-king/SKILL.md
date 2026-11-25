---
name: effect-ts-is-king
description: Maximize use of the Effect API and its ecosystem instead of writing local abstractions. Use for TypeScript backend implementation, debugging, refactoring, and code review whenever the project has an Effect dependency, meaning a package manifest lists `effect` or an `@effect/*` package, or the code imports from one. Use it even when the request does not mention Effect. Not for projects without Effect.
---

# Effect-TS Is King

This project runs on Effect. Effect and its ecosystem already ship most of the mechanics a backend needs: retries, timeouts, concurrency limits, resource cleanup, validation, configuration, dependency injection, streaming, caching, HTTP, SQL, logging, tracing, and LLM clients. Those implementations handle interruption, typed errors, and cleanup, and they compose with each other. A hand-written replacement usually handles none of that, and the team has to maintain it.

So divide the work this way: write the behavior that is specific to this application, and take the mechanics from Effect. Code that reimplements a mechanism Effect already provides is a defect to fix before handoff, in the same way a failing test is. It is not a style preference.

Most Effect code written from habit uses a small corner of the library: generators, services, and tagged errors. The rest goes unused because nobody searched for it. This skill exists to make you search.

## Scope

- Apply this only where a package manifest lists `effect` or an `@effect/*` package, or the code imports from one. If neither is true, stop. This skill is never a reason to add Effect to a project that does not use it.
- Apply it to the whole task at hand: handlers, workers, integrations, persistence, configuration, pure transformations, and tests.
- Stay inside the task. Do not rewrite unrelated code, replace the framework, or upgrade packages on your own initiative.
- Where Effect covers only part of the backend, work within the existing boundary. Do not add a second way of running effects, and do not migrate the rest without being asked.

## Do not trust your memory of the API

This skill is written for Effect 4. Most of what you remember about Effect comes from Effect 3, which is legacy, and Effect 4 changed a large part of the API. `Effect.catchAll` is now `Effect.catch`. `Effect.fork` is now `Effect.forkChild`. `Either` is now `Result`. `Context.Tag` and `Effect.Service` are now `Context.Service`. `Schema.decodeUnknown` is now `Schema.decodeUnknownEffect`. These are five examples out of hundreds, so a call that looks right from memory is often an Effect 3 call that no longer exists.

The packages changed too. The core of HTTP, SQL, RPC, AI, the command line, workflows, and clustering used to live in separate `@effect/*` packages and is now inside `effect`, under subpaths such as `effect/http`, `effect/sql`, and `effect/ai`. Four kinds of package stay separate: platform runtimes (`@effect/platform-*`), database drivers (`@effect/sql-*`), LLM providers (`@effect/ai-*`), and the test integration (`@effect/vitest`).

Before you write or change Effect code:

1. Read `AGENTS.md` in the installed `effect` package, next to its `package.json`. It is the library's own guide for coding agents, and it links to worked examples in the package's `ai-docs` folder. Read all of it, then read the examples for the area you are working in.
2. For every API you are not certain about, check its signature, error type, requirements, and interruption behavior in the package's source under `node_modules`. Trust the installed package over external documentation, blog posts, and your memory.
3. Read the `@stability` tag on an export you have not used in this project before. Many of the subpath modules are marked unstable, which is expected. When you build on an experimental export, say so in your report.
4. Read how neighboring code solves the same kind of problem, and follow that pattern unless it is the thing you are fixing.

Read the source to learn how to use the library. Import only public exports. If you cannot verify an API, say so in your report rather than guessing.

This skill tells you when to reach for Effect. The package's own guide tells you how to write it. If the two disagree about how to write Effect code, follow the package. If the project is still on Effect 3, the rules in this skill still apply, but expect different names and packages.

## Search before you write a mechanism

When you notice yourself about to write something from the left column, stop and look in the right column first.

| You are about to write | Look in Effect for |
|---|---|
| `try`/`catch`, custom error classes, a hand-made result union | The typed error channel, tagged errors, `Cause`, `Exit`, `Result`, recovery combinators |
| A retry loop, backoff, polling, `setInterval`, a fallback chain across providers | `Schedule`, retry and repeat, `ExecutionPlan` |
| `setTimeout`, `new Date()`, `Date.now()`, manual deadlines, date arithmetic | Timeouts, `Duration`, `Clock`, `DateTime` |
| `Promise.all`, `Promise.race`, a concurrency limiter, a worker pool | Concurrency options on the collection combinators, fibers, `Queue`, `PubSub`, `Deferred` |
| A mutex, a per-key lock, a gate, a list of running background tasks | `Semaphore`, `PartitionedSemaphore`, `Latch`, `FiberSet`, `FiberMap`, the `Tx*` transactional modules |
| `try`/`finally`, connection lifecycle code, shutdown handlers, a reference-counted or refreshable resource | `Scope`, acquire and release, finalizers, layer lifetimes, `RcMap`, `Resource`, `Pool` |
| A validation library, hand-written parsing, type guards such as `isString`, casts, branded types | `Schema`, `Predicate`, `Brand` |
| Null checks, a `switch` over a kind field, deep equality, comparators, collection helpers | `Option`, `Match`, `Equal`, `Order`, and the data modules for arrays, records, structs, and strings |
| `process.env` reads, a configuration object, secrets held as plain strings | `Config`, `ConfigProvider`, `Redacted` |
| Module-level singletons, clients passed through parameters, a homemade container | Services and `Layer` |
| A `fetch` wrapper, a router, middleware, multipart parsing, a hand-typed API client, hand-written OpenAPI | `effect/http`, `effect/http-api`, `effect/rpc`, `effect/graphql` |
| Database driver glue, manual transactions, migration scripts, hand-written repositories, query batching | `effect/sql`, with an `@effect/sql-*` driver |
| Async iterators, event emitters, batching, pagination loops | `Stream`, `Sink`, and their backpressure |
| A `Map` used as a cache, memoization, request deduplication | `Cache`, `ScopedCache`, `Request` and `RequestResolver` |
| A rate limiter, a circuit breaker, a key-value store, a persisted queue or cache | `effect/persistence` |
| `fs`, `path`, `child_process`, sockets, `worker_threads` | `FileSystem`, `Path`, `effect/process`, `effect/socket`, `effect/workers`, with an `@effect/platform-*` package |
| An argument parser, interactive prompts, shell completions | `effect/cli` |
| Hashing, password hashing, UUIDs, signing, encryption, JWT handling | `effect/crypto`, `effect/jose` |
| A CSV, YAML, TOML, XML, NDJSON, or server-sent events parser, base64 or hex helpers | `effect/encoding` |
| `console.log`, manual timing, passing trace identifiers around, a metrics endpoint | Effect logging, log annotations, spans, `Metric`, `effect/observability` |
| A provider SDK call to an LLM, parsing JSON out of model output, tool-call plumbing, an MCP server or client | `effect/ai`, with an `@effect/ai-*` provider |
| A cron library, a job runner, hand-made durable steps, an event log, a process that must run once across nodes | `Cron`, `Schedule`, `effect/workflow`, `effect/cluster`, `effect/eventlog` |
| Fake timers, module mocks | `effect/testing`, test layers, `@effect/vitest` |

The names in the right column come from Effect 4. Treat them as places to start looking, and confirm the exports in the installed package before you use them. The table does not list everything, so also search by the problem you have.

Start with what is already installed. Most capabilities ship inside `effect`. If you need a separate official `@effect/*` package that is not installed, such as a database driver or an LLM provider, prefer adding it over writing the mechanism yourself, and tell the user you added it.

## Choose the smallest complete solution

Take the first option that solves the problem:

1. An existing piece of this application that already does it correctly.
2. A public Effect or ecosystem API.
3. Plain TypeScript, for trivial pure computation or something Effect does not usefully cover.
4. A mature dependency, when it removes more maintenance than it adds.
5. Your own mechanism, only for a gap you can name.

For option 5, write down which APIs you checked and what specific capability was missing. If you cannot name the gap, there is no gap, so use the API.

Effect-first does not mean Effect everywhere. Leave direct arithmetic and obvious expressions as they are. Do not wrap a pure value in an effect, and do not replace a readable expression with a longer chain of combinators. Do not hide Effect behind your own facade. A service named for a domain concept that holds real application policy is useful, and a wrapper that only renames library functions is not. Do not add abstractions, options, or configuration for callers that do not exist yet.

## Keep the semantics intact

These properties are easy to lose when you write or move Effect code. Check each one that your change touches.

- **Errors.** Expected failures stay in the typed error channel. Do not turn failures into successes, convert them all into defects, or widen them to `unknown`. Keep defects and interruption distinct from expected failures.
- **Interruption.** A promise-based SDK enters Effect at one boundary. Pass the abort signal that Effect provides to the SDK, so interrupting the fiber cancels the request. Do not leave unmanaged promises, timers, or detached tasks running.
- **Resources.** A scope owns every resource and every background fiber. Anything acquired is released on success, on failure, and on interruption.
- **Runtime.** Build the production layers once, at the application's entry point, and run the program there. When a host that is not written in Effect calls into Effect, such as a framework's request handler, go through one shared `ManagedRuntime`. Do not build layers or run effects to promises ad hoc inside feature code.
- **Contracts.** Decode untrusted input with a schema at the boundary. Keep the nullability, field names, and types of the external API or database as they are. When a type is too loose, fix the contract rather than adding casts, non-null assertions, or repeated defensive checks.
- **Configuration.** One place owns each setting, its default, and its validation.
- **Guarantees.** Simplifying code must not remove backpressure, idempotency, transaction boundaries, or required validation.
- **Domain.** Keep business decisions separate from transport, persistence, and execution, so the rules stay easy to read and test.

## Before you hand off

1. Read your whole diff against the left column of the table. Replace every mechanism Effect already provides, and remove wrappers, options, and abstractions that nothing currently needs.
2. Test the behavior that matters: business decisions, error handling, interruption, resource release, retry policy, concurrency limits, and input contracts. Use the test clock and replaceable layers instead of real time and module mocks. Make sure each test double fails and cleans up the way the real service does. Skip tests that only restate types or check that a constructor exists.
3. Run the project's tests, type checking, and linting, and fix what fails. If the project uses the Effect language service, its diagnostics appear in the type check. Fix them like any other error.
4. Report what you changed, what you verified and how, and what you could not verify. For each custom mechanism you kept, name the missing capability that made it necessary.
