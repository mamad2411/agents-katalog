---
name: growth-seo-core
description: "Shared reference for the growth-seo cluster: the search-intent model every task turns on, the one-query-per-page contract, the intent→content-type matrix, the E-E-A-T/quality bar, and the funnel pipeline. USE WHEN mapping keywords to pages, judging whether content will rank, planning programmatic pages, or deciding informational vs commercial vs transactional treatment."
cluster: growth-seo
version: 1.0.0
---

# Growth-SEO Core

Shared model for the `growth-seo` cluster. Research, content, architecture, and audit spokes all
depend on these interlocking ideas — keep them consistent here so no spoke contradicts another.

## 1. The defining decision: search intent → page

Every SEO task reduces to one question: **what query does this page serve, and what does the
searcher actually want?** Get this right and ranking, structure, schema, and AI visibility follow;
get it wrong and no amount of optimization saves the page.

```
Demand (a query) ──has──> Intent ──determines──> Content type ──filled by──> ONE page ──earns──> Visibility
```

- **Intent** — the job behind the query. Four classic types (below). Misreading intent is the #1 cause of "good content that won't rank." → `searchintentautomation`, `google-official-seo-guide`
- **One primary query per page** — each URL targets one primary query (+ a tight cluster of variants). Two pages chasing the same query = **keyword cannibalization**; merge or differentiate. → `seo-content-brief`, `site-architecture`
- **Content type follows intent** — the SERP tells you the expected format; match it or lose. → matrix below.

**Rule:** name the query and its intent **before** writing, building, or auditing a page.

## 2. Intent → content-type matrix

| Intent | Searcher wants | Right page type | Primary spoke |
|---|---|---|---|
| **Informational** | to learn / an answer | guide, how-to, definition, FAQ | `seo-content-brief`, `ai-seo` |
| **Commercial** | to compare before buying | comparison, "best X", review, alternatives | `programmatic-seo`, `seo-content-brief` |
| **Transactional** | to act / buy now | product, pricing, signup, location page | `programmatic-seo`, `site-architecture` |
| **Navigational** | a specific site/brand | home, brand, login, docs landing | `site-architecture` |

Mismatch examples to avoid: a sales page targeting an informational query; a thin definition page
targeting a transactional one. The SERP's current results are the ground truth for type.

## 3. The quality / E-E-A-T bar

Rankings are earned, not manipulated. Google rewards **Experience, Expertise, Authoritativeness,
Trustworthiness**. → `google-official-seo-guide`, `seo-audit`

- Each page must add value a searcher can't get from the SERP snippet alone.
- **Programmatic pages** must clear the same bar *per URL* — real data, unique value, never thin
  doorway pages at scale. → `programmatic-seo`
- Trust signals (structure, schema, internal links, accurate sources) compound authority. → `schema-markup`, `site-architecture`

## 4. Technical foundation

Intent and quality only pay off if Google (and AI crawlers) can reach and understand the page.

- **Crawl → index → rank** is the pipeline; a page that isn't indexed can't rank. → `seo-audit`, `google-official-seo-guide`
- **Core Web Vitals** and on-page hygiene (titles, meta, headings, canonicals) are table stakes. → `seo-audit`
- **Structured data** (JSON-LD) makes content machine-readable and unlocks rich results. → `schema-markup`
- **Site architecture** (URL structure, hierarchy, internal linking) distributes authority and signals topical relevance. → `site-architecture`

## 5. AI search is downstream, not separate

AEO / GEO / LLMO (getting cited in AI Overviews, ChatGPT, Perplexity) runs on the **same**
intent + E-E-A-T + structure foundation — clear answers, quotable structure, schema, authority.
It is an extension of good SEO, not a parallel trick. → `ai-seo`

## 6. The funnel pipeline (how the spokes chain)

```
understand → research intent → brief → architect → produce/enrich → optimize
google-…guide  searchintent…   seo-content-brief  site-architecture  schema-markup / programmatic-seo  seo-audit / ai-seo
```

## 7. Shared guardrails

- **Intent before output**: name the query + intent before producing any page.
- **One primary query per page**: avoid cannibalization; merge or differentiate competitors.
- **Match type to intent**: let the live SERP decide the format.
- **Earn, don't manipulate**: genuine E-E-A-T; no thin pages, cloaking, or doorway pages — even at scale.
- **Index-able first**: crawlable, fast, structured; an unindexed page can't rank.
- **AI visibility = SEO done well**: same foundation, not a separate hack.
- State any change that affects what a URL targets or how it's crawled/indexed.
