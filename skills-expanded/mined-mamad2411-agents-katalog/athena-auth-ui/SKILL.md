---
name: athena-auth-ui
description: >
  Integrate, inspect, customize, debug, document, test, or release
  `@xylex-group/athena-auth-ui` from packages/athena-auth-ui/packages/heroui
  and the reference consumer examples/next-heroui-example. Covers public
  exports and subpaths (root, pages, plugins, primitives, tables, sidebar,
  organization, chat, email, icons, utils, client, types, styles, athena/*,
  auth/routing-debug), AuthProvider and auth pages, plugins, settings,
  organizations, workspace/admin, billing UI, storage UI, tables, chat, email
  templates, icons, sidebar, Athena client/proxy/query helpers, generated docs
  under packages/athena-auth-ui/docs/**, and next-heroui-example showcases
  (auth, settings, tables, storage, billing, chat, emails, sidebar-demo).
  Ignore packages/heroui-native and native-heroui-example. For deep table-only
  work prefer $athena-auth-ui-tables. For Athena JS SDK semantics use $athena-js.
  Use when the user runs /athena-auth-ui.
---

# Athena Auth UI

Monorepo root: `packages/athena-auth-ui` (Athena workspace) or the standalone
repo root.

## Scope (hard boundaries)

| In scope | Out of scope |
| --- | --- |
| `packages/heroui/**` — published `@xylex-group/athena-auth-ui` | `packages/heroui-native/**` |
| `examples/next-heroui-example/**` — reference Next.js consumer | `examples/native-heroui-example/**` |
| `docs/**` — generated API + guides for the heroui package | other packages under `packages/*` except tooling that serves heroui |
| Workspace root scripts that build/publish heroui or deploy the example | |

Do not load native React Native surfaces unless the user explicitly asks for
them in a separate task.

## Establish the source of truth

1. Package root: `packages/athena-auth-ui` (or standalone repo root).
2. **Published package**: `packages/heroui/package.json` — version, exports,
   peers, scripts. Version is live (currently **2.8.1**); always re-read.
3. Matching barrel under `packages/heroui/src/` for symbols on that subpath.
4. Generated docs: `docs/entrypoints/index.mdx`, then the component/hook/function
   page or a cross-cutting guide in `docs/*.mdx`.
5. Implementation + nearest `packages/heroui/tests/**` test.
6. Consumer proof: `examples/next-heroui-example` route, lib helper, or showcase
   when the seam is integration, proxy, cookies, or OpenNext/Cloudflare.

References:

- [public-api.md](references/public-api.md) — entrypoints and setup
- [implementation-map.md](references/implementation-map.md) — source ownership
- [example-app.md](references/example-app.md) — next-heroui-example map
- [repo-workflows.md](references/repo-workflows.md) — validation and gotchas

When artifacts disagree:

| Authority | Wins for |
| --- | --- |
| `packages/heroui/package.json` exports | consumer import paths |
| Subpath barrel (`src/index.ts`, `src/tables.ts`, …) | exported symbols |
| Concrete `src/**` module | runtime behavior |
| Focused package tests | seam regression proof |
| Generated `docs/**` | consumer contract — resync via `bun run docs:generate` |
| Example app | real proxy/cookie/routing/OpenNext consumption |

Never recommend deep `src/**`, `dist/**`, or `src/compat/**` imports unless the
export map publishes them. Compat files are **internal** only.

Package manager for this monorepo: **bun** (see root `AGENTS.md`). Prefer
`bun x nx …` for Nx targets.

Peers (see live `package.json`): `@xylex-group/athena` **>=3.6.4**,
`@heroui/react` / `@heroui/styles` **>=3.0.4**, React **>=19**, TanStack Query,
better-auth-ui core/react, lucide-react, gravity icons, bowser, react-email
(optional usage for email templates).

## Route the task

### Consumer integration

1. Install peers + `@xylex-group/athena-auth-ui`.
2. Import styles once:

```css
@import "tailwindcss";
@import "@heroui/styles";
@import "@xylex-group/athena-auth-ui/styles";
```

3. Resolve Athena URL and API key in **one app-owned helper** (do not scatter
   env chains). Athena JS 3 does not auto-read global env; auth client helpers
   require an explicit `key`.
4. Create clients with published helpers:

```ts
import { createAthenaAuthClient, createAthenaAuthPlugins } from "@xylex-group/athena-auth-ui"
// or: @xylex-group/athena-auth-ui/athena/client
```

5. Mount under `AuthProvider` with plugins. Prefer the narrowest published
   subpath for infrastructure-only code (`/athena/*`, `/utils`, `/types`).

Canonical example: `examples/next-heroui-example/src/components/providers.tsx`
and `src/lib/athena.ts` / `athena-server.ts` / `auth.ts`.

### Public API or documentation

Keep **four layers** aligned: export map, barrel, implementation, generated docs.
After symbol/signature changes: `bun run docs:generate`.

### Component / hook / plugin / behavior

Read the generated docs page (frontmatter source path when present), then the
implementation family in [implementation-map.md](references/implementation-map.md).
Reuse HeroUI primitives, package empty states, UI option merge, and plugin slots
instead of parallel abstractions.

### Auth routing / Athena transport

Trace across:

- base URL / upstream resolution (`athena/base-url`)
- browser vs server auth clients (`athena/client`)
- proxy handlers + cookies (`athena/proxy`)
- request-header forwarding (`athena/request-headers`)
- routing-debug config (`auth/routing-debug` + optional overlay)
- example app: `/api/auth/[...all]`, session bridge routes, `ATHENA_AUTH_ROUTING_MODE`

Keep proxy vs direct-upstream modes honest. Prefer package
`createAuthUiTanstackQueryClient` / `getAuthUiTanstackQueryClient` for Auth UI
TanStack usage — not `@xylex-group/athena/react` (different query stack).

SDK-depth work → also use `$athena-js`.

### Tables

Full table surface lives under `src/components/auth/table/**` and `/tables`.
Deep table layout, empty states, portable presets, model columns → also
`$athena-auth-ui-tables`. Keep Athena model-derived types; do not invent
colliding row wrappers.

### Workspace, admin, billing, storage, email, chat, sidebar

Treat each as a **subsystem** (barrel + types + hooks/runtime + UI + docs +
tests + example showcase). Preserve:

- workspace session/admin authorization (`checkAdminPermissions`,
  `useHasAdminAccess`, `docs/admin-access.mdx`)
- query keys / invalidation / skeletons / empty states
- email `templateKey` metadata and catalog
- billing query presets and card contracts
- sidebar path matching and visibility contracts
- portable table/chat export identity (`config_hash`, package versions)

### Example app only

Use [example-app.md](references/example-app.md). Prove via example `tsc`,
Vitest under the example, or Nx `next-heroui-example:build` / deploy targets.
Do not “fix” example bugs only in package typecheck.

## Implementation rules

- Prefer published imports and package-owned composition seams.
- Preserve `AthenaAuthUiOptions` deep-merge behavior; do not clobber unrelated
  `ui` branches when applying overrides (`deepmerge` / `DeepPartial`).
- HeroUI is the **internal** implementation; consumers import package components.
- Browser-only APIs behind client components or runtime guards.
- Server-only proxy/client helpers stay free of UI imports.
- Preserve email `templateKey` catalog stability.
- Derive table row/metadata types from `@xylex-group/athena` models.
- Keep `authMutationKeys` package-owned (do not import mutation keys from
  `@better-auth-ui/core`).
- Preserve backwards-compatible import parsing for portable table/chat presets
  (snake_case file boundary + legacy camelCase / dotted paths).
- Do not expose `src/compat/**` as a public API.
- Ignore and do not edit `packages/heroui-native` under this skill.

## Validation

Match the seam:

| Seam | Proof |
| --- | --- |
| Package behavior | focused `packages/heroui/tests/**` via package `test` / Vitest |
| Browser (passkeys, redirects, overlays, CSS order) | `test:browser` or real browser |
| Types / exports | package `build` + root `package:verify-types` when relevant |
| Public contract | `bun run docs:generate` + publish check |
| Example integration | `bunx nx run next-heroui-example:build` or example `tsc --noEmit` |
| Package release | `bun run package:publish:check` (build, publint, attw, smoke) |
| Workspace | `bun run lint`, `bun run typecheck`, `bun run package:build` |

From monorepo root:

```bash
bun run athena-js:build          # local SDK overlay when needed
bunx nx run @xylex-group/athena-auth-ui:build
bunx nx run @xylex-group/athena-auth-ui:test   # if target exists; else package scripts
bun run docs:generate
bunx nx run next-heroui-example:dev
bunx nx run next-heroui-example:build
```

Do not treat Biome/format as behavioral proof. On Windows, a successful Next
compile followed by OpenNext symlink `EPERM` under `.open-next` is an
environment limitation, not necessarily an app regression — confirm Next page
generation first and restore accidental `src/generated/build-metadata.json`
churn.

## Related skills

- `$athena-auth-ui-tables` — deep table surface
- `$athena-js` / `$athena-jsm` — Athena JS SDK client and package
- `$athena-js-typed-schema-registry` — model/registry typing
- `$athena-billing` — server billing domain (not just billing cards)
- `$athena-auth-emails` — auth service email backend
- `$heroui-react` / HeroUI skills — underlying UI primitives
- `$athena-auth-ui` (this skill) — heroui package + next-heroui-example only
