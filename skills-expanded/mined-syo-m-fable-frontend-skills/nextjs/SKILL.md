---
name: nextjs
description: Next.js App Router conventions — routing and adding pages, Server/Client Components, data fetching, caching, Server Actions, route handlers, metadata, env vars. Use for any work inside a Next.js app. 日本語の依頼例:「Next.jsで〜」「ページを追加/新規作成して」「ルーティング」「Server Action」「ルートハンドラ」「RSC/サーバーコンポーネント」「キャッシュ」。
---

# Next.js (App Router)

Check the installed Next.js major version (`package.json`) before using version-specific APIs — caching semantics changed significantly across 14 → 15 → 16.

## Server vs Client Components

- Server Components are the default. Add `'use client'` only at interaction leaves (event handlers, state, browser APIs) — never on layouts/pages wholesale.
- Push client boundaries down: pass Server Component output as `children` into client wrappers instead of converting whole trees.
- Never import server-only modules (DB clients, secrets) into client files. Add `import 'server-only'` to modules that must never reach the client.

## Data fetching

- Fetch in Server Components, close to where data is used. React deduplicates identical `fetch` calls per request; wrap non-fetch data access in `cache()` if called from multiple components.
- Parallelize independent fetches (`Promise.all` or separate components + Suspense). Sequential awaits are the #1 RSC perf bug.
- Use `loading.tsx` / `<Suspense>` for streaming; `error.tsx` per route segment; `notFound()` for missing resources.

## Caching

- Be explicit, never rely on remembered defaults (they changed between versions). Always state the intended behavior: static, revalidated (`revalidate`/`cacheLife`), or dynamic.
- Never cache per-user or personalized responses (`Cache-Control: no-store` / dynamic rendering) — a cached per-user response is a data leak, not a perf win.
- Tag cached data (`cacheTag` / fetch tags) and invalidate after mutations — do not sprinkle `router.refresh()` as a fix. Pick deliberately: `updateTag` (Server Actions only, read-your-writes for the acting user) vs `revalidateTag` (SWR-style; accepts a cacheLife profile in Next 16).

## Server Actions — treat as public HTTP endpoints

Every action, no exceptions:

1. **Authenticate**: verify the session inside the action (middleware is not sufficient — actions are directly invokable).
2. **Authorize**: check the user may act on *this* resource (IDOR check on every ID argument).
3. **Validate**: parse all arguments with zod before use. `FormData` fields are `unknown`, not `string`.
4. Return typed results (`{ ok: true, data } | { ok: false, error }`); never throw raw DB/internal errors to the client.
5. After mutation: `revalidateTag`/`revalidatePath`, then `redirect()` if needed (note: `redirect` throws — call it outside try/catch).

## Route Handlers

Same auth/validation rules as Server Actions, plus: **route handlers get NO built-in CSRF protection** (the Origin check covers Server Actions only) — cookie-authenticated mutations need explicit Origin validation or a CSRF token, and webhook endpoints need signature verification (see `frontend-security`). Use route handlers only for genuine API needs (webhooks, third-party callbacks, non-React clients) — prefer Server Components for reads and Actions for mutations.

## Env vars

- `NEXT_PUBLIC_*` is compiled into the client bundle — public by definition. Everything secret: no prefix, read only in server code.
- Never pass secret-bearing objects as props to client components. Consider `experimental_taintObjectReference` for sensitive models.

## Routing & misc

- Use `<Link>` for internal route navigation, `next/image` for images, `next/font` for fonts. Plain `<a>` is CORRECT for external links, downloads, and same-page hash anchors — never wrap those in `<Link>`. No `<img>`, no CSS `@import` of font CDNs.
- Metadata via the `metadata` export / `generateMetadata` — not manual `<head>` tags.
- `useSearchParams` requires a Suspense boundary; forgetting it de-optimizes the whole page.
- Dynamic route params: validate (zod) before use — they are user input.
