---
name: ui-stack-next
description: "Building interfaces with Next.js (App Router, 15 and 16): project layout, route groups, parallel and intercepting routes, server components with small client leaves and serialisable props, data fetching and the two caching models (fetch options, cache, use cache and Cache Components, dynamic triggers, Partial Prerendering), server actions with useActionState, loading, error and not-found files, streaming with Suspense, metadata, next/font, next/image, next/link, proxy and middleware redirects, public and server environment variables, reading next build, and Next's own traps. Read when the project uses Next.js."
---

# Next.js (App Router)

The generated Next.js app puts `"use client"` at the top of every page,
fetches its own `/api` routes in `useEffect` behind a spinner, keeps the
starter's font, SVGs and favicon, and grows its client bundle with every
import. React rules apply (`ui-stack-react`) and the server side is in
`backend-stack-next`; these are Next's own: where the client boundary goes,
how data and caching work, the special files, and the built-ins.

## 1. Know the version

Read `next` in `package.json` first, and an API's page in the docs that ship
in `node_modules/next/dist/docs/` (16.2+) rather than recalling it. 16 is
current (16.3 in September 2026) and changed what you will meet:

- `middleware.ts` became `proxy.ts` (exporting `proxy`, on Node.js);
  `middleware.ts` still works, deprecated, for the edge runtime.
- `params`, `searchParams`, `cookies()` and `headers()` are async only.
- `next build` no longer lints and `next lint` is gone; Turbopack is the
  default, and a custom `webpack` config fails the build until migrated.
- Cache Components (`cacheComponents: true`) replace the PPR and
  `dynamicIO` flags; `revalidateTag` takes a second argument.
- `next/image`: `preload` replaces `priority`; quality 75 only, unless
  `images.qualities` lists more. Parallel route slots need `default.tsx`.

## 2. Project layout

```text
app/layout.tsx              <html lang>, fonts, providers
app/globals.css             tokens and base styles, imported once, here
app/(marketing)/layout.tsx  the site frame: header, footer
app/(app)/layout.tsx        the app shell: sidebar, top bar
app/(app)/orders/page.tsx   loading.tsx and error.tsx beside it
components/ui/  components/orders/   primitives, then feature parts
server/                     data access, `import "server-only"` in each
proxy.ts                    middleware.ts before 16
```

- `app/layout.tsx` holds `<html lang="...">`, the fonts, and the header and
  footer every page shares. Route groups give different frames without
  appearing in the URL; a `_components` folder is private, never a route.
- Parallel routes (`@panel`) for panes that load and fail on their own;
  intercepting routes (`@modal/(.)photos/[id]`) for a record opened as a
  modal over its list with its own URL. Only where that URL behaviour is
  wanted; a dialog's open state is simpler.
- Every link in the navigation points at a route that exists.

## 3. Server by default, small client leaves

- Components are server components by default. `"use client"` goes on the
  small interactive leaves (a menu button, a form, a chart), never at the
  top of a page or layout: everything a client file imports ships.
- Props into a client component are serialisable: plain objects, arrays,
  strings, numbers, booleans, `Date`, `Map`, `Set`, promises, server
  actions. Not functions, class instances or database rows: pass the fields
  shown (`backend-stack-next`). Server content goes in as `children`:

```tsx
export default async function OrdersPage() {
  const orders = await listOrders();  // the server-only data layer
  return (
    <FilterPanel>                    {/* "use client": holds its open state */}
      <OrderTable orders={orders} /> {/* still rendered on the server */}
    </FilterPanel>
  );
}
```

- `import "server-only"` in modules holding queries or secrets,
  `import "client-only"` in modules touching `window`: a leak becomes a
  build error.

## 4. Data and caching

- Fetch in server components, close to where the data is shown, through
  the data layer. Never `useEffect` with `fetch("/api/...")` for a page's
  first data, and never a page calling its own route handler.
- Start independent reads together (`Promise.all`), or give each slow part
  its own `<Suspense>` so it streams without holding the rest. `cache()`
  from React dedupes a call within one request.

Which caching model runs is in `next.config.ts`:

| | Cache Components (`cacheComponents: true`, 16) | Previous model (15, or the flag off) |
|---|---|---|
| Default | Nothing cached; each route prerenders a static shell and the rest streams in (Partial Prerendering) | `fetch` not cached; a route is static unless it reads request data |
| To cache | `"use cache"` at the top of the function or component, with `cacheLife("hours")` and `cacheTag("orders")` | `fetch(url, { next: { revalidate: 3600, tags: ["orders"] } })`, `unstable_cache` for other reads, `export const revalidate` |
| `cookies()`, `headers()`, `searchParams` | Read inside `<Suspense>`; only that part waits | The whole route becomes dynamic |
| `Date.now()`, random ids | After `await connection()`, inside Suspense | A dynamic route, or `export const dynamic = "force-dynamic"` |

Arguments and captured values become part of a `"use cache"` key: never
cache one user's data under a shared key. Say in the report what is cached,
for how long, and what is dynamic.

## 5. Mutations: server actions and forms

Server actions (`"use server"`) for the app's own forms and buttons; route
handlers for webhooks, other clients and files (`backend-stack-next`).
Every action validates its input and checks the user.

```ts
"use server"; // app/(app)/orders/actions.ts
import { z } from "zod";
import { updateTag } from "next/cache";
import { redirect } from "next/navigation";
import { insertOrder, requireUser } from "@/server/orders";
const Order = z.object({ title: z.string().trim().min(1, "Give the order a title.") });
export type OrderState = { errors?: { title?: string[] }; title?: string };
export async function createOrder(_: OrderState, data: FormData): Promise<OrderState> {
  const user = await requireUser();
  const parsed = Order.safeParse({ title: data.get("title") });
  if (!parsed.success) {
    return { errors: z.flattenError(parsed.error).fieldErrors, title: String(data.get("title") ?? "") };
  }
  const order = await insertOrder(user, parsed.data);
  updateTag("orders"); // revalidatePath("/orders") before 16
  redirect(`/orders/${order.id}`);
}
```

```tsx
"use client"; // app/(app)/orders/new/order-form.tsx
import { useActionState } from "react";
import { createOrder } from "../actions";
export function OrderForm() {
  const [state, action, pending] = useActionState(createOrder, {});
  return (
    <form action={action}>
      <label htmlFor="title">Title</label>
      <input id="title" name="title" defaultValue={state.title}
        aria-invalid={!!state.errors?.title} aria-describedby="title-error" />
      <p id="title-error">{state.errors?.title?.[0]}</p>
      <button type="submit" disabled={pending}>{pending ? "Creating..." : "Create order"}</button>
    </form>
  );
}
```

- `redirect()` and `notFound()` throw: call them outside `try`/`catch`.
- After a write: `updateTag(tag)` in an action (16) shows the user their
  change at once; elsewhere, `revalidateTag(tag, "max")` or `revalidatePath`.
- Pending: `useActionState`'s third value, or `useFormStatus` in a child of
  the form; `useOptimistic` for a list that changes before the server
  answers. React resets an uncontrolled form after its action: on a
  failure, return the values and feed them back as `defaultValue`.
- A form that only navigates (search, filters) is `<Form action="/search">`
  from `next/form`: the query lands in the URL and the route is prefetched.

## 6. Loading, errors and not found

- `loading.tsx` in each segment that loads data: a skeleton of the real
  layout (the same header and columns), not a centred spinner.
- `error.tsx` (`"use client"`) says what failed in words and offers a retry
  (`retry()` from 16.3, `reset()` before); it does not cover its own
  segment's layout. `global-error.tsx` covers the root layout with its own
  `<html>` and `<body>`, without the global styles or the theme.
- `notFound()` renders the nearest `not-found.tsx`; `app/not-found.tsx`
  offers a way back. Expected failures are returned and shown, not thrown
  (`frontend-errors`); `catchError` from `next/error` (16.3) puts a
  boundary with a retry around one part of a page.

## 7. Metadata, fonts, images, links

```tsx
// app/layout.tsx; the root element: <html lang="en" className={`${display.variable} ${sans.variable}`}>
import type { Metadata } from "next";
import { Newsreader, Public_Sans } from "next/font/google"; // the faces DESIGN.md names
const display = Newsreader({ subsets: ["latin"], variable: "--font-newsreader" });
const sans = Public_Sans({ subsets: ["latin"], variable: "--font-public-sans" });
export const metadata: Metadata = {
  metadataBase: new URL("https://[domain]"),
  title: { default: "[Product]", template: "%s · [Product]" },
  description: "[What it does, in one sentence]",
};
```

- A title and description per page: `export const metadata`, or
  `generateMetadata` when they depend on data (`params` is a promise; share
  the page's read through `cache()`). `opengraph-image.tsx`, `icon.svg`,
  `sitemap.ts` and `robots.ts` are files in `app/` (`frontend-seo`).
- Fonts only through `next/font` (`google` or `local`), self-hosted at
  build and exposed as CSS variables; never a `<link>` or `@import` to
  Google Fonts. Map them under another name (`@theme inline { --font-display:
  var(--font-newsreader); }`): a variable set to itself is invalid.
- Images with `next/image`: `width` and `height`, or `fill` with `sizes` in
  a positioned parent; `sizes` that match the layout (`"(min-width: 1024px)
  50vw, 100vw"`); `preload` (`priority` before 16) or `fetchPriority="high"`
  on the one image that is the largest thing on first view, and on no
  other; remote hosts in `images.remotePatterns` (`ui-part-images`).
- Internal links with `next/link`; they prefetch in production as they
  scroll into view. `prefetch={false}` on long lists of row links;
  `useLinkStatus()` inside a link for a pending hint on a slow route.

## 8. Proxy, and environment variables

```ts
// proxy.ts (16); before it, middleware.ts exporting `middleware`
import { NextResponse, type NextRequest } from "next/server";
export function proxy(request: NextRequest) {
  if (request.cookies.has("session")) return NextResponse.next();
  const login = new URL("/login", request.url);
  login.searchParams.set("next", request.nextUrl.pathname);
  return NextResponse.redirect(login);
}
export const config = { matcher: ["/app/:path*", "/settings/:path*"] };
```

- An optimistic redirect, not authorisation: the data layer checks the
  user on every read and write (`backend-auth`). `middleware.ts` runs on
  the edge runtime: no Node APIs, no database driver. The sign-in page
  accepts only a relative `next`, or it is an open redirect.
- `NEXT_PUBLIC_` variables are compiled into the browser bundle at build:
  never a key, and a change needs a rebuild. Server values have no prefix
  and are read in server-only modules; `.env.example` lists the names.

## 9. Styling and traps

- Styling: the project's method (Tailwind, `ui-stack-tailwind` and
  `ui-stack-shadcn`; CSS Modules; or tokens in `app/globals.css`), tokens
  once. Themes: `next-themes` with `suppressHydrationWarning` (`ui-themes`).
- Hydration mismatches: dates formatted in the server's time zone or locale
  (pass `timeZone` and the locale, or format after mount), `Math.random()`
  or `Date.now()` in render (`useId` for ids), `typeof window` branches, a
  `<div>` in a `<p>`. `suppressHydrationWarning` only where it is meant.
- One import pulling a whole library into a client file (charts, dates, a
  barrel of icons): import the one function, load heavy client-only
  widgets with `next/dynamic`, list barrels in
  `experimental.optimizePackageImports`.
- `searchParams` read in a layout (layouts do not get them), `params` read
  without `await`, `cookies().set()` in a server component (only actions
  and route handlers set cookies).

## Check it

- `npm run build` type-checks and prerenders every route; fix what it
  reports. Its table marks each route static (○), prerendered with params
  (●), partially prerendered (◐) or dynamic (ƒ): a page meant to be static
  that shows ƒ reads request data somewhere. Next 15 prints First Load JS
  per route; in 16, `npx next experimental-analyze` (16.1+).
- `npm run lint` for lint (in 16 the build no longer runs it).
- Look at the result with the `preview` tool: `url` `http://localhost:3000/`
  and `start` `npm run dev -- -p 3000`; it starts the server, waits for it
  and stops it afterwards. Caching and streaming differ in dev: check them
  against `npm run build && npm run start`, and in the page source.

## Avoid

`"use client"` at the top of pages; `useEffect` for a page's first data; a
page fetching its own API route; a client component importing the database
client; fonts from a Google `<link>`; `<img>` for content images; `preload`
on several images; auth only in proxy or middleware; a key in a
`NEXT_PUBLIC_` variable; one user's data in a shared cache; `redirect()`
inside `try`; a spinner where `loading.tsx` could show the layout; the
starter's SVGs, font and favicon left in place.
