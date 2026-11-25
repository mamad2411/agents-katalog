---
name: searching-with-serpapi
description: Use when an agent needs live, structured search-engine data through SerpApi (web results, news, shopping, local, jobs, flights, scholar, images, video). Covers picking the right engine for the intent, choosing compact vs complete output, query operators, pagination, deduping and citing results, and when NOT to search. Triggers on "search the web", "current/latest", "rank tracking", "SERP", "google results", "serpapi".
---

# Searching with SerpApi

SerpApi runs a query against a real search engine, solves CAPTCHAs and proxies, and returns clean structured JSON. This skill is the *procedure* layer: it assumes you already have a SerpApi search capability available (the official `serpapi-mcp` MCP server, or the `serp` CLI in this repo) and tells you how to use it well so you spend few tokens and get trustworthy results.

The single biggest mistake agents make with a SERP tool is dumping the full raw JSON into context. SerpApi responses are large. Treat the context window as a public good: ask for the narrowest result that answers the question.

## Decision: do you even need to search?

Search when the answer is **time-sensitive, niche, or must be cited** (prices, news, rankings, "latest", a specific page's current content, anything post-training-cutoff). Do **not** search for stable general knowledge you already hold, for math, or to re-fetch something already in context. A wasted search costs tokens and latency on both sides.

## Step 1 — pick the engine by intent

`engine` defaults to `google_light` (fastest). Override it to match the intent:

| Intent | Engine |
|--------|--------|
| General web results, fastest | `google_light` |
| Full Google SERP (answer box, knowledge graph, AI Overview) | `google` |
| News / recency | `google_news` |
| Shopping / product listings + prices | `google_shopping` |
| Local businesses, maps | `google_local` |
| Job postings | `google_jobs` |
| Flights / hotels | `google_flights` / `google_hotels` |
| Academic | `google_scholar` |
| Images / video | `google_images` / `youtube_search` |
| Marketplaces | `amazon`, `ebay`, `walmart` |
| Non-Google web | `bing`, `duckduckgo`, `baidu`, `yandex`, `yahoo` |

If you are unsure which parameters an engine accepts, read the engine resource first: `serpapi://engines` lists every engine, and `serpapi://engines/<engine>` gives that engine's parameters. Read the one engine you need, not the whole index.

## Step 2 — choose output mode: compact first

- **`compact`** (prefer this): drops `search_metadata`, `search_parameters`, `search_information`, `pagination`, and `serpapi_pagination`. Use it for almost everything — you keep the actual results and shed the bookkeeping.
- **`complete`**: only when you specifically need pagination tokens, the search-information totals, or metadata for a follow-up call.

Default to `compact`. Reach for `complete` deliberately.

## Step 3 — write a tight query

- Quote exact phrases: `"senior rails engineer"`.
- Scope by site: `site:news.ycombinator.com`.
- Exclude noise: `rails -jobs`.
- Constrain freshness with the engine (`google_news`) rather than stuffing date words into `q`.
- Set geo for local or geo-sensitive intent instead of baking the city into `q`. The `serp` CLI now forwards `--location` (e.g. `"Austin, TX"` or `Brazil`), `--gl` (two-letter country, e.g. `br`), and `--hl` (UI language, e.g. `pt`); the MCP server takes the same `location`/`gl`/`hl` params. Example: `serp search "best noise cancelling headphones" --engine google --location Brazil --gl br --hl pt --fields title,link`.
- Keep `num` small (5–10). You rarely need 100 results; you need the right 5.

## Step 4 — read narrow, then widen only if needed

Prefer several small targeted searches over one broad search you then scroll. Pull `title`, `link`, `snippet` (and `price`/`date` when relevant) from the top results. If the answer isn't in the first page, refine the query before asking for more pages — a sharper query beats deeper pagination.

## Step 5 — dedup and cite

- Dedup by normalized URL/domain before presenting; the same story often appears across results.
- Always cite the `link` for any claim drawn from a result. Never present a scraped snippet as your own knowledge.
- If results conflict, say so and cite both rather than silently picking one.

## Anti-patterns

- Returning full `complete` JSON into context "just in case" — strip to `compact`.
- Searching for something already in the conversation.
- Asking for `num=100` then summarizing — search narrower instead.
- Inventing a result `link` or a date the response didn't contain.
- Looping the same query with tiny wording changes — change the engine or add operators instead.

## Examples / evals

These double as the skill's evals — each should be answerable with one or two well-shaped calls.

1. **"What's the latest news on the Google vs SerpApi lawsuit?"**
   → `engine=google_news`, `q="Google SerpApi lawsuit"`, `mode=compact`, `num=5`; cite the top 2–3 `link`s with dates.

2. **"Cheapest 1TB NVMe SSD right now?"**
   → `engine=google_shopping`, `q="1TB NVMe SSD"`, `mode=compact`; sort the returned `shopping_results` by `price`, cite the merchant `link`.

3. **"Coffee shops near downtown Austin."**
   → `engine=google_local`, `q="coffee shops"`, `location="Austin, TX"`, `mode=compact`; return name + address + rating, not the raw blob.

4. **"Does serpapi.com currently list a Senior Fullstack role?"**
   → `engine=google`, `q="site:serpapi.com careers senior fullstack"`, `mode=compact`; confirm from the `link`, don't guess.

## When to reach for the CLI instead of the MCP

For high-frequency, stateless lookups in a long agent session, the `serp` CLI in this repo returns only the fields you ask for and costs almost no standing context, where an always-loaded MCP server pays its tool schema on every turn. Use the MCP server when you want a hosted, multi-client connection; use the CLI for cheap one-shot calls inside a coding loop. Both are complements to SerpApi's official `serpapi-mcp`, not replacements.
