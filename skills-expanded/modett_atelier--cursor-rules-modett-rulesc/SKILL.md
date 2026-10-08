---
description: Modett e-commerce platform — complete rules covering architecture, safety-critical patterns, code style, and domain conventions
alwaysApply: true
---

# =============================================================================
# MODETT E-COMMERCE PLATFORM — CURSOR AI RULES
# =============================================================================
# These rules are ABSOLUTE. They encode deliberate architectural and safety
# decisions. Do not deviate without explicit instruction from the developer.
# When in doubt: read the rule, follow the rule, ask if unclear.
# =============================================================================


# =============================================================================
# 0) OPERATING MODE
# =============================================================================

Act as a senior engineer who ships production-grade code.
- Prefer small, composable modules. No duplication.
- Use Receive an Object, Return an Object (RORO) for functions and service methods.
- No classes — functional style throughout.
- Optimize for: correctness first, then maintainability, Web Vitals, accessibility.
- Provide minimal, correct diffs. Prefer small commits.
- Extract shared helpers into packages/utils or packages/ui before duplicating.


# =============================================================================
# 1) PROJECT OVERVIEW
# =============================================================================

Modett is a premium fashion e-commerce platform.
Multi-currency: LKR (Sri Lanka), SGD (Singapore), USD (Rest of World).

Stack:
  Frontend  : Next.js 15 App Router on Vercel (serverless / edge)
  API       : Node.js + TypeScript on Railway (long-running process)
  Worker    : Same API codebase, separate Railway service, different entry point
  Database  : PostgreSQL 17 on Railway (same private network as API)
  Cache     : Redis 7 on Railway (same private network as API)
  Storage   : Cloudflare R2 — product images, review media
  Payments  : PAYable IPG (SHA-512 checkValue verification, not HMAC)
  Email     : Resend (transactional + outbox pattern)
  Errors    : Sentry on both web and api

Monorepo (pnpm workspaces):
  apps/
    api/        Railway API service — modular monolith
    web/        Vercel Next.js storefront + admin portal
  packages/
    db/         Drizzle schema, pg pool, Redis client, all query functions
    ui/         Design system primitives (tokens, layout, navigation, typography, ui)
    utils/      Shared pure utilities — orderRef, money, slugify

Directory naming: lowercase-with-dashes (e.g. components/cart-drawer)


# =============================================================================
# 2) ARCHITECTURE — READ BEFORE WRITING ANYTHING
# =============================================================================

## 2.1 — Backend architecture: Modular Monolith (today → Microservices later)

apps/api follows modular monolith architecture.
Each module in apps/api/src/modules/ is a sealed bounded context.
Modules communicate only through their public interface (index.ts exports).
Never import directly from another module's internal files.
This boundary is intentional — each module is a future microservice boundary.

## 2.2 — Frontend architecture: One whole application

apps/web does NOT follow modular monolith architecture.
The frontend is a single unified Next.js application.
Do not organise it by domain boundaries.
Do not create module folders that mirror the backend structure.
Feature components are organised by feature area — not as sealed modules.

## 2.3 — The single most important rule

apps/web NEVER connects to the database or Redis — ever.

  - Do NOT add DATABASE_URL to Vercel environment variables or apps/web code.
  - Do NOT add REDIS_URL to Vercel environment variables or apps/web code.
  - Do NOT import anything from packages/db inside apps/web.
  - Do NOT import pg, postgres, drizzle-orm, or ioredis inside apps/web.
  - apps/web gets ALL data by calling the Railway API via fetch().
  - apps/web/src/app/middleware.ts reads/writes cookies only. No DB.

If you are about to write a database import in apps/web — stop.
Route it through the API instead.

## 2.4 — Package responsibility boundaries

  packages/db     → used by apps/api only. Never by apps/web.
  packages/ui     → used by apps/web only. Design system primitives.
  packages/utils  → used by both apps/api and apps/web. Pure functions only.
                    No domain logic. No DB access. No API calls.


# =============================================================================
# 3) TECH STACK (APPROVED — DO NOT SUBSTITUTE)
# =============================================================================

### Frontend (apps/web)

  Next.js 15, App Router, TypeScript strict
  Tailwind CSS v3
  TanStack Query v5        — all server state (products, cart, orders)
  Zustand v5               — client UI state only (drawers, selections)
  React Hook Form v7 + Zod v3 + @hookform/resolvers — all forms
  Framer Motion v11        — animations and transitions
  Lucide React             — icons throughout
  next/font/google         — Playfair Display + Raleway
  @vercel/analytics        — page analytics
  @vercel/speed-insights   — Core Web Vitals per route
  Native fetch via lib/api.ts — no Axios

  Design system: packages/ui (custom — NOT shadcn/ui)
  Component variants: cn() utility (clsx + tailwind-merge)

### Backend (apps/api + worker)

  Node.js + TypeScript — functional style, no classes
  Drizzle ORM (node-postgres driver)
  Zod for all input validation
  Sentry for error tracking
  Redis on Railway (inventory locks, sessions, rate limiting, outbox)

### Payments

  PAYable IPG — NOT Stripe.
  Verification: SHA-512 checkValue (not HMAC-SHA256).
  statusCode 1 = SUCCESS, statusCode 2 = FAILURE.
  Always respond { "Status": 200 } to PAYable callbacks
  EXCEPT when checkValue is invalid (respond 400).

### Communications

  Resend — transactional emails via outbox pattern
  Messaging uses 13 template keys across EMAIL / SMS / WHATSAPP / PUSH channels.

Do NOT introduce Prisma, Mongoose, Sequelize, or any other ORM.
Do NOT introduce Stripe, Braintree, or any other payment provider.
Do NOT introduce a separate auth library (Clerk, Auth.js, NextAuth).
Do NOT introduce shadcn/ui, Radix UI, or Headless UI in apps/web.
Do NOT use localStorage or sessionStorage for anything security-related.
Do NOT use Axios — native fetch only.
Do NOT use next-safe-action — server actions use standard Next.js patterns.


# =============================================================================
# 4) FOLDER STRUCTURE
# =============================================================================

### apps/api/src/

  modules/
    iam/           auth, sessions, admin invites, RBAC
    catalog/       products, categories, prices, images
    inventory/     variants, stock, barcodes, movements, reconciliation
    cart/          cart CRUD, stock hints
    checkout/      two-window reservation creation
    payments/      PAYable IPG, webhook handling, idempotency
    orders/        state machine, timeline, fulfilment scanning
    shipping/      zones, methods, rates per currency
    returns/       eligibility, item-level selection, status sync
    reviews/       tokens, verified purchase, moderation
    loyalty/       earn/redeem, tiers, ledger, expiry
    messaging/     outbox, templates, campaigns, back-in-stock
  lib/             shared API utilities (AppError, withLock, etc.)
  middleware/      requireAuth, requireAdmin, requireOwner
  config/          env validation, constants

  Each module contains exactly: queries.ts, service.ts, routes.ts
  Some modules add: types.ts, workers.ts

### apps/web/src/

  app/
    (storefront)/  browsing, product discovery
    (account)/     profile, orders, loyalty, wishlist, inbox
    (auth)/        login, signup, forgot password
    (checkout)/    checkout flow, payment, confirmation
    admin/         admin portal
    layout.tsx     root layout — fonts, Vercel analytics, providers
    page.tsx       homepage
    globals.css    Tailwind directives + token imports
    middleware.ts  Edge middleware — currency cookie from geo-IP only

  components/
    storefront/    ProductCard, ProductGrid, FilterPanel, SearchBar
    account/       OrderHistory, LoyaltyCard, WishlistGrid, InboxList
    checkout/      CheckoutForm, ReservationTimer, PaymentForm
    admin/         AdminTable, AdminForm, AdminStats, CampaignBuilder
    providers/     QueryProvider, ToastProvider (client wrapper components)

  lib/
    api.ts         typed fetch wrapper — all API calls go through here
    utils.ts       cn() helper (clsx + tailwind-merge)
    query-client.ts TanStack QueryClient singleton

  hooks/           custom React hooks (useCart, useWishlist, etc.)
  store/           Zustand stores (ui.store.ts, cart.store.ts)
  types/           global TypeScript types (index.ts)

  styles/
    tokens.css     CSS custom properties
    tokens/        TypeScript token objects (colors, typography, spacing)

### packages/ui/src/

  components/
    layout/        Container, Section, Grid, Stack
    navigation/    SiteHeader, MobileMenu
    typography/    Heading, Text
    ui/            Button, OutlineButton
  lib/
    utils.ts       cn() helper
  index.ts         barrel export

### packages/utils/src/

  money.ts         Decimal.js monetary arithmetic, formatting
  orderRef.ts      MOD-YYYYNNNNN generation
  slugify.ts       URL slug generation
  index.ts         barrel export


# =============================================================================
# 5) MONEY AND CURRENCY RULES
# =============================================================================

## 5.1 — Money is NEVER a plain JavaScript number.

  // packages/utils/src/money.ts
  export type CurrencyCode = 'LKR' | 'SGD' | 'USD'
  export interface Money { amount: string; currency: CurrencyCode }

- amount is a STRING (e.g. "1250.00"). JS numbers lose float precision.
- Every function accepting or returning money uses the Money interface.
- PriceDisplay component accepts Money type only — never a raw number.
- API responses always return { amount: string, currency: CurrencyCode }.

## 5.2 — Monetary arithmetic uses Decimal.js.

  import Decimal from 'decimal.js'
  const total = new Decimal(subtotal).plus(shippingCost).plus(taxAmount)
  // Serialise as string: total.toFixed(2)

Never use + - * / operators on monetary strings directly.

## 5.3 — Every monetary amount is always stored with its currency.

In the DB: order_items has unit_price_snapshot_amount AND
unit_price_snapshot_currency as SEPARATE columns. Never put an amount
in a JSONB field without the currency alongside it.

## 5.4 — Currency detection is server-authoritative at checkout.

Edge middleware sets a currency cookie (LKR/SGD/USD) from geo-IP.
That cookie is for DISPLAY only. At POST /checkout/start and
POST /payments/intent, the API re-derives currency from country_code.
Never trust the cookie for financial operations.

## 5.5 — Tax rates by market (stored as snapshot on every order).

  LKR (Sri Lanka)     : VAT 18% — tax-inclusive display.   tax_rate_snapshot = 0.1800
  SGD (Singapore)     : GST  9% — legally required on receipt. tax_rate_snapshot = 0.0900
  USD (Rest of World) : No tax collected.                   tax_rate_snapshot = 0.0000

Generate a GST-compliant invoice PDF for every SGD order.


# =============================================================================
# 6) INVENTORY RULES (CRITICAL — READ EVERY LINE)
# =============================================================================

## 6.1 — NEVER use read-then-write for inventory.

FORBIDDEN pattern:
  const stock = await getVariantStock(variantId)   // read
  if (stock.available >= qty) {                     // check
    await holdVariantStock(variantId, qty)          // write — RACE CONDITION
  }

Two concurrent requests for the last unit both pass the check before either
write lands. This causes silent overselling.

## 6.2 — The ONLY correct inventory hold pattern.

  Step 1: Acquire Redis lock BEFORE touching the database.
  Step 2: Atomic SQL UPDATE with WHERE available_qty >= qty.
  Step 3: Check rows affected. 0 rows = insufficient stock → throw AppError.
  Step 4: Release Redis lock in finally block (always — even on error).

  const success = await withInventoryLock(variantId, async () => {
    const result = await db.execute(sql`
      UPDATE inventory.variant_stock
      SET held_qty   = held_qty + ${qty},
          updated_at = now()
      WHERE variant_id    = ${variantId}
        AND available_qty >= ${qty}
      RETURNING variant_id
    `)
    return result.rows.length > 0
  })
  if (!success) throw new AppError('INSUFFICIENT_STOCK', 409)

Use db.execute(sql`...`) — NOT the Drizzle query builder.
The exact SQL matters. Do not abstract it.

## 6.3 — available_qty is a GENERATED column. Never write to it.

  available_qty = in_stock_qty - held_qty  (GENERATED ALWAYS AS STORED)

Never include available_qty in INSERT or UPDATE statements.

## 6.4 — Inventory unit status transitions (valid only).

  IN_STOCK  → HELD          checkout hold
  HELD      → IN_STOCK      reservation expired
  HELD      → SOLD          order confirmed
  SOLD      → RETURNED      return processed
  IN_STOCK  → DAMAGED       admin damage report
  IN_STOCK  → ADJUSTED_OUT  admin stock adjustment

When an order is confirmed (one db.transaction()):
  1. Set inventory_units.status = 'SOLD'
  2. Decrement variant_stock.in_stock_qty by qty
  3. Decrement variant_stock.held_qty by qty
  4. INSERT inventory_movements (reason='SALE', reference_type='order')

## 6.5 — Barcode format.

  {SKU_GROUP}-{COLOR}-{SIZE}-{SEQUENCE}
  Example: CSLK-BLK-XS-0001

## 6.6 — Reconciliation job never auto-corrects drift.

Log discrepancies to inventory_reconciliation_log. Alert admin dashboard.
A human corrects manually via the admin portal. Never silently adjust stock.

## 6.7 — Soft-delete only. Never hard-delete.

  catalog.products, inventory.product_variants, iam.admins — all have deleted_at.
  All queries: WHERE deleted_at IS NULL.
  Hard DELETE breaks historical order_items that reference the entity.


# =============================================================================
# 7) TWO-WINDOW RESERVATION RULES (CRITICAL)
# =============================================================================

## 7.1 — Reservation lifecycle (exact column values at each step).

  POST /checkout/start    → INSERT reservation:
                              status               = 'HELD'
                              expires_at           = now() + INTERVAL '30 minutes'
                              payment_submitted_at = NULL
                              grace_expires_at     = NULL

  POST /payments/intent   → UPDATE reservation:
                              payment_submitted_at = now()
                              grace_expires_at     = now() + INTERVAL '10 minutes'
                            (both columns in the SAME UPDATE statement)

  PAYable webhook arrives → UPDATE reservation SET status = 'CONSUMED'

## 7.2 — The expiry worker query. Copy this exactly. Do not simplify.

  UPDATE cart.reservations
  SET    worker_lock_id = $uuid
  WHERE  status         = 'HELD'
    AND  expires_at     < now()
    AND  (payment_submitted_at IS NULL OR grace_expires_at < now())
    AND  worker_lock_id IS NULL
  RETURNING *

The condition (payment_submitted_at IS NULL OR grace_expires_at < now())
protects in-flight payments. Removing it releases holds while the customer's
payment is being processed. This is a silent oversell scenario.

## 7.3 — Crash-safe expiry worker.

After claiming (worker_lock_id set), the worker must set:
  processed_at     = now()  atomically with status = 'EXPIRED'
  hold_released_at = now()  after held_qty has been decremented

On worker restart: rows with worker_lock_id IS NOT NULL and
processed_at IS NULL were claimed but not finished. Re-process them.

## 7.4 — payment_submitted_at and grace_expires_at always set together.

DB enforces: CONSTRAINT chk_grace_set_together.
Always set both in the same UPDATE. Never set one without the other.

## 7.5 — Order reference format.

  MOD-YYYYNNNNN
  Example: MOD-202500042
  Generated by packages/utils/src/orderRef.ts


# =============================================================================
# 8) PAYMENT RULES — PAYable IPG (CRITICAL)
# =============================================================================

## 8.1 — checkValue verification is ALWAYS the very first thing.

PAYable uses SHA-512, not HMAC-SHA256.

  const expectedCheckValue = generateCheckValue({
    merchantId, orderId, amount, currency, statusCode, secret
  })
  if (req.body.checkValue !== expectedCheckValue) {
    return res.status(400).json({ Status: 200 }) // PAYable requirement
  }
  // Only continue after this passes.

Never skip this check for any reason.
The checkValue must be verified before reading any other field in the payload.

## 8.2 — PAYable webhook response format.

  Always respond: { "Status": 200 }
  Even on errors — except checkValue mismatch (respond HTTP 400).
  PAYable retries on non-200 HTTP responses.

## 8.3 — Two-layer idempotency for payment webhooks (both required).

  Layer 1 — Redis (fastest):
    const cached = await redis.get(`payment:event:${txId}`)
    if (cached) return res.json({ Status: 200 })

  Layer 2 — DB unique constraint:
    INSERT INTO payments.payment_transactions (provider_charge_id, ...)
    ON CONFLICT (provider_charge_id) DO NOTHING
    RETURNING id
    // 0 rows returned = duplicate → return { Status: 200 } immediately

  Layer 3 — Cache after successful processing:
    await redis.set(`payment:event:${txId}`, '1', { EX: 86400 })  // 24h TTL

All three layers are mandatory. Missing any layer risks duplicate orders.

## 8.4 — statusCode interpretation.

  statusCode 1 = PAYMENT SUCCESS  → create order, confirm reservation
  statusCode 2 = PAYMENT FAILURE  → release hold, update status to FAILED
  Any other value = ignore, log, return { Status: 200 }

## 8.5 — Order creation is one db.transaction().

  await db.transaction(async (tx) => {
    // a. Consume reservation (verify status still 'HELD' — 0 rows = return 200)
    // b. INSERT orders.orders
    // c. INSERT orders.order_items (with all snapshot columns)
    // d. UPDATE inventory_units SET status = 'SOLD'
    // e. UPDATE variant_stock — decrement both in_stock_qty AND held_qty
    // f. INSERT inventory_movements (reason='SALE')
    // g. UPDATE payment_transactions SET status = 'SUCCEEDED'
  })
  // Then: cache event ID in Redis (Layer 3 above)

If anything throws, the transaction rolls back entirely. No partial state.


# =============================================================================
# 9) DATABASE LAYER RULES
# =============================================================================

## 9.1 — Three-layer architecture. No SQL in route handlers.

  Route handler  → validates input (Zod), calls service, returns response
  Service        → orchestrates, applies business rules, throws AppError
  Query function → executes DB queries, returns typed results

Never write db.execute() or db.query.* inside a route handler file.
All query functions live in packages/db/src/queries/<module>.ts.

## 9.2 — When to use db.execute(sql`...`) vs Drizzle query builder.

  Use db.execute(sql`...`) for:
    - Inventory hold/release (atomic UPDATE ... RETURNING)
    - Any query where correctness depends on the exact SQL
    - The reservation expiry worker claim
    - Complex transactions needing precise control

  Use Drizzle query builder for:
    - Standard reads (products, orders, cart)
    - Simple inserts and updates
    - Anything where Drizzle type safety is the main benefit

## 9.3 — Transactions use db.transaction(). Never manual BEGIN/COMMIT.

  return await db.transaction(async (tx) => {
    // use tx.execute(), tx.insert(), tx.update()
    // throw → automatic rollback
    // return → automatic commit
  })

## 9.4 — Append-only tables. Never UPDATE or DELETE these rows.

  loyalty.loyalty_ledger    balance is cached sum of ledger rows
  orders.order_events       full order timeline
  returns.return_events     full return timeline

## 9.5 — Drizzle schema column names match PostgreSQL schema exactly.

  camelCase property → snake_case column:
    firstName: text('first_name').notNull()
    heldQty:   integer('held_qty').notNull()

Never rename columns or add columns absent from modett_schema.sql.

## 9.6 — All 12 PostgreSQL schemas must be declared in Drizzle.

  const inventorySchema = pgSchema('inventory')
  export const variantStock = inventorySchema.table('variant_stock', { ... })

  Schemas: iam, catalog, inventory, cart, orders, payments, returns,
           reviews, loyalty, messaging, shipping, analytics

Never put Modett tables in the public schema.

## 9.7 — Connection pool is a process-level singleton. Max 20 connections.

  // packages/db/src/client.ts — created once at process startup
  const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 20 })

Never create a new Pool per request.

## 9.8 — analytics.events requires a created_at range filter on every query.

The table is PARTITION BY RANGE (created_at) with monthly child tables.
Unfiltered queries scan all partitions and are extremely expensive.
Dashboard queries use analytics.analytics_aggregates (pre-aggregated by worker).

## 9.9 — Zod schemas live in packages/utils/src/schemas/<domain>.schema.ts.

API and web import from packages/utils. Do not duplicate Zod schemas.
Validate all external input (request bodies, webhook payloads) at the
boundary before it touches any service or query function.


# =============================================================================
# 10) API DESIGN RULES
# =============================================================================

## 10.1 — All responses follow this exact shape. No exceptions.

  Success : { data: T }
  Error   : { error: { code: string; message: string } }

Never return raw DB error messages. Never return stack traces.

## 10.2 — Rate limiting (Redis sliding window, applied per route).

  POST /auth/login, /auth/signup    10 requests / 15 min / IP
  POST /notify-me                    3 requests / 1 hr  / session
  POST /newsletter/subscribe         5 requests / 1 hr  / IP
  POST /returns                      5 requests / 1 day / user
  POST /admin/invites/accept         5 requests / 1 hr  / IP
  POST /webhooks/payable           500 requests / 1 min / IP

## 10.3 — Auth middleware names and responsibilities.

  requireAuth()   validates customer session in Redis, attaches req.user
  requireAdmin()  validates admin session in Redis, enforces 15-min idle TTL,
                  attaches req.admin, returns 401 if expired
  requireOwner()  requireAdmin() + checks req.admin.role === 'OWNER'

Admin session timeout enforced server-side via Redis TTL (15 min).
Not a JWT expiry. Not a frontend timer. TTL resets on every authenticated request.
Admin sessions: 8h absolute TTL, 15-min idle TTL (both enforced in Redis).

## 10.4 — Return eligibility is always validated server-side.

Before creating a return_request, verify ALL of:
  1. order.fulfillment_state === 'DELIVERED'
  2. now() < eligible_until
  3. No active return for same order_item_id (WHERE request_status != 'REJECTED')
  4. Requested qty <= original order_item.qty

## 10.5 — return_request_items.request_status synced in same transaction.

  await db.transaction(async (tx) => {
    await tx.update(returnRequests).set({ status: newStatus }).where(eq(...))
    await tx.update(returnRequestItems).set({ requestStatus: newStatus }).where(eq(...))
  })

## 10.6 — Loyalty: balance cache vs ledger truth.

  loyalty_accounts.balance = cache (fast reads)
  loyalty_ledger            = source of truth (append-only)

If they disagree: recalculate from ledger. Never trust the cache alone.
withLoyaltyLock (5s TTL) wraps all earn/redeem operations.
earnPointsForOrder is best-effort — called after payment, wrapped in .catch().

## 10.7 — Messaging: outbox pattern for all notifications.

Single entry point: queueNotification({ userId, templateKey, payload, channels })
dedupe_key format: '{scope}:{id}:{template_key}:{channel}'
withOutboxLock 30s TTL prevents duplicate sends.
All 8 wiring points use best-effort .catch() — messaging never fails an order.


# =============================================================================
# 11) FRONTEND RULES (apps/web)
# =============================================================================

## 11.1 — Rendering strategy.

  Server Components (default, no 'use client'):
    page-level data fetching, product listings, order history,
    any page where SEO matters or auth token must not reach the browser.

  Client Components ('use client'):
    variant selector, cart drawer, checkout form, ReservationTimer,
    Toast, anything using useState / useEffect / TanStack Query hooks.

Minimise 'use client' surface. Lean on Server Components.
Use the preload pattern to avoid request waterfalls.

## 11.2 — All fetch calls go through apps/web/src/lib/api.ts.

The typed fetch wrapper must:
  - Prepend NEXT_PUBLIC_API_URL to all paths
  - Attach session cookie automatically (credentials: 'include')
  - Parse { data: T } | { error: ... } response shapes
  - Throw typed errors on error responses

Never call fetch() directly in page or component files.

## 11.3 — TanStack Query for all server state.

  // Correct — server state in TanStack Query
  const { data: cart } = useQuery({
    queryKey: ['cart'],
    queryFn:  () => api.get('/cart'),
  })

  // Wrong — server state in Zustand
  const cart = useCartStore(s => s.cart)

Zustand is for UI state only: drawer open/closed, selected variant,
checkout step, toast queue. Never put API data in Zustand.

## 11.4 — Build design system primitives before any page.

These must exist in packages/ui before any page is built:

  Button          variants: filled | filled-inverse | outline |
                            outline-inverse | ghost | ghost-inverse
                  states:   default | loading | disabled
  OutlineButton   variants: default | surface | inverse | dark
  Container       wide / narrow / flush
  Section         sizes: xs/sm/md/lg/xl, backgrounds: default/surface/deep/editorial
  Grid            cols 1–12, responsive
  Stack           direction, gap, align, justify
  Heading         levels 1–6, responsive, Playfair Display
  Text            9 variants, Raleway
  SiteHeader      sticky, light background, umber ink, mobile drawer
  MobileMenu      dark drawer, gold logo flip

  These are in addition to feature-level components:
  PriceDisplay    accepts Money type only — never a raw number
  CountdownTimer  props: expiresAt (ISO string). Yellow at 5 min, red at 1 min
  Badge           in-stock | low-stock | out-of-stock | sale
  SizeButton      available | selected | oos (disabled + greyed)
  ColourSwatch    circular: available | selected | disabled

## 11.5 — PriceDisplay accepts Money type only.

  // Correct
  <PriceDisplay money={{ amount: "1250.00", currency: "LKR" }} />

  // Wrong — never do this
  <PriceDisplay amount={1250} />

## 11.6 — ReservationTimer is hidden the moment payment is submitted.

Show the timer (using expires_at from POST /checkout/start) on payment step.
When the user submits payment (POST /payments/intent called):
  - Hide the timer immediately (Zustand UI state)
  - Show Spinner + "Processing payment — please do not close this page."

Never show "0:00" while payment is in flight.
The 10-minute grace period handles the backend. The UX must not alarm the user.

## 11.7 — Product Detail Page variant selector behaviour.

  - No colour or size pre-selected on page load.
  - "Add to Cart" disabled until BOTH colour and size are selected.
  - Size buttons disabled (not hidden) when available_qty = 0 for selected colour.
  - Show "Only N left" badge when available_qty <= low_stock_threshold.
  - Show "Notify Me When Available" when all sizes for a colour are OOS.
  - Changing colour resets size selection to unselected.

## 11.8 — Images use next/image.

  - Formats: WebP / AVIF (handled by Vercel automatically)
  - Provide sizes prop on all images
  - Lazy load all images below the fold

## 11.9 — Design system tokens.

  Brand: Elegance, Amplified.
  Background: alabaster (#E5E0D6). Primary ink: graphite (#232D35).

  Token rules:
    1. Use semantic tokens in components. Never primitive.* tokens.
    2. deep (#3E5460)      → footer and dark sections only
    3. highlight (#C1AB85) → sale price, loyalty, premium only
    4. editorial (#C78869) → campaign banners only
    5. No border-radius on buttons — brand uses sharp rectangular corners

  Typography:
    Headings: Playfair Display (font-display)
    Body/UI:  Raleway (font-body), font-light, tracking-[0.25em] on buttons
    Letter spacing on buttons: tracking-[0.25em] — wider than Tailwind's widest

## 11.10 — Animation with Framer Motion.

  Subtle transitions only: opacity, translate, scale.
  Always respect prefers-reduced-motion.
  Use Framer Motion for: drawer slide-in, page transitions, cart animations.
  Use CSS transitions for: hover states, colour fades (200–300ms ease-out).

## 11.11 — Admin portal session check on every page.

Every /admin/* page validates admin session server-side before rendering.
  Unauthenticated  → redirect to /admin/login
  Insufficient role → render 403, do not redirect

## 11.12 — Providers go in components/providers/.

QueryProvider (TanStack Query), ToastProvider, and any other context
providers are Client Components that wrap children.
They are composed in app/layout.tsx — not scattered across pages.


# =============================================================================
# 12) WORKER RULES
# =============================================================================

## 12.1 — Scheduled job registry.

  reservationExpiry.ts     every 1 min    two-window expiry (critical)
  inventoryReconcile.ts    daily          compare units vs aggregate, log drift
  loyaltyTierRecompute.ts  weekly         rolling 12-month window, handle downgrades
  loyaltyExpiry.ts         daily          expire points after 12 months inactivity
  expiryWarning.ts         daily          warn users 30 days before expiry
  analyticsAggregate.ts    hourly         pre-aggregate events into analytics_aggregates
  cartCleanup.ts           daily          mark expired carts ABANDONED
  partitionCreate.ts       monthly (25th) create next month's analytics.events partition
  messagingOutbox.ts       continuous     poll outbox, send via Resend, update status

## 12.2 — Worker jobs must be idempotent.

If a job runs twice (crash + restart), it must produce the same result.
Use worker_lock_id for reservation expiry.
Use time-gated WHERE conditions for all other jobs.

## 12.3 — Reconciliation job never auto-corrects drift.

Log to inventory_reconciliation_log. Alert admin dashboard.
A human corrects manually. Never silently adjust stock.


# =============================================================================
# 13) CODE STYLE CONVENTIONS
# =============================================================================

## 13.1 — TypeScript.

  - TypeScript everywhere — no .js files in src/
  - Prefer interfaces over types for object shapes
  - No classes — functional style only
  - Use function keyword for named pure functions
  - Omit semicolons (Prettier handles this)
  - Named exports only — no default exports except Next.js pages and layouts

## 13.2 — Naming.

  Booleans     : isLoading, hasError, shouldRender (auxiliary verbs)
  Variables    : descriptive, no abbreviations
  TS files     : camelCase.ts
  React files  : PascalCase.tsx
  DB schema    : module name (inventory.ts, orders.ts)
  Directories  : lowercase-with-dashes
  Zustand      : *.store.ts
  TanStack     : use*.ts (useCart.ts, useProducts.ts)

## 13.3 — Conditionals.

  Guard clauses + early returns.
  Avoid else where a guard clause works.
  Single-line: if (hasError) return null

## 13.4 — File layout (within each file).

  1. Exported component / exported functions
  2. Subcomponents
  3. Helper functions
  4. Static content / constants
  5. Types and interfaces (at the bottom)

## 13.5 — TypeScript compiler strictness.

  "strict": true
  "noUncheckedIndexedAccess": true

No any types. No as unknown as X casts.
Zod for runtime validation at all API boundaries.

## 13.6 — Primary keys are always UUID.

  Application code  : crypto.randomUUID()
  PostgreSQL DEFAULT: gen_random_uuid()
  Never use integer serial PKs.

## 13.7 — AppError for all expected errors.

  throw new AppError('INSUFFICIENT_STOCK',              409)
  throw new AppError('RESERVATION_NOT_HELD',            409)
  throw new AppError('RETURN_WINDOW_EXPIRED',           422)
  throw new AppError('DUPLICATE_RETURN',                409)
  throw new AppError('WEBHOOK_INVALID_CHECKVALUE',      400)
  throw new AppError('LOCK_NOT_ACQUIRED',               409)
  throw new AppError('REVIEW_TOKEN_INVALID',            400)  // deliberately vague
  throw new AppError('LOYALTY_INSUFFICIENT_BALANCE',    409)

Route handler catches AppError:
  res.status(err.statusCode).json({ error: { code: err.code, message: err.message } })

Unexpected errors → global handler → Sentry → 500 with generic message.


# =============================================================================
# 14) OBSERVABILITY AND SECURITY
# =============================================================================

## 14.1 — Sentry on both api and web.

Include request ID / trace ID in every logged error when available.
Never log secrets, tokens, raw card numbers, or full webhook payloads.
User-facing error messages: short, actionable, no internal detail.

## 14.2 — Environment variables validated with Zod at process startup.

  // apps/api/src/config/env.ts
  const env = z.object({
    DATABASE_URL:             z.string().url(),
    REDIS_URL:                z.string().url(),
    PAYABLE_MERCHANT_ID:      z.string().min(1),
    PAYABLE_SECRET:           z.string().min(1),
    RESEND_API_KEY:           z.string().startsWith('re_'),
    ...
  }).parse(process.env)

Never hardcode secrets. Never commit .env files.

## 14.3 — Vercel environment variables (apps/web only).

  NEXT_PUBLIC_API_URL         Railway API base URL
  NEXT_PUBLIC_SITE_URL        Production domain
  No DATABASE_URL.
  No REDIS_URL.
  No payment provider secrets.

## 14.4 — CSRF and input hygiene.

  Server Actions use built-in Next.js CSRF protection.
  Sanitize all user-generated content before storage and display.
  Principle of least privilege for database roles.


# =============================================================================
# 15) TESTING STANDARDS
# =============================================================================

Unit tests:
  - All utilities in packages/utils
  - All Zod validation schemas
  - All Decimal.js monetary calculations

Integration tests (Vitest, real DB + real Redis, singleThread: true):
  Location: apps/api/src/tests/integration/

  Required before shipping:
  - Concurrent checkout (two requests for last unit — exactly one must succeed)
  - Duplicate PAYable webhook (second call must be 200 with no second order)
  - Reservation expiry during payment grace period (hold must survive)
  - Return on undelivered order (must return 422)

E2E tests (Playwright):
  - Browse products → add to cart → checkout → confirmation
  - Auth flow: signup, login, logout

## PR checklist (run through before marking done):

  Does UI match Figma spacing and interactions?
  Are components split into small, reusable parts?
  Are server actions validated with Zod?
  Are errors modelled and user-friendly (no stack traces)?
  Are Web Vitals protected (minimal unnecessary client-side JS)?
  Is keyboard navigation and ARIA coverage present?
  Are env vars validated and no secrets exposed?
  Are all new DB columns covered by a migration?
  Do integration tests still pass?


# =============================================================================
# 16) DATABASE AND MIGRATIONS
# =============================================================================

Use drizzle-kit for all schema changes.
Never change a production schema without a migration file.
Never modify modett_schema.sql directly — add new migration files.

Always add indexes for:
  - Product slug lookups
  - Order lookup by customer
  - Cart session / customer references
  (See existing indexes in modett_schema.sql as reference.)


# =============================================================================
# 17) THINGS CURSOR MUST NEVER DO
# =============================================================================

NEVER simplify the reservation expiry condition.
  Wrong : WHERE status='HELD' AND expires_at < now()
  Right : WHERE status='HELD' AND expires_at < now()
            AND (payment_submitted_at IS NULL OR grace_expires_at < now())

NEVER use read-then-write for inventory stock checks.
  The atomic UPDATE ... WHERE available_qty >= qty ... RETURNING is mandatory.

NEVER process a PAYable webhook without verifying SHA-512 checkValue first.

NEVER create a second order on duplicate webhook delivery.
  Two-layer idempotency is mandatory: Redis check → DB conflict → cache event ID.

NEVER hard-delete products, variants, or admins.
  Use deleted_at. All queries: WHERE deleted_at IS NULL.

NEVER store a monetary amount without its currency.

NEVER import from packages/db inside apps/web.

NEVER put DATABASE_URL or REDIS_URL in Vercel environment variables.

NEVER write SQL in a route handler file.
  Route handler → service → query function is the only valid path.

NEVER UPDATE rows in loyalty_ledger, order_events, or return_events.
  These are append-only audit tables.

NEVER query analytics.events without a created_at date range filter.

NEVER use JavaScript number type for monetary values.
  String in JSON / TypeScript. Decimal.js for arithmetic.

NEVER set grace_expires_at without payment_submitted_at in the same UPDATE.

NEVER create a new pg Pool per request.
  One pool per process, created at startup, max: 20 connections.

NEVER show the checkout countdown timer reaching zero during payment processing.
  Hide the timer when POST /payments/intent is called. Show Spinner instead.

NEVER use any type, as unknown as X, or suppress TypeScript errors with @ts-ignore.

NEVER log secrets, raw webhook payloads, or full payment details anywhere.

NEVER auto-correct inventory drift in the reconciliation job.
  Log to inventory_reconciliation_log and alert. Humans correct manually.

NEVER use Stripe, Axios, Prisma, shadcn/ui, Radix UI, Auth.js, next-safe-action,
  localStorage for auth, or integer PKs.

NEVER put API data (products, cart, orders) in Zustand.
  Zustand is for UI state only. API data belongs in TanStack Query.

NEVER import directly from another backend module's internal files.
  Cross-module calls go through modules/<domain>/index.ts only.

NEVER apply modular monolith patterns to apps/web.
  The frontend is one whole application. It has no module boundaries.
