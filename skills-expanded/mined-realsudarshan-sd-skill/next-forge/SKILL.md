---
name: next-forge
description: 'next-forge expert guidance â€” production-grade Turborepo monorepo SaaS starter by Vercel. Use when working in a next-forge project, scaffolding with `npx next-forge init`, or editing @repo/* workspace packages.'
metadata:
  priority: 6
  docs:
    - "https://next-forge.com/docs"
    - "https://github.com/haydenbleasel/next-forge"
  pathPatterns:
    - 'pnpm-workspace.yaml'
    - 'apps/app/**'
    - 'apps/web/**'
    - 'apps/api/**'
    - 'apps/email/**'
    - 'apps/docs/**'
    - 'apps/studio/**'
    - 'apps/storybook/**'
    - 'packages/auth/**'
    - 'packages/database/**'
    - 'packages/design-system/**'
    - 'packages/payments/**'
    - 'packages/email/**'
    - 'packages/analytics/**'
    - 'packages/observability/**'
    - 'packages/security/**'
    - 'packages/ai/**'
    - 'packages/cms/**'
    - 'packages/collaboration/**'
    - 'packages/feature-flags/**'
    - 'packages/internationalization/**'
    - 'packages/notifications/**'
    - 'packages/rate-limit/**'
    - 'packages/seo/**'
    - 'packages/storage/**'
    - 'packages/webhooks/**'
    - 'packages/next-config/**'
    - 'packages/typescript-config/**'
    - '**/keys.ts'
    - '**/env.ts'
    - '**/proxy.ts'
    - 'biome.jsonc'
  bashPatterns:
    - '\bnext-forge\b'
    - '\bnpx\s+next-forge\b'
    - '\bpnpm\s+migrate\b'
    - '\bpnpm\s+bump-deps\b'
    - '\bpnpm\s+bump-ui\b'
    - '\bprisma\s+(generate|db\s+push|format|studio)\b'
    - '\bstripe\s+listen\b'
    - '\bnpx\s+shadcn@latest\s+add\b.*-c\s+packages/design-system\b'
  importPatterns:
    - '@repo/auth'
    - '@repo/database'
    - '@repo/design-system'
    - '@repo/payments'
    - '@repo/email'
    - '@repo/analytics'
    - '@repo/observability'
    - '@repo/security'
    - '@repo/ai'
    - '@repo/cms'
    - '@repo/collaboration'
    - '@repo/feature-flags'
    - '@repo/internationalization'
    - '@repo/notifications'
    - '@repo/rate-limit'
    - '@repo/seo'
    - '@repo/storage'
    - '@repo/webhooks'
    - '@repo/next-config'
    - '@t3-oss/env-nextjs'
    - '@rescale/nemo'
  promptSignals:
    phrases:
      - 'next-forge'
      - 'next forge'
      - '@repo/'
    allOf:
      -
        - 'monorepo'
        - 'saas'
        - 'starter'
      -
        - 'turborepo'
        - 'clerk'
        - 'stripe'
    anyOf:
      - 'saas starter'
      - 'production monorepo'
      - 'keys.ts'
      - 'pnpm-workspace'
    noneOf:
      - 'create-t3-app'
    minScore: 6
---

# next-forge

You are an expert in next-forge v5 â€” a production-grade Turborepo monorepo starter for SaaS applications, created by Vercel. It wires together 20+ packages (auth, database, payments, email, analytics, observability, security, AI, and more) into a cohesive, deploy-ready monorepo.

## Monorepo Structure

```
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ app/          # Main SaaS app (port 3000) â€” Clerk auth, route groups
â”‚   â”œâ”€â”€ web/          # Marketing site (port 3001) â€” blog, pricing, i18n
â”‚   â”œâ”€â”€ api/          # API server (port 3002) â€” webhooks, cron jobs
â”‚   â”œâ”€â”€ email/        # React Email preview (port 3003)
â”‚   â”œâ”€â”€ docs/         # Mintlify docs
â”‚   â”œâ”€â”€ studio/       # Prisma Studio
â”‚   â””â”€â”€ storybook/    # Component dev (port 6006)
â”œâ”€â”€ packages/
â”‚   â”œâ”€â”€ ai/               # @repo/ai â€” AI SDK + OpenAI
â”‚   â”œâ”€â”€ analytics/        # @repo/analytics â€” PostHog + GA + Vercel Analytics
â”‚   â”œâ”€â”€ auth/             # @repo/auth â€” Clerk
â”‚   â”œâ”€â”€ cms/              # @repo/cms â€” BaseHub
â”‚   â”œâ”€â”€ collaboration/    # @repo/collaboration â€” Liveblocks
â”‚   â”œâ”€â”€ database/         # @repo/database â€” Prisma + Neon
â”‚   â”œâ”€â”€ design-system/    # @repo/design-system â€” shadcn/ui + Geist
â”‚   â”œâ”€â”€ email/            # @repo/email â€” Resend + React Email
â”‚   â”œâ”€â”€ feature-flags/    # @repo/feature-flags â€” Vercel Flags SDK
â”‚   â”œâ”€â”€ internationalization/ # @repo/internationalization â€” next-international
â”‚   â”œâ”€â”€ next-config/      # @repo/next-config â€” shared Next.js config
â”‚   â”œâ”€â”€ notifications/    # @repo/notifications â€” Knock
â”‚   â”œâ”€â”€ observability/    # @repo/observability â€” Sentry + BetterStack
â”‚   â”œâ”€â”€ payments/         # @repo/payments â€” Stripe
â”‚   â”œâ”€â”€ rate-limit/       # @repo/rate-limit â€” Upstash Redis
â”‚   â”œâ”€â”€ security/         # @repo/security â€” Arcjet + Nosecone
â”‚   â”œâ”€â”€ seo/              # @repo/seo â€” metadata + JSON-LD
â”‚   â”œâ”€â”€ storage/          # @repo/storage â€” Vercel Blob
â”‚   â”œâ”€â”€ typescript-config/ # @repo/typescript-config
â”‚   â””â”€â”€ webhooks/         # @repo/webhooks â€” Svix
â”œâ”€â”€ turbo.json
â”œâ”€â”€ pnpm-workspace.yaml
â””â”€â”€ biome.jsonc           # Biome via ultracite
```

**Key principle**: Packages are self-contained â€” they do not depend on each other. Apps compose packages.

## Getting Started

```bash
npx next-forge@latest init     # Scaffold project (interactive)
# Post-install:
pnpm migrate                   # prisma format + generate + db push
pnpm dev                       # Start all apps via turbo
```

**Minimum env vars to run locally**: `DATABASE_URL` + Clerk keys + app URLs. Everything else is optional.

## Workspace Imports (@repo/*)

All packages use `@repo/*` workspace protocol with specific subpath exports:

```ts
// Auth
import { auth } from "@repo/auth/server";
import { ClerkProvider } from "@repo/auth/provider";
import { currentUser } from "@repo/auth/server";

// Database
import { database } from "@repo/database";

// Design System
import { Button } from "@repo/design-system/components/ui/button";
import { DesignSystemProvider } from "@repo/design-system";
import { fonts } from "@repo/design-system/lib/fonts";

// Payments
import { stripe } from "@repo/payments";

// Email
import { resend } from "@repo/email";

// Observability
import { log } from "@repo/observability/log";
import { captureException } from "@repo/observability/error";

// Analytics
import { AnalyticsProvider } from "@repo/analytics/provider";

// Security
import { secure } from "@repo/security";

// Feature Flags
import { createFlag } from "@repo/feature-flags";

// SEO
import { createMetadata } from "@repo/seo/metadata";
import { JsonLd } from "@repo/seo/json-ld";

// Storage
import { put } from "@repo/storage";

// AI
import { models } from "@repo/ai/lib/models";
```

## Environment Variables

### Type-safe env validation

Every package has a `keys.ts` using `@t3-oss/env-nextjs` + Zod. Apps compose them in `env.ts`:

```ts
// apps/app/env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { auth } from "@repo/auth/keys";
import { database } from "@repo/database/keys";
import { payments } from "@repo/payments/keys";
export const env = createEnv({ extends: [auth(), database(), payments()] });
```

### Env file locations

| File | Purpose |
|------|---------|
| `apps/app/.env.local` | Main app env vars |
| `apps/web/.env.local` | Marketing site |
| `apps/api/.env.local` | API server |
| `packages/database/.env` | `DATABASE_URL` |

### Required env vars (minimum)

| Var | Package | Required for |
|-----|---------|-------------|
| `DATABASE_URL` | database | Any database access |
| `CLERK_SECRET_KEY` | auth | Authentication |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | auth | Client-side auth |
| `NEXT_PUBLIC_APP_URL` | â€” | Cross-app linking |
| `NEXT_PUBLIC_WEB_URL` | â€” | Cross-app linking |
| `NEXT_PUBLIC_API_URL` | â€” | Cross-app linking |

### Optional service env vars

| Service | Vars |
|---------|------|
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` |
| Resend | `RESEND_TOKEN`, `RESEND_FROM` |
| PostHog | `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST` |
| Sentry | `NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_ORG`, `SENTRY_PROJECT` |
| BetterStack | `BETTERSTACK_API_KEY`, `BETTERSTACK_URL` |
| BaseHub | `BASEHUB_TOKEN` |
| Arcjet | `ARCJET_KEY` |
| Liveblocks | `LIVEBLOCKS_SECRET` |
| Knock | `KNOCK_SECRET_API_KEY`, `NEXT_PUBLIC_KNOCK_API_KEY` |
| Upstash | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| Vercel Blob | `BLOB_READ_WRITE_TOKEN` |
| Svix | `SVIX_TOKEN` |
| OpenAI | `OPENAI_API_KEY` |
| Feature Flags | `FLAGS_SECRET` |

## Middleware / Proxy Pattern

next-forge uses `proxy.ts` (Next.js 16+), NOT `middleware.ts`:

```ts
// apps/app/proxy.ts â€” Clerk auth + Nosecone security
import { clerkMiddleware } from "@clerk/nextjs/server";
import { createMiddleware as createNosecone } from "@nosecone/next";
export default clerkMiddleware(createNosecone());
```

```ts
// apps/web/proxy.ts â€” Clerk + i18n + Arcjet + Nosecone, composed with nemo
import { compose } from "@rescale/nemo";
export default compose([clerkMiddleware, i18nMiddleware, arcjetMiddleware, noseconeMiddleware]);
```

## Database (Prisma + Neon)

- Schema: `packages/database/prisma/schema.prisma`
- Client: `import { database } from "@repo/database"`
- Config: `packages/database/prisma.config.ts` (Neon adapter)
- Commands: `pnpm migrate` (format + generate + db push)
- Studio: `apps/studio` (Prisma Studio)

## Key Commands

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Start all apps |
| `pnpm dev --filter app` | Start single app |
| `pnpm build` | Build all |
| `pnpm migrate` | Prisma format + generate + db push |
| `pnpm bump-deps` | Update all dependencies |
| `pnpm bump-ui` | Update shadcn/ui components |
| `pnpm run boundaries` | Check Turborepo boundaries |
| `npx next-forge@latest update` | Update next-forge (diff-based) |
| `npx shadcn@latest add <comp> -c packages/design-system` | Add UI component |
| `stripe listen --forward-to localhost:3002/webhooks/payments` | Local Stripe webhooks |

## Deployment to Vercel

Deploy as **3 separate Vercel projects** (app, api, web), each with Root Directory set to `apps/<name>`:

1. Create project â†’ set Root Directory to `apps/app`
2. Add environment variables (use Team Environment Variables to avoid duplication)
3. Repeat for `apps/api` and `apps/web`

Recommended subdomains: `app.yourdomain.com`, `api.yourdomain.com`, `www.yourdomain.com`

## API App Patterns

```
apps/api/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ cron/           # Cron jobs (GET handlers)
â”‚   â”‚   â””â”€â”€ keep-alive/route.ts
â”‚   â”œâ”€â”€ webhooks/       # Inbound webhooks
â”‚   â”‚   â”œâ”€â”€ auth/route.ts      # Clerk webhooks
â”‚   â”‚   â””â”€â”€ payments/route.ts  # Stripe webhooks
â”‚   â””â”€â”€ health/route.ts
â””â”€â”€ vercel.json         # Cron schedules
```

## Design System

- shadcn/ui (New York style, neutral palette)
- Geist Sans + Geist Mono fonts
- Tailwind CSS v4 + tw-animate-css
- Components at `packages/design-system/components/ui/`
- Add components: `npx shadcn@latest add <name> -c packages/design-system`

## Common Gotchas

1. **Env vars are validated at build time** â€” optional services still require env vars if the package is imported. Remove the import or provide a value.
2. **Multiple .env file locations** â€” each app and the database package have separate env files. There is no single root `.env`.
3. **`pnpm migrate` before first run** â€” without this, you get "table does not exist" errors.
4. **Clerk webhooks cannot be tested locally** â€” need a staging deployment.
5. **Heavy middleware imports** â†’ edge function >1MB on Vercel. Keep proxy.ts imports light.
6. **Prisma v7**: use `--config` not `--schema` for `prisma studio`.
7. **next-forge is a boilerplate, not a library** â€” updates via `npx next-forge update` need manual merge with your changes.
8. **`turbo.json` globalEnv** â€” when adding new env vars used at build time, declare them in `turbo.json` `globalEnv` or they won't invalidate cache.

## Removing Optional Services

To remove an unused service (e.g., Stripe, BaseHub, Liveblocks):
1. Delete the package directory (`packages/<service>/`)
2. Remove all `@repo/<service>` imports from apps
3. Remove the `keys()` call from each app's `env.ts`
4. Remove the workspace entry from `pnpm-workspace.yaml` if needed
5. Run `pnpm install` to clean lockfile

## Migration Alternatives

| Category | Default | Alternatives |
|----------|---------|-------------|
| Auth | Clerk | Auth.js, Better Auth, Supabase Auth |
| Database | Prisma + Neon | Drizzle, Supabase, PlanetScale, Turso |
| Payments | Stripe | Lemon Squeezy, Paddle |
| CMS | BaseHub | Content Collections |
| Docs | Mintlify | Fumadocs |
| Feature Flags | Vercel Flags | Hypertune |
| Storage | Vercel Blob | UploadThing |
| Formatting | Biome | ESLint |

## Cross-references

=> skill: turborepo â€” Monorepo configuration, caching, remote cache
=> skill: auth â€” Clerk setup, middleware patterns, sign-in/up flows
=> skill: payments â€” Stripe integration, webhooks, pricing
=> skill: email â€” Resend + React Email templates
=> skill: shadcn â€” shadcn/ui components, theming, CLI
=> skill: observability â€” Sentry + logging setup
=> skill: vercel-storage â€” Blob, Neon, Upstash
=> skill: vercel-flags â€” Feature flags with Vercel Flags SDK
=> skill: ai-sdk â€” AI SDK integration
=> skill: bootstrap â€” Project bootstrapping flow

## Official Documentation

- https://docs.next-forge.com
- https://github.com/vercel/next-forge
