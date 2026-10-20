---
name: workos-authkit
description: Integrate WorkOS AuthKit for hosted authentication and session management, with authkit-nextjs helpers, withAuth, middleware, and callback routes. Use when the user adds or debugs AuthKit sign-in.
---

# WorkOS AuthKit

AuthKit is WorkOS's hosted auth UI plus session layer. The app redirects to
AuthKit for sign-in; WorkOS redirects back with a code; the SDK exchanges it
and stores an encrypted session cookie.

## Next.js (App Router): @workos-inc/authkit-nextjs

```bash
npm i @workos-inc/authkit-nextjs @workos-inc/node   # node SDK is a peer dep
```

```bash
# .env.local
WORKOS_API_KEY=sk_...                # server-only secret
WORKOS_CLIENT_ID=client_...
WORKOS_COOKIE_PASSWORD=<32+ chars>   # encrypts the session cookie
NEXT_PUBLIC_WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
```

Middleware (session refresh + optional route gating):

```ts
// middleware.ts (proxy.ts on Next.js 16+)
import { authkitMiddleware } from "@workos-inc/authkit-nextjs";
export default authkitMiddleware();
export const config = { matcher: ["/", "/dashboard/:path*", "/auth/callback"] };
```

Secure-by-default variant: `authkitMiddleware({ middlewareAuth: { enabled:
true, unauthenticatedPaths: ["/", "/pricing"] } })` protects every matched
route unless listed.

Callback route (must match the redirect URI configured in the Dashboard):

```ts
// app/auth/callback/route.ts
import { handleAuth } from "@workos-inc/authkit-nextjs";
export const GET = handleAuth();
```

Provider + reading the user:

```tsx
// app/layout.tsx: wrap children in <AuthKitProvider>
import { withAuth, getSignInUrl, signOut } from "@workos-inc/authkit-nextjs";

export default async function Page() {
  const { user } = await withAuth();                       // null if signed out
  // const { user } = await withAuth({ ensureSignedIn: true }); // redirect instead
  if (!user) return <a href={await getSignInUrl()}>Sign in</a>;
  return <form action={async () => { "use server"; await signOut(); }}>...</form>;
}
```

Client components use the `useAuth()` hook. Role and permissions claims ride
on the session: `const { user, role, permissions } = await withAuth()`.

## Other stacks

- Node/serverless: `@workos-inc/node` (v9 line):
  `workos.userManagement.getAuthorizationUrl({ provider: "authkit", clientId, redirectUri })`
  then `workos.userManagement.authenticateWithCode({ code, clientId })`, and
  `loadSealedSession` for cookie-based session verification.
- React SPA: `@workos-inc/authkit-react`; plain JS: `@workos-inc/authkit-js`.
- Python/Ruby/Go/etc. SDKs mirror the same User Management API.

## Session security model

- Session is a sealed (encrypted) cookie; `WORKOS_COOKIE_PASSWORD` must be
  32+ chars, random, and rotated like a secret.
- Access tokens are short-lived JWTs, refreshed automatically by the
  middleware; verify them in APIs against your WorkOS JWKS
  (`https://api.workos.com/sso/jwks/<client_id>`).
- On sign-out call `signOut()` so both the cookie and the WorkOS session end.

## Checklist

- Redirect URI in code, env, and Dashboard must match exactly (scheme, port,
  path).
- Callback route included in the middleware matcher.
- Mutations re-check `withAuth()` server-side; client `useAuth()` state is
  presentation only.
- Add production and staging redirect URIs as separate entries per
  environment (see `workos-setup`).
