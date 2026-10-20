---
name: ecommerce-architecture
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: ecommerce architecture, shopping cart design, checkout flow optimization, inventory management system, pricing engine, order lifecycle management, marketplace architecture, product catalog design, ecommerce platform, fulfillment system, order routing, dynamic pricing
compose: caching-strategies
---

# Skill — Ecommerce Architecture

## When this skill activates
This skill activates when designing shopping cart flows, checkout experiences, inventory management systems, pricing engines, order lifecycle workflows, product catalog architectures, marketplace platforms, or fulfillment/logistics systems for ecommerce.

## Mandatory actions when this skill is active

### Before writing any code
1. Design cart and checkout state machine: anonymous cart → logged-in cart (merge/replace strategy), cart → checkout (address validation), checkout → payment → order confirmation, with explicit timeout handling for abandoned carts (30 min session, 7 day recovery email)
2. Model inventory architecture: real-time available-to-promise (ATP) calculation across warehouses, reserved inventory during checkout (soft hold 15 min, hard hold at payment), backorder handling, and oversell prevention with pessimistic locking
3. Map order lifecycle stages: order placed → payment authorized → fraud screening → fulfillment assigned → picked → packed → shipped → delivered → returns window, with event-driven state transitions and webhook notifications at each stage

### During implementation
- Implement cart persistence with multi-device sync: store cart in database (not just sessions), deduplicate items by SKU+options hash, handle quantity updates with stock validation, expire abandoned carts after 30 days, support guest cart migration to user account on login
- Build pricing engine with rule evaluation: base price → promotional discounts (BOGO, percentage off, fixed amount) → coupon codes (stackable/non-stackable) → volume discounts → tax calculation (Avalara/TaxJar API), with price display consistency (cart/checkout/confirmation must match)
- Design inventory reservation system: when checkout starts, create soft reservation (pessimistic lock), release on timeout or explicit cancel, convert to hard reservation on payment success, allocate to specific warehouse based on proximity to shipping address and stock availability
- Implement order routing logic: evaluate fulfillment options (ship from warehouse, dropship from vendor, ship from store), calculate shipping cost and delivery ETA per option, optimize for cost vs speed vs carbon footprint, handle split shipments when inventory spans locations
- Build product catalog with faceted search: index products in Elasticsearch/Algolia with attributes (category, brand, color, size, price), support filters (multi-select facets), range queries (price slider), text search with typo tolerance, and sort options (relevance, price, rating, recency)

### After implementation
- Validate checkout flow conversion: measure cart abandonment rate by stage (cart → checkout → payment → confirmation), identify friction points (shipping cost surprise, account creation forced, payment failure), implement address autocomplete (Google Places API), express checkout options (Apple Pay, Shop Pay)
- Test inventory consistency under load: simulate concurrent purchases of last item in stock (race condition), verify oversell prevention, validate soft reservation expiry releases inventory back to available pool, confirm hard reservation deducts from ATP correctly
- Execute fraud screening integration: verify address verification system (AVS) checks, CVV validation, velocity checks (too many orders from same IP/card), device fingerprinting (Sift/Forter), manual review queue for high-risk orders

## Self-check before task completion
- [ ] Cart supports guest and logged-in users, syncs across devices, handles item updates with real-time stock validation
- [ ] Pricing engine evaluates all discount layers (promotions → coupons → volume → tax) with consistent display across cart/checkout/confirmation
- [ ] Inventory reservation implemented: soft hold during checkout (15 min timeout), hard hold post-payment, pessimistic locking prevents oversell
- [ ] Checkout flow optimized: address autocomplete, saved payment methods, express checkout options (Apple Pay), progress indicator
- [ ] Order lifecycle event-driven: state machine with webhook notifications (order placed, shipped, delivered), customer email templates
- [ ] Product catalog searchable: faceted filters, text search with typo tolerance, sort options, pagination or infinite scroll
- [ ] Fraud screening integrated: AVS/CVV checks, velocity limits, device fingerprinting, manual review queue for high-risk transactions
