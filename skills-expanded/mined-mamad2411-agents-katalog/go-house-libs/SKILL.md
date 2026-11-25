---
name: go-house-libs
version: 0.6.1
description: Maps a need to the ralvarezdev shared Go modules — restkit, ginkit, pgkit, mcpkit (REST envelope and problem details, gin, Postgres, MCP), protos and connectrpckit (shared protobuf contracts and platform-service stubs, ConnectRPC servers and clients), identity and identitygin (accounts, auth, PATs), ratelimit, email, webpush, termkit (CLI UI), svckit (server lifecycle), tick (periodic jobs), sqlitekit (SQLite), resilience (retry, backoff, supervisor). Use when building or extending a Go API, MCP server, gRPC or Connect service, CLI, service or Postgres/SQLite store, before hand-writing envelopes, cursors, protobuf contracts, Connect servers or clients, pgtype conversions, auth, rate limiting, mail, push, a server start/shutdown block, a ticker loop, a retry loop or a SQLite open.
---

# Go House Libs

Small, reusable Go modules extracted from code that several projects repeated. This skill is for *using* them; [go-library-builder](../go-library-builder/SKILL.md) is for creating a new one. `email`, `ratelimit` and `webpush` follow its port-and-adapter shape (a port in the root package, adapters in technology-named subpackages), and `identity` its vertical-slice shape. `restkit`, `pgkit`, `mcpkit`, `termkit`, `svckit`, `tick`, `sqlitekit` and `resilience` are toolkits of helpers with no domain port, and `ginkit` and `identitygin` are framework adapter modules; the builder does not describe those two shapes. The cross-cutting rules live in the architect skills; the modules are how this house implements them.

## 1. Pick the package

Read the linked reference before wiring; it has the package layout, a recipe and the gotchas.

| Need | Package | Reference |
|---|---|---|
| Response envelope, list `Meta`, cursor token, RFC 9457 problems, typed HTTP client for a CLI or MCP, ETags, the idempotency contract, a `net/http` service without gin | `restkit` | [RESTKIT](references/RESTKIT.md) |
| Gin responders, validation, request-id, logger, recovery, body cap, CORS, `Idempotency-Key`, rate-limit middleware, handler test helpers | `ginkit` | [GINKIT](references/GINKIT.md) |
| pgx/sqlc value conversion, `RunInTx`, per-module goose migrations, Postgres idempotency store, pool metrics, container-backed DB tests | `pgkit` | [PGKIT](references/PGKIT.md) |
| MCP server: panic recovery, backend-delegated auth, per-caller state, error text for agents | `mcpkit` | [MCPKIT](references/MCPKIT.md) |
| User accounts, login, sessions, TOTP and WebAuthn, RBAC, personal access tokens | `identity` | [IDENTITY](references/IDENTITY.md) |
| Cookie and PAT auth middleware for gin on identity | `identitygin` | [IDENTITYGIN](references/IDENTITYGIN.md) |
| Throttle by key (user, IP, API key), in memory or shared through Valkey | `ratelimit` | [RATELIMIT](references/RATELIMIT.md) |
| Send email (SMTP, log-only, in-memory for tests) | `email` | [EMAIL](references/EMAIL.md) |
| Web Push with VAPID and a Postgres subscription store | `webpush` | [WEBPUSH](references/WEBPUSH.md) |
| Terminal UI: tables, charts, forms, session shell, dates, json/yaml/csv output | `termkit` | [TERMKIT](references/TERMKIT.md) |
| Transport-neutral error vocabulary (`Kind`, `Issue`) and small generic helpers | `corekit` | [COREKIT](references/COREKIT.md) |
| Shared protobuf contract types (pagination, error details, money, dates) | `protos` | [PROTOS](references/PROTOS.md) |
| gRPC server and client with house defaults: recovery, logging, request-id, validation, `corekit.Kind` → gRPC code mapping via `MapError`, bearer auth, the gRPC health service, reflection toggle | `grpckit` | [GRPCKIT](references/GRPCKIT.md) |
| ConnectRPC server/client with house defaults (recovery, logging, request-id, validation, corekit.Kind → connect.Code, health, reflection) | `connectrpckit` | [CONNECTRPCKIT](references/CONNECTRPCKIT.md) |
| Starting and stopping servers: bind failure that fails the process, graceful HTTP/gRPC shutdown, several services in a group, signals and exit codes | `svckit` | [SVCKIT](references/SVCKIT.md) |
| A periodic background job (reaper, pruner, refresh): no overlap, jitter, timeout, panic recovery | `tick` | [TICK](references/TICK.md) |
| Opening SQLite (modernc, pragmas on every connection, WAL, busy timeout) and embedded goose migrations | `sqlitekit` | [SQLITEKIT](references/SQLITEKIT.md) |
| Retry with backoff and jitter, a reusable backoff, a restart supervisor for goroutines | `resilience` | [RESILIENCE](references/RESILIENCE.md) |
| A secret from a file (`<VAR>_FILE`) instead of the environment, or rejecting secrets in a TOML config | `viperkit` | [VIPERKIT](references/VIPERKIT.md) |

## 2. Shape and dependency direction

- **The root package is the port.** `restkit`, `email`, `ratelimit` and `webpush` import no third-party code at their root; adapters live in subpackages (`smtp`, `valkey`, `vapid`, `postgres`). An app depends on the port (`email.Mailer`, `ratelimit.Limiter`, `webpush.Sender`) and picks the adapter in its bootstrap package.
- **Direction**: `ginkit -> restkit, ratelimit`; `pgkit -> restkit`; `identity -> email, pgkit, ratelimit`; `identitygin -> identity`; `webpush -> pgkit`; `connectrpckit -> corekit`; `grpckit -> corekit`; `sqlitekit`, `svckit`, `tick` and `resilience` are leaves that import no other kit, and `corekit` and `protos` are leaves too (`corekit` is the shared error vocabulary and `xconv` helpers; `protos` is a contract module with no kit imports). Never the reverse, and never a kit importing a consumer. `ginkit` uses an idempotency store through `restkit/idempotency`, so it never imports `pgkit`.
- **Connect is gRPC's sibling, not a replacement.** `connectrpckit` is the Connect counterpart of `grpckit` over the same `corekit` error vocabulary: one generated service behind one `http.Handler` serves the Connect, gRPC and gRPC-Web protocols. A service that speaks Connect depends on both `connectrpckit` (transport) and `protos` (contract types), and keeps the port protocol-agnostic so a `grpckit` adapter can replace the Connect one without a rewrite. Both `grpckit` and `connectrpckit` map a handler's `*corekit.Error` to their own code through `corekit.Kind`, so a service returns `*corekit.Error` and stays transport-agnostic.
- **Adapters own their dependency**, per package: gin in `ginkit`; goose in `pgkit/migrate` and `sqlitekit/migrate`; modernc.org/sqlite in `sqlitekit`; testcontainers in `pgkit/pgtest`; Prometheus in `pgkit/pgmetrics`; Valkey in `ratelimit/valkey`; go-mail in `email/smtp`; `webpush-go` in `webpush/vapid`; the MCP SDK in `mcpkit`. A consumer that does not use one must not pull it in.
- A different HTTP framework gets its own `<framework>kit` adapter, not a branch inside `restkit`.

## 3. Rules

- **Do not hand-write lifecycle, ticker, retry or SQLite-open code.** A `go srv.ListenAndServe()` that only logs on failure while `main` waits on `ctx.Done()` idles forever on a bind error (`svckit.Serve`); a `time.NewTicker` select loop is `tick.Every`; an `Exec("PRAGMA ...")` or a mattn-style DSN (`_journal_mode=`) on modernc leaves SQLite without WAL or a busy timeout (`sqlitekit`); a retry that retries every error with no jitter belongs in `resilience/retry`.
- **Do not re-declare a kit type locally.** A second `Response[T]`, cursor codec, `pgtype` helper or mailer interface is a bug; import the module.
- **A project keeps one wire contract.** A project that adopted the `restkit.Response` envelope keeps it (`Meta` camelCase, bodies snake_case; its frontend, CLI and MCP clients depend on it). A project built on bare resources keeps returning them with problem+json errors: adopt the middleware and `problem` there, not the envelope. New projects start on RFC 9457.
- **Do not leak internals on 5xx.** Never pass `err.Error()` to `ginkit.Err` for a 5xx: log the real error, answer with a generic message, and show the raw text only in debug mode (`problem.RedactServerError`, or an app-level helper that does the same). Tool errors to agents go through `mcpkit.ErrorMsg`.
- **Idempotency fails closed.** A store outage refuses the request, never runs the handler; release the key on 5xx or panic.
- **Generated code is types only.** oapi-codegen never generates a client or server; hand-write calls on `restkit/client.Do`.
- **Infrastructure is its own module, not part of the app or identity.** Rate limiting is not login throttling (`identity/auth.AttemptLimiter`); email and push are not identity concerns. Wire them, do not fold them in.
- **Promote only with a second consumer.** Code moves into a module when a second project needs it (`svckit`, `tick`, `sqlitekit` and `resilience` were created once four to six projects repeated the same code). The exception is `mcpkit`, extracted up front for planned reuse and kept on v0.x until a second MCP server adopts it.
- **Verify a release against its previous tag** (`git diff <prev-tag>`) before labelling it additive, and check `STACK.md`: modules pin older siblings, so the consumer's `go.mod` may resolve a different version than the latest tag.
- **A tag is a promise about behavior.** A change that turns a call that returned nil into an error (for example `webpush` `Send`) is breaking for callers even when the signature is unchanged; say so in the commit and the docs.

## 4. Adding to a module

1. Confirm a second consumer exists and the code imports no project domain package.
2. Add it to the narrowest module that fits (§1, §2), with a test.
3. Tag, then migrate the consumer in one commit and delete the local copy.
4. Update the module's file in `references/`, the table in §1, and [STACK.md](STACK.md) (tag, pins, consumers).

A new module gets its own `references/<NAME>.md` (UPPER_SNAKE_CASE) and a row in §1. See [STACK.md](STACK.md) for tags, Go versions, dependency pins and consumers.
