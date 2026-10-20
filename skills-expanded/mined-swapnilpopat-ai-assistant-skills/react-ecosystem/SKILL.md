---
name: react-ecosystem
description: Expert React 19 + Next.js 15 guidance covering Server Components, Actions, Suspense, the React Compiler, data fetching, rendering performance, accessibility, and testing. Use when writing, reviewing, or refactoring React or Next.js code.
source: https://github.com/JetBrains/skills/tree/main/react-best-practices
---

# React Ecosystem

Production-grade React 19 and Next.js 15 (App Router) practices: server/client boundary discipline, Suspense-driven data flow, the React Compiler, Actions for mutations, and a measurable approach to rendering performance, accessibility, and testing.

## Stack Baseline (2026)

| Component | Default | Notes |
| --- | --- | --- |
| React | 19.x | Stable Server Components, Actions, `use`, `useOptimistic`, `useFormStatus`, asset loading, ref as prop. |
| React Compiler | Stable (`babel-plugin-react-compiler`) | Replaces most `useMemo` / `useCallback` / `memo`. |
| Next.js | 15.x (App Router) | Async `cookies()`/`headers()`/`params`, Turbopack dev/prod, Partial Prerendering (PPR), `after()`, `unstable_cache` -> `cacheLife`/`cacheTag` ("use cache"). |
| Build | Turbopack (Next 15) or Vite 6 + `@vitejs/plugin-react`/`@vitejs/plugin-react-swc` | For non-Next apps. |
| Routing (non-Next) | TanStack Router 1.x or React Router 7 (data APIs) | Pick one; do not mix. |
| Data fetching (client) | TanStack Query v5 / SWR 2 | Plus RSC server fetches with `cache`. |
| Forms | React 19 Actions + `useActionState` + `useOptimistic` | No third-party form lib needed for most cases. |
| State | Zustand / Jotai / Redux Toolkit (rare) | Server state lives in cache (TanStack Query / RSC), not Redux. |
| Styling | Tailwind 4 + CSS modules, or vanilla-extract | CSS-in-JS runtime libs (styled-components, emotion) struggle with RSC; prefer compile-time. |
| Testing | Vitest + React Testing Library + Playwright | Jest still works; Vitest is faster. |
| TypeScript | 5.6+, `strict: true` | Required. |

## When to Use

- New React/Next.js component or route.
- Refactoring large components, hooks, or fetching code.
- Reviewing the server/client boundary in an App Router project.
- Optimizing bundle size, hydration cost, INP, or re-renders.
- Migrating from Pages Router to App Router, or React 18 -> 19.

## Instructions

### 1. Decide the Runtime Model First

Before writing code, classify:

| Runtime | When | Implication |
| --- | --- | --- |
| Pure client SPA (Vite + React) | Browser-only app, embedded widget, internal tool | All code ships to browser; data fetched in client; use TanStack Query |
| SSR/SSG without RSC (Remix v2, older Next Pages) | Legacy or non-RSC stack | Loaders + actions; document choice |
| RSC + Streaming (Next 15 App Router, Remix/React Router v7 with RSC) | New full-stack web apps | Default to **Server Components**; opt into client with `"use client"` |

In an RSC app, **Server Components are the default**. Add `"use client"` only when you need interactivity, browser-only APIs, or React state/effects.

### 2. Server Components: Default to the Server

```tsx
// app/products/[id]/page.tsx  - Server Component (no "use client")
import { db } from "@/lib/db";
import { ProductGallery } from "./product-gallery";        // Client Component
import { AddToCartButton } from "./add-to-cart-button";    // Client Component
import { Suspense } from "react";
import { Reviews } from "./reviews";

export default async function ProductPage({
  params,
}: { params: Promise<{ id: string }> }) {
  const { id } = await params;                              // Next 15: async
  const product = await db.product.findOrThrow(id);

  return (
    <main>
      <h1>{product.name}</h1>
      <ProductGallery images={product.images} />
      <AddToCartButton productId={product.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={product.id} />                  {/* Streams in */}
      </Suspense>
    </main>
  );
}
```

Rules:

- Server Components can be `async` and `await` data directly. Forget `useEffect` for fetching.
- Pass only **serializable** props to Client Components (no functions, Dates outside JSON, class instances).
- Never import a Server Component from a Client Component (top-down only). Pass server-rendered content as `children` instead.
- Keep secrets and DB clients in server-only modules. Add `import "server-only";` to enforce.

### 3. Eliminate Waterfalls with Parallel Fetches and Suspense

```tsx
// BAD: sequential awaits create a waterfall
const user = await getUser(id);
const posts = await getPosts(user.id);   // can be parallel if posts only needs id
const orders = await getOrders(id);

// GOOD: start all independent work; await together
const [user, posts, orders] = await Promise.all([
  getUser(id),
  getPosts(id),
  getOrders(id),
]);
```

Suspense boundaries split rendering so slow data does not block fast data:

```tsx
<Suspense fallback={<HeaderSkeleton />}>
  <Header />
</Suspense>
<Suspense fallback={<FeedSkeleton />}>
  <Feed />
</Suspense>
```

In Next 15, enable **Partial Prerendering** (PPR) to ship static shell + streamed dynamic regions from one route.

### 4. Cache and Dedupe on the Server

In RSC, fetches are deduplicated within a request via React's `cache` and the Next data cache.

```tsx
// lib/get-user.ts
import "server-only";
import { cache } from "react";

export const getUser = cache(async (id: string) => {
  return db.user.findOrThrow(id);
});                                                          // dedupes per request
```

Next 15 directive-based caching ("use cache"):

```tsx
// app/products/page.tsx
import { unstable_cacheLife as cacheLife, unstable_cacheTag as cacheTag } from "next/cache";

async function getFeaturedProducts() {
  "use cache";
  cacheLife("hours");
  cacheTag("products", "featured");
  return db.product.featured();
}
```

Invalidate with `revalidateTag("products")` from a Server Action.

### 5. Mutations: Server Actions + `useActionState` + `useOptimistic`

```tsx
// app/cart/actions.ts
"use server";
import { revalidateTag } from "next/cache";
import { z } from "zod";

const addSchema = z.object({ productId: z.string().uuid(), qty: z.coerce.number().int().min(1).max(99) });

export async function addToCart(prev: ActionState, formData: FormData): Promise<ActionState> {
  const parsed = addSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { ok: false, error: parsed.error.flatten().fieldErrors };

  const session = await requireSession();                    // authn at every action entry
  await db.cart.add(session.userId, parsed.data);
  revalidateTag(`cart:${session.userId}`);
  return { ok: true };
}
```

```tsx
// app/cart/add-to-cart-button.tsx
"use client";
import { useActionState, useOptimistic } from "react";
import { useFormStatus } from "react-dom";
import { addToCart } from "./actions";

export function AddToCartButton({ productId }: { productId: string }) {
  const [state, formAction] = useActionState(addToCart, { ok: false });
  return (
    <form action={formAction}>
      <input type="hidden" name="productId" value={productId} />
      <input name="qty" type="number" min={1} defaultValue={1} aria-label="Quantity" />
      <SubmitButton />
      {state.error && <p role="alert">{state.error.qty?.[0]}</p>}
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button type="submit" disabled={pending}>{pending ? "Adding..." : "Add to cart"}</button>;
}
```

Optimistic UI for instant feedback:

```tsx
const [optimisticItems, addOptimistic] = useOptimistic(items, (state, item) => [...state, item]);
```

Always (1) authenticate in the action, (2) validate input with zod/valibot, (3) authorize the resource, (4) `revalidateTag` or `revalidatePath`.

### 6. Client Data Fetching with TanStack Query v5

For client components that fetch from your API:

```tsx
"use client";
import { useQuery } from "@tanstack/react-query";

export function ProductReviews({ productId }: { productId: string }) {
  const { data, isPending, error } = useQuery({
    queryKey: ["reviews", productId],
    queryFn: ({ signal }) => fetch(`/api/products/${productId}/reviews`, { signal }).then(r => r.json()),
    staleTime: 60_000,
  });
  if (isPending) return <ReviewsSkeleton />;
  if (error) return <p role="alert">Failed to load reviews.</p>;
  return <ReviewList items={data} />;
}
```

Rules: always pass `signal` for cancellation; tune `staleTime` (>0) to prevent thundering refetches; use `placeholderData: keepPreviousData` for paginated UIs.

### 7. The React Compiler: Stop Hand-Memoizing

With the React Compiler enabled (`babel-plugin-react-compiler` or Next 15's built-in flag), most `useMemo` / `useCallback` / `React.memo` becomes unnecessary - the compiler memoizes for you.

```jsonc
// next.config.ts
export default { experimental: { reactCompiler: true } };
```

Anti-patterns it makes obsolete:

- Wrapping every callback in `useCallback`.
- `useMemo` on cheap computations.
- `React.memo` on every leaf component "just in case".

What still matters: stable component boundaries, splitting state, and keeping render-time pure.

### 8. State: Derive in Render, Not in Effects

```tsx
// BAD: effect derives state from props -> double render, drift risk
const [full, setFull] = useState("");
useEffect(() => setFull(`${first} ${last}`), [first, last]);

// GOOD: derive directly
const full = `${first} ${last}`;
```

Use `useEffect` only for: subscribing to external systems, syncing with non-React stores, focus/scroll side-effects, manual DOM measurements.

For complex client state, prefer Zustand or Jotai over Redux. For server data, do **not** mirror it into Redux - cache it (TanStack Query / RSC).

### 9. Performance: Concurrent React + Web Vitals

- **`useTransition` / `startTransition`** for non-urgent updates (filter changes, tab switches).
- **`useDeferredValue`** for keeping input snappy while a heavy list re-renders.
- **List virtualization**: `@tanstack/react-virtual` for >200 rows.
- **Code splitting**: `React.lazy` + Suspense for routes; in Next, route segments split automatically.
- **`<Image>`** (Next) and `loading="lazy"` for off-screen images. Always provide `width`/`height` to prevent CLS.
- **`<Script strategy="afterInteractive" | "lazyOnload">`** for third-party scripts.
- **Preloading**: React 19 ships `prefetchDNS`, `preconnect`, `preload`, `preinit` exports - use them for critical fonts and scripts.

Targets (Core Web Vitals 2026):

- **LCP** <= 2.5s, **INP** <= 200ms, **CLS** <= 0.1.
- Measure in the field with `web-vitals` -> your analytics; don't rely on Lighthouse alone.

### 10. Accessibility (Non-Negotiable)

- Semantic HTML first (`<button>`, `<nav>`, `<form>`); ARIA only when there is no native equivalent.
- Visible focus indicators; never remove `:focus-visible`.
- Form fields paired with `<label>`; error text linked via `aria-describedby` and `role="alert"`.
- Live regions for async updates (`aria-live="polite"`).
- Color contrast 4.5:1 for body text (WCAG 2.2 AA).
- Lint with `eslint-plugin-jsx-a11y` (in `next/core-web-vitals` config) and test with Axe in CI (`@axe-core/react` or Playwright `axe-playwright`).

### 11. Security Checklist

- Never inject untrusted HTML via `dangerouslySetInnerHTML` without sanitization (DOMPurify).
- Always validate and authorize inside Server Actions - the form is public.
- Set CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` (Next: `headers()` in `next.config.ts`).
- Don't ship server-only env vars; only `NEXT_PUBLIC_*` is exposed to the client.
- Sanitize URLs used in `<a href>` (no `javascript:` URLs).
- See OWASP Top 10 for Web (2021) - and Top 10 for LLM Apps (2025) if you ship AI features.

### 12. Testing Strategy

| Tier | Tooling | Use for |
| --- | --- | --- |
| Unit | Vitest + RTL | Pure components, hooks (`renderHook`), reducers |
| Integration | Vitest + RTL + MSW (mock HTTP) | Components with data fetching |
| E2E | Playwright | Critical user flows across browsers |
| Visual | Playwright snapshots / Chromatic | Design-system regressions |
| A11y | Axe in unit + E2E | WCAG smoke check |

Always test from the **user's perspective** (`getByRole`, `getByLabelText`), not implementation details. Avoid `getByTestId` unless nothing else fits.

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| Adding `"use client"` to the page root | Whole tree ships to browser; loses RSC benefits | Push `"use client"` down to leaves |
| Importing a Server Component into a Client Component | Doesn't work; subtle bundling errors | Pass via `children` prop |
| `useEffect` to fetch on mount in Next App Router | Double-render, no SSR data | Fetch in the Server Component or use `use(promise)` |
| `useEffect` -> `setState` to derive from props | Extra render, drift | Compute during render |
| Wrapping everything in `useMemo` / `useCallback` | Adds cost, no benefit; dead code with Compiler | Trust Compiler; measure if unsure |
| Defining child component inside parent function | New type each render -> remount | Hoist out or to module scope |
| Not passing AbortSignal to fetch | Stale responses race in | Forward `signal` from query/effect |
| Shipping unsanitized HTML | XSS | DOMPurify or strip |
| Server Action without authn/validation | Anyone can call it | `requireSession` + zod first lines |
| Using `cookies()` / `headers()` / `params` synchronously in Next 15 | Throws | They are async - `await` them |
| Mirroring server data into Redux | Two sources of truth | TanStack Query / RSC cache only |
| Inline arrow handlers in big lists | Many handlers, fine in most cases - but keep keys stable | Stable `key={item.id}` always |

## Output Format

When applying this skill, deliver:

1. Runtime model classification (RSC / SSR / SPA).
2. Component boundary plan (which components are server, which client, why).
3. Data flow diagram (server fetch + Suspense + actions).
4. Caching/revalidation plan (`cacheLife`, `cacheTag`, or TanStack Query keys).
5. Performance budget (LCP/INP/CLS targets, bundle size).
6. A11y checklist results (axe pass, keyboard nav, contrast).
7. Test coverage plan (unit + integration + E2E + a11y).

## Authoritative References

- React 19 docs: https://react.dev/
- React Server Components: https://react.dev/reference/rsc/server-components
- React Compiler: https://react.dev/learn/react-compiler
- Next.js 15 docs: https://nextjs.org/docs
- Next.js App Router: https://nextjs.org/docs/app
- Next.js caching: https://nextjs.org/docs/app/building-your-application/caching
- Partial Prerendering: https://nextjs.org/docs/app/building-your-application/rendering/partial-prerendering
- TanStack Query v5: https://tanstack.com/query/latest/docs
- TanStack Router: https://tanstack.com/router/latest/docs
- React Router v7: https://reactrouter.com/
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- Vitest: https://vitest.dev/
- Playwright: https://playwright.dev/
- Web Vitals (`web-vitals` library): https://github.com/GoogleChrome/web-vitals
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- OWASP Top 10: https://owasp.org/Top10/
- MDN Web Docs: https://developer.mozilla.org/