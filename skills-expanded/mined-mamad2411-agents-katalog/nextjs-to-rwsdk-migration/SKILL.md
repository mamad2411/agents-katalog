---
name: nextjs-to-rwsdk-migration
description: Port a Next.js 14/15/16 App Router site to RedwoodSDK on Cloudflare Workers without rewriting the component tree. Triggers when a darkmatter Next.js repo needs to move off OpenNext + Alchemy.Worker to rwsdk + Cloudflare.Worker, when someone asks "migrate this Next site to RedwoodSDK / rwsdk / Cloudflare workers without Next", when planning a deploy stack swap away from `@opennextjs/cloudflare`, or when removing `next/link` / `next/image` / `next/navigation` / `next/font` / `next/og` / `next/headers` usage from a TypeScript + React codebase. Also triggers when wiring per-PR preview deploys for a Cloudflare Worker via Alchemy. Do NOT trigger for Pages Router migrations (the App Router conventions don't apply), for non-React frameworks, or for projects that are already on RedwoodSDK and just need feature work.
---

# Migrating Next.js → RedwoodSDK

End-to-end playbook for porting a Next.js App Router site to RedwoodSDK + Cloudflare Workers, derived from the live `darkmatter/web` migration (PR #16, merged 2026-05-26). The shape of that port is the path you should follow for every other darkmatter Next site: scaffold the rwsdk skeleton, shim the Next.js modules so the existing component tree compiles unchanged, do a mechanical per-page port with a codegen helper, then wire Alchemy preview deploys onto a PR-driven CI.

## When to use

- "Migrate `<repo>` to RedwoodSDK" / "drop Next from `<repo>`"
- "Move `<repo>` off OpenNext to rwsdk"
- "Set up Alchemy preview deploys for the rwsdk app"
- "Why doesn't `next/link` / `next/image` / `next/navigation` work in rwsdk?"
- A repo with `next.config.{js,mjs,ts}` + `app/**/page.tsx` and `alchemy.run.ts` pointed at `.open-next/dist/worker.js`.
- A repo that uses `Cloudflare.Vite` and bombs with `rollup: must supply options.input`.

## When NOT to use

- Pages Router (`pages/_app.tsx`, `pages/[slug].tsx`). RedwoodSDK isn't a drop-in for the old routing model; that migration is best done in two passes (Pages → App Router → rwsdk) using Next's own codemod first.
- Non-React frameworks (Vue, Svelte, Solid). RedwoodSDK is React-only.
- An rwsdk repo asking for feature work — read [docs.rwsdk.com](https://docs.rwsdk.com) and skip this skill.
- An OpenNext-only deploy refactor that wants to keep Next as the framework — that's a deploy ADR, not a framework migration.

## Don't invent — follow the docs

RedwoodSDK ships with sharp opinions and their docs are precise about the load-bearing pieces. Before solving a problem from first principles, check:

- [Quick start](https://docs.rwsdk.com/getting-started/quick-start/)
- [Request handling & routing](https://docs.rwsdk.com/core/routing/) — `defineApp`, `route()`, `render(Document, ...)`, params, middleware
- [React Server Components](https://docs.rwsdk.com/core/react-server-components/) — RSC default, `"use client"`, server functions
- [Tailwind CSS](https://docs.rwsdk.com/guides/frontend/tailwind/) — `environments: { ssr: {} }` stub + `?url` CSS import + `<link>` in Document
- [Frontend → Documents](https://docs.rwsdk.com/guides/frontend/documents/), [Metadata](https://docs.rwsdk.com/guides/frontend/metadata/), [Public assets](https://docs.rwsdk.com/guides/frontend/public-assets/)
- [Hosting](https://docs.rwsdk.com/core/hosting/) — what `wrangler.jsonc` should contain
- [Reference: sdk/router](https://docs.rwsdk.com/reference/sdk-router/), [sdk/worker](https://docs.rwsdk.com/reference/sdk-worker/), [sdk/client](https://docs.rwsdk.com/reference/sdk-client/)

Also scaffold a clean reference app in a scratch dir before touching the target repo — it pins the exact file layout the SDK expects:

```bash
mkdir -p /tmp/rwsdk-ref && cd /tmp/rwsdk-ref
bunx create-rwsdk@latest create reference-app -f
```

Copy that app's `src/{worker.tsx, client.tsx, app/document.tsx}`, `vite.config.mts`, `wrangler.jsonc`, `tsconfig.json`, and `types/` into your target as the starting point. Everything else in the target repo is layered on top.

## Migration roadmap

These eight phases are how the `darkmatter/web` port landed in 4 commits + 1 fix-up:

1. **Worktree + clean scaffold.** Branch + worktree off `main`, then drop in the rwsdk scaffold from the reference app. Delete `next.config.*`, `next-env.d.ts`, `middleware.ts`, `open-next.config.ts`, `.next/`, `.open-next/`.

2. **Rewrite the four build-system files.**
   - `package.json` — replace `next` + `@opennextjs/cloudflare` + `next-*` plugins with `rwsdk` (pin exact version), `react-server-dom-webpack`, `@cloudflare/vite-plugin`, `@tailwindcss/vite`. Pin `alchemy` exactly to a known-good version (caret can resolve to a `pipeline-v2-test` tag and brick CI; see `reference/alchemy-deploy.md`).
   - `tsconfig.json` — add `"@/*": ["./*"]` plus alias entries that mirror the Vite shims (`next/link`, `next/image`, …). Force a single `@types/react` + `csstype` via top-level `overrides` + `resolutions` so radix subdeps don't bring in a second copy.
   - `vite.config.mts` — the load-bearing one. `environments: { ssr: {} }` stub (tailwind needs it), `resolve.alias` for every `next/*` module to a local shim, plugins in order: `cloudflare({ viteEnvironment: { name: "worker" } })`, `tailwindcss()`, `redwood()`. See `reference/vite-config.md`.
   - `wrangler.jsonc` — `main: "src/worker.tsx"`, `compatibility_date` matching your old config, `compatibility_flags: ["nodejs_compat", "nodejs_compat_populate_process_env", "global_fetch_strictly_public"]` if you were using nodejs_compat already, `assets.binding: "ASSETS"`.

3. **Shim every `next/*` module via Vite aliases.** This is the trick that makes the migration mechanical instead of file-by-file. Drop seven small shims under `src/shims/` and the existing component tree compiles untouched. See `reference/shims.md` for the full source of each shim.
   - `next/link` → `<a>` wrapper that ignores `prefetch`, `replace`, `scroll`, `shallow`, `locale`.
   - `next/image` → `<img>` wrapper handling `fill`, `width`/`height`, `sizes`, `priority`.
   - `next/navigation` → `usePathname` / `useSearchParams` / `useRouter` backed by `window.location` + `popstate` + `rwsdk:navigation` events. `notFound()` / `redirect()` throw `Response` (rwsdk catches that).
   - `next/font/{google,local}` → return `{ className: "", variable: "--font-xxx", style: {...} }` stubs; the actual fonts come from `@fontsource-variable/*` + `@font-face` in `globals.css`.
   - `next/server` → stub `NextResponse` so any stray import compiles.
   - `next/og` → re-export `ImageResponse` from `@vercel/og`. (Note: `@vercel/og` itself depends on Node APIs that don't all work in the Worker runtime — defer dynamic OG image generation behind a `workers-og` port.)
   - `next/headers` → `headers()` / `cookies()` backed by `rwsdk`'s `requestInfo.request.headers`.

4. **Document + CSS pipeline.** Per the [rwsdk tailwind docs](https://docs.rwsdk.com/guides/frontend/tailwind/):

   ```tsx
   // src/app/Document.tsx
   import styles from "./globals.css?url";
   …
   <link rel="stylesheet" href={styles} />
   ```

   Without the `?url` import + explicit `<link>`, vite emits the CSS into `dist/worker/assets/` (used during SSR only) and the client renders unstyled. This is the most common "production looks broken" trap. See `reference/document-and-css.md` for the full Document template.

5. **Worker + routing.** Build `src/worker.tsx` as a single `defineApp([…])` array: `setCommonHeaders()`, ctx-populating middleware, then one `route()` per top-level path, with all page routes wrapped in `render(Document, [...])`. **Group route families with `layout()`** (from `rwsdk/router`) when the same chrome applies to multiple routes — site header + footer on the public pages, no chrome on a `/wiki/*` section, etc. Layouts are server components and the route-table structure makes the chrome decision explicit instead of a regex inside `Document`. See `reference/worker-and-routing.md` and `reference/layouts.md`. Key conversions:
   - `app/foo/page.tsx` → `src/app/pages/Foo.tsx` (named export, not default)
   - `app/foo/[slug]/page.tsx` → `src/app/pages/Foo.tsx` taking `{ params: { slug: string } }` (NOT `Promise<>`)
   - `app/foo/[[...slug]]/page.tsx` → `src/app/pages/Foo.tsx` taking `{ params: { $0?: string } }` — convert with `params.$0?.split("/").filter(Boolean)` when the page expects `string[]`
   - `app/feed.xml/route.ts` → `src/app/routes/feed.ts`, called from `route("/feed.xml", feedHandler)` at the top of `defineApp` (outside `render(Document, …)`)
   - `app/sitemap.ts` → `src/app/routes/sitemap.ts` returning a `Response` with `Content-Type: application/xml`
   - `middleware.ts` → a function inside `defineApp([…])` that takes `({ request, ctx })` and either returns nothing (continue) or returns a `Response` (short-circuit)
   - `app/(group)/layout.tsx` → `src/app/layouts/X.tsx` exported as a React FC and wired with `layout(X, [...])`. `app/layout.tsx` stays as `src/app/Document.tsx` because it owns the `<html>` shell.

   **Route order inside `layout()` groups matters.** rwsdk matches routes in registration order; literal paths beat `:param` captures. If you have both `/internal/wiki` (literal, often in a no-chrome `WikiLayout`) and `/internal/:slug` (parametric, often in `SiteLayout`), register the `WikiLayout` group FIRST or `/internal/wiki` will be captured as `slug="wiki"` and 404.

6. **Mechanical page port.** Use `scripts/port-page.ts` from this skill (copy it into the target repo's `scripts/`) to strip Next-specific exports from each copied `app/**/page.tsx`:
   - `import type { Metadata } from "next"`
   - `export const metadata = {...}` (typed or untyped)
   - `export async function generateMetadata(...)` (entire function body)
   - `export async function generateStaticParams() {...}`
   - `export const dynamic = "force-dynamic"`, `runtime = "nodejs"`, etc.
   - Converts `params: Promise<{...}>` → `params: {...}` and drops `await params`
   - Renames `export default ...` → `export function ${Name}`

   The script handles ~95% of pages mechanically. Catch-all routes still need a manual `params.$0?.split("/")` conversion. See `reference/per-page-port-checklist.md` for the full list.

7. **Alchemy deploy.** Use `Cloudflare.Worker` (not `Cloudflare.Vite` — see gotcha) pointing at the pre-built `dist/worker/index.js` + `dist/client/` assets. `bun run build` produces both; `alchemy deploy` uploads them as a single Worker. PR-stage logic: skip custom domains when `stage === "dev" || stage.startsWith("pr-")`. See `reference/alchemy-deploy.md` for the full `alchemy.run.ts` template.

8. **Per-PR preview CI.** Two workflows: `preview-deploy.yml` on `pull_request: opened/synchronize/reopened` runs `alchemy deploy --stage pr-N`, parses the `workers.dev` URL from output, smoke-tests it, and stickies a comment via `marocchino/sticky-pull-request-comment@v2`. `preview-cleanup.yml` on `pull_request: closed` runs `alchemy destroy`. Both reuse the repo's existing `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` secrets — no new secrets needed. See `reference/preview-ci.md`.

## Order matters

Don't skip ahead. The shims (phase 3) have to land before the worker + page ports (phases 5–6) or you'll spend hours rewriting `import Link from "next/link"` lines by hand. The build-system rewrite (phase 2) has to land before the shims or vite won't know about the aliases.

If a phase explodes, revert to the previous phase's clean state and figure out what's different from the reference scaffold — that's almost always the source of the drift. The reference app's `vite.config.mts` is 12 lines for a reason.

## Verification gates

Each phase has a "definition of done" the next phase relies on:

- Phase 2 done = `bun install` succeeds.
- Phase 3 done = `tsc` clean on changed files (the shims compile + don't break consumers).
- Phase 4 done = `bun run build` produces both `dist/worker/index.js` and `dist/client/assets/globals-*.css`.
- Phase 5 done = `bun run dev` returns 200 for the home route + at least one nested route.
- Phase 6 done = every ported page returns 200 with no console errors.
- Phase 7 done = `bun alchemy deploy --stage dev` provisions a Worker and the `workers.dev` URL responds.
- Phase 8 done = a draft PR's preview workflow ends green and the sticky comment lands.

Don't claim "done" without driving the deployed preview through a real browser (playwright works fine). Reading the source isn't validation — production-only behavior like CSS bundling shape only shows up when you actually load the page.

## Known traps

These cost real time on the first migration and are worth checking up front:

1. **CSS only emits to `dist/worker` if you `import "./globals.css"` plainly.** The fix is `import styles from "./globals.css?url"` + `<link rel="stylesheet" href={styles} />` in Document. Straight from rwsdk's [tailwind doc](https://docs.rwsdk.com/guides/frontend/tailwind/). Don't invent client-side CSS imports — they don't fix it.

2. **`Cloudflare.Vite` (alchemy 2.0.0-beta.40) injects `@distilled.cloud/cloudflare-vite-plugin` which conflicts with the `@cloudflare/vite-plugin` in your `vite.config.mts`** (needed by `bun run dev`). The build dies with `rollup: must supply options.input`. Until alchemy ships an opt-out, use `Cloudflare.Worker` with pre-built `dist/` artifacts. See `reference/alchemy-deploy.md`.

3. **`^2.0.0-beta.40` resolves alchemy to the `pipeline-v2-test` dist-tag in CI** which is built against an incompatible `effect.Config` API and dies with `a.asEffect is not a function`. Pin exactly: `"alchemy": "2.0.0-beta.40"` (no caret).

4. **Two copies of `@types/react` + `csstype` from radix subdeps break tsc** with `Type 'React.CSSProperties' is not assignable to ...`. Force-resolve via `overrides` + `resolutions` in package.json on `@types/react`, `@types/react-dom`, `csstype`. Then `rm -rf node_modules bun.lock && bun install`.

5. **Wildcard params come as `params.$0: string`, not `params.slug: string[]`.** Catch-all pages need an explicit conversion line at the top of the body. The `port-page.ts` script doesn't do this conversion — handle it by hand.

6. **`Effect.gen(...).pipe(...)` doesn't act as a Promise reliably across Effect versions.** If the legacy code did `const x = await effectReturningFn(...)`, port it to `Effect.runPromise(effectReturningFn(...))` explicitly. Otherwise the failure path silently succeeds and you can leak auth-gated content. (This happened on `/posts` in `darkmatter/web`.)

7. **`fs.readFileSync` for markdown content survives via a pre-generated manifest.** Workers don't ship `fs`. If the Next codebase reads from disk in production (blog posts, wiki pages), it almost certainly already has a `bun scripts/generate-*.ts` step that produces a `*.generated.ts` fallback — keep it as part of `bun run build`.

8. **`next-themes` works as-is, no shim needed.** It's an independent npm package, not a Next.js export.

9. **OG image generation (`opengraph-image.tsx`) is the one thing that doesn't have a clean rwsdk port yet.** `@vercel/og` has Node-only deps. Use `workers-og` or write a dedicated worker route that calls `satori` directly. Defer if it's not blocking launch.

10. **The sticky PR comment action (`marocchino/sticky-pull-request-comment@v2`) needs `pull-requests: write` in the workflow `permissions:` block.** GitHub silently drops the comment if the token doesn't have it.

11. **`bun run dev` intermittently dies at cold startup with `(ssr) No module found for '/node_modules/lucide-react/dist/esm/Icon.mjs' in module lookup for "use client" directive`.** This is a race between rwsdk's directive scanner (which walks the dep graph from `src/` and registers `"use client"` files into a lookup map) and the Cloudflare vite plugin's worker-entry probe (which queries that map before the scanner has finished). It happens with any package that has a deep transitive `"use client"` chain — lucide-react is the most common in our codebases because it reaches `dist/esm/Icon.mjs` (the actual `"use client"` boundary) through several layers of barrel re-exports. **Fix:** pre-register the boundary modules with rwsdk's `forceClientPaths` so they end up in the lookup map before the scanner runs:

    ```ts
    // vite.config.mts
    redwood({
      forceClientPaths: [
        "node_modules/lucide-react/dist/esm/Icon.mjs",
        "node_modules/lucide-react/dist/esm/context.mjs",
        "node_modules/lucide-react/dist/esm/DynamicIcon.mjs",
      ],
    }),
    ```

    See `reference/vite-config.md` for the full list of packages with similar transitive `"use client"` boundaries. One-shot recovery on an already-broken cache: `rm -rf node_modules/.vite && bun run dev`.

## Tools

`scripts/port-page.ts` — one-shot codegen that strips Next.js App Router exports and renames the default export. Copy into the target repo's `scripts/` and invoke per page:

```bash
bun scripts/port-page.ts src/app/pages/Foo.tsx FooPage
```

It's idempotent and editable — read the source before running on a tree of files. Documents what each transform does inline.

## Reference

- `reference/shims.md` — full source of all seven `next/*` shims with rationale and known limits.
- `reference/vite-config.md` — annotated `vite.config.mts` + `tsconfig.json` + `package.json` deltas.
- `reference/document-and-css.md` — `Document.tsx` template, font loading, the `?url` CSS pattern, theming integration.
- `reference/worker-and-routing.md` — `defineApp`, route patterns (static / `:param` / `*`), middleware, `setCommonHeaders`, redirect helpers.
- `reference/layouts.md` — `layout()` from `rwsdk/router`, mapping Next.js `app/(group)/layout.tsx` files to server-component layouts, route-order rules when literal + parametric routes coexist across layouts.
- `reference/per-page-port-checklist.md` — what to strip / convert per `app/**/page.tsx`, plus the cases the codegen script doesn't cover.
- `reference/alchemy-deploy.md` — `alchemy.run.ts` template with `Cloudflare.Worker`, stage-aware domains, env injection, plus the `Cloudflare.Vite` gotcha writeup.
- `reference/preview-ci.md` — `.github/workflows/preview-deploy.yml` + `preview-cleanup.yml` templates with secrets, smoke tests, and the sticky comment.
- `reference/verification-checklist.md` — the eight verification gates in checkable form for self-review or a `requesting-code-review` handoff.
