# connect-sse

Server-Sent Events transport for [connect-go](https://connectrpc.com/connect). Wraps Connect's `NewServerStreamHandler` with the SSE wire format so browsers can consume server-streaming RPCs over plain `fetch` (no gRPC-Web full-duplex requirement).

## Build & Test

Requires Go 1.25+.

```bash
go test -race ./...
```

No Makefile — single-package library.

## Key files

- `client.go` — SSE client wrapping a Connect server-stream client.
- `server.go` — SSE handler wrapping a Connect server-stream handler.
- `doc.go` — package doc.
- `compression_test.go`, `client_test.go`, `server_test.go`, `example_test.go` — tests.
- `proto/example/greet/v1/greet.proto` — fixture service used by tests.

## Wire format invariants

The SSE framing is the public contract. Changing any of these is a **breaking change** — bump major.

- One SSE event per protobuf record: `event:` line + `data:` line + blank line.
- Compression negotiation via `Accept-Encoding`: `gzip` and `identity` only.
- Error frames are emitted as a final `event: error` with the connect error JSON in `data:`.
- End-of-stream marker is the EOF on the SSE response stream (no explicit terminator frame).

When `client.go`, `server.go`, or `compression_test.go` change in a way that affects framing, also publish a coordinated PR to `firetiger-oss/connect-aip` — its generated clients depend on the public types here.

## Upstream version bumps

When `connectrpc.com/connect` bumps in `go.mod`, re-run `go test -race ./...` and verify `example_test.go` still exercises a real connect-go server end-to-end (not a mocked one).

## Release cut

Tag `vX.Y.Z` from `main`; `release.yml` auto-creates a GitHub Release with auto-generated notes. No binary assets — pure Go library, distributed via `go install` / `go get` only.

See `.claude/skills/release.md` for the full release flow.
