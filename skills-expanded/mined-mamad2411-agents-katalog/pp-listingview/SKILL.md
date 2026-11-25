---
name: pp-listingview
description: "Every ListingView research tool in your terminal, plus a local database that adds drift tracking, niche scoring, and offline analysis no ListingView tool keeps. Trigger phrases: `research Etsy keyword volume`, `is this Etsy niche saturated`, `audit my Etsy listing SEO`, `what tags do top Etsy sellers use`, `find rising Etsy tags`, `use listingview`, `run listingview`."
author: "Vincent Colombo"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - listingview-pp-cli
    install:
      - kind: go
        bins: [listingview-pp-cli]
        module: github.com/mvanhorn/printing-press-library/library/marketing/listingview/cmd/listingview-pp-cli
---

# ListingView — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `listingview-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install listingview --cli-only
   ```
2. Verify: `listingview-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails (no Node, offline, etc.), fall back to a direct Go install (requires Go 1.26.4 or newer). This installs into `$GOPATH/bin` (default `$HOME/go/bin`), so add that directory to `$PATH` instead:

```bash
go install github.com/mvanhorn/printing-press-library/library/marketing/listingview/cmd/listingview-pp-cli@latest
```

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

ListingView's keyword, listing, shop, and tag research — backed by a local SQLite store that turns point-in-time estimates into change-over-time intelligence. Run `niche` for a one-command go/no-go, `drift` to catch what moved since last week, `tags consensus` for the tag set winners actually use, and `opportunities` to rank everything you've researched without spending more of your monthly quota.

## When to Use This CLI

Use this CLI for Etsy product, keyword, SEO, and tag research from the terminal or an agent: validating niches, auditing listing SEO, finding winning tags, tracking competitors and trends over time, and ranking opportunities. It is ideal when you want to batch research across many terms, keep an offline history the ListingView web app discards, or pipe structured results to an LLM.

## Anti-triggers

Do not use this CLI for:
- Do not use this CLI to place orders, fulfill print-on-demand, or edit live Etsy listings — it is research/read-focused.
- Do not use it for exact financial accounting; ListingView numbers are directional estimates derived from public Etsy signals.
- Do not use it as a general Etsy API client — it speaks ListingView's internal research surface, not Etsy's official API.

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Composite Etsy intelligence
- **`niche`** — Get a single go/no-go verdict on an Etsy niche, combining keyword demand, competition, best-seller density, price band, and how winnable the current top sellers are.

  _Reach for this before committing design time to a niche — one command replaces five hand-checks across separate tools._

  ```bash
  listingview-pp-cli niche "retro cat mom sweatshirt" --agent
  ```
- **`listings audit`** — Audit a listing's tags: extract the tags it uses and grade each by ListingView's opportunity, demand, competition, and velocity scores, flagging dead-weight tags and proposing stronger replacements.

  _Use this to revive underperforming listings — it tells you which specific tag to swap, not just that the listing is weak._

  ```bash
  listingview-pp-cli listings audit 1581100221 --agent
  ```
- **`tags consensus`** — Find the tags that repeatedly appear across the top-selling listings for a term, ranked by frequency weighted by each listing's revenue estimate.

  _Use this when writing a new listing's tags — it shows the tag set the winners actually use._

  ```bash
  listingview-pp-cli tags consensus "vinyl sticker" --agent
  ```
- **`gaps`** — Compare your shop's tags/keywords against a competitor's, ranked by the revenue those tags drive for the competitor.

  _Use this to find the SEO coverage a winning competitor has that you don't._

  ```bash
  listingview-pp-cli gaps MyShop RivalShop --agent
  ```

### Local state that compounds
- **`drift`** — Re-run your saved keyword/listing/shop queries and diff against the last snapshot: volume changes, new best-seller entrants, price drops, and SEO/rank movement.

  _Reach for this to catch the week a rival launches a bestseller or a keyword starts climbing — invisible in the web UI._

  ```bash
  listingview-pp-cli drift --since 7d --agent
  ```
- **`tags rising`** — Rank tags by ListingView's velocity score (accelerating demand) while competition is still low, surfacing early-mover windows.

  _Reach for this to get into a trend before it saturates._

  ```bash
  listingview-pp-cli tags rising "sticker" --min-competition-score 50 --agent
  ```
- **`opportunities`** — Scan everything you've already researched and rank the best untapped plays: high demand, low competition, rising velocity — with zero new API calls.

  _Reach for this to turn a month of scattered research into a ranked shortlist without spending more quota._

  ```bash
  listingview-pp-cli opportunities --limit 10 --agent
  ```

## HTTP Transport

This CLI uses Chrome-compatible HTTP transport for browser-facing endpoints. It does not require a resident browser process for normal API calls.

## Discovery Signals

This CLI was generated with browser-observed traffic context.
- Capture coverage: 20 API entries from 20 total network entries
- Protocols: rest_json (75% confidence)
- Auth signals: cookie_session_csrf; cookie — cookies: REDACTED
- Generation hints: browser_clearance_required, requires_browser_auth
- Candidate command ideas: create_add_remove_favourite — Derived from observed POST /api/proxy/api/integration/etsy/add-remove-favourite traffic.; create_analytics — Derived from observed POST /api/proxy/api/integration/etsy/listing-explorer/analytics traffic.; create_getFilteredKeywords — Derived from observed POST /api/proxy/api/integration/etsy/getFilteredKeywords traffic.; create_getFilteredListings — Derived from observed POST /api/proxy/api/integration/etsy/getFilteredListings traffic.; create_getFilteredTags — Derived from observed POST /api/proxy/api/integration/etsy/getFilteredTags traffic.; create_get_filtered_shops — Derived from observed POST /api/proxy/api/integration/etsy/get-filtered-shops traffic.; create_listings — Derived from observed POST /api/proxy/api/integration/etsy/shop-analyzer/listings traffic.; create_progress — Derived from observed POST /api/proxy/api/integration/etsy/shop-analyzer/progress traffic.

## Command Reference

**account** — Account: who am I, plan, and connected shops.

- `listingview-pp-cli account` — Show the authenticated user, plan, and connected Etsy shops.

**discover** — Discovery helpers: popular search terms and your recent research history.

- `listingview-pp-cli discover popular` — Popular search terms for a research type.
- `listingview-pp-cli discover recent` — Your recent research history for a type.

**keywords** — Search Term Analyzer — Etsy keyword research: search volume, competition, demand, recommendation score.

- `listingview-pp-cli keywords` — Search/rank keywords by volume, competition, and demand across ListingView's keyword database.

**listings** — Listing research: search the 140M+ listing database and explore any listing's analytics.

- `listingview-pp-cli listings` — Search and rank Etsy listings by sales, revenue, and trend across ListingView's database.

**shops** — Shop research: search the shop database and analyze any shop's performance.

- `listingview-pp-cli shops listings` — Top listings for a shop with sales/revenue, sortable.
- `listingview-pp-cli shops search` — Search and rank Etsy shops by sales, revenue, and trend.

**tags** — Tag intelligence: search tags, analyze a tag, generate market-validated tags, and extract a listing's tags.

- `listingview-pp-cli tags analytics` — Trend analytics over time for a tag.
- `listingview-pp-cli tags analyze` — Tag Analyzer — opportunity/demand/competition/velocity scores for a tag.
- `listingview-pp-cli tags extract` — Tag Extractor — extract the tags a given listing uses.
- `listingview-pp-cli tags generate` — Tag Generator — generate market-validated tags from a keyword.
- `listingview-pp-cli tags listings` — Top listings using a tag.
- `listingview-pp-cli tags search` — Search and rank Etsy tags by opportunity, demand, competition, and velocity.
- `listingview-pp-cli tags shops` — Top shops using a tag.

**watchlist** — Saved items: list watchlisted listings/shops/keywords and add or remove favourites.

- `listingview-pp-cli watchlist list` — List saved/favourited items (listings, shops, or keywords).
- `listingview-pp-cli watchlist toggle` — Add or remove an item from the watchlist.


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
listingview-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Recipes

### Validate a niche before designing

```bash
listingview-pp-cli niche "personalized dog bandana" --agent
```

One composite verdict from keyword demand, best-seller density, price band, and winnability.

### Audit a listing's SEO and tags

```bash
listingview-pp-cli listings audit 1581100221 --agent
```

SEO score plus a per-tag grade with replacement suggestions.

### Find the tag set winners use

```bash
listingview-pp-cli tags consensus "vinyl sticker" --agent
```

Revenue-weighted consensus tags across the term's top sellers.

### Narrow a nested response for an agent

```bash
listingview-pp-cli tags consensus "vinyl sticker" --agent --select tags.tag,tags.share_pct
```

Pull only the fields you need from a nested response with dotted --select paths to save agent context.

### See what moved this week

```bash
listingview-pp-cli drift --since 7d --agent
```

Diff saved snapshots for volume changes, new best-sellers, and price drops.

## Auth Setup

ListingView has no public API key. The CLI authenticates with your logged-in browser session: run `listingview-pp-cli auth login --chrome` to import your app.listingview.io cookies (the CLI derives the required X-CSRF-Token header from them automatically). The free plan covers the entire research surface.

Run `listingview-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  listingview-pp-cli keywords --search example-value --agent --select id,name,status
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success

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

- Use `--home <dir>` for one invocation, or set `LISTINGVIEW_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `LISTINGVIEW_CONFIG_DIR`, `LISTINGVIEW_DATA_DIR`, `LISTINGVIEW_STATE_DIR`, `LISTINGVIEW_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `LISTINGVIEW_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `listingview-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "listingview": {
        "command": "listingview-pp-mcp",
        "env": {
          "LISTINGVIEW_HOME": "/srv/listingview"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `LISTINGVIEW_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `LISTINGVIEW_HOME`, or `doctor` will not find credentials left under the former root.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
listingview-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
listingview-pp-cli feedback --stdin < notes.txt
listingview-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `LISTINGVIEW_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `LISTINGVIEW_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

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
listingview-pp-cli profile save briefing --json
listingview-pp-cli --profile briefing keywords --search example-value
listingview-pp-cli profile list --json
listingview-pp-cli profile show briefing
listingview-pp-cli profile delete briefing --yes
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

1. **Empty, `help`, or `--help`** → show `listingview-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

1. Install the MCP server:
   ```bash
   go install github.com/mvanhorn/printing-press-library/library/marketing/listingview/cmd/listingview-pp-mcp@latest
   ```
2. Register with Claude Code:
   ```bash
   claude mcp add listingview-pp-mcp -- listingview-pp-mcp
   ```
3. Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which listingview-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   listingview-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `listingview-pp-cli <command> --help`.
