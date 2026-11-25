---
name: supabase-auth-flows
description: >-
  Use when implementing Supabase Auth: sign up, sign in, OAuth, magic link, password
  reset, session handling, or protected routes. Not for RLS policies only (use
  supabase-rls-and-auth) or Stripe billing.
---

# Supabase auth flows

Pair with **`supabase-rls-and-auth`** — auth identifies the user; RLS enforces data access.

## Session (client)

```ts
const { data: { session } } = await supabase.auth.getSession();
const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
  // sync React state / redirect
});
```

Use `getUser()` for server/edge verification (not `getSession()` alone on untrusted server paths).

## Email/password

- Sign up: `signUp({ email, password, options: { emailRedirectTo } })`
- Sign in: `signInWithPassword`
- Reset: `resetPasswordForEmail` → user lands on `/reset-password` → `updateUser({ password })`

## OAuth

```ts
await supabase.auth.signInWithOAuth({
  provider: "google",
  options: { redirectTo: `${origin}/auth/callback` },
});
```

Callback route: exchange code (handled by Supabase client on redirect) then redirect to app home.

## Magic link

`signInWithOtp({ email, options: { emailRedirectTo } })` — same redirect discipline as OAuth.

## Route protection

- React: guard layouts — no session → `/login`.
- Do not fetch sensitive data before session exists.
- Edge functions: `Authorization: Bearer <jwt>` → `supabase.auth.getUser(jwt)`.

## Profiles

Create `profiles` row on signup via trigger (`postgres-triggers-and-functions`) or first-login upsert.

## Avoid

- Storing session tokens in query strings.
- Custom JWT parsing without Supabase client.
- Skipping email confirmation settings mismatch (document if disabled in dev).

## Checklist

- [ ] Sign out clears client state
- [ ] OAuth redirect URLs in Supabase dashboard match environments
- [ ] Protected routes tested signed-in and signed-out
