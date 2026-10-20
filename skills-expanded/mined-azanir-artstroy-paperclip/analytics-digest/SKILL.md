---
name: analytics-digest
description: Pull weekly traffic data from Plausible Analytics for artstroy.net, produce a structured digest with top articles, category breakdown, referrer mix, and trend signals. Posted to the root company issue weekly.
---

# Analytics Digest

Traffic data closes the feedback loop: what readers actually read versus what the team published. The digest feeds directly into `topic-prioritization` to rank next articles.

## When to Run

- Weekly (Monday morning, before the morning-brief cadence)
- After any major traffic event (article goes viral, Reddit/HN frontpage, new backlink)
- On demand when EIC asks "how is X performing?"

## Data Source: Plausible API

ArtStroy uses Plausible Analytics. Use `PLAUSIBLE_API_KEY` (declared in `.paperclip.yaml inputs.env`).

Base URL: `https://plausible.io/api/v1/stats/`

Site ID: `artstroy.net`

### Key Endpoints

**Top pages (last 7 days):**
```bash
curl "https://plausible.io/api/v1/stats/breakdown?site_id=artstroy.net&period=7d&property=event:page&limit=10&metrics=visitors,pageviews,bounce_rate,visit_duration" \
  -H "Authorization: Bearer ${PLAUSIBLE_API_KEY}"
```

**Referrer breakdown (last 7 days):**
```bash
curl "https://plausible.io/api/v1/stats/breakdown?site_id=artstroy.net&period=7d&property=visit:referrer&limit=10&metrics=visitors" \
  -H "Authorization: Bearer ${PLAUSIBLE_API_KEY}"
```

**Aggregate totals (last 7 days vs previous 7 days):**
```bash
curl "https://plausible.io/api/v1/stats/aggregate?site_id=artstroy.net&period=7d&metrics=visitors,pageviews,bounce_rate,visit_duration&compare=previous_period" \
  -H "Authorization: Bearer ${PLAUSIBLE_API_KEY}"
```

**Country breakdown (top 5):**
```bash
curl "https://plausible.io/api/v1/stats/breakdown?site_id=artstroy.net&period=7d&property=visit:country&limit=5&metrics=visitors" \
  -H "Authorization: Bearer ${PLAUSIBLE_API_KEY}"
```

## Digest Format

Post as a comment on the root company issue (or the weekly-review issue):

```markdown
## Analytics Digest — Week of {YYYY-MM-DD}

### Aggregate

| Metric | This week | vs. last week |
|---|---|---|
| Visitors | {n} | {+/-X%} |
| Pageviews | {n} | {+/-X%} |
| Bounce rate | {X%} | {+/-X pp} |
| Avg. visit duration | {Xm Xs} | {+/-X%} |

### Top 5 Articles

| Rank | Page | Visitors | Avg. Duration | Bounce |
|---|---|---|---|---|
| 1 | [{title or slug}](https://artstroy.net/{slug}) | {n} | {Xm} | {X%} |
| 2 | ... | | | |
...

### Category Breakdown (derived from slug mapping)

| Category | Visitors | Share |
|---|---|---|
| Pentesting | {n} | {X%} |
| Programming | {n} | {X%} |
| Technology/QA | {n} | {X%} |

### Referrer Mix (Top 5)

| Source | Visitors |
|---|---|
| Direct / None | {n} |
| google.com | {n} |
| dev.to | {n} |
| ... | |

### Top 5 Countries

{table}

### Signals

{2–4 bullet observations, e.g.:}
- Article `{slug}` published Monday; reached Top-5 by Wednesday — strong organic pickup
- Bounce rate on `/pentesting/` articles is {X%} vs {Y%} average — indicates high intent traffic
- dev.to referrals up {X%} after syndication on {date}
- Article `{slug}` (published {date}) still in Top-5 after 3 weeks — evergreen

---
*Data from Plausible Analytics. Period: {start} – {end}.*
```

## Deriving Category from Slug

Article category is in `category` frontmatter, but slugs also follow patterns:
- `owasp_*`, `*injection*`, `*xss*`, `*pentest*` → Pentesting
- `*playwright*`, `*testing*`, `*qa*`, `*automation*` → Technology/QA
- `*typescript*`, `*javascript*`, `*react*`, `*astro*` → Programming

Use frontmatter `category` as primary; slug pattern as fallback.

## Signals to Flag Explicitly

Always call out these patterns when detected:
- Any article with >500 visitors in its first 7 days → "strong launch"
- Any article bouncing back into Top-5 after being absent → "evergreen signal"
- Referrer source appearing for first time → "new traffic channel"
- Bounce rate >80% on a specific article → "possible content-intent mismatch"
- Visit duration <30s on non-landing pages → "possible content quality issue"

## Handoff

After posting the digest, tag the `analytics-analyst` issue with label `ready-for-topic-prioritization`. The Analytics Analyst then runs `topic-prioritization` skill to correlate this digest with pending topic briefs.
