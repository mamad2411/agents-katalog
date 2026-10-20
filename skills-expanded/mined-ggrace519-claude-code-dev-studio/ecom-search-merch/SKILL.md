---
name: ecom-search-merch
description: Search and merchandising specialist. Owns product search (Elastic, OpenSearch, Algolia, Vespa), relevance tuning, faceting, ranking, synonyms, and merchandising rules (pinning, boosting, personalization). Auto-invoked for any search, browse, or ranking work.
---

# E-commerce Search & Merchandising

Search is the store: if customers can't find it, you didn't stock it. Relevance
changes move conversion directly, so every tuning decision needs a metric and a
test, not a "looks better".

## When to reach for this

- Designing a product index (fields, analyzers, denormalization) or choosing an engine
- Tuning relevance, synonyms, or ranking signals; debugging "why does X rank above Y"
- Adding merchandising rules — pinning, boosting, demotion, personalized reranking
- Shipping any ranking change that needs an A/B or interleaved test

## Principles

1. **Define the metric before tuning.** Pick nDCG@10, MRR, or CTR@k plus a
   conversion proxy, and a baseline query set (top ~200 queries by volume +
   known-bad long tail). Tuning without a fixed eval set is motion, not progress.
2. **Two-stage ranking.** Cheap, high-recall first stage (BM25 / engine default)
   over the full index; expensive rerank (learned model or weighted business
   score) only on the top 100–200. Never run the expensive signal corpus-wide.
3. **Business signals belong in ranking** — margin, stock depth, conversion
   rate, return rate — but as bounded boosts on a relevant candidate set. A
   high-margin irrelevant product is still irrelevant.
4. **Merchandising is an overlay, not an overwrite.** Pins/boosts/demotions
   layer on top of relevance with explicit precedence (pin > demotion > boost >
   organic) and an expiry date on every rule. Rules without owners and expiries
   accumulate into an unexplainable ranking.
5. **Out-of-stock handling is a ranking decision.** Demote or filter
   unavailable items at query time from a fresh availability signal — don't wait
   for full reindex; stale stock in results burns trust on both ends.
6. **Every change ships behind a test.** A/B or interleaving with a
   pre-registered metric; interleaving needs far less traffic for ranking
   comparisons.

## Index design checklist

- [ ] Searchable text fields with per-language analyzers; `keyword` subfields for exact match/facets
- [ ] Synonym set is data, deployable without reindex (search-time synonyms)
- [ ] Facet fields denormalized onto the product doc (brand, category path, price bucket, attributes)
- [ ] Ranking signals (margin, conversion, stock) updated on their own cadence — partial update or join, not full reindex
- [ ] Variant collapsing decided (index parent + roll up variants vs collapse at query time)
- [ ] Zero-results queries logged with filters applied — top source of synonym and taxonomy fixes
- [ ] Eval set + metric stored in-repo and runnable against any index build

## Pitfalls

- Tuning field boosts by hand against three pet queries and regressing the long tail
- Synonyms applied index-time only — every fix forces a reindex
- Business boosts so large they reorder irrelevant items into the top 10
- Merchandising rules with no expiry, owner, or audit log
- Facet counts computed post-filter on a truncated result page instead of by the engine
- Personalized reranking evaluated with non-personalized offline metrics only

---
*Related: `ecom-inventory` (the availability signal itself),
`ecom-storefront-perf` (search latency on the critical render path),
`ecom-promotions` (promoted-product boosts) · domain agent: `ecom-architect`
(search platform topology) · output/ADR format: `playbook-conventions`*
