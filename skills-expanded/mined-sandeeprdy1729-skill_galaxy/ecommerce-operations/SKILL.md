---
name: ecommerce-operations
description: "Build and manage e-commerce operations integrations including Shopify Admin API, Amazon Seller Central, inventory management, order fulfillment, and multi-channel commerce automation."
license: Apache 2.0
tags: ["ecommerce", "shopify", "amazon", "inventory", "fulfillment", "retail", "mcp"]
difficulty: intermediate
time_to_master: "8-14 weeks"
version: "1.0.0"
---

# E-Commerce Operations

## Overview

Modern e-commerce runs on API-connected platforms — Shopify, Amazon Seller Central, WooCommerce, BigCommerce — each handling products, orders, inventory, and fulfillment. AI agents that can manage these platforms enable automated inventory rebalancing, pricing optimization, order tracking, and multi-channel sync. This skill covers the APIs, data models, and automation patterns for e-commerce operations.

## When to Use This Skill

- Building MCP servers for Shopify store management
- Automating inventory sync across multiple sales channels
- Creating AI-powered order management and fulfillment workflows
- Implementing dynamic pricing strategies
- Building multi-channel product catalog management

## Core Concepts

### E-Commerce Platform Landscape

| Platform | Market Share | API Style | Best For |
|----------|-------------|-----------|----------|
| Shopify | 28% | GraphQL + REST | SMB to mid-market |
| Amazon Seller Central | 38% marketplace | REST (SP-API) | Marketplace sellers |
| WooCommerce | 23% | REST | WordPress sites |
| BigCommerce | 3% | REST + GraphQL | Mid-market |

### Core Data Model

```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│ Products │────►│ Variants │────►│  Inventory   │
│          │     │ (SKUs)   │     │  Levels      │
└──────────┘     └──────────┘     └──────────────┘
                      │
                      ▼
┌──────────┐     ┌──────────┐     ┌──────────────┐
│ Customer │────►│  Orders  │────►│ Fulfillments │
│          │     │          │     │              │
└──────────┘     └──────────┘     └──────────────┘
                      │
                      ▼
                 ┌──────────┐
                 │ Payments │
                 │ Refunds  │
                 └──────────┘
```

## Implementation Guide

### Shopify Admin API (GraphQL)

```typescript
import Shopify from "@shopify/shopify-api";

// Search products
const response = await client.query({
  data: `{
    products(first: 10, query: "status:active AND product_type:clothing") {
      edges {
        node {
          id
          title
          status
          totalInventory
          variants(first: 5) {
            edges {
              node {
                sku
                price
                inventoryQuantity
              }
            }
          }
        }
      }
    }
  }`,
});

// Update inventory levels
const inventoryAdjust = await client.query({
  data: {
    query: `mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
      inventoryAdjustQuantities(input: $input) {
        inventoryAdjustmentGroup { reason }
        userErrors { field message }
      }
    }`,
    variables: {
      input: {
        reason: "correction",
        name: "available",
        changes: [{
          delta: -5,
          inventoryItemId: "gid://shopify/InventoryItem/123",
          locationId: "gid://shopify/Location/456",
        }],
      },
    },
  },
});
```

### Order Management MCP Tools

```typescript
server.tool(
  "get_recent_orders",
  "Fetch recent orders with status, items, and totals",
  {
    status: z.enum(["open", "closed", "cancelled", "any"]).default("open"),
    days: z.number().default(7),
    limit: z.number().default(20),
  },
  async ({ status, days, limit }) => {
    const since = new Date(Date.now() - days * 86400000).toISOString();
    const orders = await shopify.order.list({
      status,
      created_at_min: since,
      limit,
    });

    const summary = orders.map(o => ({
      id: o.order_number,
      customer: o.customer?.first_name + " " + o.customer?.last_name,
      total: o.total_price,
      items: o.line_items.length,
      status: o.fulfillment_status || "unfulfilled",
      created: o.created_at,
    }));

    return {
      content: [{ type: "text", text: JSON.stringify(summary, null, 2) }],
    };
  }
);

server.tool(
  "check_inventory_levels",
  "Check inventory levels for products, flagging low stock",
  {
    threshold: z.number().default(10).describe("Low stock threshold"),
  },
  async ({ threshold }) => {
    const products = await shopify.product.list({ limit: 250 });
    const lowStock = [];

    for (const product of products) {
      for (const variant of product.variants) {
        if (variant.inventory_quantity <= threshold) {
          lowStock.push({
            product: product.title,
            variant: variant.title,
            sku: variant.sku,
            quantity: variant.inventory_quantity,
            status: variant.inventory_quantity === 0 ? "OUT OF STOCK" : "LOW",
          });
        }
      }
    }

    return {
      content: [{
        type: "text",
        text: `${lowStock.length} items at or below threshold (${threshold}):\n\n` +
          lowStock.map(i => `[${i.status}] ${i.product} - ${i.variant} (SKU: ${i.sku}): ${i.quantity} left`).join("\n"),
      }],
    };
  }
);
```

### Multi-Channel Inventory Sync

```python
class InventorySyncManager:
    """Keep inventory levels synchronized across sales channels."""

    def sync_all_channels(self, sku):
        # Get true inventory from warehouse management system
        warehouse_qty = self.wms.get_quantity(sku)

        # Calculate available per channel (reserve safety stock)
        safety_stock = max(5, int(warehouse_qty * 0.1))
        available = warehouse_qty - safety_stock

        # Allocate across channels based on velocity
        allocations = self.calculate_allocations(sku, available)

        # Update each channel
        for channel, qty in allocations.items():
            self.channels[channel].update_inventory(sku, qty)

        return {"sku": sku, "total": warehouse_qty, "allocations": allocations}

    def calculate_allocations(self, sku, available):
        """Allocate inventory proportionally to sales velocity."""
        velocities = {ch: self.get_velocity(sku, ch) for ch in self.channels}
        total_velocity = sum(velocities.values()) or 1

        return {
            channel: int(available * (vel / total_velocity))
            for channel, vel in velocities.items()
        }
```

## Best Practices

1. **Webhook-driven sync** — subscribe to order/inventory webhooks instead of polling
2. **Idempotent operations** — use order IDs and SKUs as idempotency keys
3. **Safety stock buffers** — never allocate 100% of inventory to any single channel
4. **Rate limit awareness** — Shopify allows 2 requests/sec; Amazon SP-API varies by endpoint
5. **Bulk operations for catalogs** — use bulk mutations for product updates over 50 items
6. **Test with sandbox stores** — both Shopify and Amazon offer development/sandbox environments

## Resources

- [Shopify Admin API Reference](https://shopify.dev/docs/api/admin-graphql)
- [Amazon SP-API Documentation](https://developer-docs.amazon.com/sp-api/)
- [Shopify App Development](https://shopify.dev/docs/apps)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
