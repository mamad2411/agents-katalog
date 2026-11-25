---
name: shopify-app-patterns
description: "Comprehensive patterns and best practices for building Shopify apps. Covers GraphQL API usage, admin/checkout/POS/storefront extensions, Shopify Functions, webhooks, metafields/metaobjects, authentication, App Bridge, Polaris, and Built for Shopify standards. Use this skill whenever building a Shopify app, creating Shopify extensions, working with Shopify APIs (Admin GraphQL, Storefront), implementing webhooks, writing Shopify Functions, designing admin UI extensions, checkout extensions, POS extensions, theme app extensions, or anything related to Shopify app development patterns. Also trigger when the user mentions Shopify CLI, shopify.app.toml, Polaris components, App Bridge, metafields, metaobjects, or any Shopify app architecture question. This skill assumes setup is already done — it focuses entirely on implementation patterns."
---

# Shopify App Patterns

Patterns and best practices for building Shopify apps, distilled from Shopify Academy's "Developing Apps for Shopify" learning path and official Shopify developer documentation. This skill assumes the project is scaffolded and focuses on **how to build well**, not how to set up.

## Architecture Mental Model

A Shopify app has two halves:

**App home** (you host it): Your backend + embedded frontend rendered in an iframe/WebView inside the Shopify admin. Built with React Router (recommended template), Polaris for UI, and App Bridge for communication with the admin shell.

**Extensions** (Shopify hosts them): Declarative pieces that plug into defined surfaces — admin pages, checkout, online store themes, POS, Flow, Sidekick. Extensions are rendered with native technologies, versioned and deployed together with your app config.

The golden rule: push logic into extensions wherever possible. Extensions are faster (native rendering), safer (sandboxed), and more merchant-friendly (no iframe navigation). Use the app home for configuration dashboards and complex workflows that don't fit an extension.

### Extension-Only Apps

Apps composed entirely of extensions — no app home, no web server. Shopify hosts everything. Ideal for simple, focused tools (a single admin action, a discount function). Limitation: can only use custom distribution, not the App Store. If you need API calls beyond Admin GraphQL, third-party integrations, or secret storage, you need a server-hosted app.

## GraphQL Admin API Patterns

REST is legacy (since October 2024). All new development uses GraphQL.

### Core patterns

```graphql
# Single endpoint for everything
POST https://{shop}.myshopify.com/admin/api/2026-01/graphql.json

# Authentication header
X-Shopify-Access-Token: {access_token}
```

**In React Router apps**, use the authenticated helper:
```typescript
import { authenticate } from "../shopify.server";

export async function loader({ request }) {
  const { admin } = await authenticate.admin(request);
  const response = await admin.graphql(`
    query { shop { name } }
  `);
  const data = await response.json();
  return data;
}
```

**In UI extensions** (Direct API Access):
```javascript
// Authentication is automatic — no tokens needed
const response = await fetch('shopify:admin/api/2026-01/graphql.json', {
  method: 'POST',
  body: JSON.stringify({
    query: `query { shop { name } }`,
  }),
});
const { data } = await response.json();
```

### Rate limits

GraphQL uses **calculated query cost**, not call count. Each field costs points. The budget is 1000 points per query, restored at 50 points/second. Design queries to request only what you need. For bulk data, use `bulkOperationRunQuery` instead of paginating — it handles arbitrarily large datasets asynchronously.

### Error handling

GraphQL returns HTTP 200 even for errors. Always check both `data` and `errors` in responses. For mutations, always request `userErrors { field message }` — this is where validation failures surface.

### Pagination

Use cursor-based pagination with `first`/`after` (forward) or `last`/`before` (backward). Always fetch `pageInfo { hasNextPage endCursor }` alongside your edges.

> For deep dives on GraphQL patterns: read `references/graphql-patterns.md`

## Authentication & Authorization

### Session tokens (embedded apps)

Embedded apps authenticate using JWT session tokens issued by App Bridge. The token lives for 1 minute and must be fetched on every request. The scaffolded React Router app handles this automatically via `authenticate.admin(request)`.

Key concepts:
- **Session tokens** = authentication (who is making this request?)
- **Access tokens** = authorization (what can this app do on this store?)
- **Token exchange** = the recommended flow where session tokens are exchanged for API access tokens, replacing the old OAuth redirect dance
- **Shopify managed installation** = Shopify handles the install flow when you declare scopes in `shopify.app.toml` — no custom OAuth needed

Declare scopes in your app config:
```toml
# shopify.app.toml
[access_scopes]
scopes = "read_products,write_products,read_orders"
```

## App Surfaces & Extensions

Shopify apps extend multiple surfaces. Choose the right surface for your feature.

> For complete extension patterns with code: read `references/extensions-guide.md`

### Admin extensions

| Type | Purpose | Trigger |
|------|---------|---------|
| **Admin action** | Modal workflows (create, edit, confirm) | Dropdown on resource pages (Products, Orders, Customers) |
| **Admin block** | Persistent cards showing data or edit forms | Added to resource detail pages by merchants |
| **Admin print action** | Print documents from admin | Print menu on orders/products |
| **Admin link** | Deep link to your app page | Resource page "More actions" menu |

Admin UI extensions use a component-based model with `@shopify/ui-extensions-react/admin`. They have a 64 KB compressed bundle limit — keep them lean.

### Checkout extensions

| Type | Purpose |
|------|---------|
| **Checkout UI extension** | Custom UI in checkout (banners, fields, upsells) |
| **Shopify Functions** | Backend logic (discounts, shipping, validation, payment) |
| **Web pixel** | Analytics/tracking in checkout |
| **Payments extension** | Custom payment methods |

Checkout is upgrade-safe — your extensions survive Shopify's checkout improvements (one-page checkout, Shop Pay, etc.). Never use `checkout.liquid` (deprecated/sunset).

### Online store extensions

**Theme app extensions** are mandatory for App Store apps. Two types:
- **App blocks**: Inline content on pages (product badges, reviews, widgets). Merchants place them via theme editor.
- **App embed blocks**: Floating/overlay elements (chat widgets, banners). No UI component or overlaid element.

Theme app extensions don't edit theme code — this is a core design principle. Benefits: no breaking changes to themes, clean uninstall, better merchant experience.

**App proxies** forward requests from `https://{shop}.myshopify.com/...` to your server, solving CORS. Return Liquid templates, JSON, or static assets.

### POS extensions

POS UI extensions render as native components on iOS/Android. Three target types:
- **Tiles**: Smart grid items on home screen
- **Actions**: Menu buttons that launch modals
- **Blocks**: Custom sections within screens (product details, cart)

POS extensions can query Admin GraphQL directly via `fetch()`. For anything beyond Admin API (third-party APIs, secrets), you need a server-hosted backend.

## Shopify Functions

Functions customize Shopify's backend logic by injecting WebAssembly code at defined extension targets. They don't have URLs — Shopify invokes them as-needed.

**Pattern**: Input (GraphQL query → JSON) → Logic (Wasm) → Output (JSON operations)

Available Function APIs:
- **Discounts** — product, order, shipping, and combined discounts
- **Payment customization** — hide/reorder/rename payment methods
- **Delivery customization** — rename/reorder/hide shipping options
- **Cart validation** — block checkout based on custom rules
- **Order routing** — location rules, fulfillment constraints
- **Bundles** — group products as a single purchasable unit

**Language**: Shopify strongly recommends **Rust** for performance. JavaScript is supported but risks failure with large carts. Functions compile to Wasm.

```toml
# shopify.extension.toml for a discount function
[[extensions]]
name = "volume-discount"
type = "function"
api_version = "2026-01"

[extensions.targeting]
target = "purchase.discount.run"
```

> For function implementation patterns: read `references/functions-patterns.md`

## Webhooks

Webhooks deliver near-real-time event data. Prefer webhooks over polling.

### Key patterns

1. **Subscribe declaratively** in `shopify.app.toml`:
```toml
[webhooks]
api_version = "2026-01"

[[webhooks.subscriptions]]
topics = ["orders/create", "products/update"]
uri = "https://your-app.com/webhooks"
```

2. **Delivery options** (in order of preference):
   - Google Cloud Pub/Sub (recommended by Shopify)
   - Amazon EventBridge
   - HTTPS endpoint

3. **Verify webhooks** using HMAC-SHA256 with your app's client secret against the `X-Shopify-Hmac-Sha256` header.

4. **Handle duplicates** — compare `X-Shopify-Event-Id` headers. Shopify doesn't guarantee exactly-once delivery.

5. **Don't assume ordering** — a `products/update` can arrive before `products/create`. Use `X-Shopify-Triggered-At` timestamps to reconstruct order.

6. **Respond fast** — return 2xx within 5 seconds. Do heavy processing asynchronously.

## Data Modeling: Metafields & Metaobjects

### Metafields

Extend existing Shopify resources (products, customers, orders) with custom key-value data.

**Two ownership models:**

| Model | Namespace | Created via | Who can edit |
|-------|-----------|------------|--------------|
| App-owned | `$app` (GraphQL) / `app` (TOML) | `shopify.app.toml` or GraphQL | Only your app |
| Merchant-owned | Any non-reserved (e.g. `custom`) | GraphQL only | Merchants + all apps |

**App-owned metafield via TOML** (preferred for app-managed data):
```toml
[product.metafields.app.internal_sku]
name = "Internal SKU"
description = "Internal inventory tracking code"
type = "single_line_text_field"
access.admin = "merchant_read"
access.storefront = "none"
```

**App-data metafields** — tied to `AppInstallation`, completely hidden from admin. Use for per-install config. Store via `metafieldsSet` mutation with `ownerId` = your `AppInstallation` GID.

### Metaobjects

Standalone structured data with multiple fields (size charts, author profiles, FAQ entries).

**App-owned metaobject via TOML:**
```toml
[metaobjects.app.author]
name = "Author"
access.admin = "merchant_read_write"
access.storefront = "public_read"

[metaobjects.app.author.fields.full_name]
name = "Full Name"
type = "single_line_text_field"

[metaobjects.app.author.fields.bio]
name = "Biography"
type = "multi_line_text_field"
```

**Decision framework**: Single custom value on an existing resource → metafield. Multi-field structured data that stands alone → metaobject. When in doubt, start with metafields.

## Deployment & Versioning

All extensions and app config are versioned together as a single **app version**.

```bash
# Deploy = create + release a new app version
shopify app deploy
```

Key behaviors:
- Releasing replaces the active version for all installed stores
- Rollback is possible from the Dev Dashboard
- Some extension types require review before release
- CI/CD integration: use `shopify app deploy` in your pipeline with `SHOPIFY_CLI_PARTNERS_TOKEN`

## Built for Shopify Standards

Meeting these standards earns badges, search ranking boosts, and App Store promotion.

**Quality pillars:**
1. **Safety & security** — proper auth, clean install/uninstall, API compliance
2. **Performance** — fast admin embedding, minimal checkout/storefront impact
3. **Ease of use** — embedded in admin, intuitive UI, follows Polaris patterns
4. **Proven usefulness** — installs, reviews, ratings over a rolling window

**Non-negotiable requirements for App Store:**
- App must be embedded in the Shopify admin
- Use theme app extensions (not ScriptTag/Asset API) for storefront integration
- Clean uninstall — no orphaned code in themes
- Minimize checkout speed impact
- Follow [App Design Guidelines](https://shopify.dev/docs/apps/design-guidelines)

## Reference Files

For deeper implementation details, read these companion files:

| File | When to read |
|------|-------------|
| `references/graphql-patterns.md` | Writing complex queries, bulk operations, pagination, error handling |
| `references/extensions-guide.md` | Building any extension type with code examples and configuration |
| `references/functions-patterns.md` | Implementing Shopify Functions (discounts, validation, shipping, etc.) |
