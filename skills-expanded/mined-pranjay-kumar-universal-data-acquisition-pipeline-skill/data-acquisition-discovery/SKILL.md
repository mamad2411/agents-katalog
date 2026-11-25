---
name: data-acquisition-discovery
description: "Use for discovering and reverse-engineering data sources: official APIs, XHR/fetch, GraphQL, persisted queries, Algolia, Shopify, Salesforce Commerce Cloud, sitemaps, feeds, embedded JSON, hydration state, page-data routes, pagination limits, headers, params, and endpoint templates."
---

# Data Acquisition Discovery

Act as the endpoint/source discovery specialist. Prefer structured routes over brittle DOM extraction.

## Shared Core

Read from `../data-acquisition-core/references/`:

- `source-access.md`
- `pattern-library.md`
- `endpoint-discovery.md`
- `probing.md`
- `source-strategies.md`
- `output-contracts.md`
- `compliance-boundaries.md`

## Output

Return:

- `ModeSelection`
- `SourceAccessClass`
- `SourcePlan`
- `EndpointPlan`
- `HeaderProfile`
- `ProbeResults`
- pagination/limit findings
- `ApprovalGate`

Use tiny probes. Do not harvest broad lists just to learn pagination.
