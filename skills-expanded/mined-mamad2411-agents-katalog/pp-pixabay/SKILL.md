---
name: pp-pixabay
description: "Every Pixabay search filter the API has — plus a 24-hour local cache, offline search, resumable downloads with built-in attribution, live rate-limit awareness, and agent-native JSON no other Pixabay tool ships. Trigger phrases: `find a royalty-free photo of`, `search pixabay for`, `get stock video of`, `download free images of`, `find an illustration of`, `use pixabay`, `run pixabay`."
author: "Vincent Colombo"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - pixabay-pp-cli
    install:
      - kind: go
        bins: [pixabay-pp-cli]
        module: github.com/mvanhorn/printing-press-library/library/media-and-entertainment/pixabay/cmd/pixabay-pp-cli
---

# Pixabay — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `pixabay-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install pixabay --cli-only
   ```
2. Verify: `pixabay-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails (no Node, offline, etc.), fall back to a direct Go install (requires Go 1.26.4 or newer). This installs into `$GOPATH/bin` (default `$HOME/go/bin`), so add that directory to `$PATH` instead:

```bash
go install github.com/mvanhorn/printing-press-library/library/media-and-entertainment/pixabay/cmd/pixabay-pp-cli@latest
```

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

The only maintained Pixabay CLI is ten years dead and images-only; the only agent-native tool emits text you have to scrape. This one unifies image and video search, caches results in a local SQLite store for up to 24 hours (per Pixabay's API Terms) so you can search offline with `search`, credits Pixabay with a visible link on every result, and adds commands the raw API can't do: `media search` merges photos and video, `pull` does resumable downloads with attribution and 24h URL re-resolution, and `quota` surfaces the rate-limit headers nobody else exposes so you can pace within limits.

## When to Use This CLI

Use this CLI when an agent or developer needs royalty-free photos, illustrations, vectors, or videos by search query and wants the results as structured JSON, persisted locally for offline reuse, or downloaded in bulk. It is the right choice for content pipelines, media-picker backends, and any workflow that re-uses the same searches and benefits from a local cache, attribution tracking, and respecting the API's rate and result limits.

## Anti-triggers

Do not use this CLI for:
- Do not use Pixabay content or this CLI's output for AI or machine-learning training, model fine-tuning, dataset generation, or automated scraping — the Pixabay API Terms of Service explicitly prohibit it.
- Do not run this CLI from unattended automation, cron jobs, or background daemons. Pixabay requires API usage to remain user-triggered; each invocation must correspond to a real user request.
- Do not use this CLI to upload, edit, or manage Pixabay content — the API is read-only search and has no write operations.
- Do not use it for generic web-image search across the whole internet; it only queries Pixabay's own library.
- Do not use it to scrape the Pixabay website (which is Cloudflare-protected) — it talks only to the documented /api/ endpoints.
- Do not systematically mass-download the library; the Pixabay license forbids it. Always credit Pixabay with a visible link when displaying results.

## Pixabay API Compliance

This CLI is built to honor the [Pixabay API Terms of Service](https://pixabay.com/api/docs/). When you use it, you agree to:

1. **Credit Pixabay with a visible link** whenever you display search results. The CLI prints a Pixabay credit line on human output and returns a `pageURL` (Pixabay link) with every result — surface it wherever results appear.
2. **Cache, don't archive.** API responses are cached locally for up to 24 hours to avoid repeated identical queries, then expire. The local SQLite store is a 24-hour cache, not a permanent dataset.
3. **Keep usage user-triggered.** Every invocation must correspond to a real user request. Do not run this CLI from cron jobs, background daemons, or unattended automation.
4. **No AI/ML or scraping.** Pixabay content may not be used for AI or machine-learning training, dataset generation, or automated scraping.

These obligations are why this CLI ships without a bulk-corpus "harvest" command and treats its local store as a 24-hour cache.

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Search & acquisition
- **`pull`** — Download chosen size variants for a collection with parallel workers, re-resolving 24h-expired URLs by id and writing per-file attribution sidecars; re-runs skip what's already on disk.

  _Use this to materialize an already-curated collection to disk safely; it survives interruptions and expired URLs that break naive downloaders._

  ```bash
  pixabay-pp-cli pull --from-collection winter --size large --workers 8 --resume
  ```
- **`media search`** — Fan one query across both the image and video endpoints in parallel and merge stills and footage into a single ranked, persisted result set.

  _Use this when a task needs both photos and video for a theme and you don't want to run two searches and merge by hand._

  ```bash
  pixabay-pp-cli media search "drone coastline" --limit 40 --agent
  ```

### Agent-native plumbing
- **`quota`** — Surface the X-RateLimit-Limit/Remaining/Reset headers from your last call (which no other Pixabay tool exposes) and project how many requests a planned batch of requests will cost before it throttles.

  _Check this before a big batch so an agent can pace itself instead of dying mid-run on an HTTP 429._

  ```bash
  pixabay-pp-cli quota --agent
  ```

### Local state that compounds
- **`similar`** — Find synced hits that share the most tags with a given id using a local tag-set overlap (Jaccard) score — no API endpoint for this exists.

  _Reach for this to expand a curated set with visually-related assets you already pulled, with zero extra API quota._

  ```bash
  pixabay-pp-cli similar 195893 --limit 20 --agent
  ```
- **`trends`** — Snapshot views/downloads/likes/comments on each sync and report the deltas per tag or id between sync runs.

  _Use this to see which themes are gaining downloads/likes week over week — impossible from a single API response._

  ```bash
  pixabay-pp-cli trends --tag winter --since 7d --agent
  ```
- **`contributors`** — Aggregate synced image and video hits by contributor and rank them by total or average downloads, likes, or views across your store.

  _Use this to find the strongest contributors for a theme so you can source consistently from people whose work performs._

  ```bash
  pixabay-pp-cli contributors --by downloads --min-assets 3 --agent
  ```
- **`collection`** — Group synced hits into named local collections that feed downstream pull, similar, and trends — persistence no Pixabay tool offers.

  _Use this as the backbone for curation — build a set once, then download, expand, or track it later without re-searching._

  ```bash
  pixabay-pp-cli collection add winter 195893,1850181
  ```

## Command Reference

**images** — Search Pixabay photos, illustrations, and vectors

- `pixabay-pp-cli images get` — Get image(s) by ID
- `pixabay-pp-cli images search` — Search images by query and filters

**videos** — Search Pixabay videos (film and animation)

- `pixabay-pp-cli videos get` — Get video(s) by ID
- `pixabay-pp-cli videos search` — Search videos by query and filters


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
pixabay-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Recipes

### Find Editor's Choice nature photos, agent-ready

```bash
pixabay-pp-cli images search "forest" --image-type photo --category nature --editors-choice --order popular --agent --select hits.id,hits.tags,hits.largeImageURL,hits.likes
```

Narrows to award-winning nature photos and returns only the fields an agent needs, keeping payloads small.

### Search videos and pull the smallest rendition URL

```bash
pixabay-pp-cli videos search "ocean waves" --video-type film --per-page 10 --agent --select hits.id,hits.duration,hits.videos.tiny.url,hits.videos.large.url
```

Video hits nest renditions deeply (videos.tiny.url, videos.large.url); --select with dotted paths extracts just the URLs you want.

### Download a curated collection with attribution

```bash
pixabay-pp-cli pull --from-collection campaign --size large --workers 6
```

After adding IDs with 'collection add campaign ...', materialize the set to disk with parallel workers and per-file credit sidecars.

### Check quota before a batch

```bash
pixabay-pp-cli quota --agent
```

Reads the persisted rate-limit headers so an automated job can pace itself instead of failing on a 429.

## Auth Setup

Pixabay uses a single free API key passed as a query parameter. Get one from your account at pixabay.com/api/docs (when logged in), then set PIXABAY_API_KEY in your environment or run `pixabay-pp-cli auth set-token <key>`. The API is read-only — search only, no writes.

Run `pixabay-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  pixabay-pp-cli images get mock-value --agent --select id,name,status
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Read-only** — do not use this CLI for create, update, delete, publish, comment, upvote, invite, order, send, or other mutating requests

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal AND no machine-format flag (`--json`, `--csv`, `--compact`, `--quiet`, `--plain`, `--select`) is set — piped/agent consumers and explicit-format runs get pure JSON on stdout.

## Paths and state

Agents should treat the CLI's path resolver as part of the runtime contract:

- Use `--home <dir>` for one invocation, or set `PIXABAY_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `PIXABAY_CONFIG_DIR`, `PIXABAY_DATA_DIR`, `PIXABAY_STATE_DIR`, `PIXABAY_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `PIXABAY_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `pixabay-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "pixabay": {
        "command": "pixabay-pp-mcp",
        "env": {
          "PIXABAY_HOME": "/srv/pixabay"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `PIXABAY_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `PIXABAY_HOME`, or `doctor` will not find credentials left under the former root.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
pixabay-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
pixabay-pp-cli feedback --stdin < notes.txt
pixabay-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `PIXABAY_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `PIXABAY_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled agent calls the same command every run with the same configuration - HeyGen's "Beacon" pattern.

```
pixabay-pp-cli profile save briefing --json
pixabay-pp-cli --profile briefing images get mock-value
pixabay-pp-cli profile list --json
pixabay-pp-cli profile show briefing
pixabay-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `pixabay-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

1. Install the MCP server:
   ```bash
   go install github.com/mvanhorn/printing-press-library/library/media-and-entertainment/pixabay/cmd/pixabay-pp-mcp@latest
   ```
2. Register with Claude Code:
   ```bash
   claude mcp add pixabay-pp-mcp -- pixabay-pp-mcp
   ```
3. Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which pixabay-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   pixabay-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `pixabay-pp-cli <command> --help`.
