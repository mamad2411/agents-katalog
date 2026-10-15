---
name: reduck
description: |
  Run web tasks through the Reduck CLI: scrape a site, extract structured
  records, search LinkedIn/Reddit/Google, log in and pull messages, fetch
  SPA/JS-gated pages, paginate site-search. Use when the user says
  "scrape", "get data from <site>", "search <site> for X", "pull my latest
  messages on <platform>", "look up reviews/posts/listings", "extract
  <field> from <URL>", or asks for any data that lives behind a webpage
  rather than a public API. Treat Reduck as a function: discover the
  method, call it, read the records. NOT for: writing browser automation
  from scratch, headed Playwright/Puppeteer scripts, or tasks where a
  first-party API already exists.
license: Complete terms in LICENSE
---

# Reduck

Reduck is a **function**: pass arguments, records come back. The default LLM failure is to chat with it — write narrative prompts, run one at a time, answer from the `output` string. Correct for that.

## Prerequisites

```bash
npm install -g @reduck-ai/cli
reduck login        # OAuth PKCE, opens a browser
reduck devices      # pick the device this CLI will dispatch to
```

Optional: set `REDUCK_DEVICE_ID=<chrome-profile>` so multiple agents can run sessions on the same machine concurrently — Chrome profile accepts concurrent sessions.

## CLI surface (live)

The four blocks below use a bash-macro syntax that some loaders (e.g. Claude Code) expand at load time, inlining live `--help` output. If they render as literal text instead, run the four commands yourself before discovery — the contracts change between releases.

!`reduck --help 2>&1`
!`reduck run --help 2>&1`
!`reduck search --help 2>&1`
!`reduck get --help 2>&1`

## Discovery (3 progressive hops)

`search` ranks **hosts** by name-substring match — it is not method-aware. `get` is the catalog and contract.

1. **`reduck search <query>`** → newline-separated hosts. Use a host token (`linkedin`, `reddit`) not a verb-phrase (`messages` returns nothing).
2. **`reduck get <host>`** → slim catalog: one line per method (`slug: description`). Scan descriptions for intent.
3. **`reduck get <host>/<slug>`** → fat single method: args schema (with `required`) and `output_schema`. The complete invocation contract for `reduck run --method <host>/<slug>`.

Canonical run, "latest messages on LinkedIn":

```
reduck search linkedin                                    # → linkedin.com
reduck get linkedin.com                                   # scan for messaging slugs
reduck get linkedin.com/get_latest_conversations          # confirm shape
reduck run --method linkedin.com/get_latest_conversations --output-format yaml 2>/dev/null
```

When `search` returns nothing, fall back to: (a) try common host tokens (`google`, `x`, `reddit`, `wikipedia`), (b) Google site-search (see Corrections) for unindexed sites.

## Corrections

- **Parallel = one Bash tool call per run, in the same assistant message.** The harness runs them concurrently; each returns its own stdout. Cap at 3-5 concurrent (extension saturates beyond). Never shell-`&` inside one Bash call — that conflates stdouts. For 1–2 runs, sequential is fine.
- **Clean stdout:** `--output-format json 2>/dev/null` silences stderr logs; parse the result directly. Don't pipe to `/tmp`.
- **Rounds, not one-shot.** Discover broad (3–5 angles) → refine operators in place (`OR`, `"exact"`, `-term`) → deep-dive parallel on winning IDs. Widening fanout after a miss doubles noise, not signal.
- **Records answer — `envelope.extractions` (json/yaml) or `~/.reduck/…yaml` (disk) carry the same data. `output` only confirms.**
- **Read structured output whole, don't parse it.** `--output-format yaml|json` → `Read` the file. `head`/`awk`/`grep`/python-extract on a structured dump truncates past the field you needed and forces a re-run. Occam: necessary and sufficient.
- **`null` ≠ `""` in records.** Null = the source wasn't in the page text the LLM was given (often virtualization, partial hydration, or a dead selector). Empty string = source was present and legitimately empty. Treat null as "data missing for this row," not "field is empty." If a field is mostly null and you can see it on screen, the call was partial — re-run, or check the schema's `required`.
- **Google site-search as a generic discovery primitive.** For any host indexed by Google, `google.com/site_search` (site, query, optional path_pattern, period) paginates through all unique results and matches body text — strictly wider than most sites' native search. Prefer it over per-host `google_search_*` aliases unless the host has a specialized SERP extractor (LinkedIn posts/profiles, Medium, Substack — these lift entity labels and likes counts and stay). Pagination is sequential with early exit on 0-new or Google's "omitted similar entries" notice; you don't need to know the page count up front. Don't parallelize per-page — Google self-terminates around 70-100 unique results, so parallel always pays full N pages while sequential stops at the natural end.

- **Fetching SPA or other hard to fetch content with headless**: When a page hides behind cookies / JS / login and headless returns just the wall, use a generic `reduck run -q` plus an inline `--output-schema` with a single `transcription` string field:
```
reduck run -q "Go to <URL>" \
  --output-schema '{"type":"object","properties":{"transcription":{"type":"string","description":"Verbatim copy of <what you want>"}}}' \
  --output-format yaml 2>/dev/null
```
The schema's `description` IS the steering prompt — narrow it to drop noise ("Include role names and step-by-step instructions; ignore footer/nav"). Cookie banners are dismissed automatically. Multi-frame pages are walked in one call. Use this any time you'd reach for a heavier headless-browser fetch.
