# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pnpm install
pnpm db:up                              # Postgres 16 via docker compose (POSTGRES_PORT, default 5432)
cp .env.example .env                    # set AI_PROVIDER=mock to run with no API key
pnpm prisma:generate && pnpm prisma:deploy   # or prisma:migrate to author a new one
pnpm --filter @dukkanify/core build     # REQUIRED before running either app (see below)
pnpm dev                                # web :3000 + api :4000 in parallel
```

`pnpm verify` is the whole gate — core build → lint → format:check → typecheck → test. It is what
the `pre-push` hook and CI both run; if it passes locally, CI will pass. Run it before proposing
a change is finished.

Other scripts: `pnpm dev:web` / `pnpm dev:api`, `pnpm build`, `pnpm lint`, `pnpm lint:fix`,
`pnpm format`, `pnpm db:down`, `pnpm prisma:seed` (demo user "Abdullah").

### Tests

```bash
pnpm test                                                # everything (102 core + 237 API + 89 web)
pnpm --filter @dukkanify/core test                       # the contract tests
pnpm --filter @dukkanify/api test                        # pipeline, isolation, errors, config
pnpm --filter @dukkanify/web test                        # mapper, history stack, API error contract
pnpm --filter @dukkanify/core exec vitest run -t "rejects negative"   # single test by name
pnpm --filter @dukkanify/core exec vitest                # watch mode
```

API tests construct services directly (`new AiGenerationService(provider, prompts, metrics, images)`)
rather than through `Test.createTestingModule`. That is deliberate: no DI container, no database,
no provider, so the suite is fast and tests logic instead of wiring. **The wiring is covered by
CI**, which boots the built artefact against a real Postgres and probes `/health`. Prefer adding
to the unit suites; reach for `@nestjs/testing` only when the thing under test _is_ the wiring.

`apps/api/vitest.config.ts` injects a valid-shaped `DATABASE_URL` and `JWT_SECRET`. Nothing
connects to them — but `env()` validates at import time, so the shape has to parse.

Suites that construct `AiGenerationService` pass a stub for `ImageSearchService` (a
`findForProducts` that returns nulls). Let a suite reach the real one and it will call Openverse
over the network — slow, flaky, and rude to a free service.

### Git hooks (husky)

| Hook         | Runs                                                      | Why there                                                      |
| ------------ | --------------------------------------------------------- | -------------------------------------------------------------- |
| `pre-commit` | `lint-staged` (eslint --fix + prettier), then `pnpm lint` | Every commit is lint-clean. ~2s for the full pass              |
| `commit-msg` | `commitlint`                                              | Conventional Commits with a closed scope list                  |
| `pre-push`   | core build → typecheck → test → `pnpm build`              | Nothing reaches the remote that won't compile, pass, or deploy |

`pre-commit` runs two lint passes because they catch different things. `lint-staged` fixes the
staged files in place; the workspace-wide `pnpm lint` then catches breakage in files you did not
touch — a removed export, a renamed symbol another module still imports.

`pre-push` ends with the full production build, so a green hook means a green Vercel deploy rather
than a hopeful one. It takes about 20 seconds from a clean tree.

Commit format: `type(scope): subject`. Scopes are enumerated in `commitlint.config.mjs`
(`core`, `api`, `web`, `db`, `auth`, `ai`, `store`, `editor`, `ci`, `deps`) — adding a new one
means editing that file, which is the point.

## Build-order gotchas

- `@dukkanify/core` resolves through `main: ./dist/index.js`, not source. Both apps break with
  unresolved-import errors until `pnpm --filter @dukkanify/core build` has run. When editing the
  contract during development, run `pnpm --filter @dukkanify/core dev` (tsc watch) alongside `pnpm dev`.
- The Prisma schema lives at `apps/api/prisma/schema.prisma`, alongside `seed.ts`. The root
  `prisma:*` scripts delegate to the API package with `dotenv -e ../../.env`.
- All three packages extend `tsconfig.base.json`, which is strict _and_ enables
  `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`. Array indexing needs a
  non-null assertion or a guard.
- **Do not import `express` directly in `apps/api`.** It is a transitive dependency of
  `@nestjs/platform-express`, so it resolves in development and then fails at runtime from the
  built output under pnpm's strict `node_modules`. Use the adapter API (`app.useBodyParser(…)`).
  This was a real production-build-only crash; CI's boot step exists to catch its kind.

## Architecture

**The one decision everything rests on: the LLM emits validated _data_, never code or markup.**

```
prompt → AiProvider → extract JSON → Zod validate → [1 repair pass] → normalise → Prisma txn
                                                                          ↓
                                              StoreRenderer (section registry) → UI
```

### `packages/core` is the contract

`StoreDefinitionSchema` (`packages/core/src/schema.ts`) is imported by the API validator, the
prompt builder, the HTTP DTOs, and the React renderer — one source of truth, no drift. It encodes
domain rules as `superRefine` checks:

- 8–30 products (the prompt asks for exactly 8; the schema leaves room);
- exactly one home / about / contact page, and home must contain a hero + products section;
- `direction` must match `directionForLocale(locale)` — derived from the **language**, so `ar-SA`
  and `ur-PK` are RTL too. It used to compare against `ar-AE`, which meant the schema demanded a
  Saudi store be left-to-right while generation set it right-to-left;
- a categories section lists 3–24 categories and **may not name one no product belongs to**. A
  dead link is a nav entry to an empty shelf, and the model produced them despite being asked not
  to, so it is a constraint rather than a request.

Also in core: `cultural.ts` (locales, currencies, `directionForLocale`, `currencyForLocale`, and
the `CULTURAL_CATEGORIES` vocabulary — a _hint_ for Arab-market stores, not a checklist),
`store-categories.ts` (the ten fixed platform categories), `localized.ts`, and `money.ts`
(**all prices are integer minor units / fils** — 79.00 AED = 7900).

**Platform category ≠ store category.** `STORE_CATEGORY_IDS` is a closed tuple of ten trades the
merchant picks from; the categories _inside_ a generated store are the model's, per store. A
perfume house and a Korean skincare brand are both `beauty` and share no catalogue. Collapsing
the two layers turns a store builder into a template picker.

Changing the schema has four downstream effects, all automatic: the prompt's JSON schema
(`PromptService` derives it from the same Zod object via `zod-to-json-schema`), the DTO validation,
the persistence mapping, and the renderer's types.

### Adding a section type (the canonical extension)

1. Add the variant to the `SectionSchema` discriminated union in `packages/core/src/schema.ts`.
2. Whitelist/describe it in `PromptService.buildSystemPrompt` if the AI should generate it.
3. Add one row to `SECTION_REGISTRY` in `apps/web/components/storefront/StoreRenderer.tsx`.

No other rendering code changes; the registry is `Record<SectionType, Component>` so a missing
entry is a type error.

### API (`apps/api`, NestJS 10)

Feature modules: `auth`, `ai`, `stores`, `health`.
Cross-cutting: `common/config`, `common/errors`, `common/observability`, `common/throttling`,
`common/prisma`.

Cross-cutting concerns are registered as `APP_*` providers in `app.module.ts`, not in `main.ts`,
so they participate in DI and are present in testing modules too.

- `AiController` is mounted at the **root** (`@Controller()`), so the real paths are
  `POST /generate` and `POST /generate/stream` — _not_ `/ai/generate`.
- The AI provider is chosen at wire-up in `ai.module.ts` from `AI_PROVIDER` env
  (`anthropic` | `openai` | `gemini` | anything else → `MockProvider`), with
  `AI_FALLBACK_PROVIDER` chaining a second. Everything depends on the `AiProvider` interface
  behind the `AI_PROVIDER` symbol token, never on a vendor SDK. `MockProvider` returns a
  deterministic valid store through the identical validation + persistence path — use it for
  offline dev, CI and demos.
- `AiGenerationService.generate` gets exactly **one** repair attempt (re-prompting with the
  concrete Zod issues) and then throws. Never persist a store that failed validation. The
  one-attempt bound is asserted by test: an unbounded repair loop is an unbounded bill.
- **`locale` and `currency` on `GenerationInput` are optional, and absent means "infer".** They
  used to default to en-AE/AED and then overwrite whatever the model returned, so a London coffee
  brand came back priced in dirhams. Present means the merchant chose, and the choice wins.
- **The model may not supply `product.imageUrl`.** Asked for one it invents
  `via.placeholder.com` URLs, which pass the contract's URL check and then block the real lookup.
  `normalise` strips the field; `ImageSearchService` owns it.
- `ImageSearchService` (`ai/images/`) finds real photographs at generation time from Openverse —
  time-boxed, cached, one query per category, deduped across the page, denylisted, and unable to
  fail a generation. Search context must be a _word_ (the trade), never the store description: a
  sentence-long query matched nothing for every trade.
- SSE streams coarse milestones (`theme_generated`, …), not raw tokens — the client only ever
  renders the final validated object. `generateStream` converts **every** failure into a terminal
  `generation_failed` event; a stream that ends without one leaves the client spinner running.
- Authorization is always derived from `@CurrentUser().id` (re-loaded from the DB in
  `JwtStrategy.validate`), never from a client-supplied id. Keep ownership checks in
  `StoresService`, not the controller.
- `StoresRepository.save` wraps slug de-duplication, wholesale replacement of products/pages/
  sections, and an append-only `StoreVersion` snapshot in a single transaction.

#### Errors: services throw domain errors, the filter maps them to HTTP

Services throw `AppError` subclasses (`common/errors/app-error.ts`) — framework-free, carrying a
`kind`, a `publicMessage` safe to show a user, and a `context` object that is **logged and never
serialised**. `AllExceptionsFilter` is the single place a thrown value becomes a status code.

When adding a failure mode, add an `AppErrorKind` rather than throwing `HttpException` from a
service. That keeps business logic transport-agnostic and keeps the API from answering 500 for
something it understands. Unrecognised throws become a flat 500 with a generic message.

Ownership failures answer **404, never 403** — a 403 confirms the id exists, which is an
enumeration oracle. See `stores/stores.errors.ts`.

#### Configuration

`common/config/env.ts` parses `process.env` once through a Zod schema. `env()` is memoised;
read configuration through it rather than touching `process.env`. Production-only `superRefine`
rules refuse to boot on a placeholder `JWT_SECRET`, `ENABLE_DEV_LOGIN=true`, `SameSite=None`
without `Secure`, or `AI_PROVIDER=anthropic` without a key.

Note the ordering quirk: Zod runs `superRefine` only after the object parse succeeds, so a missing
`DATABASE_URL` masks the production checks until it is fixed.

#### Rate limiting & observability

- `UserThrottlerGuard` is global. It keys on the authenticated user, falling back to IP. Because
  global guards run **before** route guards, `req.user` is unset — the guard verifies the session
  cookie itself. `/generate` tightens the budget with `@Throttle`; `/health` opts out.
- `RequestIdMiddleware` → `LoggingMiddleware` run in that order on every route. Logging is
  middleware, not an interceptor, precisely because guards run before interceptors: an interceptor
  never sees a 401 or a 429, which are the requests you most want on a dashboard.
- `MetricsService` is a small in-process registry (counters + p50/p95), exposed at
  `/health/metrics`. Per-instance and reset on restart — correct for one node, explicitly wrong
  at horizontal scale. Same caveat applies to the throttler's in-memory storage.

### Web (`apps/web`, Next.js 15 App Router)

- `StoreRenderer` is used by **both** the builder's live preview and the public storefront —
  builder state is a `StoreDefinition` in memory; the public page fetches the relational payload
  and maps it back through `lib/mapStore.ts`.
- Editing is an immutable update of the `StoreDefinition`, routed through `useHistory`
  (past/present/future stacks) — that's what gives instant preview plus undo/redo with no
  AI round-trip and no DOM surgery.
- `lib/api.ts` is the only place that talks to the API. Every failure becomes an `ApiError`
  carrying `status`, `code` and `requestId`; network failures are caught so the UI never sees a
  raw `TypeError: Failed to fetch`. Add new endpoints here, not inline in components.
- **RTL:** `StoreRenderer` sets real `dir` and `lang` attributes from the store's own data, so an
  Arabic storefront renders right-to-left inside the left-to-right dashboard shell. Layout uses
  flexbox and logical spacing, so nothing needs mirroring by hand. Do not add `left-`/`right-`
  offsets to storefront components.
- Tailwind brand colors `sand` / `oud` / `gold` sit alongside the shadcn/ui CSS-variable tokens.
  Storefront section colors come from the store's own `theme.palette` via inline styles, not
  Tailwind classes — the palette is per-store data.
- `dangerouslySetInnerHTML` is never used, and must not be. Generated and merchant-edited copy is
  untrusted text; React's escaping is what makes an `<script>` payload in a product name inert.
- **Interface language is not store language.** `lib/i18n/` holds the shell's dictionary; a
  storefront carries its own language in its own data and is never translated there. An Arabic
  store inside an English dashboard is correct.
- The UI locale lives in a cookie, read on the server in `app/layout.tsx`, and sets `lang`/`dir`
  on `<html>`. It must stay server-resolved: doing it on the client paints an English page and
  then reverses the whole layout in front of the user.
- Key parity between `en` and `ar` is a **compile error** — `ar` is typed
  `Record<TranslationKey, string>`. The spec covers what types cannot: nothing blank, and Arabic
  that is not silently a copy of the English string.
- The switcher is the one surface allowed to show both languages, because naming the choice is its
  job. Everywhere else renders exactly one. Never label a language with a flag alone — a flag
  names a country, and Arabic is not the UAE.
- Builder chrome: `BuilderTopBar` (back, breadcrumb, undo/redo, save, publish, language) and
  `PreviewFrame` (page tabs, viewport toggle). Lifecycle actions belong to the document and stay
  above it; the left panel is for editing only.
- Product imagery degrades through a chain — the product's own `imageUrl`, then the curated
  `photo-catalogue.ts` entry for its subject, then a deterministic gradient. `subjectFor` matches
  Arabic as well as English; it used to strip non-`[a-z]` characters, so every product on an
  Arabic storefront fell through to a gradient.

### Persistence

Core entities are relational (`User → Store → Page → Section`, `Product`, `StoreVersion`); only
`Section.content` and `StoreVersion.snapshot` are JSONB, and their shape is Zod-validated before
write. See `apps/api/prisma/schema.prisma` header comments and `docs/decisions.md`.

## CI

`.github/workflows/ci.yml` — two jobs: `quality` (lint, format, typecheck, test) and `build`
(Prisma `migrate deploy` against an empty Postgres, seed, production build, then **boot the built
API and poll `/health`**). `.github/workflows/pr-hygiene.yml` — commitlint over the PR's commits,
gitleaks over full history, plus an assertion that `.env` is untracked.

CI runs with `AI_PROVIDER=mock`, so it never needs a key and never spends tokens.

## Known gaps

Kept current deliberately — `docs/qa-checklist.md` §12 is the authoritative, fuller list, and
`docs/next-phases.md` is the sequenced plan for closing them.

- Realtime is a single-process `EventEmitter`, so a second tab only follows along when both are
  served by the same instance. Redis pub/sub behind `StoreEventsService` is the fix.
- Metric values are per-process. That is correct for Prometheus (it scrapes and aggregates each
  instance), but the exported latency summary carries pre-computed quantiles, which cannot be
  aggregated — a bucketed histogram is the migration.
- `AI_FALLBACK_PROVIDER` chains exactly two vendors.
- **Application i18n is partial.** The landing page and `BuilderTopBar` switch language; the
  dashboard, the builder's left panel (`BuilderClient`, `CategoryChooser`) and `PreviewFrame` do
  not — `PreviewFrame`'s page tabs and viewport labels are hardcoded English. Their keys already
  exist in both dictionaries, unused. A user switching to Arabic gets an Arabic landing page and
  an English builder.
- **No shared authenticated shell.** The dashboard has its own `<header>`, the builder has
  `BuilderTopBar`. There is no `/stores` route, no account menu and no mobile menu.
- The `date` photo subject was removed — every candidate turned out to be the calendar sense of
  the word — so stores selling dates render gradients. `oud` and `bukhoor` share one pool of
  three, so an eight-product fragrance grid repeats a photograph.
- Google OAuth has never been run end to end. State signing, cookie attributes and callback
  rejection are unit-tested; the consent screen needs real credentials.

## Traps worth knowing

- **`pnpm test` builds the contract first.** The API's tests import `@dukkanify/core` through its
  compiled `dist/`, so a bare `vitest` run in `apps/api` fails with "Failed to resolve entry for
  package" whenever `dist/` is missing or stale. Build core, or use the root script.
- **A `loading.tsx` changes HTTP status codes.** It wraps its segment in Suspense, so the response
  streams and the status is committed before the page body runs — a later `notFound()` can no
  longer set 404. Keep loading boundaries off segments that call `notFound()`; there is one on
  `app/dashboard/` for that reason, and deliberately none at the app root.
- **Never invalidate a cache tag from a client component.** `revalidateTag` is server-only, so the
  storefront's `store:<slug>` tag is invalidated from `app/builder/actions.ts`. A write added
  elsewhere will silently leave published pages stale for up to five minutes.
- **Publishing is not part of saving.** `PATCH /store/:id/status` is the only thing that changes
  `status`; `save` deliberately preserves it.
- **Stop the dev server before pushing.** `pre-push` ends in `pnpm build`, which writes to the
  same `apps/web/.next` a running dev server is reading from. The push then fails with
  "Failed to collect page data" for a route that is perfectly fine. `rm -rf apps/web/.next` and
  retry. This looks exactly like a code defect and is not one.
- **`dev-login` always returns the same demo user.** Two calls are one tenant, so a multi-tenancy
  probe built on it proves nothing. Create a second `User` row directly and sign a session with
  `JWT_SECRET` to test isolation for real.
- **Openverse needs `category=photograph`.** Without it the index leans on public-domain scans,
  and a perfume store comes back illustrated with botanical plates and 1920s magazine
  advertisements — correctly licensed, on subject, and obviously not product photography.
- **Grep the source, not the tree.** `apps/web/.next/types/**` is generated and full of `any` and
  `@ts-ignore`. An audit that includes it reports violations the repository does not have;
  exclude `.next`, `dist` and `node_modules` before believing a count.

## Reference docs

`docs/interview-prep.md` is the crib sheet for the post-submission technical review:
the architectural defense, the live-coding drills, and the weaknesses to volunteer.

`docs/architecture.md` (system diagram, scaling story), `docs/decisions.md` (ADR-style rationale
for each of the choices above), `docs/ai-workflow.md` (how AI assistants were used to build this),
`docs/qa-checklist.md` (per-item QA status with the command that verifies each one),
`docs/deployment.md` (Vercel settings for the web app, why the API needs a container host, and
the cookie/CORS variables the two halves must agree on), `docs/implementation-plan.md`
(the closed roadmap that took the repo to spec compliance), `docs/next-phases.md` (what remains,
sequenced into commit-sized tasks).
