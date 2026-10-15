---
name: clawpify
description: Query and manage Shopify stores via GraphQL Admin API. Use when working with products, orders, customers, inventory, discounts, marketing, translations, fulfillments, or any Shopify store data.
dependencies:
  - node>=18
---

# Shopify Admin GraphQL

A comprehensive skill for interacting with Shopify's GraphQL Admin API. This skill enables Claude to query and manage all aspects of Shopify store data including products, orders, customers, inventory, marketing, discounts, translations, fulfillments, and more.

## Prerequisites

- A Shopify store with Admin API access
- An Admin API access token with appropriate scopes
- Environment variables configured:
  - `SHOPIFY_STORE_URL` - Your store URL (e.g., `my-store.myshopify.com`)
  - `SHOPIFY_ACCESS_TOKEN` - Admin API access token

## Quick Start

### Basic Product Query

```graphql
query {
  products(first: 10) {
    nodes {
      id
      title
      status
    }
  }
}
```

### Create a Product

```graphql
mutation CreateProduct($product: ProductCreateInput!) {
  productCreate(product: $product) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:
```json
{
  "product": {
    "title": "New Product",
    "status": "DRAFT"
  }
}
```

## Instructions

When working with Shopify GraphQL:

1. **Always use the `shopify_graphql` tool** to execute queries and mutations
2. **Check for errors** in responses:
   - `errors` array indicates GraphQL/syntax issues
   - `userErrors` in mutations indicate validation/business logic issues
3. **Use pagination** for large result sets with `first`/`after` cursors
4. **Format IDs correctly** - All Shopify IDs are global: `gid://shopify/Resource/123`

## Critical Operations & Permissions

IMPORTANT: Before executing any of the following operations, you MUST ask for explicit user permission. These operations are irreversible or have significant business impact.

### Immediately Dangerous Operations

- Refunds: Create refunds (permanent financial transactions, cannot be undone)
- Order Cancellations: Cancel orders (may trigger automatic refunds)
- Gift Card Deactivation: Permanently disable gift cards (irreversible)
- Gift Card Balance Changes: Credit or debit gift card balances (affects customer funds)
- Inventory Adjustments: Modify stock levels (affects product availability)

### State-Changing Operations

- Activate/Deactivate Discounts: Change discount status (immediately affects customer pricing)
- Product Status Changes: Publish products (makes them visible to customers)
- Complete Draft Orders: Convert draft orders to real orders (commits the transaction)
- Fulfillment Creation: Create fulfillments (triggers shipping notifications to customers)
- Fulfillment Cancellation: Cancel fulfillments (may confuse customers)
- Hold/Release Fulfillment Orders: Pause or resume order processing

### Deletion Operations

- Delete Products/Variants: Permanent removal (cannot be recovered)
- Delete Discounts: Permanent removal (customers can no longer use codes)
- Delete Draft Orders: Permanent removal
- Delete Webhooks: Stops event notifications (may break integrations)
- Bulk Delete Operations: Delete multiple items at once (high-impact)

### Permission Protocol

When Claude encounters any critical operation:

1. Describe the operation and its specific impact
2. Show what will be changed/deleted (IDs, names, values)
3. Wait for explicit user confirmation before proceeding
4. Only proceed after receiving "yes", "confirm", "proceed", or equivalent affirmative response
5. Never assume permission even if the user's request seems clear

Example:
```
WARNING: This will permanently deactivate gift card gid://shopify/GiftCard/123 
with a balance of $50.00. This action cannot be undone.

Do you want to proceed? (yes/no)
```

## Capabilities

This skill provides comprehensive patterns for all major Shopify domains:

### Core Commerce

| Domain | Operations | File |
|--------|------------|------|
| **Products** | List, get, search, create, update, delete products and variants | [products.md](products.md) |
| **Orders** | List, get details, fulfill, cancel orders | [orders.md](orders.md) |
| **Customers** | List, get, create, update customers | [customers.md](customers.md) |
| **Inventory** | Check levels, adjust quantities, manage locations | [inventory.md](inventory.md) |
| **Collections** | List collections, manage products in collections | [collections.md](collections.md) |

### Marketing & Promotions

| Domain | Operations | File |
|--------|------------|------|
| **Discounts** | Code/automatic discounts, BXGY, free shipping | [discounts.md](discounts.md) |
| **Marketing** | Marketing activities, events, consent | [marketing.md](marketing.md) |
| **Segments** | Customer segments for targeting | [segments.md](segments.md) |

### International

| Domain | Operations | File |
|--------|------------|------|
| **Translations** | Translate products, pages, content | [translations.md](translations.md) |
| **Markets** | Multi-market setup, localized content | [markets.md](markets.md) |

### Content & Storefront

| Domain | Operations | File |
|--------|------------|------|
| **Pages** | Create/update store pages | [pages.md](pages.md) |
| **Blogs** | Blogs and articles | [blogs.md](blogs.md) |
| **Menus** | Navigation menus | [menus.md](menus.md) |
| **Files** | File uploads, media library | [files.md](files.md) |
| **Metafields** | Custom data, metaobjects | [metafields.md](metafields.md) |

### Fulfillment & Shipping

| Domain | Operations | File |
|--------|------------|------|
| **Fulfillments** | Create fulfillments, tracking | [fulfillments.md](fulfillments.md) |
| **Shipping** | Delivery profiles, zones, rates | [shipping.md](shipping.md) |
| **Locations** | Manage inventory locations | [locations.md](locations.md) |

### Financial

| Domain | Operations | File |
|--------|------------|------|
| **Draft Orders** | Create orders on behalf of customers | [draft-orders.md](draft-orders.md) |
| **Refunds** | Process refunds, restocking | [refunds.md](refunds.md) |
| **Gift Cards** | Create, credit, debit gift cards | [gift-cards.md](gift-cards.md) |
| **Subscriptions** | Subscription contracts, billing | [subscriptions.md](subscriptions.md) |

### Store Management

| Domain | Operations | File |
|--------|------------|------|
| **Shop** | Store info, settings, ShopifyQL | [shop.md](shop.md) |
| **Webhooks** | Event subscriptions | [webhooks.md](webhooks.md) |
| **Bulk Operations** | Large async queries/mutations | [bulk-operations.md](bulk-operations.md) |

## Common Patterns

### ID Format
All Shopify GraphQL IDs are globally unique:
```
gid://shopify/Product/123
gid://shopify/Order/456
gid://shopify/Customer/789
```

### Pagination
Use cursor-based pagination for large datasets:
```graphql
query($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      title
    }
  }
}
```

### Money Fields
Prices return as `MoneyV2` objects:
```graphql
totalPriceSet {
  shopMoney {
    amount
    currencyCode
  }
}
```

### Mutations Always Return userErrors
Always request and check `userErrors`:
```graphql
mutation {
  productCreate(product: $product) {
    product { id }
    userErrors {
      field
      message
    }
  }
}
```

### Search Syntax
Filter queries use Shopify's search syntax:
```graphql
products(first: 10, query: "title:*shirt* AND status:ACTIVE")
```

## API Scopes Required

### Core Scopes
- `read_products`, `write_products` - Products and variants
- `read_orders`, `write_orders` - Orders and fulfillments
- `read_customers`, `write_customers` - Customer data
- `read_inventory`, `write_inventory` - Inventory levels

### Marketing & Discounts
- `read_discounts`, `write_discounts` - Discount codes
- `read_marketing_events`, `write_marketing_events` - Marketing activities

### Content
- `read_content`, `write_content` - Pages, blogs, articles
- `read_online_store_navigation`, `write_online_store_navigation` - Menus
- `read_files`, `write_files` - File uploads
- `read_metafields`, `write_metafields` - Metafields
- `read_metaobjects`, `write_metaobjects` - Metaobjects

### International
- `read_translations`, `write_translations` - Translations
- `read_markets`, `write_markets` - Markets
- `read_locales`, `write_locales` - Locales

### Fulfillment
- `read_shipping`, `write_shipping` - Shipping settings
- `read_locations` - Location data
- `read_assigned_fulfillment_orders`, `write_assigned_fulfillment_orders` - For fulfillment services

### Financial
- `read_draft_orders`, `write_draft_orders` - Draft orders
- `read_gift_cards`, `write_gift_cards` - Gift cards
- `read_own_subscription_contracts`, `write_own_subscription_contracts` - Subscriptions

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Access denied` | Check API token has required scopes |
| `Invalid ID` | Ensure ID format is `gid://shopify/Resource/123` |
| `userErrors` returned | Check field-specific validation messages |
| `Throttled` | Reduce request rate, use bulk operations for large updates |
| `Resource not found` | Verify the ID exists and you have read access |

## Examples

### List Recent Orders with Customer Info

```graphql
query RecentOrders {
  orders(first: 10, sortKey: CREATED_AT, reverse: true) {
    nodes {
      id
      name
      createdAt
      displayFinancialStatus
      totalPriceSet {
        shopMoney {
          amount
          currencyCode
        }
      }
      customer {
        displayName
        defaultEmailAddress {
          emailAddress
        }
      }
    }
  }
}
```

### Search Products by Title

```graphql
query SearchProducts($query: String!) {
  products(first: 20, query: $query) {
    nodes {
      id
      title
      status
      vendor
    }
  }
}
```
Variables: `{ "query": "title:*shirt* AND status:ACTIVE" }`

### Update Inventory

```graphql
mutation AdjustInventory($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) {
    inventoryAdjustmentGroup {
      reason
      changes {
        name
        delta
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

### Create Discount Code

```graphql
mutation CreateDiscount($basicCodeDiscount: DiscountCodeBasicInput!) {
  discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
    codeDiscountNode {
      id
    }
    userErrors {
      field
      message
    }
  }
}
```

## Best Practices

1. **Use bulk operations** for large data exports/imports
2. **Implement pagination** for lists that may grow
3. **Check userErrors** in all mutation responses
4. **Request only needed fields** to optimize response size
5. **Use webhooks** instead of polling for real-time updates
6. **Cache when appropriate** to reduce API calls
7. **Handle rate limits** with exponential backoff
