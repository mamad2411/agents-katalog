---
name: vibe-security
description: Security guardrails for AI-built (vibe-coded) web apps using Supabase, Firebase, Stripe or AI APIs. Use when writing or reviewing auth, database queries, Supabase RLS policies, Firebase rules, migrations, environment variables, API keys or payment code, or before launching an app built with Lovable, Bolt, Cursor, Replit or v0.
license: MIT
metadata:
  author: SealMyApp
  homepage: https://sealmyapp.com
---

# Vibe-coded app security

Apply these rules whenever you touch keys, env vars, database access, auth or payments. If the user asks for something that breaks them, explain the risk and offer the safe alternative.

## 1. Secrets stay on the server
- Never put a secret in client code or in a browser-exposed variable (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `PUBLIC_`, `REACT_APP_`).
- Secret: Stripe `sk_` / `rk_` / `whsec_`, OpenAI or Anthropic `sk-` / `sk-ant-`, Supabase `service_role` / `sb_secret_`, AWS `AKIA`, GitHub `ghp_` / `github_pat_`, Resend `re_`, SendGrid `SG.`, database URLs with passwords, private keys.
- Public by design: Supabase anon / `sb_publishable_` key, Stripe `pk_` key, Firebase web config `apiKey` (but a Gemini `AIza` key is secret).
- Call paid APIs from server code that checks the signed-in user and rate-limits.
- A secret that was ever in the frontend or a public repo must be **rotated first** (new key, revoke old). Removing it from the code is not enough.
- When checking whether a key is safe, look only at its prefix; don't ask the user to paste a whole secret.

## 2. Supabase: RLS on, owner policies, no `using (true)`
- Enable RLS on every `public` table.
- Use owner-based policies with `(select auth.uid())`, scoped `to authenticated`; update policies need both `using` and `with check`.
- Never fix empty results or permission errors with `using (true)`, `with check (true)`, disabling RLS or granting to `anon`. Find out why the owner check fails (not signed in, wrong column) and fix that.
- `using (true)` is only OK on SELECT for genuinely public data, never for writes or personal data.
- Keep the `service_role` / secret key server-only.
- Users must not be able to update their own role, plan, credits or admin flags.
- API-exposed views use `security_invoker = true`; private files go in private buckets.

Example owner policy:

```sql
alter table public.notes enable row level security;
create policy "notes: read own" on public.notes
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "notes: update own" on public.notes
  for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
```

## 3. Firebase: lock the rules
- No test-mode rules (`allow read, write: if true;` or the date-limited test rule).
- Rules check `request.auth != null` and `request.auth.uid` against the owner field.

## 4. Server code and payments
- Every API route, server action and edge function checks the signed-in user and ownership; admin routes check the role on the server.
- Prices and paid status come from the server or a verified payment webhook, never from the client.

## Free tools
- MCP server with an offline key checker, Supabase RLS audit SQL, policy templates and a pre-launch checklist: https://github.com/toby7979/sealmyapp-tools
- Browser key checker: https://sealmyapp.com/tools/key-checker
- Supabase RLS audit: https://sealmyapp.com/tools/supabase-rls-audit
- Free ownership-verified scan of an app you own: https://sealmyapp.com
