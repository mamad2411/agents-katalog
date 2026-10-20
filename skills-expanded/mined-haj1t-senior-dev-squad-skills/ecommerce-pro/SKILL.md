---
name: ecommerce-pro
description: "Cart, catalog, inventory, payments, checkout, orders, search, personalization. Use when building or reviewing e-commerce features."
---

# E-Commerce Pro

## Purpose

Build production e-commerce platforms: product catalog, shopping cart, checkout flow, inventory management, payment processing, order management, and search.

## When to Use

**Use this when:**
- Building or extending an e-commerce platform: catalog, cart, checkout, orders, or payments
- Designing product variant models, inventory systems, or discount/promo logic
- Integrating a payment provider (Stripe, Braintree) or search engine (Algolia, Meilisearch) into a storefront

**Use this ESPECIALLY when:**
- Implementing the checkout flow — stock reservation, order creation, and payment must be transactional and idempotent
- Prices, discounts, or taxes are involved — integer-cent arithmetic and per-jurisdiction tax rules must be correct from day one
- Cart state is being stored client-side — server-side carts are required for multi-device and recovery flows

**Don't skip when:**
- Adding any inventory mutation — oversell prevention requires locking at order placement, not at add-to-cart
- Building the payment integration — idempotency keys and webhook deduplication are non-negotiable

## Core Patterns

### 1. Product Catalog

```sql
-- Polymorphic product model
CREATE TABLE products (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku             TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    slug            TEXT UNIQUE NOT NULL,
    description     TEXT,
    category_id     UUID REFERENCES categories(id),
    price           BIGINT NOT NULL,          -- Cents
    compare_at_price BIGINT,                  -- Original price for discounts
    status          TEXT CHECK (status IN ('draft', 'active', 'archived')),
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE product_variants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID NOT NULL REFERENCES products(id),
    sku             TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,              -- "Small Blue"
    attributes      JSONB NOT NULL,            -- { "size": "M", "color": "blue" }
    price_adjustment BIGINT DEFAULT 0,
    stock           INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN DEFAULT true
);

CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category ON products(category_id) WHERE status = 'active';
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));
```

### 2. Cart (Server-Side)

```typescript
// Server-managed cart (not localStorage — survives devices)
interface Cart {
  id: string
  userId?: string       // Null for guest carts
  sessionId: string     // For guest users
  items: CartItem[]
  appliedPromo?: string
  createdAt: Date
  updatedAt: Date
}

interface CartItem {
  variantId: string
  quantity: number
  price: number        // Snapshot at time of add
}

// Recalculate on every read
function calculateCart(cart: Cart): CartSummary {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const discount = calculateDiscount(cart)
  const tax = calculateTax(subtotal - discount)
  const shipping = calculateShipping(cart)
  return { subtotal, discount, tax, shipping, total: subtotal - discount + tax + shipping }
}
```

### 3. Order Management

```typescript
enum OrderStatus {
  PENDING_PAYMENT, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED, REFUNDED
}

async function placeOrder(cartId: string, userId: string): Promise<Order> {
  return await db.$transaction(async (tx) => {
    const cart = await tx.cart.findUnique({ where: { id: cartId }, include: { items: true } })
    if (!cart || cart.items.length === 0) throw AppError.badRequest('Cart is empty')

    // Validate stock & reserve inventory
    for (const item of cart.items) {
      const variant = await tx.productVariant.findUnique({ where: { id: item.variantId } })
      if (!variant || variant.stock < item.quantity) {
        throw AppError.conflict(`Insufficient stock for ${variant.sku}`)
      }
      await tx.productVariant.update({
        where: { id: item.variantId },
        data: { stock: { decrement: item.quantity } },
      })
    }

    // Create order
    const order = await tx.order.create({
      data: {
        userId,
        status: OrderStatus.PENDING_PAYMENT,
        items: { create: cart.items.map(i => ({ variantId: i.variantId, quantity: i.quantity, price: i.price })) },
        total: calculateCart(cart).total,
      },
    })

    // Clear cart
    await tx.cartItem.deleteMany({ where: { cartId } })

    return order
  })
}
```

### 4. Search & Filtering

```typescript
// Algolia / Meilisearch / Typesense
const searchClient = new MeiliSearch({ host: 'http://search:7700', apiKey: 'key' })

async function searchProducts(query: string, filters: ProductFilters): Promise<SearchResult[]> {
  const results = await searchClient.index('products').search(query, {
    filter: [
      `price >= ${filters.minPrice ?? 0}`,
      `price <= ${filters.maxPrice ?? 999999}`,
      filters.category ? `category = "${filters.category}"` : '',
      filters.inStock ? 'stock > 0' : '',
    ].filter(Boolean),
    sort: [filters.sortBy === 'price_asc' ? 'price:asc' : 'price:desc'],
    hitsPerPage: filters.perPage ?? 20,
    page: filters.page ?? 1,
  })
  return results
}
```

### Checklist

- [ ] Product catalog: polymorphic model (simple + variant products)
- [ ] Prices in cents (no float rounding errors)
- [ ] Server-side cart (survives device switch)
- [ ] Stock reservation at order placement (not at add-to-cart)
- [ ] Transactional order placement (all-or-nothing)
- [ ] Payment intent with idempotency key
- [ ] Order status state machine with valid transitions
- [ ] Inventory: real-time stock, low-stock alerts, oversell prevention
- [ ] Search: full-text, faceted filters, typo tolerance
- [ ] Abandoned cart recovery flow
- [ ] Tax calculation per jurisdiction
- [ ] Shipping: rates, zones, carriers, tracking

## Related Skills

- **backend-senior-engineer** — design the service layer for cart, order, and inventory domains before wiring up e-commerce-specific logic
- **postgres-pro** — tune product catalog queries, variant joins, and full-text search indexes that power storefront listing pages
- **fintech-pro** — apply payment processing, idempotency, and ledger patterns when checkout integrates real money movement
- **code-reviewer** — validate cart, product, and order REST contracts for pagination, error shapes, and versioning before clients integrate
- **security-reviewer** — audit PCI-scope endpoints, payment token handling, and customer PII storage against OWASP guidelines
- **performance-engineer** — profile catalog search, cart recalculation, and checkout transaction throughput under peak traffic
- **test-engineer** — build integration test suites covering checkout state machines, stock reservation races, and payment webhook replay
