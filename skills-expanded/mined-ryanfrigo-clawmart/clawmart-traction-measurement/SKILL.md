---
name: clawmart-traction-measurement
description: Use this skill during the autopilot observe phase to pull traction metrics (totalCalls, averageRating, catalog size) from clawmart's public /api/catalog endpoint, compare against the previous tick's snapshot, and append a new row to autopilot-state/metrics-history.jsonl. This is the *only* authoritative measurement step — do not invent metrics.
---

# Measuring clawmart traction

## Why this exists

Autopilot decisions must be grounded in real numbers, not vibes. The Convex `skills` collection already tracks `totalCalls` and `averageRating` per skill, and `/api/catalog` exposes them as a public JSON endpoint with CDN caching. That's our signal source.

## How to run

### 1. Pull the live catalog

```bash
curl -s https://clawmart.co/api/catalog | jq '.catalog | {totalSkills, paymentAddress, skills: [.skills[] | {id, name, totalCalls, rating, price: .price.raw}]}'
```

Fallback if the site is down (e.g. deploy in flight):

```bash
npx convex run skills:list 2>/dev/null
```

### 2. Sanity-check `PAYMENT_ADDRESS`

If `paymentAddress` in the response is `0x0000000000000000000000000000000000000000`, **record this warning in the journal** and stop the tick before any code changes — new routes would be unpayable.

### 3. Build the metrics row

```jsonc
{
  "ts": "<ISO-8601>",
  "tick": <N>,
  "catalog_size": <count>,
  "total_calls_sum": <sum of totalCalls across active skills>,
  "per_skill": {
    "<slug>": {"calls": <int>, "rating": <float>, "price": <float>}
  },
  "payment_address_configured": <true if not the zero address>
}
```

Append it to `autopilot-state/metrics-history.jsonl` (one line per row, no trailing comma).

### 4. Compute deltas

Read the previous row (second-to-last line). For each skill slug present in both:

- `calls_delta = current.calls - previous.calls`
- `rating_delta = current.rating - previous.rating`

For the overall catalog:
- `total_calls_delta`
- `catalog_size_delta` (new skills launched since last tick)

### 5. Summarize for the caller

Output a terse block like:

```
Tick 7 (2026-04-16T14:30:00Z)
  Catalog: 5 skills (+0)
  totalCalls: 142 (+23 since tick 6)
  Movers:
    web-summarize        +12 calls  (3h since tick 6)
    data-extractor        +8 calls
    sentiment-analyzer    +3 calls
  Flat: code-reviewer, voicecharm-receptionist
  Payment address: configured ✓
```

## Things not to do

- Don't page Convex directly with a deploy key — the public `/api/catalog` is intentionally the ground truth (it's what agents see).
- Don't invent metrics the endpoint doesn't expose. If you want USD-paid numbers, that's a separate integration that doesn't exist yet — flag it as a backlog item, don't fake it.
- Don't mutate `metrics-history.jsonl` rows you didn't just write. It's append-only.
