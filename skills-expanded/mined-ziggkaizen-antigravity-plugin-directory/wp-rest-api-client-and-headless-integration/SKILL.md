---
name: wp-rest-api-client-and-headless-integration
description: Designs resilient WordPress REST API clients and headless integrations with discovery, pagination, field selection, authentication, retries, caching, preview, and contract-drift handling. Use for external or decoupled consumers.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Client and Headless Integration

## Use this skill when

- Building a headless frontend, mobile app, integration service, or CLI client.
- Consuming core or custom WordPress REST routes.
- Implementing preview, draft, media, search, or authenticated editing.
- Fixing over-fetching, pagination, retries, or contract drift.

## Approach

1. Record server, client, authentication, proxy/CDN, and deployment requirements.
2. Discover available namespaces and schemas instead of assuming routes.
3. Define client types from the server contract.
4. Request only needed fields and embedded relationships.
5. Implement pagination, cancellation, timeouts, errors, and bounded retries.
6. Separate public and private caches.
7. Define preview, draft, media, redirect, webhook/invalidation, and fallback behavior.
8. Add contract fixtures and compatibility monitoring.

## Workflow

Use [headless-client-integration-workflow.md](workflows/headless-client-integration-workflow.md).

## Resources

- [client-integration-checklist.md](resources/client-integration-checklist.md)
- [discovery-pagination-and-fields.md](resources/discovery-pagination-and-fields.md)

## Output

Return:

- Client/server compatibility baseline.
- Authentication and secret-storage plan.
- Typed contract or schema strategy.
- Pagination, field, cache, retry, and failure behavior.
- Preview and content lifecycle plan.
- Contract and integration tests.
