---
name: seo-backlinks-profile
description: Full backlink profile for a domain — referring domains, anchor text distribution, authority distribution, IP and subnet diversity, growth/decay trend, toxic-candidate flagging. Distinct from `seo-backlink-gap` (which is gap-vs-competitor only). Produces a profile health score and reviewable disavow candidate list (never auto-disavow). Use when the user asks "backlink profile", "link profile audit", "anchor distribution", "toxic links", "disavow candidates", or "backlink health".
---
> Example output: [examples/seo-backlinks-profile-stripe-com-20260514/PROFILE.md](../../examples/seo-backlinks-profile-stripe-com-20260514/PROFILE.md)

# Backlinks Profile

A complete backlink profile audit for a domain. Surfaces composition (where do links come from?), quality (what's the authority distribution?), diversity (concentrated in a few IPs/subnets, or spread out?), trajectory (growing or decaying?), and risk (which links look manipulative?). Output includes a health score and a reviewable disavow-candidate list — never an auto-disavow.

## Single-source by design

This skill consults **only the DataForSEO backlink index**. We don't blend Ahrefs / Moz / Majestic / Common Crawl into the same report. That's a deliberate choice, not a limitation:

- **Internally consistent metrics.** Authority scores, anchor counts, and refdomain totals are computed against a single crawl. Multi-source blends produce numbers that look authoritative but actually average across crawls with different sampling, different freshness, and different definitions of "backlink" — the resulting ratios (e.g. dofollow %, anchor distribution) are noise.
- **Reproducible health scores.** The 100-point health score in this report can be re-run a quarter later against the same source and the deltas are meaningful. With multi-source blends, a score drift can mean *anything*: source A reweighted, source B refreshed, source C changed its toxic heuristic.
- **No data-source independence to model.** Any "do these sources agree?" question is unanswerable without a second backlink graph; we don't pretend to answer it. If you need cross-source confirmation (e.g. before legal disavow, before a high-stakes outreach campaign), pair this profile with a manual spot-check against Ahrefs/Majestic — that's a research task, not a skill output.

If your workflow specifically *requires* multi-source blending (large agencies, link-builders billing on link counts), this skill is the wrong tool — use a vendor that aggregates multiple indexes. For everyone else, single-source produces the more honest report.

## Prerequisites

- DataForSEO MCP server connected.
- User provides: a target domain.
- Claude's `WebFetch` tool optional (for spot-checking flagged toxic candidates).
- `mcp__firecrawl-mcp__firecrawl_scrape` optional (for the new step 8b — link-source verification).

## Process

1. **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (cost note, Firecrawl availability, Google APIs). Skill-specific notes:
   - Normalise domain before continuing.
   - Cost note: DataForSEO bills per call; this run issues ~15 calls. Use the documented `limit`/`ceiling` params to cap.
   - Firecrawl: optional. When `--verify-sources` is passed, step 8b (link-source verification) scrapes top-20 referring domains' linking pages to verify each link is still present and what `rel` it carries (dofollow / nofollow / sponsored / UGC), ~20 Firecrawl credits per run. Default off; pass `--no-firecrawl` to skip even if available.
   - Google APIs: not used.

2. **Profile summary** `mcp__dataforseo__backlinks_summary`
   - Total backlinks, total referring domains, dofollow/nofollow ratio, link-type distribution (text / image / form / frame), growth velocity over the last 30/90 days.

3. **Referring domains** `mcp__dataforseo__backlinks_referring_domains`
   - Top N referring domains by rank. Pull rank score, link count per domain, domain TLD, country.

4. **Anchor distribution** `mcp__dataforseo__backlinks_anchors`
   - Top anchor texts by frequency.
   - Classify each anchor: branded (contains brand name), exact-match commercial (the target's primary commercial keyword), partial-match, generic ("click here", "read more", "this page"), naked URL, image-alt-derived.

5. **Rank distribution** `mcp__dataforseo__backlinks_bulk_ranks` and `mcp__dataforseo__backlinks_summary`
   - Histogram of referring-domain rank (0–1000): how many rank 0-99, 100-199, etc. (Derive the histogram from the ranks of referring domains.)
   - A healthy profile has a long tail; an unhealthy profile is concentrated at low rank.

6. **IP and subnet diversity** `mcp__dataforseo__backlinks_referring_networks`
   - Total unique IPs hosting referring domains (set `network_type` to `ip`).
   - Total unique /24 subnets (set `network_type` to `subnet`).
   - Compute concentration ratio: `referring_domains / unique_subnets`. Healthy: ~3–10. Unhealthy: many domains share few subnets (PBN signal).

7. **Growth / decay trend** `mcp__dataforseo__backlinks_timeseries_new_lost_summary`, `mcp__dataforseo__backlinks_bulk_new_lost_referring_domains`
   - Net new backlinks per month (last 6 months).
   - Net new referring domains per month.
   - Velocity changes — sharp spikes or sharp losses both deserve flags.

8. **Lost links list** `mcp__dataforseo__backlinks_bulk_new_lost_backlinks`, `mcp__dataforseo__backlinks_bulk_new_lost_referring_domains`
   - Sample recent losses. Are any high-rank losses?

8b. **Optional: live link-source verification** `mcp__firecrawl-mcp__firecrawl_scrape`
   - Triggered only when `--verify-sources` is passed (default off — credit-conscious).
   - For the top 20 referring domains by authority (from step 3), pick the highest-authority linking page per domain. Scrape each (20 Firecrawl credits typical).
   - For each scrape, parse the returned `html` for `<a href>` matching the target domain. Capture: link still present (`true`/`false`/`page-404`), `rel` attribute (`dofollow` if absent or empty, else the literal value: `nofollow`, `ugc`, `sponsored`, or combinations), surrounding context (anchor text + 50 chars before/after).
   - Surface mismatches against the DataForSEO-reported state in `evidence/08b-source-verification.md`:
     - Link gone — DataForSEO still reports it as live (lag/error).
     - `rel` attribute differs from what DataForSEO flagged.
     - Source page returns non-200.
   - Feeds into step 9: a verified-gone link or `rel=nofollow` discovered post-hoc upgrades the toxic-candidate signal for that referring domain.
   - **If Firecrawl unavailable (or flag not passed):** skip entirely. DataForSEO's flagged state remains the source of truth — the skill's "Single-source by design" framing already explains why that's a deliberate trade-off.

9. **Toxic candidate detection** `mcp__dataforseo__backlinks_bulk_spam_score` (plus the heuristic — see Tips for the rules)
   - Pull `spam_score` for the referring domains — this is the toxic-signal proxy. Then apply the toxic heuristic to the referring-domain list.
   - Flag candidates. Each row gets a `risk_score` and `triggers` (which heuristic rules fired, including high `spam_score`).
   - **Never auto-disavow.** Output is a reviewable list, not an action.

10. **Synthesise** `PROFILE.md`

## Output format

Create a folder `seo-backlinks-profile-{target-slug}-{YYYYMMDD}/` with:

```
seo-backlinks-profile-{target-slug}-{YYYYMMDD}/
├── PROFILE.md                       (synthesised report — primary deliverable; inlines summary, authority distribution, diversity, trend)
├── 02-referring-domains.md          (top N with rank — load-bearing reference for outreach/audit)
├── 03-anchors.md                    (anchor distribution + classification — load-bearing reference)
├── disavow-candidates.csv           (toxic-flagged rows for review — load-bearing CSV)
└── evidence/
    ├── 01-summary.md                (backlinks_summary top-line — raw step output)
    ├── 04-rank-distribution.md      (histogram — raw step output)
    ├── 05-diversity.md              (IPs + subnets + concentration — raw step output)
    ├── 06-trend.md                  (last 6 months new/lost — raw step output)
    ├── 07-losses-sample.md          (recent lost backlinks)
    └── 08b-source-verification.md   (only if --verify-sources ran: live link + rel attribute checks for top-20 sources)
```

Step files 01, 04, 05, 06 are inlined as sections in `PROFILE.md`; the copies in `evidence/` preserve raw step output for reproducibility. `02-referring-domains.md`, `03-anchors.md`, and `disavow-candidates.csv` stay at top level — outreach/audit teams consult them directly.

Note: `04-rank-distribution.md` holds the referring-domain rank histogram described in step 5.

`PROFILE.md` follows this shape:

```markdown
# Backlinks Profile: {domain}

> Snapshot dated {YYYY-MM-DD}

## Health score: **{n}/100**

| Dimension | Score | Notes |
|---|---|---|
| Rank distribution | {n}/20 | {comment} |
| Anchor diversity | {n}/20 | {comment} |
| IP/subnet diversity | {n}/20 | {comment} |
| Growth trajectory | {n}/20 | {comment} |
| Toxic candidate ratio | {n}/20 | {comment} |

## Top-line numbers

| Metric | Value |
|---|---|
| Backlinks | {n} |
| Referring domains | {n} |
| Dofollow / nofollow | {n}% / {n}% |
| Unique IPs | {n} |
| Unique subnets | {n} |
| Domain : subnet ratio | {ratio} |
| New ref-domains last 30d | {n} |
| Lost ref-domains last 30d | {n} |
| Toxic candidates flagged | {n} ({% of total}) |

## Rank distribution

| Rank bucket | Domains | % |
|---|---|---|
| 700+ | {n} | {%} |
| 500–699 | {n} | {%} |
| 300–499 | {n} | {%} |
| 100–299 | {n} | {%} |
| 0–99 | {n} | {%} |

## Anchor distribution

| Class | Count | % | Healthy range | Status |
|---|---|---|---|---|
| Branded | {n} | {%} | 30–60% | {✓/⚠} |
| Generic | {n} | {%} | 15–30% | {✓/⚠} |
| Naked URL | {n} | {%} | 10–25% | {✓/⚠} |
| Partial-match | {n} | {%} | 10–20% | {✓/⚠} |
| Exact-match commercial | {n} | {%} | <5% | {✓/⚠ over-optimised} |
| Image-alt-derived | {n} | {%} | <10% | {✓/⚠} |

## Trend (last 6 months)

| Month | New backlinks | Lost backlinks | Net |
|---|---|---|---|
| {M-5} | {n} | {n} | {n} |
| {M-4} | {n} | {n} | {n} |
| ... |

## Toxic candidates ({n} flagged)

See `disavow-candidates.csv`. Top 10 by risk_score:

| Domain | Rank | Triggers | Risk |
|---|---|---|---|
| {domain} | {rank} | {rank<100, sitewide>5, exact-match-anchor} | High |
| ... |

**⚠ NEVER AUTO-DISAVOW.** Hand this list to a human for review. Disavow a domain only after confirming the link is manipulative AND the domain is not delivering referral traffic AND removal requests have failed.

## Recommended next steps

1. {Action}
2. {Action}
3. {Action}
```

`disavow-candidates.csv` columns: `domain,rank,spam_score,backlinks_count,sitewide_links,top_anchor,anchor_class,risk_score,triggers,sample_url`

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent. Skills pace sequentially. The endpoints in steps 2–8 are ~15 calls.
- Cost: DataForSEO bills per call; a full profile run issues ~15 calls. Use `limit`/filters to cap large referring-domain/backlink lists. Optional step 8b adds 20 Firecrawl credits when `--verify-sources` is passed (one scrape per top-20 source domain).
- **Toxic heuristic rules** (any 2+ triggers = candidate):
  - DataForSEO `rank` < 100 or high `spam_score` (low-trust source).
  - Sitewide link count > 5 (footer/sidebar links across many pages — manipulation signal).
  - Exact-match commercial anchor on >50% of links from this domain.
  - Hosted in known link-farm subnet (when unique IPs / unique subnets ratio is heavily concentrated).
  - Domain name is a non-pronounceable string of characters (very strong PBN signal).
  - TLD is in the high-spam list (`.xyz`, `.click`, `.work` historically; verify against current spam-domain reports).
- **Healthy anchor distribution**: branded should be the largest class (30–60%); exact-match commercial should be small (<5%) — over-optimised commercial anchors trigger Penguin-era penalties.
- **Healthy growth**: steady 10–20% YoY referring-domain growth is the goal. Sharp spikes (>50% in a month) often indicate paid links and trigger algorithmic suspicion.
- **Disavow conservatively.** Removing links via outreach is preferred. Disavow only as a last resort; never disavow domains that send referral traffic.
- Pair with `seo-backlink-gap` for prospecting (gap analysis vs competitors).
- Pair with `seo-drift` to track profile composition over time.
