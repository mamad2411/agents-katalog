---
name: design-protobuf-grpc-service
description: Designs and evolves gRPC/protobuf service contracts — message and service definitions, unary vs streaming RPC selection, wire-compatible schema evolution (reserved tags, safe vs breaking changes), canonical status codes, deadlines/cancellation, interceptors, and buf-driven codegen plus breaking-change detection.
when_to_use: User is writing or changing a .proto/gRPC service, picking unary vs streaming, worried about breaking wire compat on a rolling deploy, wiring multi-language codegen, or adding deadlines/auth/error semantics. This is the binary RPC contract; HTTP/JSON REST or GraphQL surfaces are rest-graphql-contract.
---

## When to Use

Reach for this skill when the contract is a **.proto / gRPC wire format**, not an HTTP/JSON shape:

- "Design the messages and RPCs for this new service" / "add a method to this `.proto`"
- "Is renaming/renumbering this field safe to deploy?" — wire-compat review
- "Should this be unary, server-streaming, or bidi?" / "stream vs websocket?"
- "Wire codegen for Go + TS + Python off one schema" / "set up `buf` + breaking-change CI"
- "Set deadlines / map our errors to gRPC status codes / add an auth interceptor"
- "Expose this to a browser" → gRPC-Web / Connect

NOT this skill:
- REST resources, JSON envelopes, OpenAPI/SDL, HTTP versioning/pagination → rest-graphql-contract
- Reviewing an existing HTTP/RPC API *diff* for naming/compat as an audit pass → api-design-review
- Issuing/verifying JWTs, OAuth/OIDC flows, RBAC logic (the interceptor *calls* this) → auth-jwt-session
- Adding tracing/metrics/logs to the service internals → observability-instrument
- Correctness of the streaming/concurrency code itself (races, missing await) → async-concurrency-correctness

## Steps

1. **Model messages — field numbers are the contract, names are not.** The tag number is what goes on the wire; renaming a field is free, renumbering is catastrophic.
   - Number `1–15` cost 1 byte; reserve them for the hot, always-present fields. `16+` cost 2 bytes.
   - **Removing a field:** delete it *and* `reserved` both its number and name, so nobody reuses them. This is non-negotiable.
     ```proto
     message User {
       reserved 4, 7 to 9;            // retired tags — never reuse
       reserved "email_verified";     // retired name — block re-add under old meaning
       string id = 1;
       string display_name = 2;
       optional string email = 3;     // optional => field presence (knows set-vs-default)
     }
     ```
   - Use `optional` (proto3) when you must distinguish "unset" from zero-value; bare scalars can't tell `0`/`""`/`false` from absent.
   - **Every enum starts at `0 = *_UNSPECIFIED`.** 0 is the default on the wire; if 0 means a real state you can't detect "not set," and you can't safely add values before it.
     ```proto
     enum Status { STATUS_UNSPECIFIED = 0; STATUS_ACTIVE = 1; STATUS_BANNED = 2; }
     ```
   - Prefer `google.protobuf.Timestamp`/`Duration` over raw int64; `map<k,v>` over parallel lists; a `Money{currency_code, units, nanos}` message over a float. Never put currency in a `double`.

2. **Pick the RPC shape from the data flow — default to unary.** Streaming is for unbounded or incremental data, not for "it's faster."

   | Shape | Signature | Use when | Don't use for |
   |---|---|---|---|
   | **Unary** | `rpc Get(Req) returns (Resp)` | request/response, bounded payload — **the default** | huge/unbounded results |
   | Server-streaming | `returns (stream Resp)` | feed/tail, large result set, server-push progress | a single object that fits in memory |
   | Client-streaming | `(stream Req) returns (Resp)` | chunked upload, batch ingest, client-side aggregation | small fixed-size input |
   | Bidi | `(stream Req) returns (stream Resp)` | live chat, long-lived sync, interactive session | anything a sequence of unary calls covers |

   - **Stream vs websocket:** if both ends are gRPC and you need typed messages + backpressure + deadlines, use a gRPC stream. Reach for a websocket only when a *browser* needs raw duplex and you're not on Connect/gRPC-Web.
   - Page large reads with `page_size`/`page_token` (AIP-158) **before** reaching for server-streaming — pagination is resumable and cacheable; a broken stream restarts from zero.

3. **Run the wire-compat checklist before any schema change** — clients and servers deploy at different times, in multiple languages, and old binaries must keep parsing new messages.

   | Change | Wire-safe? | Why |
   |---|---|---|
   | Add a new field (new tag) | ✅ | old readers skip unknown fields |
   | Add a new RPC / new message | ✅ | additive |
   | Rename a field (same tag/type) | ✅ wire / ⚠️ JSON | wire keys on number; **gRPC-JSON/Connect keys on name** — breaks JSON clients |
   | Add an enum value | ✅ | but old clients see it as the unknown/default — handle that branch |
   | `int32`↔`int64`, `sint`↔`int`, `optional`↔`repeated` | ❌ | different wire encoding → silent corruption |
   | Reuse / renumber a tag | ❌ | old data deserializes into the wrong field |
   | Remove a field without `reserved` | ❌ | tag can be reused later → corruption |
   | Change a field's type/cardinality | ❌ | re-version the message or add a new field instead |
   | Rename/move a service or package | ❌ | path is `/pkg.Service/Method` — old stubs 404 with `UNIMPLEMENTED` |

   To evolve incompatibly: **add a new field/method, deprecate the old (`[deprecated = true]`), migrate, then `reserved` it** — never mutate in place. Enforce this with `buf breaking` (step 6).

4. **Error & control plane — set a deadline on every call, return canonical codes.**
   - **Deadlines are mandatory.** A call without one can hang forever and pin a server thread. Set an absolute deadline client-side (`context.WithTimeout`, ~the SLO); servers must check `ctx.Err()`/`isCancelled` and stop work when the client gives up. Propagate the deadline to downstream calls — don't reset it.
   - Map failures to the [canonical status codes](https://grpc.io/docs/guides/status-codes/), not a generic `UNKNOWN`/`INTERNAL`:

     | Code | Use for | Retry? |
     |---|---|---|
     | `INVALID_ARGUMENT` | malformed request, fails regardless of state | no |
     | `FAILED_PRECONDITION` | valid request, wrong system state | no (fix state first) |
     | `NOT_FOUND` / `ALREADY_EXISTS` | missing / duplicate resource | no |
     | `PERMISSION_DENIED` / `UNAUTHENTICATED` | authz fail / missing-bad creds | no |
     | `RESOURCE_EXHAUSTED` | quota / rate limit | yes, with backoff + honor `Retry-After`-style detail |
     | `DEADLINE_EXCEEDED` | call ran past deadline | yes if idempotent |
     | `UNAVAILABLE` | transient — server down/restarting | yes, backoff (the canonical retryable code) |
     | `ABORTED` | concurrency conflict (CAS/txn) | yes, after re-read |

   - Attach machine-readable detail with `google.rpc.Status` + typed details (`ErrorInfo` with a stable `reason` + `domain`, `BadRequest.field_violations`, `QuotaFailure`) — not a prose string clients must regex.
   - **Retry only idempotent methods.** Configure a service-config retry policy (`maxAttempts`, `UNAVAILABLE`/`DEADLINE_EXCEEDED` only, exponential backoff). For non-idempotent creates, pass a client-generated idempotency key in metadata and dedupe server-side. Cancellation propagates automatically when the client closes the stream/context — release resources on it.

5. **Cross-cutting concerns belong in interceptors + metadata, not in every method.**
   - **Interceptors** (chained, ordered) for auth, logging, tracing, panic-recovery, rate-limit. Auth interceptor reads the token from metadata and *delegates verification* (that logic lives in auth-jwt-session) — return `UNAUTHENTICATED` (missing/invalid creds) vs `PERMISSION_DENIED` (valid identity, not allowed).
   - **Metadata** = gRPC's headers/trailers. Lowercase ASCII keys; a key carrying raw bytes must end in `-bin` (e.g. `trace-id-bin`) so the runtime base64-handles it. Carry auth (`authorization: Bearer …`), request id, idempotency key, locale. Never put a deadline in metadata — it's a first-class call property. Reserved `grpc-*` keys are runtime-owned; don't set them yourself.
   - **TLS always; mTLS for service-to-service.** Never run a non-loopback gRPC server on an insecure channel — h2c in the clear leaks every byte.
   - **Browser/edge:** native gRPC needs HTTP/2 trailers a browser can't send, so expose **Connect** (speaks gRPC, gRPC-Web, *and* JSON over the same handler — easiest) or **gRPC-Web** behind an Envoy/proxy translation layer. Don't try to call raw gRPC from `fetch`.

6. **Codegen + lint with `buf`, not raw `protoc` — and wire breaking-change detection into CI.** `protoc` plugin/path juggling is the classic footgun; `buf` makes the schema the source of truth.
   ```yaml
   # buf.yaml
   version: v2
   lint:   { use: [STANDARD] }
   breaking: { use: [WIRE_JSON] }   # catch tag/type/name breakage
   ```
   ```yaml
   # buf.gen.yaml — one schema, many languages
   version: v2
   plugins:
     - { remote: buf.build/protocolbuffers/go,    out: gen/go,  opt: paths=source_relative }
     - { remote: buf.build/connectrpc/go,         out: gen/go,  opt: paths=source_relative }
     - { remote: buf.build/bufbuild/es,           out: gen/ts }
   ```
   ```bash
   buf lint                                   # naming/style/UNSPECIFIED rules
   buf breaking --against '.git#branch=main'  # FAIL CI on any wire/JSON break
   buf generate                               # regenerate all stubs from .proto
   ```
   Check generated stubs into VCS *or* regenerate in CI — pick one and enforce it; a stale committed stub that disagrees with the `.proto` is a silent contract drift. Back the contract with a contract test (step in Verify) so the running server and the `.proto` can't diverge.

## Common Errors

- **Reusing or renumbering a field tag.** Old bytes deserialize into the wrong field — silent data corruption, no error. Always `reserved` removed tags *and* names; `buf breaking` catches it if you let it.
- **Enum without `0 = *_UNSPECIFIED`.** 0 is the wire default, so you can't distinguish "unset" from your first real value, and you can't prepend values later. Always reserve 0 for UNSPECIFIED.
- **No deadline on the call.** One slow/hung downstream pins server resources indefinitely and cascades into outage. Set an absolute deadline on every client call; propagate, don't reset, downstream.
- **Returning `INTERNAL`/`UNKNOWN` for everything.** Clients can't tell retryable from fatal and either hammer a down service or give up on a transient blip. Map to the specific canonical code; reserve `INTERNAL` for genuine server bugs.
- **Retrying non-idempotent RPCs.** A retried `Create`/`Charge` after a timeout double-executes. Restrict the retry policy to idempotent methods; for the rest use a server-deduped idempotency key.
- **Changing a scalar type to a "compatible-looking" one** (`int32`→`int64`, `optional`→`repeated`). Different wire encoding → garbled values on old readers. Add a new field instead and migrate.
- **Renaming a field assumed free, but a Connect/gRPC-JSON client keys on the name.** Wire-safe, JSON-breaking. If any client speaks JSON, treat a rename as breaking.
- **Calling raw gRPC from a browser.** Native gRPC needs HTTP/2 trailers the browser can't produce. Use Connect or gRPC-Web through a proxy.
- **`protoc` plugin/import-path hell producing stale or wrong stubs.** Use `buf` with a remote plugin set so paths and versions are pinned and reproducible.
- **Insecure (h2c, no TLS) channel in prod.** Everything including bearer tokens is in cleartext. TLS always; mTLS between services.
- **Breaking-change check missing from CI.** A bad merge ships an incompatible schema and breaks every deployed client. `buf breaking --against main` must gate merges.

## Verify

1. **Lint clean:** `buf lint` passes — every enum has `*_UNSPECIFIED = 0`, fields snake_case, services/methods follow the standard naming rules.
2. **Breaking-change gate:** `buf breaking --against '.git#branch=main'` is green; deliberately renumber a tag locally and confirm it goes **red** (proves the gate actually fires).
3. **Codegen reproducible:** `buf generate` from a clean tree produces stubs byte-identical to what's committed (no uncommitted diff) for every target language.
4. **Wire round-trip across versions:** serialize a message with the *new* schema, parse it with a binary built on the *old* schema (and vice-versa) — no error, no field loss for additive changes. This is the real proof of compatibility, not eyeballing the diff.
5. **Deadline honored:** a call given a 100ms deadline against an artificially slow method returns `DEADLINE_EXCEEDED` near 100ms (not hanging), and the server logs show it cancelled work rather than running to completion.
6. **Status mapping:** each error path returns its specific canonical code (asserted in tests), and retry policy retries `UNAVAILABLE`/`DEADLINE_EXCEEDED` only — a deliberate `INVALID_ARGUMENT` is not retried.
7. **Streaming flow:** a server-stream consumer that cancels mid-stream causes the server's context to cancel and stop producing (no leaked goroutine/thread); a client-stream upload that drops mid-send leaves no half-written state.
8. **Auth interceptor:** missing token → `UNAUTHENTICATED`; valid token without permission → `PERMISSION_DENIED`; both asserted, and the path runs over TLS (insecure channel rejected).
9. **Contract test:** a cross-language client built from the generated stub calls the running server end-to-end and gets the expected typed response — proves `.proto`, server, and stubs agree.

Done = `buf lint` and `buf breaking --against main` pass in CI (and the gate provably fails on a real break), `buf generate` leaves no diff, the old↔new wire round-trip and the cross-language contract test both pass, every call sets a deadline, and each error path returns its specific canonical status code over TLS.
