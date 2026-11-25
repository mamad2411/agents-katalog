---
name: ecommerce-demo-db
description: Query the e-commerce database (users, products, orders, order_items) through the MCP SQL tool. Use whenever the user asks questions about users, products, orders, revenue, or sales — e.g. "how many orders do we have?", "top customers by spend", "revenue by category".
---

# E-commerce database

The database is exposed as the MCP tool **`sql_ecommerce_demo`**. Answer questions by sending a single SQL query string (PostgreSQL dialect) to that tool. Results come back as JSON rows, truncated to the configured row limit (default 100) — use `LIMIT`, aggregation, or `ORDER BY` to keep result sets small and relevant.

## Schema

- **users** — `id`, `email`, `full_name`, `country` (ISO 3166-1 alpha-2), `created_at`
- **products** — `id`, `sku`, `name`, `category` (Electronics, Furniture, Accessories, Stationery), `price_cents`, `created_at`
- **orders** — `id`, `user_id` → users, `status` (`pending`, `paid`, `shipped`, `delivered`, `cancelled`), `placed_at`
- **order_items** — `id`, `order_id` → orders, `product_id` → products, `quantity`, `unit_price_cents`

## Relations

- One user has many orders (`orders.user_id` → `users.id`).
- One order has many order items (`order_items.order_id` → `orders.id`); each item references one product (`order_items.product_id` → `products.id`).
- A product appears at most once per order (`order_id, product_id` is unique).

## Conventions

- All money values are integer cents; divide by 100.0 for display. Amounts have no currency column — treat them as USD.
- Order totals are not stored — compute them by joining `order_items` (`quantity * unit_price_cents`).
- `unit_price_cents` is the price at purchase time and may differ from the current `products.price_cents`.
- Cancelled orders should normally be excluded from revenue and sales figures.

## Guidelines

- Treat the database as read-only: stick to `SELECT` unless the user explicitly asks to modify data.
- Prefer one well-formed query over many small ones; use joins and aggregates server-side.
