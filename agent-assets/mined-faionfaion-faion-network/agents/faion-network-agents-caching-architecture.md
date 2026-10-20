# Caching Architecture

## Summary

**One-sentence:** Design multi-layer caching (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around.

**One-paragraph:** Caching architecture is a contract between layers about who reads, who writes, who invalidates, and what TTL applies. Output is a per-data-class caching policy document plus a Redis/CDN config that implements it. Wrong pattern choice creates either thundering herds (cache-aside without single-flight) or stale data (write-behind without idempotency).

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- At least one read-heavy endpoint with p95 latency above the SLO budget.
- Database costs dominated by read traffic, not writes.
- Data classes have distinguishable freshness requirements (real-time vs minutes vs hours).

## Skip If (ANY kills it)

- Write-heavy workload with cache hit rate < 30%.
- Strict consistency required end-to-end (cache adds risk without latency win).
- Prototype with no SLO commitments.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-endpoint RPS + latency profile | table | observability backend |
| Per-data-class freshness budget | table | PM/architect |
| Cache substrate (Redis/Memcached/CDN) | name + version | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Gateway is one cache layer. |
| `solo/dev/software-architect/database-selection` | DB choice influences cache pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for the caching policy + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: profile → classify → pick pattern → TTL → invalidation → load test | ~900 |
| `content/05-examples.xml` | medium | Worked example: product detail cache-aside + checkout no-cache | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-data` | sonnet | Per-endpoint data class assignment. |
| `pick-pattern` | sonnet | Per-data-class pattern selection. |
| `audit-cross-layer` | opus | Detect inconsistent TTLs across layers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-policy.md.j2` | Per-data-class caching policy with pattern + TTL + invalidation rule. |
| `templates/caching-policy.md` | Per-data-class caching policy with pattern + TTL + invalidation rule. Generated from `templates/caching-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/redis-config.conf` | Production Redis standalone config: maxmemory + eviction policy + bind + auth. |
| `templates/cache-service.py` | Python cache-service skeleton: get-or-set + stampede protection + tag invalidation. |
| `templates/django-cache-settings.py` | Django `CACHES` settings block wired to Redis with per-view + low-level patterns. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-architecture.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-gateway-patterns]]
- [[database-selection]]
- [[data-modeling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
