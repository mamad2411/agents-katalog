# AGENTS.md — `@t/auth`

## What this owns

Clerk-backed identity: JWT verification, current-user projection, webhook sync.
Credential/session lifecycle (sign-up, sign-in, refresh, logout) is delegated entirely
to Clerk's own client SDKs (`@clerk/nextjs`, `@clerk/clerk-expo`). This package owns
server-side token verification and the canonical `AuthProvider` port only.

**Supabase auth is retired.** No `@supabase/auth-helpers-*` imports, no Supabase session
code. Delete on sight.

## Layout

```
packages/auth/src/
  entities/
    ports/      AuthProvider.ts         — abstract port (verify / currentUser / syncFromWebhook)
    schemas/    AuthUserSchema.ts, WebhookEventSchema.ts
    types/      AuthError.ts, AuthProviderOptions.ts, UserSyncCallback.ts
  infrastructure/
    clerk/      ClerkAuthProvider.ts    — live Clerk impl
    noop/       NoopAuthProvider.ts     — test / missing-key fallback
  dependency-injection/
    registerAuthDI.ts                  — registers AUTH token
  index.ts
```

## DI registrar

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\auth\src\dependency-injection\registerAuthDI.ts

```ts
registerAuthDI(container: Container, opts: RegisterAuthDIOptions): void
```

`RegisterAuthDIOptions` requires `config: ConfigRepository` and `environment`.
Optional: `userSync?: UserSyncCallback`, `authorizedParties?: readonly string[]`.

Selection order (first match wins):
1. `environment === "testing"` → `NoopAuthProvider`
2. `!config.auth.clerkSecretKey` → `NoopAuthProvider` + warning log
3. otherwise → `ClerkAuthProvider`

Token key: `dependencyKeys.global.AUTH` (`"auth"`).

## Consumers

- `apps/api` — tRPC middleware resolves `AUTH` to verify tokens and populate `ctx.user`
- `apps/web` — uses `@clerk/nextjs` directly for client-side flows; server reads
  `ctx.user` from tRPC context
- `apps/mobile` — `@clerk/clerk-expo` + SecureStore; forwards `getToken()` JWT to API

Consumers import only `AuthProvider`, `AuthUser`, `AuthError` — never `ClerkAuthProvider`.

## Conventions

- **Clerk-only.** No Supabase auth anywhere. No other identity provider.
- **No client-side token storage.** Clerk owns session cookies (web) and SecureStore
  (mobile). Apps never write raw JWTs to `localStorage` or custom cookie stores.
- **`AuthError` over bare throws.** All auth failures are `AuthError` with a typed
  `AuthErrorCode`. Never `throw new Error("unauthorized")`.
- `verify()` always throws on invalid input — never returns `null` for bad tokens.
- `currentUser()` swallows `AuthError` and returns `null` for unauthenticated callers.
- `authorizedParties` must list all client origins; absent in `testing` env.

## Links

- Auth architecture: docs/architecture/platform/auth.md
- Root conventions: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md
- DI token registry: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\dependency-injection\src\entities\dependencyKeys.ts
