---
name: nextjs-quality
description: Next.js 16 App Router best practices for this repo. Use when creating routes, layouts, data fetching, metadata, or anything touching the Next.js framework surface.
---

# Next.js Quality

This repo runs **Next.js 16** — newer than most training data. When in doubt about an
API, read the bundled docs in `node_modules/next/dist/docs/` instead of guessing from
memory. Heed deprecation notices.

## Golden rules

- **Server Components by default.** Add `"use client"` only when the component needs
  state, effects, event handlers, or browser APIs — and push that directive as deep into
  the tree as possible (leaf components, not layouts).
- **`next lint` does not exist in Next 16.** Linting is the plain `eslint` CLI
  (`npm run lint`). Never add `next lint` to scripts or docs.
- **Fetch data on the server.** Prefer `async` Server Components and route handlers over
  client-side `useEffect` fetching. Cache deliberately — know whether each fetch is
  static, revalidated, or dynamic.
- **Never leak server code to the client.** Secrets, DB clients, and privileged logic stay
  in Server Components, server actions, or `route.ts` handlers.

## Routing conventions

- New route = `src/app/<segment>/page.tsx`. Route-specific components live next to the
  route; shared components go in `src/components/`.
- Use the special files for their purpose: `layout.tsx` (persistent shell),
  `loading.tsx` (Suspense fallback), `error.tsx` (error boundary, must be a client
  component), `not-found.tsx`.
- Dynamic params and `searchParams` are **async** in Next 16 — `await` them:
  `const { slug } = await params`.
- Navigation uses `next/link`; programmatic navigation uses `useRouter` from
  `next/navigation` (never `next/router`).

## Framework features over hand-rolling

- Images: `next/image` (automatic sizing/optimization) — never bare `<img>`.
- Fonts: `next/font` (already configured with Geist in the root layout).
- Metadata: export `metadata` or `generateMetadata` from pages/layouts — never manual
  `<head>` tags.
- Env vars: server-side via `process.env.X`; browser-visible only with `NEXT_PUBLIC_`
  prefix. Document new variables in `.env.example`.

## Legacy patterns — never introduce

- `pages/` directory, `getServerSideProps`, `getStaticProps`, `getInitialProps`
- `next/head`, `next/router`
- `useEffect` + `fetch` for data that could be fetched on the server
- API routes under `pages/api/` (use `src/app/**/route.ts`)

## Verify

After framework-level changes, run `npm run build` — it type-checks generated route types
and catches invalid segment configs that dev mode tolerates.
