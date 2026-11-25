---
name: model-radar
description: Find, compare, and recommend LLM models on OpenRouter. Use when picking a model by budget, context window, capabilities (tool use / vision / reasoning / structured output), or modalities; comparing two or more models side-by-side; recommending a model for coding / batch / chat / vision workloads; or answering "cheapest model with vision under $X / MTok", "what's the most popular Claude", "fastest model with 1M context". Triggers on tasks involving model selection, LLM pricing comparison, capability filtering, or "which model should I use".
license: MIT
metadata:
  author: primexiao
  version: "1.0.0"
---

# Model Radar

OpenRouter model selection CLI. Parses natural-language constraints into
`token:value` arguments, queries a local cache of model metadata + rankings,
and emits JSON for the agent to render as a markdown table.

## Setup

- Runtime: Node.js 18+ (no install step and no npm dependencies)
- No API key — uses OpenRouter public endpoints
- Run all commands from this skill directory (the one containing this file)
- First run populates the cache from the network; subsequent calls hit the
  local cache (models TTL 6h, rankings TTL 24h)
- Self-updates are enabled by default. Each CLI run checks the fixed GitHub
  source at most once every 24h and applies updates automatically for installed
  copies. Set `MODEL_RADAR_AUTO_UPDATE=0` to disable.

## Workflow

0. Run `node scripts/self-update.js auto` before using the skill. If stderr
   prints `MODEL_RADAR_UPDATED`, re-read this `SKILL.md` before continuing.
1. Parse the user's request into `token:value` arguments using the **Intent → Token** mapping below
2. Pick the command: `list` (filter+sort), `recommend` (weighted score against a preset), `compare` (side-by-side)
3. Run from the skill directory. `scripts/main.js` also runs the same self-update
   preflight automatically, so direct CLI usage stays current.
4. Render the JSON output as a **markdown table** (see [Output](#output))
5. End with `Data as of {fetched_at}`; suggest `refresh` if older than 12h

## Commands

```bash
node scripts/main.js list      [tokens...]    # filter + sort
node scripts/main.js recommend [tokens...]    # weighted score against a preset
node scripts/main.js compare   <id|name>...   # side-by-side comparison
node scripts/main.js refresh                  # force-refresh both caches
node scripts/self-update.js status            # inspect update state
node scripts/self-update.js check             # check GitHub for updates
node scripts/self-update.js apply             # apply the latest skill update
```

## Self-Update

- Source is fixed by `package.json.repository`: `primexiao/agent-skills`, path
  `skills/model-radar`.
- Installed copies update automatically. Source checkouts skip auto-update unless
  `MODEL_RADAR_AUTO_UPDATE_SOURCE=1` is set.
- Local uncommitted changes under the skill directory cause auto-update to skip.
- Direct `scripts/main.js` usage restarts the current command after a successful
  self-update so the result is produced by the updated code.
- Updates use a temp checkout, validate required files, back up the current skill,
  replace non-runtime files, and roll back on failure.
- Successful updates clear `cache/raw.json`, `cache/models.json`, and
  `cache/rankings.json` so new code does not mix with old data cache.
- Self-update status and warnings go to stderr. Command JSON stays on stdout.

## Token Syntax

Tailwind-inspired positional `token:value` arguments. Order doesn't matter.

| Token    | Meaning                          | Value format                              | Examples                        |
| -------- | -------------------------------- | ----------------------------------------- | ------------------------------- |
| `sort`   | sort dimension                   | preset word (see below)                   | `sort:cheap` `sort:popular`     |
| `price`  | $/MTok blended                   | `..max` / `min..` / `min..max` / bare=max | `price:..10` `price:5..20`      |
| `ctx`    | context length                   | same, `k`/`m` suffix, bare=min            | `ctx:128k` `ctx:128k..1m`       |
| `out`    | max output tokens                | same, bare=min                            | `out:32k`                       |
| `cap`    | capabilities (AND)               | comma-separated                           | `cap:tool_use,reasoning`        |
| `in`     | input modalities (AND)           | comma-separated                           | `in:image` `in:audio,image`     |
| `gen`    | output modalities (AND)          | comma-separated                           | `gen:image` `gen:audio`         |
| `open`   | open-source filter               | `true` / `false`                          | `open:true`                     |
| `top`    | result limit                     | number (default: list=20, recommend=3)    | `top:5`                         |
| `preset` | scoring preset (recommend only)  | preset name                               | `preset:coding`                 |

**`sort` values:** `cheap` `expensive` `new` (default) `ctx` `popular` `throughput` `latency`

**Capabilities:** `tool_use` `reasoning` `structured_output` `vision` `long_output` `prompt_caching` `web_search` `audio_input` `video_input` `file_input` `image_generation` `audio_output`

**Input modalities:** `text` `image` `audio` `video` `file`
**Output modalities:** `text` `image` `audio`

**Recommend presets:** `coding` `batch` `chat` `vision` (see [`config/presets.json`](config/presets.json) for weights and required capabilities)

## Intent → Token

| User says                           | Token(s)                              |
| ----------------------------------- | ------------------------------------- |
| "budget $X" / "under $X"            | `price:..X`                           |
| "at least $X" / "premium tier"      | `price:X..`                           |
| "at least Nk context"               | `ctx:Nk`                              |
| "needs tool use / vision / reasoning" | `cap:tool_use` / `cap:vision` / `cap:reasoning` |
| "structured output" / "JSON mode"   | `cap:structured_output`               |
| "can take audio / image input"      | `in:audio` / `in:image`               |
| "can generate images / audio"       | `gen:image` / `gen:audio`             |
| "open source only"                  | `open:true`                           |
| "cheapest" / "most affordable"      | `sort:cheap`                          |
| "most popular" / "trending"         | `sort:popular`                        |
| "newest" / "latest"                 | `sort:new`                            |
| "fastest" / "lowest latency"        | `sort:latency`                        |
| "highest throughput"                | `sort:throughput`                     |
| "coding agent"                      | `recommend preset:coding`             |
| "batch / bulk job"                  | `recommend preset:batch`              |
| "vision agent"                      | `recommend preset:vision`             |

## Model Matching (`compare`)

Match priority for each argument to `compare`:

1. **Exact id** — `anthropic/claude-sonnet-4-5`
2. **Suffix-exact** — `claude-sonnet-4` → `anthropic/claude-sonnet-4` (never the `-fast` variant)
3. **Partial substring** on id/name, newest release wins — `claude-sonnet` → latest Sonnet

## Output

Always render the JSON output as a **markdown table** — tables are the primary display format.

### `list`

```
| # | Model | $/MTok (P/C/Blend) | Ctx | Output | Caps | Pop# |
```

- `$/MTok`: prompt / completion / blended prices
- `Caps`: short tags (`tool` `reason` `vision` …)
- `Pop#`: popularity rank if rankings cache is fresh, else `—`

### `recommend`

```
| Rank | Model | Score | Cost↑ | Ctx↑ | Out↑ | Cap↑ | $/MTok | Caps |
```

Add a one-line rationale per model. Score and per-dimension scores are in `[0, 1]`.

### `compare`

Vertical table — one column per model, one row per dimension:

```
| Dimension          | Model A | Model B | Model C |
| ------------------ | ------- | ------- | ------- |
| Price (P/C/Blend)  |   …     |   …     |   …     |
| Context            |   …     |   …     |   …     |
| Max output         |   …     |   …     |   …     |
| Input modalities   |   …     |   …     |   …     |
| Output modalities  |   …     |   …     |   …     |
| Capabilities       |   …     |   …     |   …     |
| Popularity rank    |   …     |   …     |   …     |
| Weekly requests    |   …     |   …     |   …     |
```

**Always end with:** `Data as of {fetched_at}`. If older than 12h, suggest the user run `node scripts/main.js refresh`.

## Caching

```
cache/
  raw.json       — OpenRouter frontend card data adapted to local raw schema (TTL 6h)
  models.json    — enriched: normalized pricing + capability labels (TTL 6h)
  rankings.json  — popularity / throughput / latency + usage analytics (TTL 24h)
config/
  presets.json
  tier1-categories.json
```

- Cache files live under `cache/` and are **not committed** — first run hits the network
- On TTL expiry, the CLI refetches with a 10s timeout
- On any fetch failure, it falls back to the stale cache and emits `[warn]` on stderr — so read-only / offline sandboxes still answer (possibly stale)
- A successful skill self-update deletes the model-data cache files. The next
  model command repopulates them.

## Sandbox Notes

- **Codex CLI:** needs `-s workspace-write` (CLI writes to `cache/`) and network egress to `openrouter.ai`. Within TTL, no network calls.
- **First call in a fresh checkout** is the only one that strictly requires network.
- Self-update needs filesystem write access to this skill directory and network
  access to GitHub. If unavailable, it warns or skips and the model command still
  runs with the current local copy.

## Known Issues

- The OpenRouter **frontend** API (`/api/frontend/v1/models/find?active=true&fmt=cards`) is unofficial; if it fails, the CLI falls back to stale cache where available and emits `[warn]`.

## Data Sources

- **Models:** `https://openrouter.ai/api/frontend/v1/models/find?active=true&fmt=cards`
- **Rankings:** same endpoint with `order=top-weekly`, `order=throughput-high-to-low`, and `order=latency-low-to-high`
