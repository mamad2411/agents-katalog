# Pawser Platform — Cursor Rules

---

## Project

- **Name:** Pawser Platform
- **Monorepo:** Turborepo + pnpm workspaces
- **Apps:**
  - `portal` (Next.js 14) — Marketing site at `getpawser.io`
  - `admin` (Next.js 14) — Shelter dashboard at `app.getpawser.io`
  - `widget` (Vite + React) — Embeddable JS bundle at `cdn.getpawser.io/widget.js`
  - `api` (Express) — REST API at `api.getpawser.io`
- **Packages:** `@pawser/database` (Prisma), `@pawser/shared` (types, crypto), `@pawser/ui` (shared components)

---

## Product Architecture

Pawser is a backend SaaS for animal shelters. Shelters pay a subscription, connect
their ShelterLuv account via API key, and receive an embeddable JavaScript widget
(`<script>` tag + `<div id="pawser-root">`) they drop into their existing website.

**Three front-end surfaces:**
1. `apps/portal` → Marketing/landing site. Explains Pawser, pricing, sign-up. NOT a hosted animal portal.
2. `apps/admin` → Shelter staff dashboard. Connect API key, configure widget, copy embed code, manage billing.
3. `apps/widget` → Vite-bundled embed. Mounts on `#pawser-root`, reads `window.pawserSettings`. This is what adopters see.

The `apps/portal/app/[domain]/` routing that previously hosted animal grids is preserved
only as a demo/preview environment. It is not the product.

---

## Design System: Kindred Slate

**Full spec:** `1-PRD/stitch-export/DESIGN.md`
**Reference HTML files:** `1-PRD/stitch-export/*.html`

Key rules:
- Font: Source Sans 3 (Google Fonts)
- Icons: Material Symbols Outlined
- Primary color: `#00113f` (deep slate navy) — never generic `#3B82F6`
- Surface hierarchy: 6 tonal levels, NO 1px borders for layout separation
- Border radius: 12px default, 16px large, `full` for pills
- Shadows: ultra-diffuse only (`0 4px 20px rgba(0,0,0,0.02)`) — never `shadow-md`
- All Tailwind token names must match DESIGN.md exactly (e.g. `bg-surface-container-low`)

---

## Hard Constraints

- All DB/cache operations scoped by `organizationId`
- Encrypt/decrypt ShelterLuv API keys with AES-256-GCM (`ENCRYPTION_KEY`)
- Sync cadence by tier: trial=30m, basic=15m, pro=5m, enterprise=2m
- Handle ShelterLuv 429: exponential backoff + jitter; respect `Retry-After`
- Never expose adopter PII; store animal data only
- At least one owner per organization; prevent removal of last owner

---

## Coding Standards

- TypeScript strict; eslint + prettier
- Validate all inputs with Zod
- Use `async/await`; no promise nesting
- Error handling: never swallow; log to Sentry with context
- Use `'use client'` directive for interactive components in Next.js
- No `.css` files in portal, admin, or widget — Tailwind utility classes only
- No inline `style={{}}` props — use Tailwind (exception: single `primaryColor` brand accent)
- All new components in `_components/` folder co-located with the page that uses them
- Shared UI components go in `packages/ui/src/components/`

---

## Architecture Patterns

### API (apps/api)
- Tenancy: resolve org by `Host` header OR URL path param → attach `orgId` to request
- Redis keys: `tenant:{orgId}:animals:list`, `tenant:{orgId}:animal:{id}`
- BullMQ job key: `tenant:{orgId}:sync`
- Idempotent upsert: `(organizationId, externalId)`

### Widget (apps/widget)
- Reads config from `window.pawserSettings` (apiUrl, orgSlug, primaryColor, adoptUrlBase)
- Fetches data from `{apiUrl}/api/v1/animals?orgSlug={orgSlug}`
- Builds to `dist/widget.js` (IIFE format) + `dist/widget.css`
- Uses HashRouter (no server needed, drops into any existing site)
- All styles scoped — no global CSS leakage into host page

### Admin (apps/admin)
- All routes auth-protected (JWT, existing auth middleware)
- Sidebar nav layout: w-64 fixed + main content area
- Key pages: overview, widget-builder, embed-code, integration, billing, settings

### Portal (apps/portal)
- Marketing site only — no tenant-specific animal data on main routes
- Demo routes: `/demo/[slug]/animals` preserved for sales/preview purposes

---

## shelterluv_app Migration

When porting components from `shelterluv_app` into `apps/widget`:
- See `apps/portal/MIGRATION.md` for complete field mapping
- `animal.Type` → `animal.species`
- `animal.InternalID` → `animal.id`
- `animal.CoverPhoto` / `animal.Photos[]` → `animal.mediaAssets[].url`
- `animal.Breed` → `animal.breedPrimary`
- `animal.Age` (string) → `animal.ageYears` + `animal.ageMonths` (integers)
- `animal.AdoptionURL` → `animal.adoptionUrl`
- Do NOT port `useAnimals`/`useAnimal` hooks — widget uses its own fetch hooks against Pawser API

---

## Security

- JWT access + refresh with rotation; scrypt passwords (bcrypt fallback)
- RBAC: `super_admin` (global), `owner`, `admin`, `viewer` (org-scoped)
- CSP on Next.js apps
- Widget: all styles scoped, no global leakage
- Rate limiting per tenant; audit sensitive actions

---

## Package Naming

- `@pawser/database`
- `@pawser/shared`
- `@pawser/ui`
- `@pawser/portal`
- `@pawser/admin`
- `@pawser/widget`

---

## Docs

- `1-PRD/stitch-export/DESIGN.md` — design system source of truth
- `1-PRD/stitch-export/*.html` — visual reference screens from Stitch
- `1-PRD/2016-01-14/` — PRD documents
- `1-PRD/2016-01-14/0-developer-handbook.md` — technical handbook
- `apps/portal/MIGRATION.md` — shelterluv_app → widget type mapping
