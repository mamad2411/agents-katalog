---
description: Stock management platform goals, stack, architecture, RBAC, i18n (km | en), UI reference dashboard starter, stock/POS/reports, and delivery priorities for Printora Inventory.
globs: "**/*"
alwaysApply: true
---

# Stock Management Platform Project Rules

## Project Goal

Build a simple, reliable, and maintainable stock management platform for a small business.

The system must support:

- Product management
- Category management
- Supplier management
- Stock receiving
- Stock adjustment
- POS sales
- Auto stock deduction
- Low stock alert
- Sales report
- Stock report
- Profit report
- Telegram sale alert
- Two user roles: Business Owner and Cashier/Staff
- UI language switching: English (`en`) and Khmer (`km`)

Do not overengineer the solution. Keep the system clean, modular, and easy to maintain.

---

## Technology Stack

Use the following stack:

- Next.js App Router
- TypeScript
- PostgreSQL
- Supabase Auth
- Supabase Database
- Supabase CLI for schema versioning and migrations (`supabase/migrations`)
- Supabase Storage for product images
- Tailwind CSS
- shadcn/ui
- React Hook Form
- Zod
- Telegram Bot API for sale alerts
- Vercel for deployment
- Internationalization: [`next-intl`](https://next-intl.dev/) (or equivalent) for App Router locales `en` and `km`

Avoid adding extra libraries unless they clearly solve a real project need. i18n qualifies because the product is bilingual.

**Dashboard UI reference (patterns only):** Agents should mirror layout and visual style from [next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) (MIT) for owner/back-office screens — see **UI Rules → UI reference**. Do not adopt its auth/vendor stack by default.

## Architecture Rules

Use feature-based structure.

Recommended structure (align with dashboard reference where helpful — `components/layout`, `components/ui`, feature folders):

```txt
src/
  app/
  components/
    layout/
    ui/
  features/
  lib/
  constants/
  messages/
    en.json
    km.json
```

Place locale JSON (or TS message modules) under `src/messages/` or project-root `messages/`; keep exactly `en` and `km` catalogs in sync (same keys).

Each feature should own its own business logic.

Example:

```txt
features/products/
  actions/
  components/
  services/
  types/
  validations/
```

Use this structure for:

- products
- stock
- sales
- reports
- users
- settings

Do not place business logic directly inside UI components.

UI components should call actions or services.

### Database Rules

Use PostgreSQL.

Main tables:

- users
- categories
- suppliers
- products
- stock_receives
- stock_receive_items
- stock_movements
- sales
- sale_items
- stock_adjustments
- system_settings

Every stock change must create a stock movement record.

Product current stock can be stored in the products table for fast access, but stock_movements must remain the source of truth for stock history.

When creating sale items, store snapshot fields such as:

- product name
- SKU
- unit price
- cost price

This keeps old sale records correct even after product data changes.

### Schema migrations (Supabase CLI)

- **Source of truth:** PostgreSQL DDL lives in versioned SQL files under `supabase/migrations/` (created and applied with the [Supabase CLI](https://supabase.com/docs/guides/cli)), not only in the Dashboard SQL editor.
- **Workflow:** Use `supabase migration new <description>` for each change, edit the generated SQL, then apply with `supabase db push` against the linked project (or local `supabase start` during development). Commit migration files with application code.
- **Avoid:** Hand-editing production schema only in the Dashboard without a matching migration file — that drifts from the repo and breaks reproducible deploys.
- Optional one-off fixes in the Dashboard should be rare and followed by capturing the change in a new migration (e.g. via `supabase db diff`) when practical.

### Role Rules

There are only two roles:

- OWNER
- CASHIER

**Business Owner can:**

- Manage products
- Manage categories
- Manage suppliers
- Receive stock
- Adjust stock
- View all sales
- View reports
- Manage staff accounts
- View profit reports
- Manage settings (including default UI language for new sessions if modeled in settings)

**Cashier can:**

- Use POS
- Search products
- Add products to cart
- Change sale quantity
- Apply discount only if allowed
- Complete sale
- Print receipt
- View own sale history

**Cashier cannot:**

- Edit product cost
- Edit selling price
- Delete products
- Change stock manually
- View profit reports
- Manage users
- Manage settings

Always check role permission before allowing sensitive actions.

### Naming Rules

Use PascalCase for variable names.

Good:

```ts
const ProductName = 'Coffee Cup'
const CurrentStock = 10
const SaleTotal = 120
```

Use camelCase for function and method names.

Good:

```ts
getProductList()
createSale()
updateStock()
sendTelegramAlert()
```

Do not create very long function names.

Avoid:

```ts
calculateTheFinalSaleAmountAfterDiscountAndTax()
```

Prefer:

```ts
calculateSaleTotal()
```

Use clear and simple names.

### Code Style Rules

- Use TypeScript for all application code.
- Prefer simple readable code over clever code.
- Do not overengineer.
- Do not create unnecessary abstractions.
- Do not create generic helpers before they are needed.
- Keep functions small.
- Keep files focused on one responsibility.
- Use early return to reduce nested logic.
- Use async/await for asynchronous code.
- Validate input with Zod before saving to database.
- Use server-side checks for important business rules.
- Do not trust client-side validation only.

### Comment Rules

Comments are allowed, but keep them short.

Good:

```ts
// Prevent sale when stock is not enough
```

Avoid long explanation comments.

Code should be readable by itself.

Use comments only when the reason is not obvious.

### Stock Rules

Stock must not change when product is added to cart.

Stock changes only when sale is completed.

**When sale is completed:**

- Create sale record
- Create sale item records
- Deduct product stock
- Create stock movement records
- Send Telegram alert
- Show or print receipt

**When sale is cancelled:**

- Do not change stock

**When item is refunded and returned:**

- Increase stock
- Create stock movement record

**Low stock rule:**

```txt
CurrentStock <= MinimumStock
```

### POS Rules

POS must be simple and fast.

Cashier should be able to search by:

- Product name
- SKU
- Size
- Color
- Category

Always check stock before completing sale.

Do not allow completed sale if quantity is greater than available stock.

Receipt number should be generated by the system.

Example:

```txt
INV-0001
INV-0002
```

### Report Rules

Business Owner reports should include:

- Today's sales
- Monthly sales
- Low stock products
- Total products
- Total stock quantity
- Best-selling products
- Recent sales
- Recent stock movements
- Profit report

Cashier can only view their own sale history.

Do not show profit data to cashier.

### UI Rules

Keep UI simple and clean.

Use shadcn/ui components when possible.

Use Tailwind CSS for styling.

Avoid complicated layouts.

Prioritize:

- Fast POS workflow
- Easy product search
- Clear stock status
- Clear owner dashboard
- Mobile/tablet-friendly layout where useful
- Visible language switcher (`en` | `km`) on primary layouts (POS, dashboard, settings)

### Loading states

Every user action that waits on the network or a route transition must show loading feedback. Do not leave buttons, links, or forms appearing idle while work is in progress.

**Infrastructure (reuse — do not reinvent):**

- `PlatformLoadingShell` + `LoadingProvider` wrap the app (`src/app/[locale]/layout.tsx`).
- `LoadingIndicator` — global top progress bar (navigation) and full-page overlay with spinner (navigation + server actions).
- `useLoadingAction()` — wrap async **server actions** and mutations (`run(async () => …)`). Sets `actionPending` until the promise settles.
- `useNavigationLoading()` — call `startNavigation()` before programmatic `router.push` / `router.replace` (e.g. filters, locale switch).
- `LoadingLink` (`src/components/layout/loading-link.tsx`) — **default link** for in-app navigation in client UI. Calls `startNavigation()` on click and dims while navigation is pending.
- `PageBreadcrumb` (`src/components/layout/page-breadcrumb.tsx`) — breadcrumbs in server pages; uses `LoadingLink` for segments with `href`.
- `(dashboard)/loading.tsx` — route-level fallback while a dashboard page’s RSC payload loads.
- `NavigationLoadingListener` — backup for plain `<a>` clicks; prefer explicit `LoadingLink` in new UI.

**When to apply what:**

| Action type | Pattern |
|-------------|---------|
| Link / breadcrumb / sidebar nav to another page | `LoadingLink` or `PageBreadcrumb` |
| Form submit → server action | `useLoadingAction` + disable fields + button shows `common.loading` |
| Toggle / delete / other mutation + `router.refresh()` | `useLoadingAction` + disable control |
| Search / filter → `router.replace` with query | `startNavigation()` + disable filter inputs while pending |
| Lazy fetch in expanded row / combobox (no full navigation) | Local `useState` loading + inline `Spinner`; do not use full overlay |
| Auth-only marketing links | Plain `Link` is acceptable |

**Checklist for new screens:**

- Primary CTAs that navigate (Add product, Receive stock, Edit, Back, Cancel) use `LoadingLink`.
- Breadcrumbs on server pages use `PageBreadcrumb`.
- Submit buttons show loading label and disable during submit.
- Add `(segment)/loading.tsx` when a route group fetches heavy server data.

**Do not:**

- Leave navigation links as raw `Link` in dashboard/back-office UI unless there is a documented exception.
- Rely only on the thin top bar — navigation must trigger the same visible overlay as actions (`LoadingIndicator` shows both).
- Block collapse or cancel while a nested inline fetch runs unless double-submit is a real risk.

### UI reference — next-shadcn-dashboard starter

Use **[Kiranism/next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter)** (MIT) as the **sample for platform chrome**: dashboard shell (sidebar, header, main content spacing), overview-style cards, list/table pages, forms built from shadcn/ui, Tailwind rhythm, and optional theme/dark-mode patterns.

- **Demo:** [shadcn-dashboard.kiranism.dev](https://shadcn-dashboard.kiranism.dev/dashboard) — use for density, hierarchy, and component composition cues.
- **Apply mainly to** Business Owner / back-office routes (dashboard, products, stock, reports, settings). **POS** stays optimized for speed and cashier workflow (touch-friendly, minimal chrome); reuse tokens and components, not necessarily the full admin shell.
- **Do not treat the starter as the source of truth for backend/auth:** This repo uses **Supabase Auth**, **Supabase DB**, **React Hook Form**, **next-intl**, and **Zod** as specified above. **Do not** add Clerk, Clerk Billing/Organizations, Sentry, Kanban/Chat demo modules, or other starter-only dependencies unless the product explicitly requires them.
- **Structure:** Prefer mirroring the starter’s separation of `components/layout`, `components/ui`, and `features/*` when implementing new screens so the codebase stays consistent with that mental model.
- **Scope:** Copy **patterns** (layout, styling, table/toolbar composition). Avoid wholesale file dumps from upstream; adapt to Printora routes, RBAC, and i18n message keys.

### Internationalization (i18n) Rules

**Locales**

- Supported locale codes: `en` (English), `km` (Khmer).
- Do not add extra locales in v1 unless product asks for it.

**Routing**

- Use locale-aware URLs with App Router, for example `app/[locale]/layout.tsx` and routes under `[locale]`.
- Middleware should negotiate locale (cookie and/or `Accept-Language`) and redirect to a valid locale prefix.

**Strings**

- All user-visible UI copy (labels, buttons, empty states, validation messages shown to users, dialog titles) must come from locale message catalogs, not hard-coded in one language only.
- Product/catalog data stored in the database (names, categories as entered by staff) is **not** auto-translated by the system; only the **application chrome** is bilingual.

**Formatting**

- Format dates, numbers, and currency using the active locale (Khmer digits and formatting where appropriate for `km`).

**Persistence**

- Persist the user’s choice (cookie and/or `users.preferred_locale`; optional `system_settings.default_locale` for first-time visitors). Owner-managed default in settings is optional but recommended.

**Errors**

- Map server validation and business-rule failures to stable error codes or keys, then render translated messages on the client or from server components using the active locale.
- Do not leak raw DB errors; user-facing text stays translated.

**Telegram**

- Compose Telegram sale alert text using the **cashier’s active UI locale** at the moment the sale completes (so alerts match what they saw on screen).

### Error Handling Rules

Show clear error messages (in the user’s active locale).

Examples (provide equivalent strings in `en` and `km` catalogs):

- Product not found
- Stock is not enough
- Sale could not be completed
- User does not have permission
- Telegram alert failed

Do not expose database errors directly to the user.

Log technical errors server-side.

### Telegram Alert Rules

Send Telegram alert only after sale is completed.

Alert should include:

- Receipt number
- Cashier name
- Total amount
- Payment method
- Sale date

If Telegram alert fails, the sale should still remain completed.

Mark `telegram_sent` as false if alert fails.

### Best Practice Rules

- Follow existing project patterns when editing old code.
- Do not rewrite unrelated code.
- Do not change database schema without updating related types and services.
- Schema changes must ship as Supabase CLI migrations under `supabase/migrations/` (see **Database Rules → Schema migrations**).
- Do not add new dependencies without clear reason.
- Generated code must be production-ready, readable, and consistent with the existing codebase.
- When adding or refactoring **owner/back-office** UI, default to the **next-shadcn-dashboard-starter** patterns described under UI reference unless this repo already defines a conflicting convention.

---

## Version 1 scope (final recommendation)

For your first version, build only the core modules:

```txt
1. Login + roles
2. Products
3. Categories
4. Suppliers
5. Stock receive
6. POS sale
7. Stock movements
8. Sales history
9. Owner dashboard (layout/visual patterns aligned with next-shadcn-dashboard-starter)
10. Low stock report
11. Telegram sale alert
12. UI language switching (en | km) with persisted preference
```

Avoid building advanced refund, audit log, expense tracking, and complex analytics in version 1. Your current business need is mainly to replace Excel with a clean stock + POS + report system.
