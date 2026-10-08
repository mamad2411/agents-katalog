# Routes — `src/routes/`

File-based routing. **`src/routeTree.gen.ts` is generated** — never edit it
(`.vscode/settings.json` marks it readonly and excludes it from search and the file
watcher). The Vite plugin regenerates it on the fly; `npm run generate-routes` is for a
cold build or after a mass rename.

**Route files hold routing only** — `createFileRoute`, `ssr`, `beforeLoad`,
`validateSearch`, and a component that reads the route's own hooks (`Route.useParams`,
`Route.useSearch`, `Route.useRouteContext`) and passes plain props down. A feature
component takes props instead of calling `Route.useX()`: it keeps TanStack Router's
inference intact and stays movable.

**A component never calls `supabase` directly** — that rule has exactly one exception here:
`_authenticated.tsx`, `login.tsx` and `reset-password.tsx` read the session in
`beforeLoad`, which is a routing concern, not a screen's.

**Route `loader`s are isomorphic** — they run in the browser too. Never touch the database
from one; go through `createServerFn`.

## `__root.tsx`

Acts as the full HTML shell (`<html>`, `<head>`, `<body>`) via `shellComponent`, mounts
`TanStackDevtools` in dev, and carries the `ScriptOnce` that toggles `.dark` before
hydration plus the two `theme-color` metas (see `src/styles/CLAUDE.md` for why they are
written directly in `<head>`).

The context is typed via `createRootRouteWithContext<MyRouterContext>`, so
`context.queryClient` is available in route `loader`s — that is the mechanism for
preloading data server-side rather than fetching inside components.

## SSR

**Back-office routes are `ssr: false`.** The Supabase session lives in the browser, so
running the guard during SSR would conclude "signed out" on every request. Children inherit
the setting and can only make it more restrictive.

**`/m/$venueSlug` must stay SSR** — it is reached by scanning a QR code. It is the only
SSR'd route with data, which has two consequences:

- `src/lib/supabase.ts` is evaluated **on the server too**, and it is a singleton shared
  across requests. Safe only because this page reads as `anon` and never authenticates.
  Opening a server-side session would require a per-request client.
- The route loads through `context.queryClient.ensureQueryData(publicMenuQueryOptions(…))`,
  so the query dehydrates to the client instead of being refetched on hydration.

An unknown slug throws `notFound()` so the response is a real **404**: these URLs are
printed on QR codes.

## `_authenticated.tsx`

A pathless layout route that both guards `/admin` and provides the shell.

- **A `beforeLoad` guard protects the screen, not the data.** Under the RLS design the real
  boundary is Postgres; bypassing the guard grants nothing.
- **`router.invalidate()` must follow sign-in and sign-out**, otherwise `beforeLoad` keeps
  its previous verdict and bounces the user straight back. For sign-in it lives inside
  `useSignIn` rather than in the route: React Query awaits the hook's `onSuccess` before
  the per-call one, so the invalidation is guaranteed to finish before the route navigates.
  Sign-out still does it by hand here, which also navigates.
- **The in-page back links are `lg:hidden`, not deleted.** The sidebar only exists from
  `lg`; below it, « ← Établissements » and « ← Retour à la carte » are the only way out.

## `login.tsx`

**The `redirect` search param is optional and sanitized** (internal paths only, rejecting
`//host`). Keeping the key always present made the router rewrite `/login` to
`/login?redirect=%2Fadmin` on every direct visit.

## `forgot-password.tsx` / `reset-password.tsx`

The two halves of a password reset, and the only two public routes that are not the
customer menu. The domain rules are in `src/features/auth/CLAUDE.md`; what belongs here is
that they do **not** answer the SSR question the same way:

- **`/forgot-password` is server-rendered**, like any page that reads no session. The
  origin the mail must point back to is read in the submit handler, in the browser.
- **`/reset-password` is `ssr: false`** — it reads the session — and **carries no guard**.
  Copying `login.tsx`'s « already signed in → /admin » here would make the screen
  unreachable: the recovery link opens a session before the route is even matched.
- **It is the only route with a `pendingComponent`.** Every other wait in this application
  is a `localStorage` read; this one can be a network round trip, because the client
  fetches the user behind the recovery token before a session exists. `pendingMs` (1s)
  plus the ossature's own 140ms fade means a fast check still shows nothing.
