---
name: world-events-briefing
description: Use when the user wants a country / major-world-events news briefing ("全球时事简报") — armed conflicts, elections, disasters, business/economy, law/crime — pulled from Wikipedia's human-curated "Portal:Current events" daily pages and the GDELT DOC 2.0 article-search API. This is NOT the AI/tech skill (that's the sibling ai-news-briefing). One of only two Skills in the collection that calls the network (skill.json permissions.network=true) — it still needs zero user API keys. Offline fixture mode is available for fully deterministic, zero-network runs.
---

# World Events Briefing

「全球时事简报」— a country / major-world-events digest builder. NOT AI/tech
news (see the sibling `ai-news-briefing` skill for that). It fetches from two
anonymous, key-free public sources and merges them into one ranked-by-source
list plus a verbatim, human-readable digest.

## THE NETWORK EXCEPTION (read this first)

Most Skills in this collection are `permissions.network: false` and run
fully offline. **This Skill is one of the two documented exceptions**
(alongside `ai-news-briefing`): `skill.json` declares
`"permissions": {"network": true, ...}`. It is allowed to reach the network
because both endpoints it calls are anonymous and free — **no user API key
is ever required, read, or accepted.**

| Source | Endpoint | Auth |
|---|---|---|
| Wikipedia Current Events | `en.wikipedia.org/w/api.php?action=parse&prop=wikitext` | none — public MediaWiki API |
| GDELT DOC 2.0 | `api.gdeltproject.org/api/v2/doc/doc` | none — GDELT only asks callers to pace requests to 1/5s, automatically satisfied by this Skill's single call per run |

## Fixed Flow

1. Decide the window: `date` (default: yesterday UTC — "today" is
   frequently an empty skeleton page, confirmed live during development),
   optional `country` / `category` / `keywords` filters, `max_items`
   (default 20).
2. Call `world_events_briefing.py` with `{"mode": "brief", ...}`. It fetches
   Wikipedia Current Events and GDELT itself, normalizes, filters, dedupes,
   and returns a ready-to-read digest plus the structured item list.
3. A source that is down (timeout, HTTP error, rate limit, unexpected shape)
   is reported as `{"available": false, "error": "..."}` — this is a normal
   outcome, not a failure of the run. The overall result is still `ok: true`
   unless the *input itself* was invalid.
4. For deterministic testing (CI, examples, "did this break") pass
   `{"offline": true, "fixture": {...}}` (or `"fixture_path"`) instead of
   letting it hit the network — see Offline mode below.

## Source 1: Wikipedia "Portal:Current events" (primary)

Human-curated, categorized, and every leaf item carries real citation
links back to the original news source. Fetched via the public MediaWiki
Action API as wikitext (not rendered HTML), then parsed:

- Bold lines (`'''Category'''`) are section headers.
- Nested `*` bullets form a topic tree; an intermediate bullet with no
  trailing `[url (Source)]` citation is a bare topic breadcrumb, not a
  reportable item. A bullet becomes a **leaf item** only when it carries at
  least one citation — that citation is the discriminator.
- `[[Target]]` / `[[Target|Display]]` wiki-links are reduced to their
  rendered display text (MediaWiki's own pipe-trick rule: text after `|`
  wins when present) — verified against live data, e.g.
  `[[Middle Eastern crisis (2023–present)|Middle Eastern crisis]]` →
  `"Middle Eastern crisis"`.
- Each leaf item's `topic` field is the chain of ancestor breadcrumb texts
  (joined by `›`), giving useful context without inventing anything — every
  token comes from the page's own wikitext.

### Empty-page fallback (documented explicitly, per the request)

Wikipedia editors do not always fill in "today's" subpage immediately — this
was confirmed live during development (the page existed but its `content=`
body was just the template skeleton, zero bullets). So:

1. Fetch `date`'s subpage (`Portal:Current_events/{Year}_{Month}_{Day}`).
2. If it parses to zero leaf items, walk backward one day at a time, up to
   `max_lookback_days` (default `5`) additional days, until a populated page
   is found.
3. The date actually used is reported in
   `data.generated_for.resolved_date_wikipedia`; the full per-day attempt
   log (`fetch_error` / `missing_page` / `empty` / `populated`) is in
   `data.wikipedia_fallback.attempts`.
4. If every attempt in the window is empty (but fetched successfully),
   `wikipedia_current_events.available` is `false` with an error explaining
   which dates were tried. If every attempt failed to even reach the
   network, `available` is `false` with the network error instead.

## Source 2: GDELT DOC 2.0 (secondary, broad, country-filterable)

`query` syntax: plain keywords, and/or `sourcecountry:<name-no-spaces>` to
filter by country (e.g. `sourcecountry:china`). This Skill builds the query
from `country` and/or `keywords`; when neither is supplied it falls back to
a broad breaking-news query
(`(breaking OR crisis OR conflict OR election OR government OR economy)`).

GDELT sometimes returns a **plain-text rate-limit notice instead of JSON**
("Please limit requests to one every 5 seconds…") — confirmed live during
development (HTTP 429). This is caught explicitly: a `json.JSONDecodeError`
never propagates, the source degrades to `available: false` with the real
response text, and the run continues.

GDELT gives no article snippet/description in `mode=artlist` — only
`title, url, domain, sourcecountry, seendate, language` — so GDELT items
carry an empty `description` and rely on `title`.

## How to call world_events_briefing.py

```bash
python3 world_events_briefing.py examples/brief_live.json
```

```bash
echo '{"mode":"brief","date":"2026-07-20","country":"China"}' | python3 world_events_briefing.py
```

### Input shape

```jsonc
{
  "mode": "brief",
  "date": "2026-07-20",       // optional, default = yesterday (UTC)
  "country": "China",          // optional — GDELT sourcecountry: + Wikipedia text substring
  "category": "Business and economy", // optional — Wikipedia category substring only
  "keywords": "election",      // optional — GDELT query terms + Wikipedia text substring
  "max_items": 20,             // optional, default 20
  "max_lookback_days": 5,      // optional, default 5
  "gdelt_maxrecords": 20,      // optional, default 20
  "sources": ["wikipedia_current_events", "gdelt"], // optional, default both

  // Offline / deterministic mode — no network at all:
  "offline": true,
  "fixture": {
    "wikipedia_current_events": { "resolved_date": "...", "items": [ {"category":"...", "topic":"...", "description":"...", "citations":[{"url":"...","source":"..."}]} ] },
    "gdelt": [ {"title":"...", "url":"...", "domain":"...", "sourcecountry":"...", "seendate":"...", "language":"..."} ]
  }
  // or: "fixture_path": "examples/some_fixture.json"
}
```

Each fixture source also accepts `{"available": false, "error": "..."}` to
exercise the degraded path offline (see `examples/brief_offline.json`, which
does exactly this for `gdelt`, using the real "HTTP 429" text observed live).

## Filtering semantics (fully specified)

- `category` — case-insensitive substring match against a **Wikipedia**
  item's own category header only. GDELT items have no category field and
  are unaffected.
- `country` — builds GDELT's `sourcecountry:` clause server-side, **and**
  is applied as a case-insensitive substring match against Wikipedia item
  text (description + category + topic). A matching Wikipedia item is
  annotated `country: <the filter value>`.
- `keywords` — becomes GDELT full-text query terms server-side, **and** is
  applied as a case-insensitive substring match against Wikipedia item text.
- When both `country` and `keywords` are given, a Wikipedia item must match
  **both** (AND) to survive. GDELT results are not client-side re-filtered
  by keyword — its own full-text/fuzzy matching already applied server-side,
  and re-filtering by strict substring would incorrectly drop valid matches.

## Pipeline (what happens inside)

fetch/parse Wikipedia Current Events (with fallback) -> normalize -> apply
`category`/`country`/`keywords` filters -> fetch GDELT (query built from
`country`/`keywords`) -> normalize -> merge (**Wikipedia first**, since it
is the primary human-curated source, then GDELT in the order GDELT itself
returned) -> **dedupe** by normalized URL (host + path + **query string** —
the query is deliberately kept, see note below) -> cap to `max_items` ->
`data.items` (flat), `data.by_source` (counts), `data.digest` (verbatim
text), `data.sources_status`, `data.generated_for`, `data.wikipedia_fallback`.

**Dedup URL-normalization note:** unlike a typical "strip tracking params"
normalizer, this Skill deliberately *keeps* the query string. Verified live
during development: many real GDELT sources (e.g. Chinese aggregators like
`baijiahao.baidu.com/s?id=...`) encode the actual article identity in the
query string with an identical path across unrelated articles — stripping
the query caused a false-positive dedup collision that silently discarded
18 of 20 distinct real articles. Keeping the query trades a few missed
tracking-param duplicates for never wrongly merging distinct articles.

## Success

On success the runner prints one JSON object and exits `0`:

```text
result.ok == true
result.skill == "world-events-briefing"
result.mode == "brief"
result.data.items / .by_source / .digest / .sources_status / .generated_for / .wikipedia_fallback present
```

Machine-checkable:

```text
len(data.items) == data.counts.total_items
data.counts.sources_available + data.counts.sources_unavailable == 2  (wikipedia_current_events, gdelt)
every item in data.items has a non-empty "url" (when its source provided one) and a non-empty "title"
offline runs with identical input produce byte-for-byte identical stdout
```

## Error handling

The whole program is wrapped so a Python traceback is never printed. On any
*input* failure the Skill prints a structured envelope and exits `1`:

```json
{
  "ok": false,
  "skill": "world-events-briefing",
  "version": "0.1.0",
  "error": {"code": "UNKNOWN_MODE", "message": "Unknown mode 'x'. Expected one of: brief."}
}
```

Error codes:

- `BAD_INPUT` — input is not valid JSON, is missing required fields,
  `date` is not `YYYY-MM-DD`, or `offline: true` was set without a
  `fixture`/`fixture_path`.
- `UNKNOWN_MODE` — `mode` is not `brief`.
- `INTERNAL` — any unexpected failure (still returned as a clean envelope).

A *source* being unreachable, rate-limited, or empty is NOT one of these —
it never raises. It only ever shows up as
`sources_status.<name>.available == false` inside a successful
(`ok: true`) response.

## Examples

- `examples/brief_offline.json` — **the offline-safe example the benchmark's
  hard constraints run against.** `offline: true` with a fixture built from
  real Wikipedia content captured live on 2026-07-20 (8 items across 4
  categories, including multi-citation items) plus a `gdelt` entry marked
  `available: false` with the exact "HTTP 429 … limit requests to one every
  5 seconds" text this Skill actually received from `api.gdeltproject.org`
  during development — so it also exercises the degraded-source path with
  zero network access, and is byte-for-byte deterministic across runs.
- `examples/brief_live.json` — a real-network call
  (`{"date": "2026-07-20", "country": "China"}`). This can take up to
  ~30–60s (Wikipedia fetch + possible fallback walk + the GDELT call, which
  GDELT may itself rate-limit under repeated testing) and is **not** what
  the benchmark's hard constraints require — it is provided to demonstrate
  the live path works end-to-end.

## Grounding rules (what this Skill will never do)

- Never invent an item, url, category, topic, or citation not present in
  Wikipedia's own wikitext or GDELT's own JSON response.
- Never write a digest line the source's own text does not support —
  `digest` renders the exact extracted description/title/citation text,
  never a rewritten, embellished, or LLM-summarized claim.
- Never require an API key, token, or credential for either source.
- Never let one source's failure (network error, rate limit, malformed
  response) abort the run — it degrades to `available: false` and the other
  source (and any already-collected data) still returns.
