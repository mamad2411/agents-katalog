# eventplane

The suite's shared **event-plane** library: the producer and consumer plumbing
behind the internal SSE event plane, wired into consumers via a committed
`replace eventplane => ../eventplane`. It is a **library, not a service** (no
port, no nginx fragment, no `bin/run`, not deployable). The producer half
(`package outbox`) provides the atomic outbox on the caller's `*sql.Tx`, the
canonical schema DDL, the `GET /feed` SSE handler, the generation/epoch sidecar
token, and background retention. The consumer half (`package consumer`) provides
the reconnect/backoff engine that streams a producer's feed past a durable
per-upstream cursor and gates cursor advance on handler return. The normative
wire contract is `../docs/event-protocol.md`; on any conflict that doc wins.

## How changes are made

Changes go through the spec under `project/`, not direct edits, settle the
spec, then let the build loop realize it. Edit code directly only on explicit
operator instruction. See the `$ikispec` skill for the `project/` spec contracts
and `$ralph` for the unattended build workflow.

## Layout

- `outbox/`: producer half: outbox append, `SchemaSQL` DDL, `FeedHandler()`, epoch token, retention.
- `consumer/`: consumer half: feed engine, reconnect/backoff, `feed_offset` cursor, `SchemaSQL` DDL.
- `routing/`: event routing helpers (`routing.go`).
- `project/`: the spec (product/design/plan) the build loop works from.

## Tests

- Unit: `go test ./...` (workspace mode via the root `go.work`).

## Versioning

Not versioned. eventplane is a shared library consumed within the mono-repo,
with no `VERSION` file and no git tag.
