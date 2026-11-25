---
name: shopify-graphql
description: >
  Shopify Admin GraphQL API navigator. Use this skill whenever you need to build GraphQL queries
  or mutations against the Shopify Admin API — product CRUD, order management, inventory,
  fulfillment, customers, discounts, subscriptions, metafields, or any other Shopify admin operation.
  Also use when the user asks about Shopify API structure, available fields, input types, or
  pagination patterns. Triggers on: Shopify, Admin API, GraphQL, product query, order mutation,
  inventory adjustment, fulfillment, metafield, or any Shopify resource name.
---

# Shopify Admin GraphQL API

This skill provides navigable access to the full Shopify Admin GraphQL API schema.
Instead of loading the entire schema (8MB+), load only the fragments you need by following
the progressive disclosure pattern below.

## How to Navigate

1. **Start here** — read the conventions below to understand API patterns.
2. **Find the right domain** — scan the domain directory to locate the business area.
3. **Load the domain file** — read the domain reference to find specific operations.
4. **Load the operation** — read the specific query or mutation `.md` file.
5. **Follow type references** — load related type files as needed to build your query.

## API Conventions

### Authentication
- Endpoint: `https://{store}.myshopify.com/admin/api/2025-01/graphql.json`
- Header: `X-Shopify-Access-Token: {access_token}`

### Global IDs
All resources use global IDs: `gid://shopify/Product/1234567890`. Always use the full GID.

### Pagination (Relay-style)
All list fields return Connection types with cursor-based pagination:

```graphql
query {
  products(first: 10, after: "cursor_string") {
    nodes {
      id
      title
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Standard pagination arguments: `first`, `after`, `last`, `before`, `reverse`, `sortKey`, `query`.
Max page size: 250. Prefer `nodes` over `edges` for simpler access.

### Mutations Pattern
All mutations return a Payload containing the resource + `userErrors`:

```graphql
mutation {
  productCreate(product: {title: "New Product"}) {
    product {
      id
    }
    userErrors {
      field
      message
    }
  }
}
```

**Always** include `userErrors { field message }` in mutation selections.

### Rate Limits
Query cost-based throttling. Max cost: 1000 points per query.
Request only fields you need. Avoid deeply nested connections.

### Scalars
`ID`, `String`, `Int`, `Float`, `Boolean`, `DateTime`, `Date`, `Money`, `Decimal`,
`URL`, `HTML`, `JSON`, `Color`, `FormattedString`, `UnsignedInt64`, `ARN`, `BigInt`,
`StorefrontID`, `UtcOffset`.

## Domain Directory

Scan this table to find the right domain, then load its reference file.

- **[apps](references/apps.md)** — App installations, webhooks, pixels, script tags, Flow, extensions (21Q, 32M)
- **[bulk_operations](references/bulk_operations.md)** — Bulk operations, file uploads, staged uploads (4Q, 11M)
- **[content](references/content.md)** — Blog posts, articles, pages, menus, themes, URL redirects, translations (30Q, 37M)
- **[customers](references/customers.md)** — Customers, companies (B2B), segments, store credit (28Q, 66M)
- **[discounts](references/discounts.md)** — Discounts, price rules, price lists, selling plans (19Q, 45M)
- **[fulfillment](references/fulfillment.md)** — Fulfillment, shipping, delivery, returns, reverse logistics (22Q, 60M)
- **[graphql_utils](references/graphql_utils.md)** — Node lookups, utility queries, saved searches (19Q, 9M)
- **[inventory](references/inventory.md)** — Inventory management, locations, stock levels (13Q, 34M)
- **[marketing](references/marketing.md)** — Marketing activities, events, campaigns (7Q, 12M)
- **[markets](references/markets.md)** — Markets, international commerce, localization (7Q, 12M)
- **[metafields](references/metafields.md)** — Metafields, metaobjects, custom data (10Q, 16M)
- **[orders](references/orders.md)** — Orders, draft orders, abandoned checkouts (17Q, 40M)
- **[payments](references/payments.md)** — Payments, gift cards, refunds, Shopify Payments, transactions (14Q, 18M)
- **[products](references/products.md)** — Products, collections, catalogs, publications, and taxonomy (33Q, 57M)
- **[shop](references/shop.md)** — Shop settings, staff, domains, tax, policies (18Q, 13M)
- **[subscriptions](references/subscriptions.md)** — Subscription contracts, billing, delivery schedules (8Q, 33M)

## File Structure

```
queries/{name}.md     — One file per query (270 total)
mutations/{name}.md   — One file per mutation (495 total)
types/
  objects/{name}.md   — Object types (1428)
  inputs/{name}.md    — Input types (525)
  enums/{name}.md     — Enum types (567)
  interfaces/{name}.md — Interfaces (44)
  unions/{name}.md    — Union types (50)
references/
  {domain}.md         — Domain-level operation indexes
  _domains.json       — Machine-readable domain index
```

Each operation file contains: description, arguments, return type fields, example query skeleton,
and links to related types. Follow the links to load type definitions as needed.

## Tips for Building Queries

1. Start from the domain reference to find the right operation.
2. Load the operation file to get the argument signature and return shape.
3. For mutations, load the input type to understand required fields.
4. For connection fields, use the pagination pattern from conventions above.
5. Only select fields you actually need — it reduces query cost.
6. Check for deprecated fields (marked in type files) and use alternatives.
