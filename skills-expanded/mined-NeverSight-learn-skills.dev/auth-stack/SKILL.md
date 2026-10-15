---
name: auth-stack
description: Auth + transactional email + asset storage on a Mongo stack, Better Auth (magic-link, hashed token at rest) on Prisma + MongoDB, AWS SES for delivery, AWS S3 + CloudFront for assets, zod-validated server env, and a single IAM-fallback contract for AWS clients. Use when touching sign-in/sign-up flows, the auth catch-all route, the `auth` config, session retrieval, magic-link emails, the `User`/`Session`/`Account`/`Verification` Prisma models, additional user fields (`role`, `preferredLocale`, etc.), SES email senders, S3 uploads, post-auth redirects, or extending the auth schema.
---

# Auth, email, and storage stack

The auth, transactional email, and asset storage layers are entangled by design: Better Auth sends magic-link emails through SES, the same SES client backs other transactional senders (invites, confirmations), and the same AWS credential strategy backs S3 uploads. One env schema, one credential contract, three SDK clients. Read the relevant topic file before editing.

> **Stack assumed.** Prisma + MongoDB (`relationMode = "prisma"`), Better Auth v1.5+, TanStack Start, AWS SES + S3 + CloudFront, Zod v4, TypeScript with `strict`. The schemas and patterns are **Mongo-specific**, adapt the Prisma decorators if you ever migrate to SQL.

> **Notation.** `<server>/lib/auth.ts`, `<server>/lib/prisma.ts`, `<server>/lib/email/`, `<server>/lib/storage/`, `<server>/lib/env.server.ts`, `<routes>/api/auth/$.ts` are placeholders for the project's actual paths and aliases. Resolve to whatever your project uses (`src/lib/...`, `app/server/...`, etc.). Helper names (`getAuthSession`, `requireAuthenticatedUser`, `sanitizePostAuthRedirectPath`, `getSesClient`, `getS3Client`, `getPublicAssetUrl`) are suggested conventions, rename to match your project's style.

> **Precedence.** These rules apply only where they don't contradict the project's own enforced rules, ESLint / Biome / Prettier configs, `tsconfig`, `CLAUDE.md` / `AGENTS.md`, contributing guides. Project rules win.

---

## Stack at a glance

| Concern        | Implementation                                                          | Topic                                            |
| -------------- | ----------------------------------------------------------------------- | ------------------------------------------------ |
| Auth core      | `better-auth` v1.5+ with `@better-auth/prisma-adapter`                  | [auth-config.md](auth-config.md)                 |
| Identity proof | `magicLink` plugin (15 min expiry, hashed token at rest)                | [auth-config.md](auth-config.md)                 |
| Cookies / SSR  | `tanstackStartCookies()` plugin                                         | [auth-config.md](auth-config.md)                 |
| Database       | MongoDB, Prisma `provider = "mongodb"`, `relationMode = "prisma"`       | [prisma-mongo.md](prisma-mongo.md)               |
| Catch-all API  | `<routes>/api/auth/$.ts` → `auth.handler(request)`                      | [session-and-routing.md](session-and-routing.md) |
| Sessions       | `auth.api.getSession({ headers })` inside a `createServerFn`            | [session-and-routing.md](session-and-routing.md) |
| Email          | `@aws-sdk/client-ses` v3, `SendEmailCommand`, locale-aware blocks       | [email-ses.md](email-ses.md)                     |
| Asset storage  | `@aws-sdk/client-s3` v3 + CloudFront base URL                           | [storage-s3.md](storage-s3.md)                   |
| Env validation | Zod v4 schema in `<server>/lib/env.server.ts`                           | [auth-config.md](auth-config.md)                 |

For the **content / i18n** layer that consumes `requireAuthenticatedUser` and additional user fields like `preferredLocale`, see the companion `content-stack` skill.

---

## Core principles

These are the **twelve rules that span more than one topic file**. Topic-specific rules live in their respective files; this list is the cross-cutting contract.

### 1. One singleton per SDK; AWS clients are factories with shared IAM fallback

`auth` is a module-level singleton in `<server>/lib/auth.ts`. `prisma` is a module-level singleton in `<server>/lib/prisma.ts`. `getSesClient()` and `getS3Client()` are **factories**, not singletons, they construct a fresh SDK client per call so the IAM-fallback decision stays visible at every call site. **Never** instantiate any of these elsewhere, duplicates leak connections (Prisma) or bypass the credential contract (AWS SDKs).

### 2. AWS credentials are optional; the IAM credential chain is the production path

`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` are **optional** in the Zod env schema. When unset, the SDK reads from the default provider chain (the IAM role attached to the production instance). Both `getSesClient()` and `getS3Client()` apply this fallback identically. **Match this pattern when adding any other AWS SDK client**, credentials must always be optional, the factory must use `undefined` when both are missing.

### 3. Magic-link tokens are hashed at rest

`storeToken: "hashed"` means the DB stores `sha256(token)`, not the token itself. The raw token only exists in the email URL. Don't try to introspect, replay, or display tokens, they're verified by completing the round-trip. The 15-minute (`60 * 15`) expiry is intentional; do not loosen below ~5 minutes (real users hit inbox delays) or extend past ~30 minutes (replay window).

### 4. Mongo `ObjectId` comes from Prisma, not Better Auth

`advanced.database.generateId: false` is the contract. Every model uses `@id @default(auto()) @map("_id") @db.ObjectId`. **Never** call `crypto.randomUUID()` or pass an `id` into a `prisma.<model>.create()` call. See [prisma-mongo.md](prisma-mongo.md) for the canonical decorator shape.

### 5. Additional user fields land on `session.user` as `unknown`

Fields declared in `auth.user.additionalFields` (e.g. `role`, `preferredLocale`) are mirrored in the `User` Prisma model and seeded in `databaseHooks.user.create.before`. On the way out, **always** narrow with a type predicate (`isRole`, `isSupportedLocale`); never `as`-cast, Better Auth's types are deliberately `unknown` because the adapter doesn't validate them at the boundary. See [session-and-routing.md](session-and-routing.md).

### 6. The catch-all is the only authorized entry to Better Auth's HTTP API

`<routes>/api/auth/$.ts` forwards both GET and POST to `auth.handler(request)`. The magic-link flow specifically POSTs to `/api/auth/sign-in/magic-link` with `{ email, callbackURL }` and `credentials: "include"`. **Never** call any auth subpath without `credentials: "include"`, the cookie won't set.

### 7. `callbackURL` MUST go through `sanitizePostAuthRedirectPath()`

Raw `?redirect=` is an open-redirect vector. The sanitizer rejects protocol-relative URLs (`//evil.com`), self-loops back to `/auth/*` or `/api/auth/*`, and strips `error` query params. The default fallback is a known-safe authenticated landing path (`/dashboard`, `/app`, etc., pick one and stick to it). See [session-and-routing.md](session-and-routing.md).

### 8. Mutating server fns gate with `requireAuthenticatedUser`; UI snapshots use `getAuthSession`

`getAuthSession` is the snapshot used by loaders and route components, it returns `{ isAuthenticated, user: null }` when there's no session, never throws. `requireAuthenticatedUser` is the gate for `createServerFn` handlers that mutate, it throws `Unauthorized` on a missing session. **Never** call `auth.api.getSession()` directly inside a feature module, duplicating the lookup splits the contract and skips the additional-field narrowing.

### 9. Transactional and marketing email travel on different FROM addresses

`SES_FROM_EMAIL` is for magic links, invites, and confirmations. `SES_MARKETING_FROM_EMAIL` is for newsletter / bulk sends. Subdomains should differ (e.g. `notify.<host>` vs `news.<host>`) so the marketing list's spam-complaint rate doesn't tank transactional deliverability. Mixing them risks users not getting sign-in links during a bad campaign.

### 10. S3 keys are content-addressed; URLs go through CloudFront

The default cache header is `public, max-age=31536000, immutable`. This is only safe because keys change when content changes (use a hash, version, or fresh ULID). Always render URLs through `getPublicAssetUrl(key)`. **Never** expose raw `s3://` URIs or pre-signed S3 URLs to clients, the bucket is private; CloudFront fronts it via OAC. See [storage-s3.md](storage-s3.md).

### 11. `serverEnv` is the only env reader

Every file imports `serverEnv` from `<server>/lib/env.server`. **Never** reach into `process.env` outside that file, it skips Zod validation, breaks test stubs, and bypasses the test-mode bypass. See [auth-config.md](auth-config.md) for the schema and the test-mode pattern.

### 12. Never read `.env` / `.env.local` from agent tools

They contain live secrets. Read `.env.example` and `<server>/lib/env.server.ts` to learn the shape; ask the user for live values.

---

## Workflow checklist

Before merging changes that touch this stack:

- [ ] `serverEnv` schema updated if any new env var is read
- [ ] `.env.example` updated to match (no real secret values committed)
- [ ] New `User` field declared in **both** Prisma schema and `auth.user.additionalFields`
- [ ] New `User` field default mirrored in `databaseHooks.user.create.before` if `@default` won't fire
- [ ] Mongo schema changes pushed and client regenerated (`prisma db push && prisma generate`)
- [ ] `session.user.<newField>` narrowed via predicate in `getAuthSession` (no `as`-casts)
- [ ] New AWS SDK client uses the same optional-credential pattern (IAM fallback)
- [ ] New transactional email uses `SES_FROM_EMAIL` and the renderer / block primitives
- [ ] New marketing email uses `SES_MARKETING_FROM_EMAIL` (with fallback for dev)
- [ ] Any client-facing `redirect=` is run through `sanitizePostAuthRedirectPath`
- [ ] Server fns that mutate gate with `requireAuthenticatedUser` (or stronger)
- [ ] Server fns return narrow `select`-shaped results, not whole rows
- [ ] No `as` casts on `session.user.*`, no `process.env.X` outside `env.server.ts`, no `.env` reads from agent tools
- [ ] Lint, typecheck, and tests clean

---

## Reference files

- [auth-config.md](auth-config.md), `betterAuth()` instance, plugins, additional fields, env schema, hard rules around `generateId`, `storeToken`, and trusted origins.
- [prisma-mongo.md](prisma-mongo.md), Mongo + Prisma model shapes for `User` / `Session` / `Account` / `Verification`, `ObjectId` decorator pattern, `relationMode`, indexes, `db push` workflow.
- [session-and-routing.md](session-and-routing.md), auth catch-all route, `getAuthSession`, `requireAuthenticatedUser`, `sanitizePostAuthRedirectPath`, sign-in / sign-up POST shape, email-exists branching, type-narrowing additional fields.
- [email-ses.md](email-ses.md), `SESClient` setup with IAM fallback, `SendEmailCommand`, block-based email composition, locale-aware copy, transactional vs marketing FROM, adding a new sender.
- [storage-s3.md](storage-s3.md), `S3Client` setup with IAM fallback, `PutObjectCommand`, CloudFront URL builder, key encoding, immutable cache header, key conventions.
