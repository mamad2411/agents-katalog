---
license: CC-BY-4.0
compatibility: >-
  opencode CLI on PATH (the JS factory spawns `opencode serve`). JS/TS
  @opencode-ai/sdk, released with OpenCode; checked against 1.18.33 source on
  2026-09-29. Go module github.com/sst/opencode-sdk-go v0.19.2 (latest tag,
  2025-12-18), Go 1.22+ per its go.mod.
description: >-
  Drive OpenCode (opencode.ai, the open-source coding agent) programmatically — the
  @opencode-ai/sdk JS/TS client, the github.com/sst/opencode-sdk-go Go client,
  and the `opencode serve` HTTP/OpenAPI server it talks to. Use when building an
  integration on top of OpenCode, calling createOpencode / createOpencodeClient,
  running `opencode serve`, hitting the OpenAPI spec at /doc, listing or prompting
  sessions over HTTP, wiring OPENCODE_SERVER_PASSWORD auth, requesting structured
  (json_schema) output, or using opencode.NewClient / Session.List / the Field
  param wrappers in Go. NOT OpenAI Codex; NOT the opencode.ai/docs/go Zen
  subscription.
argument-hint: "What do you want to build on the OpenCode SDK/server? (e.g. 'prompt a session over HTTP and get JSON back', 'spin up a server from Node', 'list sessions in Go')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode SDK & server

Control OpenCode the way the TUI does: the TUI is itself a client of the `opencode serve`
HTTP server, so the SDK can do anything the TUI does. SDK types are **generated from the
server's OpenAPI 3.1 spec** — the spec at `/doc` is the real contract; the SDK is a typed
shell over it.

> **Verify-canonical guard.** OpenCode's API moves fast and predates the model's training
> cutoff. Before writing SDK code, read `references/sdk.rst` (+ `server.rst`, `go.rst`)
> and re-check <https://opencode.ai/docs/sdk/>. **The docs page lags the package:** when
> it disagrees with the generated types (`packages/sdk/js/src/v2/gen/types.gen.ts` at the
> installed release tag of `github.com/anomalyco/opencode`) or the server's `GET /doc`,
> the types win. If the installed version differs from the pins below or the source is
> unreachable, say so and treat method shapes as unverified; don't upgrade the user's
> project to match this file.

## SDK provenance (this skill owns it)

Other `opencode-dev` skills route here for SDK versions instead of copying them.

| Thing | Pin / fact | Checked |
|---|---|---|
| JS package | `@opencode-ai/sdk`, versioned with OpenCode itself (1.18.33 at tag `v1.18.33`) | source, 2026-09-29 |
| JS entry points | `@opencode-ai/sdk` (v1 types, `{ path, body }` params) and `@opencode-ai/sdk/v2` (flat params, e.g. `{ sessionID, parts, format }`) | source |
| Go module | `github.com/sst/opencode-sdk-go@v0.19.2` — latest tag (2025-12-18); repo now `github.com/anomalyco/opencode-sdk-go`, import path still `sst` | tags + `go.mod`, 2026-09-29 |
| Go toolchain | Go 1.22+ (`go 1.22` in `go.mod`) | `go.mod` |
| Plugin types | `@opencode-ai/plugin` — same release line; API owned by `/opencode-dev:plugin` | source |

The Go SDK is generated from an **older** server API than the JS package: v0.19.2 has
no structured-output `format` field on `SessionPromptParams`. Use raw requests
(`client.Post`) or the JS SDK for newer endpoints.

## Pick your entry point

| You want to… | Use | From |
|---|---|---|
| Spawn a server **and** get a client in one Node call | **`createOpencode()`** | `@opencode-ai/sdk` or `/v2` |
| Connect to an **already-running** server | **`createOpencodeClient({ baseUrl })`** | `@opencode-ai/sdk` or `/v2` |
| Spawn only the server (`{ url, close }`) | `createOpencodeServer()` — exported by the package, not shown on the docs page | `@opencode-ai/sdk` |
| Drive from Go | **`opencode.NewClient(option.WithBaseURL(…))`** | `github.com/sst/opencode-sdk-go` |
| Talk raw HTTP / any language | `opencode serve` + the endpoints in `references/server.rst` | OpenAPI at `/doc` |

The root `createOpencode`'s `client` is the same type as `PluginInput.client` — code
written against the root entry point is reusable inside a plugin.

## `opencode serve` — the server

```
opencode serve [--port 4096] [--hostname 127.0.0.1] [--cors <origin>] [--mdns] [--mdns-domain <d>]
```

- Defaults: host **`127.0.0.1`** (loopback-only); port **`4096`**, falling back to a free
  port when 4096 is taken and no `--port` was given (v1.18.33 `server.ts`).
- **Auth is opt-in via env, not flags:** set `OPENCODE_SERVER_PASSWORD` to require HTTP basic
  auth; username defaults to `opencode` (override with `OPENCODE_SERVER_USERNAME`). No password
  set ⇒ no auth.
- `--cors` is **repeatable** (pass once per origin); browsers need it, server-to-server doesn't.
- **OpenAPI 3.1 spec lives at `GET /doc`** — fetch it to regenerate types or to find any
  endpoint not yet wrapped by the SDK. This is the source of truth, not this file.

Endpoint traps (full list in `references/server.rst`):
- Health is **`GET /global/health`** (returns `{ healthy, version }`), not `/health`.
- Send-and-wait is `POST /session/:id/message`; fire-and-forget is **`POST /session/:id/prompt_async`**.
- Search is `GET /find?pattern=`, files `GET /find/file?query=`, symbols `GET /find/symbol?query=`,
  read `GET /file/content?path=`.
- SSE event streams: `GET /event` and `GET /global/event`.

## JS/TS client

```javascript
import { createOpencode } from "@opencode-ai/sdk/v2"   // or "@opencode-ai/sdk" for v1 shapes
const { client, server } = await createOpencode()     // server.url, server.close()
```

`createOpencode` options: `hostname` (`127.0.0.1`), `port` (`4096`), `timeout` (`5000`),
`signal`, `config` (an inline `Config`, passed as `OPENCODE_CONFIG_CONTENT`, so it is merged
over `opencode.json`). It spawns the `opencode` binary from `PATH`. Always
`await server.close()` when done — the factory owns the spawned process.

`createOpencodeClient` options: `baseUrl` (`http://localhost:4096`), `fetch`, `parseAs`,
**`responseStyle`** (`"fields"` default | `"data"`), **`throwOnError`** (default `false`).
The default style returns `{ data, error, … }` — results are read as **`result.data.…`**,
so a missing `.data` is the usual "why is my field undefined" bug, and HTTP errors come
back in `result.error` rather than throwing.

API surfaces are **namespaced objects**, not flat: `client.global.health()`,
`client.app.log()/agents()`, `client.project.list()/current()`, `client.session.*`
(`list/get/create/update/delete/prompt/command/shell/messages/abort/share/init/revert/…`),
`client.find.text/files/symbols`, `client.file.read/status`, `client.tui.*`,
`client.auth.set`, `client.event.subscribe()`. Full method list in `references/sdk.rst`.
Parameter shapes differ by entry point: root `session.prompt({ path: { id }, body })`,
v2 `session.prompt({ sessionID, parts, … })`.

### Structured output (the json_schema path)

`format` is typed only in the **v2** entry point; the root (v1) `session.prompt` body type
has no `format` field (1.18.33 types).

```javascript
import { createOpencode } from "@opencode-ai/sdk/v2"
const result = await client.session.prompt({
  sessionID,
  parts: [{ type: "text", text: "…" }],
  format: { type: "json_schema", schema: { /* JSON Schema */ }, retryCount: 2 },
})
const info = result.data?.info
if (info?.error?.name === "StructuredOutputError") {
  console.error(info.error.data.message, info.error.data.retries) // fields live under .data
} else {
  console.log(info?.structured)  // the parsed object
}
```

- `format.type` is `"text"` (default) or **`"json_schema"`**; the schema goes in
  `format.schema`, retries in `format.retryCount` (default `2`).
- Under the hood the model is forced through a `StructuredOutput` tool. On failure
  `info.error.name === "StructuredOutputError"` — **the call still resolves**, so guard on
  the error field rather than a `try/catch`.
- **The docs page is wrong on two names** (checked 2026-09-29): the parsed object is
  `info.structured` (docs: `structured_output`), and the error's `message`/`retries` sit
  under `info.error.data` (docs: directly on `error`). Source: `AssistantMessage` and
  `StructuredOutputError` in `v2/gen/types.gen.ts`, `session/prompt.ts`.

See `assets/hello-sdk.ts` for a spawn → prompt → structured-output → close flow
(checked against the 1.18.33 types by reading; not compiled here).

## Go client

```go
import (
	"github.com/sst/opencode-sdk-go"
	"github.com/sst/opencode-sdk-go/option"
)
client := opencode.NewClient(option.WithBaseURL("http://127.0.0.1:4096/"))
sessions, err := client.Session.List(context.TODO(), opencode.SessionListParams{})
```

- **Set the base URL.** v0.19.2's default is `http://localhost:54321/`
  (`option.WithEnvironmentProduction`), not the server's `4096`; `NewClient()` also reads
  `OPENCODE_BASE_URL`. Without either, requests go to the wrong port.
- **Every request param is wrapped in a `Field`** to separate zero/null/omitted. Build with
  `opencode.F(v)`, `opencode.Null[T]()`, `opencode.Raw[T](any)` (and `String/Int/Float`
  helpers). A bare `""`/`0` is **not sent** unless wrapped — forgetting `F()` silently omits it.
- Response fields are plain value types; inspect presence via the per-field
  `res.JSON.<Field>.IsNull()/IsMissing()/IsInvalid()` and undocumented keys via
  `res.JSON.ExtraFields[...]`.
- Errors: `errors.As(err, &apiErr)` into **`*opencode.Error`** (`StatusCode`,
  `DumpRequest/DumpResponse`). Retries default to **2** (connection errors, 408/409/429/≥500);
  **no default timeout** — set one via `context` + `option.WithRequestTimeout()`.
- Reach endpoints the Go SDK lacks with `client.Get/Post(...)` and `option.WithJSONSet/WithQuerySet`.

Configure headers/auth via the `option` package. See `assets/hello-sdk.go`. Full API in
the SDK's own `api.md`.

## Traps to avoid

- ⚠️ **`opencode.ai/docs/go/` is the wrong page for the Go SDK** — it documents the paid
  "OpenCode Go" model subscription, not the library. The Go *SDK* is
  `github.com/sst/opencode-sdk-go` (see `references/go.rst`).
- ⚠️ **This is OpenCode, not OpenAI Codex.** Don't import Codex/`app-server` APIs.
- ⚠️ No Python package is officially verified (JS/TS + Go only).
- ⚠️ JS results are under **`result.data`** (default `responseStyle`); structured-output
  failures surface as `info.error`, not a thrown exception (unless `throwOnError`).

## Reference & example files

| File | Contents |
|---|---|
| [references/sdk.rst](references/sdk.rst) | JS/TS SDK — factories, options, all `client.*` methods, structured output |
| [references/server.rst](references/server.rst) | `opencode serve` flags, env auth, full endpoint list, OpenAPI `/doc` |
| [references/go.rst](references/go.rst) | Go SDK — install/pin, `NewClient`, `Field` wrappers, errors, retries, options |
| [assets/hello-sdk.ts](assets/hello-sdk.ts) | Node: spawn server → create session → structured prompt → close |
| [assets/hello-sdk.go](assets/hello-sdk.go) | Go: `NewClient` → `Session.List` with `*opencode.Error` handling |

Related facets: programmatic tool/hook code → `/opencode-dev:plugin`; delegating from a
Claude Code plugin (ACP / `serve` / `opencode run`) → `/opencode-dev:delegate`.
