---
name: notis-apps
description: Design and package Notis apps. Use when users want an app that groups databases, routes, documents, automations, and skills into one installable Notis product.
feature_flag: store
mcp_resource: true
mcp_tool_patterns: ["LOCAL_NOTIS_INSTALL_APP"]
---

# Notis Apps Skill

Use this skill when the user wants a packaged Notis app -- task manager, CRM, dashboard, internal tool, etc. Notis apps are **Vite + React projects** that deploy into the Notis portal as installed apps for the current user or team.

Run the Notis CLI through NPX, for example `npx --package @notis_ai/cli@latest -- notis apps list`. Sign the CLI in once with `notis login`; each account you authorize is a profile you can switch between with `notis profile use`. The CLI bundles this `notis-apps` base skill and refreshes its canonical copy under `~/.notis/skills/base/` on every launch. It is independent of account-skill sync, feature flags, target selection, and cloud deletion.

## How Apps Are Built

All Notis apps are built using the Notis CLI, either locally in a repo workspace or inside a Vercel Sandbox. The platform contract is the same in both cases:
- the app is a Vite + React project
- the app uses `@notis/sdk`
- the app is packaged as an ES module bundle
- the portal renders it as a React component inside the portal's React tree

## App Workspace Tool Rules

- Apps are the top-level packaging unit in Notis.
- Use `apps dev [folder]` to register a new local app for development. After the
  user tests it and explicitly asks to deploy, `apps deploy` promotes that DEV
  app in place. Use `LOCAL_NOTIS_CREATE_APP` only for non-CLI administrative
  flows that explicitly require a server-side app row.
- Use `LOCAL_NOTIS_UPDATE_APP` to update app metadata.
- Use `LOCAL_NOTIS_LIST_APPS` to discover the user's apps.
- The full app lifecycle uses the CLI in the shell. Always run it through the registry-resolved package, for example `npx --package @notis_ai/cli@latest -- notis apps init`; use the same prefix for `build` and `deploy`. In hosted shells, the CLI is pre-authenticated through `NOTIS_JWT`.
- There are no `save_app` or `load_app` tools. Do not attempt to call them. Use only the CLI for app file operations.
- Use `npx --package @notis_ai/cli@latest -- notis apps scaffolds list` (optionally with `--search <term>`) to discover starting points before scaffolding. Every published Store app is a scaffold; the catalog is served from the public registry, not bundled inside the CLI.
- Use `LOCAL_NOTIS_LIST_PUBLIC_APP_STORE` only to help users choose apps to install, not as a source-clone workflow.
- Use `LOCAL_NOTIS_INSTALL_APP` only when the user explicitly wants to install from a listing.
- Before installing, inspect the listing's `required_capabilities`. Explain each
  requested capability and obtain explicit approval; only then pass the matching
  token in `approved_capabilities`. Never infer capability approval. The current
  workspace-wide read token is `workspace_databases_read`; the read-only
  cloud computer token is `cloud_computer_read`.

## Architecture

```
Notis CLI (local workspace or Vercel Sandbox)
  -> Vite + React project with @notis/sdk
  -> notis apps init / dev / build / verify / create / link / pull / deploy
  -> ES module bundle (app.js + app.css) + manifest
  -> Portal renders as React component with real tools/databases
```

`deploy` updates the linked installed app for the current account or team. After the user explicitly confirms the App Details page is ready, `apps publish --confirm-ready` submits that deployed version to the Team or Public Store review flow.

### Key Components

1. **@notis/sdk** (`packages/sdk/`) -- SDK for app developers
   - `@notis/sdk` -- NotisProvider, runtime hooks, editors, selection helpers, and shortcut primitives
   - `@notis/sdk/interactions` -- headless collection actions and interaction types
   - `@notis/sdk/config` -- `defineNotisApp()` for notis.config.ts
   - `@notis/sdk/vite` -- `notisViteConfig()` for vite.config.ts
   - `@notis/sdk/styles.css` -- shadow-safe app shell styles and base app-surface classes

2. **CLI** (`packages/cli/src/command-specs/apps.js`) -- local development should center on `apps dev`, plus init, build, verify, create, deploy, link, pull, doctor, and list

3. **Server** (`server/routers/portal_views/`) -- Returns signed bundle URLs, proxies tool calls

4. **Portal** (`portal/src/components/apps/`) -- Renders app bundles as React components via AppViewRenderer

### Runtime Bridge

Apps communicate with the platform through the `NotisRuntime` interface, provided by the portal via React context:

- **Portal development**: the portal loads a local bundle for an active dev session and still provides a real `NotisRuntime`.
- **Portal**: the portal creates a real `NotisRuntime` and passes it as a prop to `NotisProvider`. All calls go to `/portal_views/runtime_query` via fetch with the user's JWT.
- The portal mounts the app inside a shadow-scoped content surface and injects the runtime before app mount. There is no supported window-global runtime fallback.

App code never accesses the runtime directly -- it uses SDK hooks (`useTool`, `useTools`, `useNotis`, etc.) which read from the `NotisProvider` context.

## Hard Rules

1. **React + Vite only** -- No Next.js, no custom server
2. **ES module bundle** -- Vite builds a library-mode bundle with React externalized
3. **Component rendering** -- Apps render as React components directly in the portal. No iframes.
   The portal owns the `ShadowRoot`, theme tokens, and runtime provider.
4. **HTTP bridge** -- Runtime calls use fetch to `/portal_views/runtime_query`
5. **Declarative tools** -- Tool access is declared in `notis.config.ts` by the final names returned by tool discovery and enforced server-side. Views can call native Notis, connected integrations, PostForMe, and MCP tools directly; metered calls use the same credit-cap and usage-billing path as the CLI.
6. **shadcn + Notis theme** -- Apps must use shadcn components with the live Notis theme provided by the portal
7. **Phosphor icons only** -- Always `phosphor:` prefix. Never emojis.
8. **Database refs only** -- `notis.config.ts` references existing databases by slug. The schema source of truth lives in the `databases` table, not in the manifest. Every native database is owned by exactly one app (`databases.owner_app_id`): creating one through `LOCAL_NOTIS_DATABASE_UPSERT_DATABASE` requires the owning app's slug or id in the `app` argument, install/dev materialization stamps ownership automatically, and deleting an app deletes its databases and their documents.
   An app-owned database slug is a stable deployed contract because bundles and
   collection routes may call it directly. Do not try to rename that slug with
   a schema tool; rename the display title instead.
9. **Use NPX for CLI commands** -- Always run `npx --package @notis_ai/cli@latest -- notis ...`.
10. **`apps deploy` is not store publishing** -- `apps deploy` updates an installed app only and persists its source snapshot. Store review starts separately with `apps publish --confirm-ready` after explicit user approval.
11. **Routes are canonical** -- Define navigation only in `manifest.routes`. Every configured route must declare an explicit `slug`. Do not rely on legacy `manifest.views`.
12. **Portal-owned sidebars stay portal-owned** -- If a route uses `collection.sidebar`, treat that sidebar as platform chrome. Do not remove it, recreate it inside app JSX, or replace it with a custom in-app folder rail.
13. **Portal globals are off-limits** -- Never use `window.__NOTIS_RUNTIME__`, query portal-owned DOM hooks, or create global DOM portals.
14. **Prefer inline optimistic edits** -- Rename-like edits for collections, app-owned rows, and sidebar-backed entities should use inline editing with an optimistic UI update, then roll back on backend failure. Use modals only when the edit requires multiple fields or destructive confirmation.
15. **Local development first; deploy is user-gated** -- Run `apps dev [folder]` once to register the root, then let the **user** test the automatically mounted app in its Workspace entry (compact `DEV` badge). The registration and host survive the command; no terminal must remain open. Do NOT run `apps create` or `apps deploy` on your own initiative, even after a clean build and verify. Building through local testing without deploying is the expected, complete outcome.
16. **Installed app identity is exact and profile-scoped** -- Identity precedence is: explicit persisted link for this API/user profile; one accessible non-development app with the exact canonical slug; isolated development runtime. Persist one unique exact-slug match, fail closed on ambiguity, and never infer from display name. After first install, keep the profile-scoped link so Portal and CLI update the same app instead of creating duplicates.
17. **Development identities stay separate** -- `.notis/state.json` uses `dev_app_id` for the hidden development-runtime row and `app_id` only for an accessible installed workspace app, scoped under the authenticated environment. Never pass a runtime app whose manifest has `is_dev: true` to `notis apps link`.
18. **Automatic mounts are multi-instance and least-authority** -- Prod, Beta, and source-development Desktop instances may mount the same source simultaneously with independent authenticated runtimes. Automatic mounting never grants capabilities: reuse existing grants and leave restricted capabilities denied until approved. Consumer leases expire after crashes so the shared host exits after the last live instance. There are no offline rows or manual start/stop controls.
19. **Store submission is user-gated** -- Run `apps publish --confirm-ready` only after the user explicitly confirms the current App Details page and Store listing are ready. Deploy the exact approved local state first. The command must reject missing confirmation, incomplete listing media, a local/deployed version mismatch, private visibility, or an existing pending review.
20. **Bump `notisAppVersion` before linked development and every Store update** -- `package.json` must contain a semver `notisAppVersion`. A linked local source substitutes its installed Workspace app only when the local version is strictly greater than the installed manifest's `release_version`; equal, lower, missing, or invalid versions keep serving the online bundle. `apps pull` retrieves the online version, so increment `notisAppVersion` before `apps dev` when continuing development. For an existing Store app, also increment it beyond the currently published registry version before deploy and submission; registry CI rejects equal or lower versions.
21. **`CHANGELOG.md` owns release history** -- Keep the complete release history in one root `CHANGELOG.md`, newest entry first. Do not add new `versionNotes` values to `notis.config.ts`. Use `## [Release title] - YYYY-MM-DD`, or `{PR_MERGE_DATE}` for an unpublished entry. App Details reads **What’s New** and **Version History** from the deployed package manifest, while the Store reads them from the latest published snapshot; unpublished workspace edits must never change the Store page. The manifest also exposes `package.json` `notisAppVersion` as the package version shown in App Details.
22. **Database rows are private unless explicitly seeded** -- A string declaration such as `databases: ['notes']` publishes schema only and never includes the developer's rows. Use `{ slug: 'templates', seedDocuments: true }` only for small, intentional starter content that every installer should receive. Never enable it for user-created notes, history, leads, or other personal data.
23. **Public submissions are complete, reviewable packages** -- The registry PR must contain the full editable source tree, Store assets, exact source-declared database schemas, and only explicitly seeded starter rows. Registry CI validates those boundaries before merge; do not hand-edit `notis-listing.json` or strip source files to make a check pass. Fix the app locally, redeploy, and resubmit.
24. **New projects default to `~/.notis/apps/<slug>`, and `[dir]` overrides it** -- `apps init` and `apps pull` use this stable, predictable home unless the app belongs in a specific repository, monorepo, or user-chosen location. In those cases, pass `[dir]` and report the resulting path. Do not nest an app inside a directory whose local workspace metadata selects an unrelated Notis runtime or profile: later CLI calls inherit that routing and may target the wrong environment.

## Anti-patterns -- NEVER do these

These are the most common mistakes agents make. Each one wastes time and produces broken results.

- **NEVER assume app deploys create databases for you** -- Create or update databases through native Notis database tools or the assistant first, then reference them by slug in `notis.config.ts`. Database creation requires the owning app to exist: pass its slug or id in the `app` argument of `LOCAL_NOTIS_DATABASE_UPSERT_DATABASE` (create the app first with `LOCAL_NOTIS_CREATE_APP` if needed). A database can only be referenced by the app that owns it.
- **NEVER bypass the supported workflow by manually stitching together low-level save or lint calls from a local workspace** -- Local agents should go through the NPX Notis CLI for `apps pull`, `apps dev`, `apps build`, `apps verify`, `apps create`, `apps link`, and `apps deploy`.
- **NEVER use `apps pull` to clone a Store listing** -- `npx --package @notis_ai/cli@latest -- notis apps pull` only pulls source for an app the user can already access as an installed app. To fork a published Store app, run `npx --package @notis_ai/cli@latest -- notis apps init "My App" --from <slug>` instead: it downloads that app's source from the public registry, and installing the app first is not required.
- **NEVER deploy on your own initiative** -- A clean `apps build` + `apps verify` is NOT a signal to deploy. `apps create` / `apps deploy` install the app onto the user's account; run them only after the user has tested the local (`apps dev`) build and explicitly asked you to deploy. When you finish building, hand off for local testing and stop — do not create or deploy unprompted.
- **NEVER submit without explicit approval** -- A deploy request alone does not authorize Store submission. Run `npx --package @notis_ai/cli@latest -- notis apps publish --confirm-ready` only when the user confirms App Details is ready for Store review.
- **NEVER write raw `views/<slug>/index.js` files** -- Write standard React pages in `app/`.
- **NEVER invent `npx --package @notis_ai/cli@latest -- notis apps push` or bypass the review flow** -- Source moves through `apps pull` and `apps deploy`; `apps publish --confirm-ready` submits the deployed snapshot through the same authenticated review endpoint as App Details.
- **NEVER treat `apps deploy` as store submission** -- It updates the linked installed app for the current account or team scope only. Store submission is a separate, explicitly confirmed step.
- **NEVER explore server code or tool schemas to invent an alternative app workflow** -- Use the Notis CLI.
- **NEVER work around a missing `collection.sidebar` portal tree by rendering a duplicate sidebar inside the app** -- keep the route manifest as the source of truth and escalate the missing portal sidebar as a platform bug instead.
- **NEVER invent a custom visual language** -- Do not ship full-screen gradients, glassmorphism, bright neon palettes, or raw HTML controls as the primary UI. Apps should look like a natural extension of the portal.
- **NEVER hand-roll buttons/cards/badges when the scaffold already provides shadcn primitives** -- Prefer `@/components/ui/*` and portal token classes such as `bg-background`, `bg-card`, `border-border`, and `text-muted-foreground`.

## Workflow

**Default to the Store scaffold catalog, not a blank project.** Every published Store app is a scaffold: `notis apps scaffolds list` reads the catalog from the public registry, and `notis apps init --from <slug>` downloads that app's source. Most user requests overlap with a published app, and starting from one is faster than a bare app.

1. **Find a starting point.** Run `npx --package @notis_ai/cli@latest -- notis apps scaffolds list` (add `--search <term>` to filter) to list the published Store apps. If something close matches, run `npx --package @notis_ai/cli@latest -- notis apps init "My App" --from <slug>` to download that app's source from the registry. Only run plain `notis apps init "My App"` when no published app fits. Either way the project lands in `~/.notis/apps/<slug>`; add a `[dir]` argument when the user wants it somewhere else (a tracked git repo, an existing monorepo), and report the path you used.
2. **Pull your own apps; fork Store apps with `--from`.** `apps pull` is for apps the user already has installed or deployed: run `npx --package @notis_ai/cli@latest -- notis apps list`, preserve any local edits in the target directory, then run `npx --package @notis_ai/cli@latest -- notis apps pull <app-id>` (lands in `~/.notis/apps/<app-slug>`; pass a `[dir]` argument to place it elsewhere). A pull reproduces the installed release, so increment `package.json` `notisAppVersion` above that release before `apps dev`; until then the online bundle remains active. To fork a published Store app, use `apps init --from <slug>` instead -- it downloads the source from the registry and does not require installing the app first.
3. **Edit the listing source.** Update `name` (slug), `title`, description, icon, accent, author, categories, tagline, databases, routes, and tools in `notis.config.ts`. Declare a database as a string for schema-only Store packaging; use `{ slug: 'templates', seedDocuments: true }` only when its rows are deliberate starter content for every installer. Keep the complete Store release history in the root `CHANGELOG.md`, newest entry first, using `## [Release title] - YYYY-MM-DD` (or `{PR_MERGE_DATE}` before publication). The first entry powers **What’s New** and the same file powers **Version History**. `icon` is a `phosphor:<name>` value or `metadata/icon.png`; when unset the app shows its **two-letter initials** everywhere (store, sidebar, app details). `accent` optionally pins the avatar color to one of `blue|violet|emerald|amber|rose|sky|fuchsia|teal` (default derived from the app id). Icon/accent flow through deploy onto the app row + listing and can also be set later via the `update_app` tool.
4. **Build pages in `app/`.** Reuse scaffold code wherever it fits.
5. **Iterate live.** Before developing a linked installed app, increment `package.json` `notisAppVersion` above the installed release. Then run `npx --package @notis_ai/cli@latest -- notis apps dev [folder]` once. It permanently registers the root; `~/.notis/apps` is already implicit. Running Desktop instances discover the root itself, direct app children, and `apps/*`, then mount each successful build automatically in Workspace. A linked build substitutes the online bundle only while its version is strictly greater; equal or stale builds remain served online. Source edits hot-reload only that app in every instance. Add `--scratch` for isolated empty resources when the work needs fixtures or destructive experiments.
6. **Capture listing screenshots.** Declare 3–6 screenshots in `notis.config.ts`, each with a stable `path`, descriptive `alt`, and optional `route`/`scenario`/`focus`/`theme`, then run `npx --package @notis_ai/cli@latest -- notis apps screenshot`. Use `focus` to frame a real app root without empty browser canvas; use `theme: 'light'` or `theme: 'dark'` to match both the Portal render and Store backdrop, and pair both modes when that best represents the app. It renders the configured states in a headless harness and writes exact 2000x1250 PNGs under `metadata/`, using the deterministic Store presentation by default (`--raw` is diagnostic only). Apps are icon-led like Raycast — the icon set in `notis.config.ts` represents the app, so there is no cover image, only these screenshots. Never hand-author the PNGs; regenerate them when routes or UI change. A `scenario` names an entry in `metadata/screenshot-fixtures.json`; besides `actions` it may carry its own `tools` and `requests`, shallow-merged per key over the file-level ones for that capture, which is how the same route is shown both populated and in its first-run empty state.
7. **Verify locally.** Run `npm install`, then `npx --package @notis_ai/cli@latest -- notis apps build` and `npx --package @notis_ai/cli@latest -- notis apps verify`. Surface the verify report and fix failures. Incomplete listing media is only a `Store readiness:` warning there; run `notis apps verify --listing` before publish to make it a failure.
8. **Local-development-first handoff — STOP HERE.** Hand off after the user can see and test the app in its DEV-badged Workspace row. Building a new app to this point, without deploying, is a **complete and expected** result. Do NOT proceed to `apps create` / `apps deploy` yet. **Before handing off, complete all three acceptance checks:**
   1. Root: `apps roots list` contains the intended folder (or the app is under the implicit default root).
   2. Bundle: the loopback `/snapshot` responds successfully and contains the expected manifest/routes.
   3. Mount and render: the app appears exactly once with a compact `DEV` badge and its default route renders. For multi-instance work, verify each requested Desktop independently.
   See Troubleshooting → *App is missing from the sidebar* if any check fails.
9. **Deploy only when the user asks.** Once the user has tested locally and explicitly requests a deploy, run `npx --package @notis_ai/cli@latest -- notis apps deploy`. A first deploy promotes the development app in place; do not create a second app or use `--direct`. For an existing remote app, link first with `npx --package @notis_ai/cli@latest -- notis apps link <id> .` and then deploy. After first install, `.notis/state.json` must point at that same promoted app id so future local-dev actions become **Update**, not another **Install**.
10. **Submit only after confirmation.** When the user explicitly confirms the current App Details page is ready, ensure the approved state is deployed, then run `npx --package @notis_ai/cli@latest -- notis apps publish --confirm-ready`. The command submits Team apps immediately or opens the Public Store registry review PR. Without that confirmation, stop after deploy.

### Quick start

Steps 1–3 are the agent's job on a build request. Step 4 is **user-gated** — do not run it until the user has tested the local build and asked you to deploy.

```bash
# 1. Pick a published Store app as the scaffold (catalog comes from the public registry)
#    The project lands in ~/.notis/apps/<slug>; append a directory argument when
#    the user wants the app in a repo they track.
npx --package @notis_ai/cli@latest -- notis apps scaffolds list
npx --package @notis_ai/cli@latest -- notis apps init "My App" --from <slug>
cd ~/.notis/apps/my-app
npm install

# 2. Develop against the Electron Portal, then HAND OFF for the user to test.
#    Keep this running — it is what substitutes the local build into the app's
#    sidebar group. This is the finish line for a build request.
npx --package @notis_ai/cli@latest -- notis apps dev
# ... iterate until the app looks right in its Workspace entry (DEV badge) ...

# 3. Build, capture listing screenshots, and verify (still local — no deploy)
npx --package @notis_ai/cli@latest -- notis apps build
npx --package @notis_ai/cli@latest -- notis apps screenshot
npx --package @notis_ai/cli@latest -- notis apps verify

# 4. ONLY after the user tested locally and asked to deploy. First deploy
#    promotes the dev app in place and writes the installed link.
npx --package @notis_ai/cli@latest -- notis apps deploy

# 5. ONLY after the user explicitly confirms App Details is ready for Store review
npx --package @notis_ai/cli@latest -- notis apps publish --confirm-ready
```

For an existing app, link the checkout first so every later command uses the
same profile-scoped installed identity:

```bash
npx --package @notis_ai/cli@latest -- notis apps link <app-id> .
npx --package @notis_ai/cli@latest -- notis apps deploy
```

Or if editing an installed app:

```bash
npx --package @notis_ai/cli@latest -- notis apps list
npx --package @notis_ai/cli@latest -- notis apps pull <installed-app-id>
cd ~/.notis/apps/my-app
npm install
# Increment package.json notisAppVersion above the pulled online release.
npx --package @notis_ai/cli@latest -- notis apps dev
npx --package @notis_ai/cli@latest -- notis apps build
npx --package @notis_ai/cli@latest -- notis apps verify
npx --package @notis_ai/cli@latest -- notis apps link <installed-app-id> .
# Only after the user explicitly asks to deploy:
npx --package @notis_ai/cli@latest -- notis apps deploy
```

## Building an App

### Step 1: Define the config

Create `notis.config.ts` with:
- **name** -- Display name
- **databases** -- Slug references to existing Notis databases
- **routes** -- Route-first sidebar entries with explicit `slug`, optional `parentSlug`, and optional `collection.sidebar` tree config
- **tools** -- Final tool names the app can call at runtime. Use the shared discovery flow (`COMPOSIO_SEARCH_TOOLS`, then `COMPOSIO_GET_TOOL_SCHEMAS`) while building the app, and copy the returned final names into this list. Examples include `LOCAL_NOTIS_DATABASE_QUERY`, `LOCAL_NOTIS_MONID_RUN`, `GMAIL_SEND_EMAIL`, `LOCAL_POSTFORME_CREATE_POST`, and `LOCAL_MCP_<SERVER>_<TOOL>`. App code calls each declared name directly through `useTool`; it does not wrap provider or MCP calls in `COMPOSIO_MULTI_EXECUTE_TOOL`. Access stays scoped to the signed-in user's own connections, native database tools stay scoped to the app's databases unless `capabilities.workspaceDatabases: 'read'` is granted, and metered tools use the CLI-equivalent credit-cap and fail-closed usage-billing path.

For collection-backed sidebars, use the route schema directly:

```ts
routes: [
  {
    path: '/',
    slug: 'notes',
    name: 'Notes',
    icon: 'phosphor:note-pencil',
    default: true,
    collection: {
      database: 'notes',
      titleProperty: 'Title',
      parentProperty: 'Parent note',
      sidebar: {
        mode: 'tree',
        allowCreate: true,
      },
    },
  },
]
```

Use the same page template for the root Notes route and collection/sub-collection detail states. The portal sidebar injects live collection items under the static route row when `collection.sidebar.mode === 'tree'`.

For arbitrary app-owned resources that are not Notis collection rows, set `resourceDeepLinks: true` on the route. Read the decoded `?resource=` identifier from `useNotis().resourceId`, and link between routes with `toRoute('/inbox', { resourceId })`. Keep collection links on `?item=`. Publish external preview/source links as the resource `url`; the host separately supplies the exact Notis review link as `active_resource.view_url` for opted-in routes. Handle missing or deleted identifiers with a safe view-level fallback.

### Step 2: Build pages

Standard React pages in `app/`. Use generic SDK tool hooks for data and build on top of the scaffolded shadcn components and portal shell classes (`notis-app-shell`, `notis-app-surface`):

```tsx
'use client';
import { useEffect, useState } from 'react';
import { useTool } from '@notis/sdk';
import { Card } from '@/components/ui/card';

type QueryTasksArgs = { database_id?: string; database_slug?: string; query: { page_size?: number } };
type TaskDoc = { document_id?: string; id?: string; title?: string; properties?: Record<string, unknown> };
type QueryTasksResult = { documents?: TaskDoc[] };

export default function TasksPage() {
  const queryTasks = useTool<QueryTasksArgs, QueryTasksResult>('LOCAL_NOTIS_DATABASE_QUERY');
  const [documents, setDocuments] = useState<TaskDoc[]>([]);

  useEffect(() => {
    void queryTasks
      .call({ database_id: 'tasks-db-id', query: { page_size: 25 } })
      .then((result) => setDocuments(result.documents || []));
  }, [queryTasks.call]);

  if (queryTasks.loading) return <div>Loading...</div>;

  return (
    <div className="p-6 space-y-4">
      {documents.map((doc) => (
        <Card key={doc.id || doc.document_id} className="p-4">
          <h3>{doc.title || 'Untitled'}</h3>
          <p className="text-muted-foreground">{String(doc.properties?.status || '')}</p>
        </Card>
      ))}
    </div>
  );
}
```

### Discovering database schema

Before writing app code, inspect the database schema to know what properties exist:

```bash
npx --package @notis_ai/cli@latest -- notis tools search "list Notis databases"
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_LIST_DATABASES --arguments '{}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_GET_DATABASE --arguments '{"database_slug":"social_media_calendar"}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_QUERY --arguments '{"database_id":"social-media-calendar-db-id","query":{"page_size":1}}'
```

Prefer the database `id` returned by `LOCAL_NOTIS_DATABASE_LIST_DATABASES` or `LOCAL_NOTIS_DATABASE_GET_DATABASE` when calling `LOCAL_NOTIS_DATABASE_QUERY`; use `database_slug` only as a fallback.

Use `LOCAL_NOTIS_DATABASE_GET_DATABASE` through `useTool` when an app needs schema detail at runtime. Keep database-specific result and property helper types inside the app code.
For document writes, declare the generated canonical tool for the target database, such as `LOCAL_NOTIS_DATABASE_UPSERT_TASKS`, and call it through `useTool`. Pass flat property values; the server wraps them:

```tsx
const upsertTask = useTool<Record<string, unknown>, { document?: { id: string } }>('LOCAL_NOTIS_DATABASE_UPSERT_TASKS');

await upsertTask.call({
  title: 'My Task',
  Status: 'Todo',
  Priority: 'P1',
  Due: '2025-04-01',
  Done: false,
  Count: 5,
});
```

Do NOT pass Notion-style wrappers (`{select: {name: "Todo"}}`) when upserting.

### Design rules

- Start from the scaffolded `@/components/ui/*` components before writing new UI primitives.
- Use restrained portal surfaces: `bg-background`, `bg-card`, `border-border`, `text-foreground`, `text-muted-foreground`.
- Keep layouts compact and dashboard-like. Prefer cards, sections, badges, and tables over marketing-style hero treatments.
- Respect the portal theme. Do not hardcode dark mode or create an app-specific palette.
- If a screen looks like a standalone microsite instead of a portal tool, it is too custom.
- For Notes-style apps, the folder tree belongs to the portal sidebar when configured via `collection.sidebar`. The page content should complement that chrome, not duplicate or replace it.
- Never indicate selected items with a heavy left-border bar (e.g. `border-l-2 border-l-foreground` paired with a muted background). It looks dated and clashes with the portal chrome. Use a single subtle background change (`bg-muted` for selected, `hover:bg-muted/50` for hover) and let typography or an icon carry the rest of the state.
- Do not render any search input inside the app (in-page search rails, "Ask Notis…" pills, command-palette-style bars, etc.). The portal already owns the top-bar search field. Wire your view to it with `useTopBarSearch({ value, onChange, placeholder, onSubmit })` from `@notis/sdk` and let the page filter or refetch on the values it receives. The hook also exposes `setLoading` so the standard top-bar spinner reflects in-flight queries.

### Sidebar invariants

- When a user asks for folders, sections, or hierarchy in the app sidebar, express that through `routes` and `collection.sidebar` in `notis.config.ts`.
- Treat an existing collection-tree sidebar as a locked structural requirement unless the user explicitly asks to change navigation architecture.
- If the sidebar appears missing for the substituted DEV entry or deployed portal build, do not silently redesign around it. Preserve the manifest contract, call out the discrepancy, and treat it as a portal/runtime bug.

### Step 3: Root layout

```tsx
import { NotisProvider } from '@notis/sdk';
import '@notis/sdk/styles.css';
import './globals.css';

export default function AppShell({ children }: { children: React.ReactNode }) {
  return <NotisProvider>{children}</NotisProvider>;
}
```

## Manifest Format

Generated by `npx --package @notis_ai/cli@latest -- notis apps build` at `.notis/output/manifest.json`:

```json
{
  "version": 1,
  "spec_version": 4,
  "app": { "name": "My App", "description": "...", "icon": "phosphor:..." },
  "routes": [
    {
      "path": "/",
      "slug": "index",
      "name": "Dashboard",
      "icon": "phosphor:squares-four",
      "default": true,
      "export_name": "index",
      "collection": null
    }
  ],
  "bundle": {
    "js": "bundle/app.js",
    "css": "bundle/app.css"
  },
  "databases": ["tasks", { "slug": "templates", "seed_documents": true }],
  "tools": ["LOCAL_NOTIS_DATABASE_QUERY"]
}
```

Use canonical `notis-*` tool names for explicit app tool declarations. App-specific TypeScript shapes for tool arguments and results live in the app code; the SDK exposes the generic `useTool<TArgs, TResult>()` hook instead of database-specific tool hooks.

Database strings package schema only. The object form shown above opts that database into copying its current rows as Store starter content. Use it sparingly and only for non-personal fixtures/templates every installer is meant to receive.

For a read-only database catalog app, declare `["LOCAL_NOTIS_DATABASE_LIST_DATABASES", "LOCAL_NOTIS_DATABASE_GET_DATABASE"]`. Use the list tool for the left/catalog pane and the get tool for the selected database detail pane.

## Database Schema

### apps table

| Column | Type | Description |
|---|---|---|
| id | uuid PK | App ID |
| user_id | uuid FK | Owner |
| team_id | uuid FK | Team (nullable) |
| name | text | Display name |
| slug | text UNIQUE | URL slug |
| description | text | App description |
| icon | text | Phosphor icon (e.g. "phosphor:list") |
| status | text | draft, active, archived |
| visibility | text | private, team |
| manifest | jsonb | Latest deployed manifest |
| current_version | integer | Version counter |
| source_listing_id | uuid FK | Source App Store listing for installed store apps; cleared when submitted as a derivative |
| installed_snapshot | jsonb | Store-installed baseline used for update/reset comparison |
| customization_overlay | jsonb | User changes over the installed store baseline |
| update_status | text | up_to_date, update_available, needs_resolution, update_failed |
| bundled_automation_ids | uuid[] | Linked automations |
| bundled_skill_ids | uuid[] | Linked skills |

### databases ownership

Every row in the `databases` table carries `owner_app_id` (uuid FK to
`apps.id`, `ON DELETE CASCADE`): a database belongs to exactly one app, and
deleting the app deletes its databases and their documents (`documents` cascade
from `databases`). Install, dev materialization, and store updates stamp
`owner_app_id` automatically; standalone creation requires the `app` argument.

### Storage (Supabase)

Files stored in `app-code` bucket at `{app_id}/v{version}/`:
- `manifest.json`
- `bundle/app.js`
- `bundle/app.css`

Editable source snapshots are stored in the private `app-source` bucket at
`{app_id}/v{version}/`. Portal App Store listing screenshots are uploaded to
the public `app-listing-assets` bucket before submission.

### Related tables

- **databases** -- Apps reference these rows by slug. Schema lives on the database row (`schema_metadata` / `original_fields`), not in the app manifest.
- **documents** -- `database_id` links to databases. Properties in `properties` jsonb.
- **app_store_listings** -- Snapshots for publishing to the app store.
- **app_submissions** -- Portal review submissions keyed to an app source version and registry slug.

## Server Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/portal_views/get` | GET | Route detail + runtime descriptor with signed bundle URLs |
| `/portal_views/runtime_query` | POST | Proxy tool calls and DB operations |
| `/portal_views/collection_items` | GET | List collection items |
| `/portal_views/collection_tree` | GET | List normalized collection tree nodes for a tree sidebar route |
| `/portal_views/collection_tree/create` | POST | Create a root or child collection row from the sidebar |
| `/portal_views/collection_tree/rename` | POST | Rename a collection tree item inline |
| `/portal_views/collection_tree/delete` | POST | Delete a collection tree item from the sidebar |
| `/portal_apps/list` | GET | List apps |
| `/portal_apps/get` | GET | Get app detail |
| `/portal_apps/publish` | POST | Submit a deployed app source snapshot for public store review |
| `/portal_apps/listing_assets/upload` | POST | Legacy pre-manifest screenshot upload; do not use for current manifest-media workflows |
| `/portal_apps/submissions` | GET/PATCH | List or edit App Store submissions |
| `/portal_apps/submissions/withdraw` | POST | Close a pending App Store submission |
| `/cli_tools` | POST | CLI tool execution (save_app_files, create_app, etc.) |

## SDK Hook Reference

All hooks and components below are imported from `@notis/sdk`. `NotisProvider`
already installs `ShortcutProvider`; app code should not add a second provider.

| API | Signature | Description |
|-----|-----------|-------------|
| `useNotis()` | `() => { app, route, databases, collectionItem, resourceId, ready }` | App metadata, current route, selected collection item, decoded exact-resource id, ready state |
| `useTool<TArgs, TResult>(name)` | `(name: string) => { call, loading, error }` | Call a declared tool with app-defined argument/result types. Identical idempotent reads may use `call(args, { dedupe: true })`; never dedupe writes |
| `useTools()` | `() => { tools, loading }` | List available tools |
| `useNotisNavigation()` | `() => { toRoute, toDocument, toApp }` | Navigate between routes (including `toRoute(path, { resourceId })`), documents, or the app root |
| `useTopBarSearch(opts)` | `({ value, onChange, placeholder?, onSubmit? }) => { setLoading }` | Bind the current view to the Portal-owned top-bar search input |
| `useBackend()` | `() => { request }` | Raw backend request proxy with JWT auth |
| `useDatabaseSubscription(slug, opts?)` | `(slug: string, opts?) => { rows, documents, loading, error, refetch, live }` | Query a database and refetch it when its rows change. `live` is false on hosts without a change feed (dev harness, vite preview) -- keep a manual refresh for those |
| `useHandover()` | `() => { handover, pending, error, available }` | Open manager chat with app/resource context plus an optional starter prompt or declared skill. Omit `prompt` for a context-only composer. `available` is false on hosts with no chat -- fall back to a copyable prompt |
| `useCloudComputer()` | `() => { facts, loading, error, refresh }` | Read-only cloud computer facts: sandbox existence/status and whether the GitHub CLI is signed in. Requires `capabilities.cloudComputer: 'read'` plus the user's approval; `facts.available === false` means answer from the app's own fallback |
| `useActiveResource(resource)` | `(ContextResource \| null) => void` | Publish the record currently open in the app so manager handover and context menus stay grounded |
| `useCollectionInteractions(opts)` | `(opts) => CollectionInteractionController` | Keyboard navigation, active-row state, range/toggle selection, marquee selection, and action dispatch for collection UIs |
| `useShortcuts(definitions, opts?)` | `(definitions, opts?) => void` | Register scoped keyboard shortcuts. Editable targets are ignored unless explicitly allowed; use `ShortcutHints` to display them |
| `MarkdownEditor` | `(NotisMarkdownEditorProps) => ReactElement` | Use the host editor with app-owned persistence, stable `resourceKey`, revision-aware `onSave`, and optional `onUploadFile` returning a durable URL |
| `NotisSelectionBoundary` | `(NotisSelectionBoundaryProps) => ReactElement` | Attach structured, explicitly untrusted app/resource/selection context to selected content and copy operations |
| `SelectionCheckbox` / `SelectionMarquee` | components | Standard selection controls backed by `useCollectionInteractions` |
| `MultiSelectActionBar` | component | Standard bulk actions with pending/disabled state and shortcut support |

Import headless collection action types and helpers from
`@notis/sdk/interactions`. Keep an open detail view synchronized with
`useActiveResource`, and wrap its selectable content in
`NotisSelectionBoundary` so the manager receives both the active record and the
user's exact selection. For `MarkdownEditor`, keep `resourceKey` stable per
record, pass the latest revision back from `onSave`, reject revision conflicts
instead of overwriting newer data, and implement `onUploadFile` whenever the
editor should accept media or file blocks.

### App configuration additions

- `devSlug` is the stable local-development identity. Set it when a display
  rename must not create a second DEV app; otherwise the CLI derives it from
  `name`.
- `toolBindings` is only for provider-generated public tool names whose upstream
  action cannot be reconstructed. Keep the exact final public `name` in
  `tools`, then bind it to `providerToolName`; the public name remains the
  permission boundary.

### Typed tool calls

`useTool` accepts generic argument and result types. Query the database at dev time to discover actual property shapes, then keep those types in the app:

```tsx
type QueryTasksArgs = { database_id?: string; database_slug?: string; query: { page_size?: number } };
interface TaskDoc {
  title: string;
  properties: {
    Status: string;
    Priority: string;
    Due: string;
  };
};
type QueryTasksResult = { documents: TaskDoc[] };

const queryTasks = useTool<QueryTasksArgs, QueryTasksResult>('LOCAL_NOTIS_DATABASE_QUERY');
const result = await queryTasks.call({ database_id: 'tasks-db-id', query: { page_size: 25 } });
// result.documents[0].properties.Status is typed as string
```

## Development Modes

### Canonical local development

```bash
npx --package @notis_ai/cli@latest -- notis apps dev
```

Runs the real desktop-local development workflow. The CLI should discover all apps in the target workspace and serve their bundles from loopback. Unpublished apps appear in the Electron Portal's Workspace group; linked apps substitute their installed entry only when the local `notisAppVersion` is strictly greater than the installed `release_version`.

## Testing

1. **Build validation**: `npx --package @notis_ai/cli@latest -- notis apps build` must succeed without errors. Vite surfaces TypeScript and bundling errors during this step.
2. **Headless render verification** (recommended after every build): run `npx --package @notis_ai/cli@latest -- notis apps verify`. It builds unless `--skip-build` is passed, spins up a loopback harness, drives `agent-browser` against every route, and reports per-route pass/fail with captured render errors and runtime calls.
3. **Local development acceptance**: Run `notis apps dev [folder]` once to register the root, then verify each signed-in Desktop instance independently. For an unpublished app, expect one DEV-badged Workspace row. For a linked app, first confirm local `notisAppVersion` is strictly greater than installed `release_version`, then expect one substituted DEV-badged row; equal or lower must keep the online row and bundle. Verify the default route renders and live edits appear without restarting the CLI or Desktop. Use `notis apps roots list` as the persistence proof. Loopback bundle health alone does not prove that an authenticated instance mounted or rendered the app.
4. **Post-deploy**: Verify the deployed bundle via `/portal_views/get` -> `runtime_descriptor.bundle.js_url`, then verify the app renders in the portal. The portal renders app bundles directly as React components, so the fastest verification is navigating to the app page in the portal.

### Headless harness verification

Run `npx --package @notis_ai/cli@latest -- notis apps verify` after `npx --package @notis_ai/cli@latest -- notis apps build`. Use `--mode live` after deploy to exercise the real `/portal_views/runtime_query` with the CLI JWT instead of stub data; live mode also fails a route whose runtime calls all errored, which a well-behaved error state would otherwise hide. If `agent-browser` is unavailable, pass `--no-browser` to print URLs and use `--keep-open` for interactive triage with `notis-browser-control`.

#### What the harness catches that `npx --package @notis_ai/cli@latest -- notis apps build` does not

- Hooks that mount but throw on first read (`useTool` called with the wrong tool name or argument shape, accessing nested props that are undefined).
- Runtime database queries whose slug is not declared by the app, and collection routes that never query their configured collection database. Declared databases may also support automations or agent workflows, so ordinary routes do not need to query every app database.
- Tool names referenced by hooks but missing from `notis.config.ts -> tools`.
- Suspense / async boundaries that never resolve because a runtime stub returned the wrong shape.
- Render-time exceptions that the portal would surface as the `View crashed` error boundary.

#### What the harness does not catch

- Bugs that only manifest with real backend data (auth-scoped filters, RLS, malformed prod records). For those, swap the stub runtime for a real one that posts to `/portal_views/runtime_query` with a JWT.
- Visual regressions (use `agent-browser screenshot` + a baseline compare if you need this).
- Bugs that depend on the portal's shadow-DOM stylesheet wrapping. The harness mounts in light DOM, so global Tailwind/shadcn classes work normally; portal-specific theme tokens injected as inline styles are not present.

## Troubleshooting

### Common issues

- **Deploy fails with network error**: Run `notis doctor`, then retry with the
  authenticated API available. Do not bypass DEV-app promotion or installed-app
  identity with a direct database/storage write.
- **App shows old code after deploy**: Bundle cache is stale. Hard refresh (Cmd+Shift+R) or clear site data in DevTools.
- **App is missing from the sidebar**: Run `apps roots list`, confirm the app is at the root, one direct child, or `apps/*`, and confirm its first build succeeds. For a linked app, compare `package.json` `notisAppVersion` with the installed manifest's `release_version`: equal, lower, missing, or invalid intentionally keeps the online app without a DEV badge. If source is stale, preserve any local edits, run `apps pull <app-id> <dir> --force` to refresh it, then increment `notisAppVersion` before continuing development. Restarting Desktop reattaches the same persistent roots; no terminal process or manual sidebar action is required.
- **`LOCAL_NOTIS_DATABASE_QUERY` returns empty documents**: Check that the database ID passed to the tool matches the intended database. Use `npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_LIST_DATABASES --arguments '{}'` to verify the ID; use the database slug only as a fallback.
- **Properties are `undefined`**: Keep app-local result types for `useTool<TArgs, TResult>` and guard optional nested properties when reading live data.
