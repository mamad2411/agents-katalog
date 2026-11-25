---
name: surfbird
description: Use a running Surfbird (self-hosted Kitesurf browser engine) instance to fetch pages, extract article markdown, take screenshots, render PDFs, and run page JS — via plain REST, no MCP or CDP client required.
---

# Surfbird REST client

Surfbird exposes a small REST layer over a real browser engine. You only need `curl`.

## Setup

Environment (ask the user if unset):
- `SURFBIRD_URL` — proxy base, e.g. `http://<vps>:8080`. The REST layer lives on the **auth image only** — a raw image's `:8787` is the bare engine (CDP + `/json/*` + `/rbi/*`) and has none of the endpoints below.
- `SURFBIRD_TOKEN` — bearer token for auth images

## Endpoints

| Method + path | Body | Returns |
|---|---|---|
| `POST /markdown` | `{"url"}` | `{title, markdown, byline, excerpt}` — article body as markdown (Readability+turndown). **Prefer this for articles** |
| `POST /content` | `{"url"}` | `{title, url, html}` — full rendered DOM (post-JS) |
| `POST /source` | `{"url"}` | `{title, url, html}` — "view source" HTML (original body, or same-origin re-fetch when the engine doesn't keep it) |
| `POST /screenshot` | `{"url","width"?,"fullPage"?}` | PNG bytes |
| `POST /pdf` | `{"url","landscape"?}` | PDF bytes |
| `POST /evaluate` | `{"url","script"}` | `{result}` — JS evaluated in page context |
| `POST /batch` | `{"action","urls"[,"script"]}` | `[{url, ok, status, data|error}]` — one action over up to `MAX_BATCH_URLS` (20) urls, sequential |
| `GET /health` | — | `{status, engine, cdpEndpoint}` — liveness + CDP WebSocket URL (no auth needed) |

## Examples

```bash
# article → markdown
curl -s -X POST "$SURFBIRD_URL/markdown" \
  -H "Authorization: Bearer $SURFBIRD_TOKEN" -H 'content-type: application/json' \
  -d '{"url":"https://zhuikan.com/repos/terry2010__surfbird"}' | jq -r .markdown

# screenshot
curl -s -X POST "$SURFBIRD_URL/screenshot" \
  -H "Authorization: Bearer $SURFBIRD_TOKEN" -H 'content-type: application/json' \
  -d '{"url":"https://zhuikan.com/repos/terry2010__surfbird","fullPage":true}' -o page.png

# run JS (e.g. collect all links)
curl -s -X POST "$SURFBIRD_URL/evaluate" \
  -H "Authorization: Bearer $SURFBIRD_TOKEN" -H 'content-type: application/json' \
  -d '{"url":"https://zhuikan.com/repos/terry2010__surfbird","script":"[...document.querySelectorAll(\"a\")].map(a=>a.href)"}'
```

## CDP 直连（交互式控制）

The REST layer is one-shot: every call opens a fresh page and discards it. For
interactive control — persistent tabs, clicking, typing, screenshots, console
and network inspection — connect to the engine's CDP WebSocket directly:

- **Endpoint**: `ws(s)://<host>/devtools/browser`
  - auth image: `ws://<vps>:8080/devtools/browser` — send
    `Authorization: Bearer $SURFBIRD_TOKEN` on the WS handshake (proxy checks it)
  - raw image: `ws://<vps>:8787/devtools/browser` — no auth (loopback only!)
  - upstream kitesurf (`wrangler dev`): same path, no auth
- **Discovery**: `GET /health` returns `cdpEndpoint` with the right scheme/host
- **Semantics**: one WebSocket = one isolated browser (per-connection state).
  `Target.createTarget`/`attachToTarget`/`Target.*` manage multiple tabs inside
  it. Closing the socket destroys every tab — there is no cross-connection state.
- **Limits**: idle disconnect after ~10 min without traffic (send any CDP
  message as keepalive), hard 60 min per connection. Reconnect = fresh browser.
- **Engine boundaries** (upstream Kitesurf, not fixable here): no JS dialogs,
  no file upload/download, no clipboard, no touch/drag, partial hit-testing,
  Boa instead of V8.
- **Agent plugins**: for DSH/OpenCode/Pi, prefer a control plugin over hand-
  rolling CDP — e.g. `dsh-control-surfbird-for-kitesurf` (DSH, `surfbird_*`
  tools) at https://github.com/terry2010/dsh-control-surfbird-for-kitesurf.

## Notes

- Every request opens a fresh isolated page — no cookies/session carry over. For logged-in flows do the steps inside one `/evaluate` script.
- Requests are rate-limited server-side (`MAX_CONCURRENT_ACTIONS`, default 2) — serialize bulk fetches or expect queuing, not errors.
- Failures: `401` = bad/missing token, `502` = engine error (often TLS/network on the target site), `504` = action timed out, `413` = body over `MAX_BODY_BYTES`, `422` = Readability found no article (try `/content` and extract yourself).
- Engine limits (upstream, not fixable here): no video decode, no file downloads, no touch gestures, JS engine is Boa not V8 — exotic sites may mis-render.
