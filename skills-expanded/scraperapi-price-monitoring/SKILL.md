---
name: scraperapi-price-monitoring
description: >-
  Use this skill whenever the user wants to check, track, or be alerted about product prices on Amazon, Walmart, or via Google Shopping. Trigger on: "monitor the price of this Amazon product", "did the price drop on [Walmart URL]?", "track these ASINs", "compare today's prices to last week", "alert me if [product] goes below $X", "what's the current price of [product]?", "check my price watchlist", "scrape the price of [URL]". Accepts ASINs, Amazon/Walmart product URLs, or free-text product queries for Google Shopping. Reads an optional baseline JSON file to detect changes, fetches live prices via ScraperAPI's structured endpoints, and reports increases, decreases, restocks, and out-of-stock transitions in a structured change report.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "💰"
    homepage: https://docs.scraperapi.com/
---

# Price Monitoring

Given a list of products (ASINs, Walmart URLs, or free-text Google Shopping queries) and an optional baseline file, fetch current prices via ScraperAPI's structured endpoints, compare against the baseline, and produce a structured change report.

**You — Claude — execute the API calls** using the `Bash` tool. Do not generate a script for the user to run; fetch the data yourself in this turn and report findings as you go. If the user explicitly asks for a CLI/cron-able script instead, point them at `scraperapi-cli` and stop.

**Auth:** All transports authenticate against ScraperAPI. The MCP server reads the key from its own configured environment when the user set it up. The curl fallback reads `$SCRAPERAPI_API_KEY` from the shell. Do not run a standalone check for the key — just make the first real request. ScraperAPI returns `401` if the key is missing or invalid, and Phase 3's failure-handling table already covers that case. Adding a pre-flight `echo` only costs the user an extra permission prompt without learning anything you wouldn't learn from the first call.

---

## Phase 1 — Parse the watchlist

Before fetching anything, classify each target. Different inputs route to different ScraperAPI endpoints, and routing wrong wastes credits.

| Input shape | Endpoint | Required param |
|-------------|----------|----------------|
| 10-char alphanumeric (e.g., `B08N5WRWNW`) | `structured/amazon/product` | `asin` |
| URL containing `amazon.` | `structured/amazon/product` | extract `asin` from URL, fall back to `url` |
| URL containing `walmart.com` | `structured/walmart/product` | `url` |
| Free-text query (e.g., `"airpods pro 2"`) | `structured/google/shopping` | `query` |
| Anything else | Tell the user it is not supported by this skill; suggest `scraperapi-autonomous-research` for arbitrary URLs |

Announce the parsed plan before running: *"Watchlist parsed: 3 Amazon products, 1 Walmart product, 1 Google Shopping query. Baseline: prices.json (last updated 2026-05-25). Fetching now."*

For Amazon URLs, extract the ASIN with a regex like `/(?:dp|gp/product)/([A-Z0-9]{10})/` — the structured endpoint is faster and cheaper when given the ASIN directly than when given the full URL.

---

## Phase 2 — Load the baseline (if any)

The baseline is a JSON file the user maintains across runs. Its shape is documented in `assets/price-baseline-template.json`. If the user references a baseline file, read it before fetching so you can compare in a single pass.

If no baseline exists, treat this run as the *first capture* — every product becomes a baseline entry, and the change report only lists currently-observed prices (no deltas). Offer to write the file at the end so the next run can compare against it.

Never silently overwrite a baseline without confirming. If the user wants the file updated, do it explicitly at the end of the run after they see the report.

---

## Phase 3 — Fetch current prices

**Use the ScraperAPI MCP server for this skill.** Tools like `amazon_product`, `walmart_product`, and `google_shopping` give typed arguments and structured responses with no shell-quoting or stdout-parsing concerns, which is what you want for a pricing workflow where field accuracy matters.

If the ScraperAPI MCP server is listed as still connecting, wait briefly and re-check with `ToolSearch` before doing anything else. If MCP is genuinely unavailable, fall back to `curl` (documented below) — do **not** reach for the `sapi` CLI here, even if it is on `$PATH`. CLI output requires shell parsing that's error-prone for price data, and this skill stays simpler by routing all price calls through one transport.

At the end of the report, if you had to use the `curl` fallback, mention that installing the MCP server (`scraperapi-mcp` skill covers setup) will simplify future runs. Never block the current run on installing tooling.

Run all targets in parallel — multiple tool calls in a single message — so a 10-product watchlist finishes in roughly one round-trip rather than ten.

### MCP tools

| Target | Tool | Key arguments |
|--------|------|---------------|
| Amazon product | `amazon_product` | `asin`, optionally `countryCode` (e.g., `"us"`), `tld` |
| Walmart product | `walmart_product` | `productId` (the digits from `/ip/<id>`, e.g., `https://walmart.com/ip/5021188053` → `"5021188053"`), `tld` |
| Google Shopping query | `google_shopping` | `query`, optionally `countryCode` |

See the `scraperapi-mcp` skill for full schemas. Walmart's MCP tool takes a *product ID*, not a URL — strip the `/ip/<id>` segment.

### `curl` fallback

```bash
curl -sG "https://api.scraperapi.com/structured/amazon/product" \
  --data-urlencode "api_key=$SCRAPERAPI_API_KEY" \
  --data-urlencode "asin=B08N5WRWNW" --data-urlencode "country=us"

curl -sG "https://api.scraperapi.com/structured/walmart/product" \
  --data-urlencode "api_key=$SCRAPERAPI_API_KEY" \
  --data-urlencode "url=https://www.walmart.com/ip/123456789"

curl -sG "https://api.scraperapi.com/structured/google/shopping" \
  --data-urlencode "api_key=$SCRAPERAPI_API_KEY" \
  --data-urlencode "query=airpods pro 2" --data-urlencode "country=us"
```

### Expected response fields (same for MCP and curl)

- **Amazon:** `pricing` (formatted string like `"$129.99"`), `list_price`, `availability_status`, `product_information.title`, offers. Parse the number out of `pricing` and carry the currency separately.
- **Walmart:** `price`, `availability`, `seller_name`, `product_name`.
- **Google Shopping:** `shopping_results[]` with `title`, `price`, `extracted_price` (numeric when ScraperAPI can parse it), `source` (retailer), `link`.

The exact field names occasionally drift — inspect the first real response of a run and adapt parsing if needed.

### Handling failures

MCP tools surface errors as tool-call errors; `curl` returns an HTTP status code.

| Status | Action |
|--------|--------|
| 200 with empty/missing price field | Treat as "price not visible" — likely out of stock or layout changed. Record `null` and surface it. |
| 401 | API key missing or invalid — stop and tell the user to set `SCRAPERAPI_API_KEY` (or fix the value). Do not retry. |
| 403 | Blocked — retry once with the premium flag (`premium: true` for MCP, `&premium=true` for curl). If it still fails, mark that target as failed and continue. |
| 404 | Product no longer exists — record as `removed` in the report. |
| 429 | Concurrent limit hit — back off (sleep 3s) and retry once. |
| 5xx | Transient — retry up to 3 times with backoff (2s, 4s, 8s). |
| MCP tool unavailable | Fall back to `curl` for the rest of the run. |

Do **not** retry forever. Failed targets after retries get a `status: "failed"` row in the report so the user knows what's missing.

### Credit budget

Each structured call typically costs ~5 credits. A 50-product watchlist is ~250 credits per run. Before kicking off batches larger than ~100 targets, tell the user the estimate and confirm. If they want recurring monitoring at large scale, recommend they move to a scheduled CLI (`scraperapi-cli`) or DataPipeline rather than burning credits through this skill on every check.

---

## Phase 4 — Compare and classify

For each target, compute the delta against the baseline. Classify into one of these states — the report becomes much easier to read when changes have consistent labels:

| State | Condition |
|-------|-----------|
| `unchanged` | Price within ±0.5% of baseline |
| `decreased` | Current < baseline by more than 0.5% |
| `increased` | Current > baseline by more than 0.5% |
| `restocked` | Baseline price was `null`, current is a number |
| `out_of_stock` | Baseline price was a number, current is `null` |
| `new` | Not in baseline at all |
| `removed` | In baseline, target returned 404 |
| `failed` | Network/API failure after retries |
| `threshold_hit` | User specified `"alert below $X"` and current ≤ X |

If the user gave an explicit alert threshold (e.g., *"tell me if AirPods drop below $200"*), check it against the current price and surface `threshold_hit` items prominently at the top of the report — that is the user's primary question.

---

## Phase 5 — Produce the report

Render results using `assets/price-report-template.md` as the structure. Group by state with the most interesting changes first: threshold hits → decreases → restocks → out-of-stock → increases → new → unchanged → failures.

For each row, include:
- product identifier (ASIN, URL, or query)
- title (from the response — helps the user recognize the item)
- baseline price → current price (with currency and date)
- delta as both absolute and percent
- direct link to the listing

End with a one-line summary: *"6 of 12 products changed price. Biggest drop: AirPods Pro 2 −15% ($249 → $211). 1 went out of stock. 1 failed."*

---

## Phase 6 — Offer to update the baseline

After presenting the report, ask whether to update the baseline file with the new prices. If yes, write the new JSON; preserve fields the user added (e.g., `notes`, `alert_below`) by merging rather than overwriting. If no, leave the file untouched.

If this was a first-run capture, *do* write the baseline (after confirming) — otherwise the next invocation will have nothing to compare against and the loop is pointless.

---

## Stop conditions

This skill is single-shot — it runs once, reports, and stops. It does **not** loop or schedule itself. If the user wants recurring monitoring:

- For ad-hoc re-checks every few hours: have them re-run the prompt.
- For nightly cron: refer them to `scraperapi-cli` to generate a script.
- For fully managed scheduling and storage: point them at DataPipeline in the ScraperAPI dashboard (https://dashboard.scraperapi.com/).

Never start a background watcher or write code that polls — that is out of scope for this skill and burns the user's credits without their direct consent each run.

---

## Anti-patterns

- **Scraping raw HTML when a structured endpoint exists.** The Amazon/Walmart/Google structured endpoints exist precisely so you don't have to parse pricing markup. Use them.
- **Silent currency assumptions.** Always carry the currency code from the response into the report. A "$1,299" reading is wrong if the listing was in CAD.
- **Comparing across countries.** If baseline `country=us` and current `country=gb`, you are comparing different listings — refuse and ask the user which country to use.
- **Overwriting the baseline by default.** The baseline is the user's record of truth; touch it only on explicit confirmation.

---

## Reference files

- `references/structured-endpoints.md` — Exact parameter names, country codes, and known response fields for `amazon/product`, `walmart/product`, and `google/shopping`. Read this before constructing the first request of a run.
- `assets/price-baseline-template.json` — Shape of the baseline file.
- `assets/price-report-template.md` — Markdown skeleton for the change report.

For deeper questions about endpoint behavior, link the user to the public docs: https://docs.scraperapi.com/.
