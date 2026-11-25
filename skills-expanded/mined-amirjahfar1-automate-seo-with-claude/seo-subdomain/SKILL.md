---
name: seo-subdomain
description: Subdomain ownership map for a domain. Lists subdomains, queries overview/keywords/competitors/backlinks per subdomain, surfaces which subdomains own which topic clusters, where there's fragmentation, and whether consolidation is warranted. Use when the user asks "subdomain analysis", "subdomain ownership", "subdomain SEO", "blog vs main domain", "support vs docs subdomain", or "should I consolidate subdomains".
---
> Example output: [examples/seo-subdomain-notion-so-20260514/SUBDOMAINS.md](../../examples/seo-subdomain-notion-so-20260514/SUBDOMAINS.md)

# Subdomain Analysis

Map a domain's subdomain ecosystem. Which subdomains exist, what each ranks for, where they overlap, and whether the structure is healthy or fragmented. Output: an ownership map (which topic is owned by which subdomain), a fragmentation report, and recommendations for consolidate / split / leave alone.

## Prerequisites

- DataForSEO MCP server connected.
- User provides: a target root domain (e.g. `example.com`). The skill discovers subdomains automatically.
- Optional: `--limit N` to cap the number of subdomains analysed (default: top 10 by ranked keyword count).

## Process

1. **Validate & preflight**
   - Normalise root domain (no protocol, no `www.`).
   - Cost note: DataForSEO bills per call; subdomain analysis is N × ~5 calls and scales with subdomain count. Use the documented `limit`/`ceiling` params (and `--limit`) to cap.

2. **Discover subdomains** `mcp__dataforseo__dataforseo_labs_google_subdomains`
   - List all subdomains of the root domain.
   - For each: keyword count, traffic estimate, backlinks count.
   - Sort by ranked-keyword count descending.
   - Apply `--limit` (default top 10).

3. **Per-subdomain overview** `mcp__dataforseo__dataforseo_labs_google_domain_rank_overview`
   - For each subdomain in scope: domain rank, traffic estimate, organic + paid keyword counts, top regions.
   - This establishes a baseline for cross-subdomain comparison.

4. **Per-subdomain top keywords** `mcp__dataforseo__dataforseo_labs_google_ranked_keywords`
   - For each subdomain: top 100 organic keywords with positions, intent, traffic.
   - Cluster keywords by topic. This skill's grouping is a lightweight per-subdomain ownership map, not a content plan — token-grouping by head term + intent is sufficient here. (For full content-cluster planning use `seo-keyword-cluster`, which now clusters by SERP overlap, not text similarity.)
   - Each subdomain gets a list of "owned topics" (clusters where it dominates) and "minor topics".

5. **Per-subdomain competitors** `mcp__dataforseo__dataforseo_labs_google_competitors_domain`
   - For each subdomain: top organic competitors by `common_keywords`.
   - Surface: do different subdomains have different competitor sets? (Sign of legitimately separate scopes.) Do they share competitors? (Sign of redundant scopes.)

6. **Per-subdomain backlinks** `mcp__dataforseo__backlinks_summary` and `mcp__dataforseo__backlinks_referring_domains` (top 20)
   - Subdomains often have separate backlink profiles. Capture each.
   - Surface: do subdomains have meaningfully different referring-domain populations?

7. **Rank distribution** `mcp__dataforseo__backlinks_bulk_ranks`
   - For each subdomain, pull the referring domains (from step 6) and derive the histogram of their DataForSEO rank.

8. **Detect fragmentation**
   - For each topic-cluster, identify all subdomains ranking for keywords in that cluster.
   - **Fragmentation signal:** ≥ 2 subdomains rank in the top 50 for the same high-volume keyword (cannibalization).
   - **Healthy split:** distinct topic clusters per subdomain, minimal overlap.

9. **Make recommendations**
   - **Consolidate:** if `blog.example.com` and `example.com/blog/` both rank for the same topic cluster but neither dominates — pick one canonical home.
   - **Split:** if a subdomain is ranking for a topic completely off-mission for the root domain, that's a split worth keeping.
   - **Leave alone:** if subdomains have distinct topic ownership and don't cannibalize, don't disturb.
   - **Investigate:** ambiguous cases flagged for human review.

10. **Synthesise** `SUBDOMAINS.md`

## Output format

Create a folder `seo-subdomain-{target-slug}-{YYYYMMDD}/` with:

```
seo-subdomain-{target-slug}-{YYYYMMDD}/
├── SUBDOMAINS.md                       (synthesised report + recommendations — primary deliverable)
├── 06-topic-ownership-map.md           (cluster × subdomain matrix — load-bearing reference content teams brief from)
├── 07-fragmentation-flags.md           (cannibalization detected — load-bearing reference for consolidation decisions)
└── evidence/
    ├── 01-subdomains-list.md           (dataforseo_labs_google_subdomains — raw step output)
    ├── 02-overview-by-subdomain.md     (per-subdomain overview rows)
    ├── 03-keywords-by-subdomain/
    │   ├── blog-example-com.md
    │   ├── docs-example-com.md
    │   └── ...                          (one per subdomain)
    ├── 04-competitors-by-subdomain.md
    └── 05-backlinks-by-subdomain.md
```

Top-level: `SUBDOMAINS.md` + `06-topic-ownership-map.md` + `07-fragmentation-flags.md`. Content teams brief from the ownership map; consolidation decisions cite the fragmentation flags directly. The 01–05 step files preserve raw API outputs in `evidence/`.

`SUBDOMAINS.md` follows this shape:

```markdown
# Subdomain Analysis: {root domain}

> Snapshot dated {YYYY-MM-DD} · Subdomains analysed: {n} of {n discovered} (limit: top {limit} by keyword count)

## Subdomain inventory

| Subdomain | Keywords | Traffic est. | Backlinks | Domain rank | Top topics owned |
|---|---|---|---|---|---|
| {root} | {n} | {n}/mo | {n} | {rank} | {topics} |
| blog.{root} | {n} | {n}/mo | {n} | {rank} | {topics} |
| docs.{root} | {n} | {n}/mo | {n} | {rank} | {topics} |
| ... |

## Topic ownership map

| Topic cluster | Owned by | Also ranks (cannibalization?) |
|---|---|---|
| {topic 1} | blog.{root} (avg pos 3.2 across 47 keywords) | {root} (avg pos 12) — {⚠ cannibalization} |
| {topic 2} | docs.{root} | (none) |
| ... |

## Fragmentation flags

### {⚠ Cannibalization detected: topic = {topic X}}
- `blog.{root}` ranks {n} keywords for {topic X}, avg position {p}.
- `{root}` (root path) ranks {m} keywords for the same topic, avg position {p}.
- The two sets overlap on {k} exact keywords.
- **Recommendation:** consolidate to `blog.{root}` (the stronger ranker). 301 the root-path duplicates with intent preserved.

### ... (per fragmentation finding)

## Recommendations summary

- **Consolidate:** {n} subdomain pairs → see fragmentation flags above.
- **Split intentional and healthy:** {n} subdomains have distinct ownership; leave alone.
- **Investigate:** {n} edge cases flagged for human review.

## Risk notes

- Subdomain consolidation requires careful 301 redirect mapping; track via `seo-drift` after the migration.
- A subdomain with separate backlinks (per `evidence/05-backlinks-by-subdomain.md`) is harder to consolidate without losing link equity — plan accordingly.

## Raw data
- See per-subdomain files under `evidence/03-keywords-by-subdomain/`.
- Topic ownership matrix: `06-topic-ownership-map.md`.
```

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent. Skills pace sequentially. The skill makes ~5 calls per subdomain. With `--limit 10`, that's ~50 calls.
- DataForSEO bills per call; cost scales with subdomain count. Use `limit`/filters (and `--limit`) to cap — a `--limit 10` run issues ~50 calls, unlimited can run much higher.
- **`--limit` is your friend.** Sites with hundreds of subdomains (large platforms) don't need every subdomain analysed — top 10 by keyword count covers >90% of organic value usually.
- **Don't conflate "subdomain has lower rank" with "subdomain is bad."** Subdomains often have lower rank than the root because they accumulate links separately. The question is topic ownership and cannibalization, not rank per se.
- **Consolidation is risky.** A 301 from `blog.example.com` to `example.com/blog/` retains most link equity but can lose 5–15% in transition. Track post-migration with `seo-drift`.
- **Don't recommend consolidation when one subdomain is on a different platform.** If `blog.example.com` is on a different CMS, the engineering cost of consolidation may exceed the SEO benefit. Surface this as a constraint, not a recommendation.
- The topic-ownership matrix is the highest-leverage artifact. Use it to brief content teams on which subdomain should publish what.
- Pair with `seo-page` to deep-dive into specific URLs flagged in cannibalization.
- Pair with `seo-drift` to baseline subdomains before major restructures.
