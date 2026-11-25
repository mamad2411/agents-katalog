---
name: trmnl-dev
description: >
  Build, update, and operate TRMNL e-ink private plugins end to end — webhook data
  updates and merge variables, Liquid markup with Framework 3.1, the per-plugin MCP
  server (stateless JSON-RPC), an offline preview/screenshot harness, and
  battery-aware refresh cadence. Use when working with TRMNL devices (OG or TRMNL X),
  trmnl.com private plugins, webhook payloads, e-ink dashboard markup, the TRMNL MCP
  API, or debugging clipped, empty, or stale TRMNL renders.
license: MIT
metadata:
  author: 0juano
  version: "1.0.0"
---

# TRMNL Dev

Field-tested knowledge for building and operating TRMNL private plugins:
what the docs say, plus the gotchas the docs don't mention (rendering
geometry that clips, MCP quirks, CSS cascade layers, payload byte limits).

## Mental model

TRMNL is server-rendered e-ink. The device polls; nothing is pushed to it.

```text
data source ──► webhook POST ──► merge variables ─┐
                                                  ├─► TRMNL renders PNG ──► device wakes,
markup editor / MCP ──► Liquid template ──────────┘    downloads image, sleeps
```

There are **two independent update paths** — never confuse them:

1. **Change what the screen says** → generate JSON → POST to the plugin webhook.
   The webhook updates merge variables only; it never changes markup.
2. **Change how the screen looks** → edit Liquid markup → save → preview →
   force refresh. The markup editor never fetches new data by itself.

A webhook post triggers a server-side re-render in ~2 s, but the physical
device only shows it on its next wake (default every 15 min). Server-side
posts do **not** wake the device and cost no battery.

## Keys and identifiers (don't mix them up)

| Credential | Looks like | Where found | Used for |
|---|---|---|---|
| Device API key | opaque token | Devices → Edit | `access-token:` header on `/api/display`, `/api/current_screen` |
| Account API key | `user_…` | Account settings | `Authorization: Bearer` on account API (devices, playlists) |
| Plugin Settings UUID | UUID in webhook URL | generated on first plugin **Save** | webhook POSTs to `/api/custom_plugins/<uuid>` |
| Plugin MCP key | `ps_mcp_…` | plugin settings page, right side after Save | `https://trmnl.com/mcp?api_key=…` |

The MCP key is **per-plugin**: it can read/write that one plugin's markup,
settings, and merge variables — no device, playlist, battery, screenshot, or
preview control, and it will not reveal the plugin UUID or webhook URL.
For device/playlist work use the account API instead.

Keep all real values in environment variables or an OS keychain, never in
committed files. Treat the webhook URL itself as a secret — anyone holding it
can write to your screen.

## Webhook data updates

Payload shape — everything lives under a top-level `merge_variables`:

```bash
curl "https://trmnl.com/api/custom_plugins/${TRMNL_PLUGIN_UUID}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"merge_variables":{"headline":"Hello TRMNL","items":[{"time":"09:00","title":"Standup"}]}}'
```

Hard limits (standard tier): **2 KB body, 12 posts/hour** (TRMNL+: 5 KB, 30/hour).
Faster sends return `429`. Plugin "Debug Logs" mode temporarily raises the limit
during development.

Rules that keep you out of trouble:

- Send only reduced display text (`{"time","title"}`), never raw upstream API
  output — you'll blow the byte limit and leak data you didn't mean to send.
- Enforce a local guardrail *below* the real limit (e.g. 1900 bytes for a 2 KB
  tier) and make the generator **degrade instead of fail**: shed rows and render
  an honest `+ N more` label rather than throwing or silently cropping.
- Keep template loop limits ≥ generator caps — a template `limit:` lower than
  what the generator sends silently drops items.
- Stateful updates: `merge_strategy: "deep_merge"` patches nested keys;
  `merge_strategy: "stream"` + `stream_limit` appends to top-level arrays with
  bounded growth. Stored data must still fit the size limit.
- `GET` the same webhook URL to fetch currently stored merge variables.

## Markup essentials

Full geometry/CSS details with the bugs they cause: [references/framework.md](references/framework.md).
The non-negotiables:

- **Author at 800x480 always.** TRMNL X renders 1040x780 at 4-bit (16 grays)
  but the framework scales your 800x480 markup automatically (`scale_factor: 1.8`).
  Never hardcode the native resolution.
- One `<div class="layout">…</div>` per view, optional sibling
  `<div class="title_bar">`. Never nest `.layout` inside `.layout`. Do **not**
  paste `.screen`/`.view` wrappers into the TRMNL editor — those are for
  offline preview only.
- The framework sizes `.layout` to `screen-h − 2×gap` (460 px inside the 10 px
  bezel; less with a `title_bar`). If you use a custom root element instead of
  `.layout`, it must copy that height:
  `height: calc(var(--screen-h, 480px) - var(--gap, 10px) * 2)`.
  `height: 100%` renders 480 px inside a 460 px box and **clips the bottom ~20 px**.
- Omitting the `title_bar` is legal and often right (it eats ~35 px). Saving
  markup without one triggers a "Missing title_bar include" warning — expected;
  ignore it.
- `plugins.css` uses CSS cascade layers: a layered `!important` beats your
  unlayered `!important` and inline styles. You cannot out-specify the
  framework's sizing — adopt its variables (`--screen-h`, `--gap`, `--full-w`)
  or its classes instead of fighting it.
- Custom `<style>` blocks are allowed in private-plugin markup, but TRMNL's
  in-app AI agent enforces "no custom styles" and will flatten your design if
  asked to "improve" it. Keep a local file as the source of truth.
- E-ink legibility: trust the physical device over any browser preview. When in
  doubt — bigger type, 2 px rules (1 px hairlines vanish at distance),
  `font-feature-settings: "tnum" 1` for aligned times, and for screens read at
  a distance don't shrink body type below ~19 px — use two columns instead.

## Per-plugin MCP

Full tool table, curl recipes, and every gotcha: [references/mcp.md](references/mcp.md).
The essentials:

- Endpoint `https://trmnl.com/mcp?api_key=…` is **stateless JSON-RPC over
  HTTP** — call `tools/list` / `tools/call` directly, no initialize handshake.
- Tool names are **PascalCase with a `Tool` suffix** (`MarkupsWriteTool`), not
  the in-app agent's snake_case names. snake_case returns `Tool not found`.
- `MarkupsWriteTool` takes `{size, content}` — passing `markup` instead of
  `content` returns an unhelpful `-32603 Internal error`.
- MCP **writes markup blind** (no screenshot/preview tool exists). Safe write
  flow: read live → back up → write → read back → unescape → compare with your
  local source. Verify visually in the editor previewer or offline harness.

## Offline preview (no account round-trips)

Render your Liquid template locally with sample data inside TRMNL's official
CSS/JS wrapper, then screenshot the `.screen` element (exactly 800x480).
Complete recipe and pitfalls: [references/preview.md](references/preview.md).

Iterate offline until the layout is right; only then push markup. Include
worst-case sample payloads (max rows, longest titles) — busy days are where
layouts break, not calm ones.

## Battery and refresh cadence

- Plugin refresh (server) and device wake (battery) are **separate**. Webhook
  posts are free; device wakes cost battery (WiFi + fetch + e-paper refresh).
- Sleep Mode is the biggest easy win: sleeping 22:00–06:00 at a 15-min cadence
  avoids ~32 wakes/day.
- Match cadence to content: dashboards fed by daily/hourly data rarely need
  15-min refresh all day. A sane profile: 15–30 min during the morning rush,
  60 min midday, 30–60 min in the evening, sleep overnight.
- `/api/display` (device key) **advances the playlist** — don't poll it for
  monitoring; use `/api/current_screen` sparingly instead.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Preview renders empty | POST a tiny payload first; confirm strategy = Webhook; payload under `merge_variables`; plugin saved once (UUID exists) |
| Bottom of screen clipped | custom root missing the `calc(var(--screen-h) - var(--gap)*2)` height; or a `title_bar` you forgot to budget for |
| Physical device looks worse than preview | trust the device: bigger type, fewer display fonts, explicit grid columns, thicker rules |
| Webhook `429` | over posts/hour cap — batch updates; enable Debug Logs during dev |
| Items missing from render | template `limit:` below what the payload contains; or payload exceeded the byte cap and the generator shed rows |
| MCP `Tool not found` | you used snake_case; use PascalCase + `Tool` suffix |
| MCP `-32603 Internal error` on write | you passed `markup`; the argument is `content` |
| MCP readback never matches local file | the envelope escapes `\n`/`\"`/`\\` — unescape before diffing |
| Editor save "Missing title_bar include" warning | expected when intentionally omitting the title bar; ignore |

## Doc links

- Docs index: https://docs.trmnl.com/go/llms.txt
- Webhooks: https://docs.trmnl.com/go/private-plugins/webhooks.md
- Templates: https://docs.trmnl.com/go/private-plugins/templates.md
- Framework 3.1: https://trmnl.com/framework/docs/3.1/v3_overview.md
- TRMNL X guide: https://trmnl.com/framework/docs/3.1/trmnl_x_guide
- Native plugin markup examples: https://github.com/usetrmnl/plugins/
