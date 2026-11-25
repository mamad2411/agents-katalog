---
name: develop-laravel-ecommerce-feature
description: Develop features for Laravel 13 + Filament v4 e-commerce. Use when adding Filament admin resources, Blade pages, Livewire components, or e-commerce logic (cart, checkout, orders) in this project.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, astro_build, astro_check, astro_dev, run_tests]
---

# Develop Laravel Ecommerce Feature

Use this skill when building or modifying features in the Laravel e-commerce platform. This extends the generic `develop-laravel-feature` skill with project-specific file map, models, and design constraints.

**Stack (2026):** Laravel 13 + Filament **v4** (Schema API) + Livewire 3 + PHP 8.3+ + Pest v5.

**Prerequisites:** Read `overlays/laravel-filament/rules/laravel-conventions.md` first for generic patterns.

## Project Map

```
/var/www/app/
├── app/
│   ├── Actions/                ← Single-action classes (ProcessCheckoutAction)
│   ├── Services/               ← Stateful services (CartService)
│   ├── Filament/Resources/     ← Admin: CategoryResource, ProductResource,
│   │                              OrderResource, ArticleResource
│   ├── Http/
│   │   ├── Controllers/        ← PageController, ProductController,
│   │   │                          ArticleController, CheckoutController
│   │   └── Requests/           ← FormRequest validation
│   ├── Livewire/               ← CartDrawer, AddToCartButton, CartIcon
│   ├── Models/                 ← Category, Product, Order, OrderItem, Article
│   └── Providers/
├── database/migrations/        ← PostgreSQL migrations
├── resources/views/
│   ├── layouts/                ← Base Blade layouts (Elomus Theme)
│   ├── pages/                  ← Static page templates
│   └── livewire/               ← Livewire component views
├── routes/web.php              ← Vietnamese-slug routes
└── tests/                      ← Pest PHP tests
```

## Core Rules

- Follow all rules from `overlays/laravel-filament/rules/laravel-conventions.md` (Thin Controller, DB::transaction, FormRequest, etc.)
- Follow all rules from `overlays/laravel-ecommerce/rules/laravel-ecommerce-rules.md` (Vietnamese slugs, VietQR, deploy targets)
- Apply design tokens from `overlays/laravel-ecommerce/rules/elomus-design-system.md` (Deep Navy + Teal palette, Outfit font, Elomus interactions)

## Suggested Process

### 1. Identify The Layer

| Task | Layer | Location |
|------|-------|----------|
| Admin CRUD | Filament Resource | `app/Filament/Resources/` |
| New public page | Controller + Blade | `app/Http/Controllers/` + `resources/views/pages/` |
| Interactive widget | Livewire | `app/Livewire/` + `resources/views/livewire/` |
| Business logic | Action / Service | `app/Actions/` or `app/Services/` |
| Schema change | Migration | `database/migrations/` |
| Payment / QR | Service + Config | `app/Services/` |

### 2. Read Existing Patterns

- **Filament**: Read `ProductResource.php` for form/table, media upload, enum selects.
- **Controller**: Read `ProductController.php` for thin-controller pattern.
- **Livewire**: Read `CartDrawer.php` for Alpine.js integration and event dispatching.
- **Model**: Read `Product.php` for casts, relationships, scopes, media conversions.
- **Action**: Read `ProcessCheckoutAction.php` for DB::transaction() pattern.

### 3. Apply Design System

- Deep Navy (`#1B2A4A`) for text, Teal (`#2BA5B5`) for CTAs.
- Outfit font from Google Fonts.
- Product card hover: swap to second image + slide-up "Thêm vào giỏ" button.
- Mobile: Sticky bottom CTA bar on PDP.

### 4. Test Critical Paths

- Cart total calculation and checkout flow (Pest PHP).
- Run: `php artisan test` or `./vendor/bin/pest`.

## Failure Modes

- **v3 Filament API used instead of v4**: a resource is written with the deprecated `Form::schema()` API. **Mitigation:** the Core Rules require the v4 `Schema::components()` API; reject v3 code.
- **Vietnamese slugs drift from web.php**: a new route uses a slug that does not match the existing convention. **Mitigation:** verify the slug pattern against the nearest sibling routes; reject non-conforming slugs.
- **DB::transaction missing on multi-table writes**: a checkout writes to orders and order_items without a transaction. **Mitigation:** the Core Rules require `DB::transaction()`; reject un-wrapped multi-table writes.
- **Sync email dispatch**: an order confirmation is sent synchronously inside the request. **Mitigation:** the Core Rules require queue dispatch; reject sync sends.
- **Hard-coded currency or QR config**: a checkout path uses hard-coded values instead of the VietQR config. **Mitigation:** reference the project config; reject hard-coded values in PR.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving Pest v5 tests pass.
- **`contracts/schemas/api-contract-spec.json`** when a new Filament v4 Resource or public Blade route introduces a typed surface.
- For checkout or cart changes, also emit **`contracts/schemas/feature-ticket.json`** with the cart-total invariant documented.

Skip structured emission for trivial UI tweaks that do not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Filament v4 Resources and FormRequest validation must enforce role-based access; customer data must not be exposed to admin roles without an explicit policy profile.
- **ASI04 Supply Chain**: every Laravel, Filament, Livewire, and Pest dependency must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: do not construct SQL queries, payment payloads, or Blade strings from external or user-supplied content without strict schema validation; reject string-concatenated SQL.
- **ASI07 Inter-Agent Communication**: the implementation result is consumed by Backend Developer, QA Engineer, and Content Manager roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a checkout change as "safe" without the actual smoke test evidence; surface the residual risk honestly.
## Checklist

- [ ] feature placed in the correct architectural layer
- [ ] thin controller pattern followed
- [ ] Livewire used only for interactive islands
- [ ] **Filament v4 `Schema::components()` used** (not deprecated v3 `Form::schema()`)
- [ ] DB::transaction() wraps multi-table writes
- [ ] migrations include indexes on slug, category_id, status columns
- [ ] SoftDeletes on Category and Product
- [ ] Elomus design tokens applied (Deep Navy, Teal, Outfit font)
- [ ] Vietnamese slug routes match web.php conventions
- [ ] FormRequest used for validation
- [ ] media via Spatie with WebP conversion
- [ ] Pest v5 tests written for critical logic (cart, checkout, state transitions)
- [ ] queue used for email, never synchronous

## Related Skills

- **develop-laravel-feature**: generic Laravel + Filament + Livewire patterns (read first)
- **review-code**: review against Laravel and project conventions
- **write-tests**: write Pest PHP tests
- **navigate-service**: understand the codebase before changes
- **commit-code**: commit with proper conventions
