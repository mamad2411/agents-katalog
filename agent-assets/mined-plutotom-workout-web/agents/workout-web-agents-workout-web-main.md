<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

## Review and merge checks

- Run `pnpm test:review` for general code reviews and before recommending a
  merge. It runs the ordinary unit suite and the strict offline account lifecycle
  gate. Report both results; `pnpm test` alone does not establish merge readiness.
- GitHub Actions runs `Unit tests` and `Offline account lifecycle` on every PR
  and merge-group commit, without path filters. Both checks must pass on the
  current integration commit before merging into `main` or `staging`.
- Do not skip cases, use test-name filters, mark failures as expected, or add
  `continue-on-error` to turn data-preservation defects into a green check.
- Account, auth, sync, SQLite migration, Convex schema, and import changes must
  preserve old users/data. Add regression coverage for the failure and verify
  offline restart, reconnect, retries, and account ownership as applicable.
- These tests use temporary SQLite files and synthetic Convex/WorkOS accounts;
  do not substitute real users, production data, or production credentials.
  See [the lifecycle gate documentation](tests/offline-accounts/README.md).

### Workout sync invariants

- Local workout edits, their monotonic revision, and their replacement outbox
  snapshot must commit together through `withWorkoutTransaction` in
  `mobile/src/data/local/workout-transactions.ts`. Cloud workout adoption uses
  the same serialized boundary. Do not write a row and queue it later.
- Preserve session, template, exercise, and set identities through adoption,
  offline restart, retries, and acknowledgments. A pending local aggregate must
  survive stale cloud delivery; acknowledging an older operation must not delete
  a newer queued operation. Track provider adoption writes with `trackLocalWrite`
  so account transitions wait for them.
- Editing a completed workout preserves its completion date and Health identity,
  never queues a second Health export, and patches an existing social post rather
  than creating another one. Explicit empty session notes override global cues;
  missing session notes inherit them.
- Equipment memory follows workout completion chronology, not edit time. A phone
  may have only partial history: historical edits preserve cached prescriptions;
  Convex refreshes eligible latest-workout weights on reconnect.
- Add production-path regression tests for any sync feature or fix. Keep
  `tests/offline-accounts/completed-workout-edits.test.js` in the required lifecycle
  gate and the SQLite atomicity/failure cases in
  `mobile/src/data/local/completed-workout-edits.sqlite.test.js`. Cover interrupted
  writes and delivery order, not just pure policy helpers or mocked happy paths.

## Backend (Convex)

Convex functions live in `backend/`. As the app grows:

- **Schemas** — `backend/schemas/` per domain; compose in `backend/schema.ts` only.
- **Routes** — `backend/routes/<feature>/` (e.g. `auth/`, `templates/`, `workouts/`) for queries, mutations, and actions. Avoid dumping new function files at `backend/` root.

See `.cursor/rules/backend-organization.mdc` for full conventions.

## Sharing workouts (export / import)

Templates move between accounts as a **portable bundle**. One format, three
transports, both apps:

| Transport    | Where                               | Offline |
| ------------ | ----------------------------------- | ------- |
| Share link   | `/share/<token>` (public preview)   | No      |
| `.json` file | Download on web, share sheet on iOS | Yes     |
| Pasted code  | `WKT1-…` base64url text             | Yes     |

- **Format** — `backend/schemas/portable.ts` holds `portableBundleValidator`,
  the single source of truth. `src/lib/workout-export.ts` derives its
  TypeScript type from it via a **type-only** import, so the wire format can't
  drift from what the server accepts. That module has zero runtime imports and
  hand-rolls its base64 (no `btoa`/`Buffer`/`TextEncoder`) because it runs in
  the browser, a service worker, Node, and Hermes.
- **Import is additive.** Nothing is ever overwritten: name collisions get a
  `(2)` suffix, and an imported exercise note is only written when the importer
  has no note for that lift.
- **Custom lifts travel with the bundle** and are recreated under the importer's
  account (matched by name, reviving archived ones) so `custom:<id>` slugs from
  another account resolve instead of dangling.
- **Weights convert** when sender and recipient use different units. `0` means
  "no preset" and stays `0`.
- **Old files must keep importing.** Frozen payloads live in
  `src/lib/fixtures/import-compat/` (Prettier-ignored so they cannot be
  rewritten). `pnpm test:import-compat` (also a pre-commit hook) parses every
  file in that folder, then runs Convex's `portableBundleValidator` on the
  object the importer would send to the server. New export fields must be
  `v.optional(...)` with client defaults — never edit those fixtures; add a
  new one. See `.cursor/rules/import-compat.mdc`.
- Share tokens are 128-bit bearer secrets — revocable, 30-day default expiry,
  50 live links per user. `shares.queries.preview` is intentionally
  **unauthenticated** (the recipient may have no account yet) and exposes only
  the bundle plus an optional sender-supplied display name — never the sender's
  email or user id. Importing still requires sign-in.

### iOS universal links

Tapping a share link opens the app instead of Safari via
`associatedDomains` in `mobile/app.json`, served from
`/.well-known/apple-app-site-association` (a rewrite to
`src/app/api/apple-app-site-association/route.ts`).

The route defaults to the team and bundle ids declared in `mobile/app.json`
(`ios.appleTeamId` / `ios.bundleIdentifier`), so universal links work without
extra configuration. `APPLE_TEAM_ID` and `APPLE_BUNDLE_ID` override them if the
app is ever signed by a different team — keep the two in sync, because iOS
caches a rejected association.

Only `workout.plutotom.com` is claimed, so on staging a tapped link stays in
the browser. The `workout://share/<token>` scheme and the file/code transports
are unaffected.

`expo-file-system` and `expo-sharing` are native modules: **the iOS app needs a
rebuild**, not just a Metro reload, before the file transport or universal links
work on device.

## iOS keyboard (Expo)

On iOS a focused text input must never sit under the software keyboard — not
the caret in a multiline note, not a comment composer, not a field in a
page sheet. This is an app-wide rule, not a per-screen fix.

Use the shared primitives in `mobile/src/components/` instead of RN's
`KeyboardAvoidingView` or `automaticallyAdjustKeyboardInsets`:

| Layout                                         | Primitive                                            |
| ---------------------------------------------- | ---------------------------------------------------- |
| Full screen with inputs                        | `Screen` (wraps `KeyboardAwareScroll`)               |
| Scroll + sticky CTA (Finish / Save / Generate) | `KeyboardAwareFooterLayout` + `KeyboardStickyFooter` |
| Non-scrolling screen                           | `Screen scroll={false}` keeps `KeyboardAvoidingView` |

`KeyboardAwareScroll` tracks the caret (including multiline) and takes a
`bottomOffset` so typing stays above a sticky footer. Do not put a focused
input in a plain `ScrollView` or a fixed footer that ignores the keyboard.

See `.cursor/rules/mobile-first.mdc` for the web/PWA counterpart
(`useVisualViewportFrame`).

## Deployment

Vercel runs `pnpm build` → `scripts/vercel-build.mjs`:

The long-lived staging branch is hosted by the isolated
`workout-web-staging` Vercel project. That project builds only `staging` and
has public deployment access for the staging custom domain. The main
`workout-web` project keeps deployment protection enabled for production and
ordinary previews.

- **Production** — `convex deploy`, then Next.js. Deploy injects
  `NEXT_PUBLIC_CONVEX_URL` for the web build.
- **Staging branch Preview** — deploys backend code to the persistent
  `preview/staging` deployment, then builds Next.js against the URL returned by
  that deploy. Its deploy key is restricted to that one deployment, so data
  survives every deployment.
- **Other Previews** — skip `convex deploy` and build against their configured
  Preview `NEXT_PUBLIC_CONVEX_URL`.

`scripts/resolve-workos-redirect-uri.mjs` sets the redirect URI from
`convex.json` `authKit.prod` on **Production** builds (custom domain) and from
`https://staging.workout.plutotom.com` on the **staging Preview** build.
Other previews use the stable `VERCEL_BRANCH_URL` (`VERCEL_URL` is only a
fallback). Override the staging origin with `STAGING_APP_URL` if its domain
changes.

Set `NEXT_PUBLIC_CONVEX_URL` on Vercel **Preview** for ordinary PR previews.
The `staging` branch build receives its URL directly from `convex deploy`.

### Vercel deploy keys

| Vercel environment  | `CONVEX_DEPLOY_KEY` source                                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Production**      | Convex Dashboard → Project Settings → **Production** Deploy Key                                                         |
| **Preview/staging** | `convex deployment token create vercel-staging --deployment preview/staging`, scoped to Vercel Preview branch `staging` |

Both variables are named `CONVEX_DEPLOY_KEY` in Vercel, but each key must be
restricted to the matching environment (Production only / Preview only). If a
production key is available during a preview build, Convex fails with:

> Detected a non-production build environment and "CONVEX_DEPLOY_KEY" for a
> production Convex deployment.

The `staging` branch always reuses `preview/staging` (see `convex.json` →
`authKit.preview`). Without its branch-scoped Preview key, staging fails closed
instead of silently building against the wrong backend. Ordinary PR previews do
not deploy backend/schema changes.

### WorkOS / AuthKit (preview builds)

`convex.json` `authKit.preview` configures WorkOS redirect URIs from
`VERCEL_BRANCH_URL` at deploy time. The Convex CLI still needs
`WORKOS_CLIENT_ID` and `WORKOS_API_KEY` in the **Vercel Preview** build
environment (not just on the Convex deployment).

1. **Convex dashboard** — create a project-level AuthKit environment for
   preview (Settings → Integrations → WorkOS on any deployment). See
   [AuthKit auto-provision](https://docs.convex.dev/auth/authkit/auto-provision).
2. **Convex preview env defaults** — set `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`,
   and `MCP_API_KEY_PEPPER` under Project Settings → Environment Variable
   Defaults → Preview (applies to new preview backends).
3. **Vercel staging branch env** — same `WORKOS_*` vars plus
   `WORKOS_COOKIE_PASSWORD`, scoped to Preview branch `staging`.
   `NEXT_PUBLIC_WORKOS_REDIRECT_URI` is set at build time by
   `scripts/resolve-workos-redirect-uri.mjs` (`VERCEL_BRANCH_URL` on preview,
   `authKit.prod` redirect URI on production).

Quick sync from local `.env.local`:

```bash
pnpm sync:preview        # Convex preview defaults + preview/staging deployment
pnpm sync:preview:all    # Also push secrets to Vercel Preview branch staging
```

`sync:preview:all` targets `workout-web-staging` by default. Set
`VERCEL_PROJECT_NAME` only when intentionally syncing another project.

The sync also registers the stable staging callback, homepage, and CORS origin
with WorkOS. Override the default custom domain with `STAGING_APP_URL` if the
staging domain changes.

For local Next.js builds without deploying Convex, use `pnpm build:web`.

Manual full prod sync (Convex env vars + WorkOS redirects): `pnpm sync:prod`.

## Local worktrees

Use the repository commands instead of copying `.env.local` or invoking
`git worktree` directly:

```bash
pnpm worktree:create <slug>
pnpm worktree:list
pnpm worktree:start <slug>
pnpm worktree:remove <slug>
```

Each `wt/<slug>` worktree receives persisted frontend and Convex Local ports,
an anonymous local Convex deployment, and an allowlisted projection of the
primary checkout's WorkOS Sandbox credentials. State and ownership manifests
live under the common Git directory. Starts remain foreground processes;
removal refuses dirty or listening worktrees and preserves the branch.

Never copy `CONVEX_DEPLOYMENT`, remote Convex URLs, Vercel OIDC tokens,
production WorkOS keys, or arbitrary environment files into a worktree.
