---
name: coding-standards
description: Load coding standards and conventions for this Next.js web project. Use when you need guidance on TypeScript patterns, Tailwind conventions, server/client component boundaries, folder layout, or env var handling.
---

Apply the following standards to all code in this project.

## TypeScript

- Never use `any` — use proper types, generics, or type guards
- Never use `as` assertions — fix types at the source (exception: `as const`)
- `tsconfig.json` runs `"strict": true` — never weaken it or add per-file `@ts-ignore`/`@ts-expect-error` to silence an error you can fix
- After any code change, run `tsc --noEmit` and fix **all** errors (zero errors is a baseline)
- Named exports only — no `export default` (exception: Next.js requires default exports for `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, and `middleware.ts` config-less files). One file = one component/hook; the file name and export name match 1:1
- No `React.FC` — type props inline or with a separate `type Props = {…}`
- Never import React as a default — `import React from 'react'` is not needed with the new JSX transform; import only what you use: `import { useState, useEffect, useRef } from 'react'`
- Arrow functions everywhere — `const MyComponent = () => …`; never `function` declarations for components, hooks, or helpers (exception: route handlers export `async function GET/POST` per Next.js convention)
- Prefer union types over multiple boolean flags: `type Status = "idle" | "loading" | "error"` instead of `isLoading + hasError`
- Type/interface names: no `T` or `I` prefix; self-documenting plain English; no abbreviations (except universally known ones like `API`, `URL`)
- Helper function naming: `get*` / `set*` / `create*` for synchronous; `fetch*` / `post*` / `patch*` / `delete*` for API calls; `is*` / `are*` for type guards and predicates

## Folder layout (App Router)

```text
app/                    # routes only — thin files that compose from src/
  (auth)/login/page.tsx
  (dashboard)/…/page.tsx
  api/webhooks/stripe/route.ts
  layout.tsx
  globals.css
src/
  components/           # shared UI (atoms → composed), one folder per component
  features/<feature>/   # feature slices: components, hooks, schema, queries per feature
  hooks/                # cross-feature hooks
  lib/                  # clients & pure utils: supabase/, stripe.ts, utils.ts
  lib/database.types.ts # GENERATED — never hand-edit
middleware.ts
```

- Route files (`page.tsx`, `layout.tsx`) stay thin — compose from `src/features/` and `src/components/`; no business logic in `app/`
- Route groups `(auth)` / `(dashboard)` split public from protected layouts without affecting URLs
- Keep files under **500 lines** — split into sub-components, hooks, or utils proactively
- Path alias: `@/*` → `./src/*` (defined in `tsconfig.json`)

## Server vs client components

- **Server by default.** No `"use client"` unless the component uses state, effects, event handlers, or browser APIs
- Push `"use client"` to the **leaves** — an interactive button doesn't make its whole page client; extract the interactive part
- Server-only secrets (service-role key, `STRIPE_SECRET_KEY`) live in modules marked `import "server-only"` — the bundler then errors if a client component ever imports them
- Never pass a Supabase client, class instance, or function across the server→client boundary — props must be serializable
- Data flows down: server components fetch and pass initial data; client components hydrate it into React Query when interactivity needs it (see `data-fetching`)
- `middleware.ts` runs on the edge — keep it to session refresh + redirects; no database queries

## Tailwind CSS (v4)

Tailwind v4 is CSS-first: there is no `tailwind.config.js` by default. Tokens are CSS variables declared in `app/globals.css` via `@theme`, and every `@theme` variable generates the matching utilities:

```css
@import 'tailwindcss';

@theme {
  --color-surface: oklch(0.98 0 0);
  --color-surface-card: oklch(1 0 0);
  --color-border-subtle: oklch(0.92 0 0);
  --color-text-secondary: oklch(0.45 0 0);
  --color-brand: oklch(0.55 0.2 260);
  --radius-card: 0.75rem;
}
```

- **No inline styles** — `style={{…}}` is banned except for genuinely dynamic values (e.g. a computed chart width); leave a `// NOTE: inline style required — <reason>` when unavoidable
- **No ad-hoc colors** — never `text-[#333]` or `bg-[rgb(…)]`; if the color isn't a token, add it to `@theme` first
- **No arbitrary values when a scale token exists** — `p-[13px]` is a smell; use the spacing scale (`p-3`, `p-4`). Arbitrary values are acceptable only for one-off constraints the scale genuinely can't express
- **Class ordering is automated** — `prettier-plugin-tailwindcss` sorts classes; never hand-order or fight the formatter
- **Conditional classes via `cn()`** (`src/lib/utils.ts`, clsx + tailwind-merge) — never template-string concatenation, which breaks tailwind-merge deduping:

  ```tsx
  <button className={cn('rounded-md px-4 py-2', isActive && 'bg-brand text-white', className)} />
  ```

- Dark mode via CSS variables: redefine the `@theme` variables under the dark selector rather than sprinkling `dark:` variants on every element; use `dark:` only for genuinely per-element exceptions
- Repeated class combos: extract a component, not an `@apply` rule — `@apply` hides the design system from the markup and resists tailwind-merge

### Tailwind v3 (classic config) is equally valid

The CSS-first `@theme` approach above is the v4 convention — don't assume it's the only correct one. A project on Tailwind v3 uses a classic JS/CJS `tailwind.config.js`/`.ts` with `content` globs and a PostCSS pipeline instead:

```js
// tailwind.config.js
module.exports = {
  content: ['./app/**/*.{ts,tsx}', './src/**/*.{ts,tsx}'],
  presets: [require('./tailwind.preset.js')], // shared tokens live in a preset, not @theme
  theme: {
    extend: {
      colors: { brand: 'oklch(0.55 0.2 260)' },
    },
  },
};
```

```js
// postcss.config.js
module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };
```

Tokens shared across multiple apps in a monorepo are typically a `presets` array entry rather than duplicated `theme.extend` blocks per app. Before assuming which version applies, check the project's actual `tailwind.config.*` / `postcss.config.*` files and the installed `tailwindcss` version in `package.json` — don't default to v4 conventions on a v3 project or vice versa.

## React / Components

- Follow React best practices (hooks, memoization, clean component structure)
- Never use `eslint-disable-next-line react-hooks/exhaustive-deps` — fix the dependency issue
- Conditional rendering: use ternary (`condition ? <X /> : null`), not `&&` — the `&&` form renders `0` when condition is a falsy number
- No margin on custom components — margins create invisible coupling between sibling layout. Use `gap-*` on the parent flex/grid container, or padding on a container instead
- Component checklist before creating: does `src/components/` already have it? Never reimplement an existing component
- Every list page renders four states deliberately: loading (`loading.tsx` or a skeleton), error (`error.tsx` boundary), empty (designed empty state, not a blank div), and data
- Images: `next/image`, never `<img>`; links: `next/link`, never `<a>` for internal navigation

## Forms & validation

- react-hook-form + zod for every form — see the `form` skill
- **zod parses every boundary**: route handler bodies, server action inputs, search params, and webhook payloads. Client-side validation is UX; server-side parsing is the security layer. The same schema file serves both
- Never use `.optional()` to silence TS errors — fix the type at the source

## State ownership

| Layer | Owner |
| --- | --- |
| Server state | React Query (client) / direct fetch (server components) |
| URL state | search params (`useSearchParams` / typed helpers) — filters, tabs, pagination live in the URL so views are shareable |
| Local UI state | `useState` / `useReducer` in the component that owns it |

If data comes from the database it belongs in React Query or a server component — never copied into long-lived client state. Reach for a global store (Zustand) only when genuinely cross-cutting client state appears (rare in a dashboard); get explicit agreement first.

## Env vars / Doppler

- Secrets via Doppler — configs `dev` / `stg` / `prd`; `.env.local` is generated, gitignored, and never the source of truth
- `NEXT_PUBLIC_` prefix **only** for values that are safe in the browser bundle (Supabase URL + anon key, Stripe publishable key, Sentry DSN). Everything else stays unprefixed and server-only
- **`NEXT_PUBLIC_` values are inlined at build time** — changing one requires a rebuild, not just a restart, and per-environment builds must run with that environment's Doppler config
- Never read `process.env` deep in components — access env in a small config module so missing vars fail loudly in one place

## Formatting

Prettier owns formatting — never hand-adjust quotes, semicolons, or wrapping. Run format-on-save (or `prettier --write`) and let it win. The project `.prettierrc` enforces:

- **Single quotes** — `'foo'`, never `"foo"` (`singleQuote: true`). Prettier still emits double quotes inside JSX attributes; that is expected, leave it.
- **Always semicolons** — terminate every statement (`semi: true`).
- Trailing commas everywhere (`trailingComma: "all"`), 2-space indent (`tabWidth: 2`), 100-char width (`printWidth: 100`).
- `prettier-plugin-tailwindcss` sorts Tailwind classes — it must stay last in the `plugins` array.
- Formatting must be **gated**, not just configured. `format:check` (`prettier --check .`) runs in the pre-push hook next to `check:tsc` and `lint`, and again in the `quality-checks` CI workflow. A `.prettierrc` with no gate is exactly how a repo drifts from its own config.

## CI / GitHub Actions

- Run a **quality-gate workflow** (`quality-checks.yml`) on every PR and on pushes to long-lived branches: `check:tsc` + `lint` + `format:check` + `test`, on source only (no Doppler/.env). It mirrors the pre-push hook so drift cannot slip through when hooks are bypassed (`--no-verify`) or uninstalled.
- **Corepack / Yarn-4 + `setup-node` trap:** `actions/setup-node@v5` defaults `package-manager-cache: true`, which runs `yarn cache dir` using the runner's **global Yarn 1.x before `corepack enable`**. Because `package.json` pins `yarn@4.x` via `packageManager`, global Yarn 1 refuses and the step **fails**. Every `setup-node` step in a Corepack/Yarn-4 project must set `package-manager-cache: false`.
- When major-bumping a GitHub Action (or Next.js), check the changed **defaults**, not just the inputs you pass — and verify with a real CI run before trusting it.

## Supabase custom schema setup

When using a custom schema (e.g. `api` instead of `public`), two steps are required before the app can query it:

**1. Expose the schema in PostgREST** — Supabase only exposes `public` and `graphql_public` by default. Add your schema via **Supabase dashboard → Settings → API → Exposed schemas**. Without this, every query returns `PGRST106: Invalid schema`.

**2. Grant privileges to roles** — Supabase no longer auto-grants privileges to `anon`/`authenticated`/`service_role` on new tables (effective 2026-05-30 for new projects, 2026-10-30 for existing). Every migration must include explicit grants:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON api.your_table TO authenticated;
GRANT ALL ON api.your_table TO service_role;
-- anon typically gets no access to B2B dashboard tables (requires auth)
```

Without this, authenticated users get `42501: permission denied for table`.

The Supabase clients must also declare the schema:

```ts
createBrowserClient<Database>(url, key, { db: { schema: 'api' } })
```

## Multi-tenancy — the house rule

Every tenant-owned table carries the tenant column (`business_id`); every query, RLS policy, route handler, and server action scopes through it via the caller's **membership**, never a client-supplied id. One business seeing another's data is the worst bug this codebase can ship — treat any shortcut here as a blocker in review.

## Production is human-gated

**Never change production yourself.** That means no deploys, migrations, RLS or schema changes, edge-function deploys, env-var edits, SQL writes, live-mode Stripe calls, or service changes on Render/Vercel/AWS against production, unless the human explicitly approves that specific action in this conversation. Approval for one action doesn't cover the next. Reading production (logs, errors, metrics) is fine when the task needs it.

Default to staging. When a server-side fix (migration, RLS policy, schema change, edge function) is verified on stg, **tell the human it still needs applying to prd** and hand them the exact command or migration. Don't run it. Server-side changes are per-project, so a fix that only reaches stg leaves production broken while staging looks healthy. Flag it every time rather than leaving prd behind silently.

## Dates

- Format dates with `date-fns` — pass an explicit locale for locale-aware output
- Render timestamps client-side or pass a fixed formatted string from the server — naive `toLocaleDateString()` in a server component formats in the *server's* locale/timezone and can hydration-mismatch against the client

## Package manager detection

This toolkit's default is Yarn, but that's a default for *new* projects, not a rule to enforce on an existing one. Before running any install/add/run command, check the existing project's `package.json` `"packageManager"` field and which lockfile is checked in:

- `pnpm-lock.yaml` present, or `"packageManager": "pnpm@..."` → use `pnpm`
- `yarn.lock` present, or `"packageManager": "yarn@..."` → use `yarn`

Running the wrong package manager's install command creates a second, conflicting lockfile and can silently diverge dependency resolution from what CI uses.

## Unit / Component Tests

- Test runner: Vitest; render helper: `@testing-library/react`
- Always wrap renders in a `renderWithProviders` helper that includes the QueryClient provider
- Assert on what the user sees (`screen.getByText`, `screen.getByRole`) — never on internal state
- Run `/react-web-plugin:testing` for canonical test patterns and provider setup
