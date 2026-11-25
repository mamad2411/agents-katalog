---
name: secure-a-frontend-app
description: Use when wiring auth/session, protecting routes, or handling secrets in a frontend app — OIDC login via NextAuth + server session store + access-token refresh & injection, route guards + permission-matrix RBAC, SSR cookie propagation + hydration, and vault secrets + public/private config split. React/Next.js reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Secure a frontend app

Auth, session, access control, and secrets for a web app. App structure: `structure-a-frontend-app`;
feature code: `write-frontend-code`.

## 1. Auth & session
- **OIDC via NextAuth.** Configure the provider (with PKCE/nonce checks) in the auth route; store the
  session **server-side** (a session-store adapter, e.g. Redis) rather than a fat JWT cookie.
- **Refresh in the session callback.** On each `session` resolve, check expiry and rotate the access
  token before handing it to the client:
  ```ts
  async session({ session, user }) {
    const acct = await store.getAccount(user.id);
    if (Date.parse(acct.expires_at) < Date.now()) {
      const next = await refreshAccessToken(acct);   // rotate
      session.accessToken = next.access_token;
    }
    return session;
  }
  ```
- **One client-side entry injects the token** into the HTTP client: a `useAuth` hook reads the session
  and calls `BaseHttp.saveToken(session.accessToken)` (the HTTP client is in `write-frontend-code` §2).
- **401 → one queued refresh + replay** at the HTTP layer (the refresh QUEUE in `write-frontend-code`
  §2): concurrent 401s wait on a single refresh, then retry.
▸ *Other stacks:* any OIDC lib (Auth.js / oidc-client) + a server session store; rotate in the session
hook, inject once into the HTTP client, queue-refresh on 401.

## 2. SSR cookie propagation + hydration
- **Pass auth cookies from SSR into the app** via the app-init hook, then read them in providers:
  ```ts
  MyApp.getInitialProps = async (ctx) => ({ cookies: parseCookies(ctx.req), origin: ctx.req.headers.host });
  // _app: <SessionProvider session={pageProps.session}><LocalizationProvider cookies={cookies}>…
  ```
- **Guard token init behind hydration** — don't read the session until the router/session is ready:
  ```ts
  useEffect(() => {
    if (!router.isReady || status === 'loading') return;
    if (session) BaseHttp.saveToken(session.accessToken);
  }, [router.isReady, status]);
  ```
▸ *Other stacks:* read auth cookies server-side, hand to a provider; gate client token use on "ready/mounted".

## 3. Route protection & RBAC
- **Roles + permissions come from one profile hook** (`useMyProfile` → memoized role booleans + a
  `permissions: string[]`). Don't re-derive roles ad hoc per component.
- **Permission matrix as `feature.action` strings.** Gate UI with a checker, routes with a guard:
  ```ts
  // component-level visibility
  can({ feature: 'listing', action: 'create' });   // → permissions.includes('listing.create')
  // route-level (a GuardContainer wrapping the app)
  const allowed = routesForPermissions(permissions).includes(currentRoute);
  if (!allowed && role) { confirm('Access denied'); router.replace(Routes.Home); }
  ```
- **`middleware.ts`** handles edge redirects/rewrites (e.g. a cookie-driven path → canonical route);
  keep it **thin** — real auth/role logic lives in the guard + matrix, not middleware.
▸ *Other stacks:* a route-guard wrapper + a permission map; render-gate by `feature.action`, redirect on deny.

## 4. Secrets & config safety
- **Server secrets from a vault, never the bundle.** Load server-only env from a mounted secrets path
  at boot (fall back to `.env` locally):
  ```js
  // next.config.js
  const paths = ['/vault/secrets/global', '/vault/secrets/app'];
  paths.every(fs.existsSync) ? paths.forEach((p) => dotenv.config({ path: p })) : dotenv.config();
  ```
- **Public vs private split in one Config module** — only `NEXT_PUBLIC_*` (client-exposed) values go in
  the public group; secrets (client secret, store password, service keys) stay server-only. Mark
  server-only vars in `.env.example` ("do not use `NEXT_PUBLIC_` — never expose to the browser").
- A value reaches the browser bundle **only** if it is `NEXT_PUBLIC_`-prefixed AND in the public Config
  group — audit both sides.
▸ *Other stacks:* the framework's public-env prefix + a settings module separating server secrets;
pull secrets from a vault/secret-manager, not committed env.

## Verification
- Login goes through the OIDC provider; tokens are stored server-side; the session callback refreshes
  expiring tokens; the client injects the token once; a 401 triggers one queued refresh + replay.
- Roles/permissions come from the profile hook; UI gates on `feature.action`; a route guard redirects
  on deny; `middleware.ts` stays thin.
- `grep -rn "NEXT_PUBLIC_" src` shows only client-safe values; secrets load from the vault path; no
  secret sits in the public Config group or the client bundle.

## Related
- `write-frontend-code` — the `BaseHttp` 401-refresh queue, SSR guards, config module.
- `structure-a-frontend-app` · `code-conventions` · `release-safety` (backend release/secrets).
