---
name: shopify-app
description: "Build Shopify apps with OAuth or session tokens, Admin GraphQL, extensions, webhooks, and billing integration."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["shopify", "app", "graphql", "webhooks", "oauth", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Shopify App Development AI Skill Guide

## Overview & Engine Architecture

Shopify apps extend merchant admin and storefronts via OAuth (or session tokens for embedded apps), Admin GraphQL/REST, webhooks, and UI extensions. Apps store shop-scoped credentials, verify webhook HMAC, and respect API versioning. Agents design idempotent webhook handlers, least-privilege scopes, and embedded auth that never trusts client-reported shop data alone.

```
Merchant shop
   -> Embedded app (App Bridge / session tokens)
       -> Your backend (validate session, shop record)
           -> Admin GraphQL API
Shopify -> webhooks (HMAC) -> Your backend
```

## When to use this skill

- Scaffolding public or custom Shopify apps
- Implementing OAuth/session-token auth correctly
- Subscribing to and processing webhooks
- Calling Admin GraphQL with cursor pagination

## Operational directives

1. Request minimum scopes; document why each scope exists.
2. Verify webhook HMAC on the raw body; process by `X-Shopify-Webhook-Id` idempotently.
3. Pin and review Admin API versions; handle deprecations before deadline.
4. For embedded apps, validate session tokens; never trust `shop` query params alone.
5. Store access tokens encrypted at rest; support app uninstall cleanup (`app/uninstalled`).

## GraphQL sketch

```graphql
query Orders($cursor: String) {
  orders(first: 50, after: $cursor) {
    edges {
      cursor
      node { id name displayFulfillmentStatus }
    }
    pageInfo { hasNextPage }
  }
}
```

## Webhook checklist

| Step | Requirement |
| --- | --- |
| Signature | HMAC of raw body with app secret |
| Idempotency | Persist webhook ID / dedupe key |
| Latency | Respond 200 quickly; heavy work async |
| Uninstall | Delete shop tokens and scheduled jobs |

## Best practices

- Prefer GraphQL Admin API over legacy REST for new work.
- Use Shopify CLI for app scaffolding, extensions, and `app dev` tunneling.
- Test billing (if used) in test stores; handle declined charges explicitly.
- Log shop domain + topic, never full PII payloads in plain logs.

## Limitations

- Theme app extensions and checkout extensibility have platform constraints by plan.
- Rate limits (cost-based GraphQL) require budgeting and backoff.
- Plus-only APIs are unavailable on standard shops.

## Related skills

- `@graphql-client` - client patterns for Admin/Storefront GraphQL
- `@nodejs` - webhook HTTP servers
- `@zapier` - lightweight merchant automations without a full app
