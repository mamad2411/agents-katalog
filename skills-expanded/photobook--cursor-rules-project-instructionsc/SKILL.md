---
alwaysApply: true
---
# Project Instructions

## Current Architecture

**Monorepo** (npm workspaces): `moments` (Astro portfolio site) + `moments-admin` (React Router 7 admin SPA).

**Infrastructure (Cloudflare):**
- **D1** — SQLite database (shared by both apps), migrations in `moments/db/migrations`
- **R2** — `moments-media` bucket (binding present; photo storage currently via WebDAV)
- **Workers/Pages** — moments deploys as Astro+Cloudflare, moments-admin as React Router Worker

**Photo storage & delivery:**
- **WebDAV** — Uploads go to NAS at `WEBDAV_BASE_URL`. Items store path as `image_id`.
- **PhotoPrism** — Import from NAS-hosted PhotoPrism. Items store `photoprism:{hash}`.
- **Image proxy** — `/api/items/:id/image` (auth) and `/api/public/items/:id/image` (public albums only) serve from WebDAV or PhotoPrism.
- **Cloudflare Image Resizing** — For public albums, use `/cdn-cgi/image/<options>/<source-url>` for edge caching, resizing (thumb/grid/hero), and format optimization.

**Auth:** Session cookies (signed), bcrypt for passwords. Default user seeded via migration.

**Data flow:** Albums CRUD, album_items for composition. Transactional Outbox for publish-affecting changes. Items reference images by `image_id` (WebDAV path or `photoprism:{hash}`).

**CI/CD:** GitHub Actions deploy on path changes — `moments/**` → moments, `moments-admin/**` and `moments/db/**` → moments-admin.

---

## General Code Style

- Keep functions small with descriptive names
- Follow Single Responsibility Principle (SRP), but avoid over-engineering
- Prefer vertical slice / feature-based architecture over layered
- Prefer functional style and stateless functions when possible
- Use functional React components
- Use TypeScript for all new files
- Avoid unnecessary abstractions and premature optimization
- Use spaces for indentation everywhere except makefiles

---

## Architecture Principles

- Cloudflare-native stack only (D1, R2, Workers, Pages)
- No external databases unless explicitly required
- Avoid introducing ORMs unless justified
- Keep SQL explicit and readable
- No dual writes to external systems (use Transactional Outbox)

---

## Database Rules

- Use snake_case for database columns
- Use ULID for primary keys
- Store JSON as TEXT (D1-compatible)
- Store money as INTEGER (cents), never float
- Enforce enum values in application layer
- Use Drizzle migrations for all DB changes
- Never modify schema without a migration
- All publish-affecting changes must:
  - bump `public_version`
  - insert corresponding row into `outbox_events` in same transaction

---

## Tagging Rules

- Tags must be normalized in `tags`
- Use `tag_refs` for polymorphic references
- Never store authoritative tags as comma-separated strings
- Filtering must use indexed tag_refs queries

---

## Storage Rules

- Media originals on NAS (WebDAV or PhotoPrism). Database stores `image_id`: WebDAV path or `photoprism:{hash}`.
- R2 binding available; use for future storage needs if needed.
- Use item_assets for variants (original, preview, thumb) when using R2.
- Do not store raw URLs as authoritative references.

---

## Eventing Rules

- Use Transactional Outbox pattern for external integrations
- No direct indexing/search writes from service layer
- Outbox writes must occur in same DB transaction as state change
- Consumers must be idempotent

---

## Multi-Tenancy

- Current model assumes per-tenant D1 database
- Avoid cross-tenant joins
- No global state unless explicitly defined

---

## Non-Goals

- No premature microservices
- No heavy infrastructure for MVP
- No inline SQL comments in Mermaid diagrams
