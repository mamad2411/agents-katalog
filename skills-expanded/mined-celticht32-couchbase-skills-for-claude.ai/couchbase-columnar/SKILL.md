---
name: couchbase-columnar
description: "Design and use Couchbase Capella Analytics (formerly Capella Columnar), the standalone columnar analytics database service on Capella. Use whenever the user asks about Capella Analytics, Capella Columnar, columnar analytics, an Analytics instance, Capella Analytics vs the operational Analytics Service, Analytics collections, links to operational data, Analytics SQL++, pricing, when to use standalone Capella Analytics vs the embedded Analytics Service, or 'I need to run analytical queries on my Couchbase data.' Distinct from the cb-analytics-* skills (which cover the Couchbase Analytics Service embedded in Couchbase Server / Capella operational clusters) — Capella Analytics is a separate, standalone columnar database product on Capella. Use proactively when the user needs OLAP-scale analytics, BI tool integration, or columnar storage for analytical workloads."
license: MIT
---

# Couchbase Capella Analytics

A skill for *designing and using* Couchbase Capella Analytics — the standalone columnar analytics database product on Capella.

> **Naming:** Couchbase formally rebranded **Capella Columnar** to **Capella Analytics**. This skill uses "Capella Analytics" for the product. The lowercase word "columnar" still appears where it describes the underlying *storage format* (columnar storage), and some API/endpoint names retain "Columnar" (e.g. Columnar Analytics Cluster) — those are left as-is where they are literal identifiers.

Distinct from the `cb-analytics-*` skills, which cover the **Analytics Service** embedded within Couchbase Server / Capella operational clusters. These are different products:

| | Analytics Service (embedded) | Capella Analytics (standalone) |
|---|---|---|
| **What it is** | Analytics service co-located with an operational cluster | Standalone columnar database, separate instance |
| **Where it runs** | On Analytics nodes of an operational cluster | Separate Capella Analytics instance on Capella |
| **Data ingestion** | DCP-based streaming from the operational cluster | Links to Capella operational cluster, S3, or external sources |
| **Storage** | Row-oriented (same as operational) | True columnar storage |
| **Best for** | Ad-hoc analytics alongside operational workloads | OLAP, BI tools, large analytical queries |
| **Skills** | `cb-analytics-*` | This skill |

## When this skill applies

- "What's Capella Analytics (Capella Columnar)?"
- "Should I use standalone Capella Analytics or the embedded Analytics Service?"
- "How do I connect Capella Analytics to my operational Capella cluster?"
- "How do I connect a BI tool (Tableau, Power BI, Looker) to Couchbase?"
- "How do I query JSON data in Capella Analytics?"
- "What's the difference between Analytics collections and operational collections?"

## Pick the right reference

| Question | Read |
|---|---|
| "Capella Analytics architecture, when to use it vs the embedded Analytics Service" | `references/architecture.md` |
| "Connecting data sources, querying, BI tool integration" | `references/usage.md` |

## Core principle: Capella Analytics is for OLAP, not OLTP

Capella Analytics is optimized for analytical queries — large scans, aggregations, GROUP BY, window functions, JOINs across large datasets. It is not a replacement for the operational cluster. Transactional writes (your application's reads/writes) still go to the operational cluster. Capella Analytics receives data via links and stores it in columnar format for efficient analytical access.

## Related skills

- `cb-analytics-*` — the Analytics Service embedded in operational clusters (different product)
- `couchbase-capella` — provisioning the operational Capella cluster that Capella Analytics links to
- `couchbase-sqlpp-tuning` — SQL++ query patterns apply to Capella Analytics with minor differences
