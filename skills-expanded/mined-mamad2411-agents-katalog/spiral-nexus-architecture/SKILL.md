---
name: spiral-nexus-architecture
description: The architectural source of truth for the Spiral Nexus IP-marketplace codebase. Use this skill whenever working in the Spiral Nexus repo - building or editing any feature, writing migrations, adding API routes or UI, setting up auth, payments, or access control, or making any decision about where code goes or how it should be shaped. Trigger it even when the user doesn't name it, any time the task touches the Spiral Nexus app, "the IP marketplace", listings, subscriptions/tiers, messaging, or the database. Consult it before writing code so structure, naming, and security stay consistent across sessions.
---

# Spiral Nexus - Architecture & Conventions

This is the shared brain for the Spiral Nexus codebase. The point of having it is consistency: the project is built over many sessions, and without a single source of truth each session reinvents folder structure, naming, and - most dangerously - access-control patterns. Read this before writing code, and follow it unless the user explicitly overrides.

## What the product is

Spiral Nexus is a two-sided marketplace for **intellectual property assets** (trademarks first for the MVP; patents later). IP owners list assets to license or sell; buyers, investors, and licensees ("Brand Partners") discover them and make contact. There's an AI-matchmaking and social layer planned, but those are post-MVP.

The core value loop to protect above all else: **an owner lists an asset -> a buyer finds it -> the buyer contacts the owner.** When a change risks that loop, flag it.

## Stack (do not add to this without asking)

- **Next.js (App Router) + TypeScript** - front end and API (route handlers / server actions).
- **Tailwind CSS + shadcn/ui** - styling and components. Use shadcn primitives; don't hand-roll what shadcn already provides.
- **Supabase** - Postgres, Auth, Storage, and Row-Level Security (RLS). This is the backbone.
- **Stripe** - subscriptions and tier gating.
- **Vercel** - hosting and CI.
- **pgvector** (later) - embeddings for matchmaking, in the same Postgres. No separate vector infra.

The stack is deliberately boring and lean. Resist microservices, extra databases, ORMs that fight Supabase, or a native mobile project - the web app is responsive and covers desktop + mobile browsers. If a task seems to need something outside this list, surface the tradeoff to the user rather than silently adding a dependency.

## Repository structure

```
app/                # Next.js App Router
  (marketing)/      # public: home, about, subscriptions
  (app)/            # authenticated product surface
    listings/       # browse, detail, create/edit
    messages/       # 1:1 messaging
    dashboard/      # owner's listings + (later) analytics
  api/              # route handlers (webhooks, server-only ops)
components/         # shared UI (ui/ = shadcn, then feature components)
lib/                # supabase client, stripe client, helpers, types
  supabase/         # server + browser client factories
  tiers.ts          # tier definitions + capability checks (see below)
supabase/
  migrations/       # SQL migrations (source of truth for schema)
  seed/             # seed data for demos
```

Keep server-only code (service-role Supabase client, Stripe secret operations) out of anything that ships to the browser. Use the server Supabase client in route handlers / server components; the browser client only for user-scoped reads with RLS doing the enforcement.

## Data model

The canonical entities. Treat `ip_assets` as the heart of the schema.

- **profiles** - mirrors `auth.users`; `id`, `display_name`, `org_name`, `role_flags` (can be both buyer and seller), `subscription_tier`, `verified` (bool), `stripe_customer_id`.
- **ip_assets** - `id`, `owner_id`, `type` ('trademark' | 'patent'), `title`, `description`, `jurisdiction`, `registration_number`, `status`, `deal_type` ('license' | 'sale' | 'both'), `asking_price`, `source` ('user_submitted' | 'ip_office'), `images`, `is_published`, `created_at`. Type-specific fields are nullable (trademarks: Nice class, mark image; patents: IPC class, abstract/claims).
- **conversations / messages** - 1:1 DMs. Enforce per-tier weekly DM limits.
- **subscriptions** - `user_id`, `tier`, `status`, `period_end`, `stripe_subscription_id`.
- **matches** (later) - AI matchmaking output: `asset_id`, `user_id`, `score`, `reason`, `status`.
- **posts / feed_items** (later) - social feed.

Keep **user-submitted listings strictly separate from any imported IP-office records** (use the `source` column or a separate table). A registry record being present does not mean its owner wants to deal - never let a user claim ownership of an asset they didn't submit without verification.

## Tiers and access control - the part to get right

Four subscription tiers map to capabilities. Centralize this; never scatter tier checks as magic strings.

- **Entry (free):** browse listings.
- **Professional (99/mo):** list up to 5 assets, 5 DMs/week, enhanced search, verified badge, seller analytics.
- **Brand Partner (99/mo):** full listing access, license-only filtering, 5 DMs/week, verified badge.
- **Enterprise (249/mo):** unlimited listings, unlimited DMs, full matchmaking, analytics.

Define capabilities once in `lib/tiers.ts` (e.g. `maxListings`, `weeklyDmLimit`, `canSeeAnalytics`) and read from there everywhere. When you add a gated feature, add the capability to this file rather than hardcoding tier names in the feature.

**Security is enforced at the database, not just the UI.** Every table gets RLS policies; hiding a button is never the security boundary. The rules of thumb:

- A user can read/write only their own rows (`owner_id = auth.uid()`) unless the data is explicitly public (e.g. published listings are world-readable).
- Tier limits (listing caps, DM caps) are enforced server-side - in a route handler or a Postgres policy/trigger - never trusted from the client.
- Service-role keys never touch client code. Webhooks and privileged ops run server-side only.

When you write a migration that adds a table, you add its RLS policies in the same migration. A table without RLS is a bug.

## Secrets and config

All secrets live in environment variables: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (browser-safe), `SUPABASE_SERVICE_ROLE_KEY` (server only), `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`. Never hardcode a key, never log a secret, never expose the service-role key or Stripe secret to the browser. Keep a `.env.example` updated as new vars appear.

## How we build: vertical slices

Features ship as complete vertical slices (schema -> RLS -> API -> UI -> seed -> test), one workflow end-to-end, demoed before the next. Don't build a whole data layer with no usable feature. The `vertical-slice` skill describes the exact steps - use it when building a feature. The MVP slice order:

1. Skeleton (auth, empty dashboard, deploy).
2. Listings CRUD (trademark).
3. Discovery (browse, detail, search/filter).
4. Contact / 1:1 messaging.
5. Subscriptions (Stripe) gating list count and DM limits.

Matchmaking, IP-office ingestion, social feed, analytics, and verification automation are explicitly **post-MVP** - don't build them into the foundation.

## Working defaults

- TypeScript everywhere; share types from `lib/types.ts`, ideally generated from the Supabase schema.
- Validate input at the API boundary (e.g. Zod); don't trust client payloads.
- Commit per slice; keep PRs reviewable. Run a security review on anything touching RLS, auth, or payments.
- Write seed data so demos never look empty - a marketplace with no listings demos badly.
- When in doubt about scope, prefer the smallest thing that completes the core loop and ask the user before expanding.
