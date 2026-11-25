---
name: launch-security-check
description: Quick pre-launch security check for Next.js + Supabase + Stripe apps. Finds public tables without row level security, service-role or secret keys reaching client code (NEXT_PUBLIC_ variables, 'use client' files), and Stripe webhook handlers without constructEvent signature verification. Use when the user asks for a launch, ship or go-live security check, or a quick security pass on a Supabase/Stripe app.
allowed-tools: Read Grep Glob
---

# launch-security-check

Read-only review. Don't edit files unless the user asks for the fixes afterwards. Every grep hit is a lead: open the file and confirm it before you report it.

## L1: Public tables without RLS (critical)
Only tables in the `public` schema (or another schema you expose through the Data API) count. Ignore `private.`, `auth.` and other schemas. Search across lines (multiline), case-insensitive, because SQL statements can wrap.
1. Grep `supabase/migrations/` for `create\s+table\s+(if\s+not\s+exists\s+)?(public\.)?"?([a-z_0-9]+)"?` and list the public table names. Skip names qualified with another schema.
2. Grep the same folder for `alter\s+table\s+(only\s+)?(public\.)?"?([a-z_0-9]+)"?\s+enable\s+row\s+level\s+security`.
3. A table from step 1 with no match in step 2 is a finding. Also grep for `disable\s+row\s+level\s+security`: any hit on a public table is a finding.
Fix: `alter table public.<t> enable row level security;` plus policies for the access the app needs. For the full RLS and grants review (R1–R6), use `supabase-rls-review`.

## L2: Service-role or secret keys reaching client code (critical)
1. Grep app code (not `*.md`) for `NEXT_PUBLIC_[A-Z0-9_]*(SERVICE_ROLE|SECRET)`. `NEXT_PUBLIC_` values are bundled into the browser, so any hit is a finding.
2. Grep for client files (pattern `^\s*['"]use client['"]`), then read the top of each one and confirm the directive is the first statement. Comments may come before it. In those files, grep for `service_role|SERVICE_ROLE_KEY|supabase/admin|createAdminClient|supabaseAdmin|STRIPE_SECRET_KEY`. Any hit is a finding.
Fix: use the service-role key and the Stripe secret key only in server code (route handlers, server actions, `server-only` modules), and never with a `NEXT_PUBLIC_` prefix. Rotate any key that was exposed.

## L3: Stripe webhooks without signature verification (critical)
1. Glob `**/*webhook*/**/route.{ts,js,mjs}` (this covers both `app/` and `src/app/`) and `**/pages/api/**/*webhook*.{ts,js}`. Keep the Stripe handlers: the files that match `stripe-signature|constructEvent|stripe\.webhooks|event\.type|checkout\.session\.completed`.
2. Any of those files that has no match for `constructEvent(Async)?\(` is a finding. Read it: it trusts an unsigned request body.
Fix (App Router): `const body = await request.text()`, then `stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET)`, and return 400 on failure. Fix (Pages Router): `export const config = { api: { bodyParser: false } }`, read the raw body into a Buffer, and pass it to `constructEvent`. For idempotency and the raw body (S2, S3, S6, S7), use `stripe-webhook-review`.

## Report
One summary line (files read, findings by severity), then a table of severity, check (L1–L3), file:line, what you saw and the fix, then anything you couldn't verify (for example, tables or policies created in the Supabase dashboard, or keys set only in hosting env vars). A clean result is not proof the app is secure.
