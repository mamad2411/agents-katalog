---
name: auth-simple
description: Protect parts of an Astro 7 site on Cloudflare Workers Static Assets with the least auth that does the job — a ladder from no auth at all to a real user portal. Use when password-protecting a site or section, gating a staging or preview deployment, adding a login for a client portal, protecting an admin area, or letting CI reach a protected environment. The ladder — Cloudflare Access at the Worker level (free for 50 users, covers workers.dev and previews), service tokens for CI, Supabase Auth only when real users own real data. Explains why the Basic Auth Worker example is non-production, why a custom cookie gate via run_worker_first bills every protected request, and Supabase's nodejs_compat requirement on Workers. Trigger on password protect, protect the preview, staging auth, client portal login, Cloudflare Access, basic auth, or gate a section. Not for security headers or CSP (web-security-headers), row-level security on data (data-layer), or the CMS OAuth worker (cms-self-edit).
---

# Simple Auth — protecting parts of a static site

> A THIN skill. The default for this catalog's archetype (marketing sites) is rung 0: no auth at all — auth exists on this stack to protect PREVIEWS, admin surfaces, and client portals, not public pages. Every rung up the ladder is a managed product before it is custom code; the one hand-rolled option Cloudflare documents is explicitly labeled not-for-production, and the custom alternative quietly bills every protected request. The anchor of this skill (Worker-level Access) shipped 2026-08-14 — days old at authoring — so it carries this catalog's most aggressive review-gate alongside Flagship.

## Contents

- The ladder
- Rung 1 — Cloudflare Access at the Worker level
- Rung 2 — Service tokens for CI and automation
- Rung 3 — Supabase Auth for a real portal
- The non-options
- The billing trap of a custom gate
- Pins and review-gates
- Limitations

## The ladder

| Rung | Mechanism | For | Cost |
|---|---|---|---|
| 0 | Nothing | Public marketing pages — the archetype default | Zero |
| 1 | Cloudflare Access, attached to the Worker | Humans reaching previews, staging, an admin surface, a gated section | Free plan covers 50 users |
| 2 | Access service tokens | CI, smoke tests, automation reaching a protected environment | Included with Access |
| 3 | Supabase Auth | Real users owning real data (a client portal with per-user rows) | Free tier 50,000 MAU |

Climb only when the rung below demonstrably cannot do the job. A "password on the site" brief is rung 1, not a login form; a "clients see their own records" brief is rung 3, and its data half belongs to data-layer's RLS discipline.

## Rung 1 — Cloudflare Access at the Worker level

Since 2026-08-14, an Access policy can attach DIRECTLY to a Worker — no zone-level application, no owned domain required for the workers.dev case. The policy follows the Worker everywhere it serves: routes, custom domains, workers.dev, and preview URLs.

The real model (field-burned 2026-08-18 on the catalog fixture): an Access application carries DESTINATIONS, and the destination type decides the blast radius —

| Destination | Protects | Use for |
|---|---|---|
| `worker` (worker_id) | EVERY request routed to the Worker: routes, custom domains, workers.dev, previews | a Worker that serves nothing public |
| `preview_worker` | only the Worker's preview URLs | gating branch previews while production stays public |
| `public` (host + path, wildcards) | just that host/path | a section — `/admin` on one preview host |

`preview_worker` and `public` take PRECEDENCE over `worker`, so narrow apps can carve exceptions out of a broad one. The trap this table exists for: when ONE Worker serves production on a custom domain AND branch previews (the normal Workers Builds shape), attaching the `worker` destination gates PRODUCTION too. "Protect the preview" is `preview_worker`; "protect a section" is `public` with a path — both attach account-level via `POST /accounts/{id}/access/apps` (type `self_hosted`, `destinations`, inline `policies`), which is also the CI-friendly path when the dashboard is not in the loop.

- Identity: One-Time PIN by email needs ONE explicit IdP add on a new org (`POST .../access/identity_providers` `{type: "onetimepin"}` or the dashboard toggle) — new Zero Trust orgs ship with ONLY Cloudflare-as-IdP since 2026-06-18, so "OTP works out of the box" is no longer true (field-verified 2026-08-18). Google/GitHub attach as standard external IdPs. All on the free plan.
- Requirements: Zero Trust enabled on the account (the free plan qualifies). Local dev testing uses the `access.dev` block in wrangler config; runtime identity (email, name) reads via `ctx.access.getIdentity()` when the Worker itself needs to know who came in.
- Scope note: the "no owned zone needed" inference for workers.dev now has field support — the fixture's account-level app with a `public` workers.dev destination referenced no zone anywhere in the flow (burn 2026-08-18). Residual honesty: that account DID own a zone, so a zone-less account remains unproven.
- Documented limitation: Worker-level Access policies do not currently support WebSocket connections — those need the hostname-based (legacy) application instead.
- Interaction with Static Assets: VERIFIED in the fixture burn (2026-08-18) — the Access check runs at the edge in front of the Worker and gated `/admin` on a static-assets+main Worker cleanly: 302 to the org login on all `/admin*` paths, OTP flow through, `CF_Authorization` session cookie, sibling paths untouched.

## Rung 2 — Service tokens for CI and automation

Access service tokens (a Client ID + Client Secret pair) let non-humans through the same policy surface: the caller sends `CF-Access-Client-Id` and `CF-Access-Client-Secret` headers and no login flow happens. This is the answer to "our smoke test cannot log in": the CI job holds the pair as secrets and hits the protected preview directly. Tokens have configurable expiry and are included with Access — no separate product, no separate bill.

## Rung 3 — Supabase Auth for a real portal

When the brief is real users with real data — a client portal, per-customer records — managed identity at the platform layer stops being enough and the stack's existing backend takes over:

- Free tier covers 50,000 monthly active users; password, magic link, OAuth providers, and anonymous sign-in are all on the free plan. Free projects PAUSE after a week of inactivity — relevant for a low-traffic portal; the first visit after a pause fails until the project wakes.
- The SSR package is `@supabase/ssr` (0.12.4 at authoring). On Cloudflare Workers it is NOT zero-friction: without the `nodejs_compat` compatibility flag and a 2025+ `compatibility_date` in wrangler config, it fails at runtime with a "dynamic require of stream" error. Set both before debugging anything else.
- The seam split: this skill owns the LOGIN (who are you); data-layer owns what a logged-in user may read or write (RLS policies keyed to `auth.uid()`). A portal composes both — do not let auth code grow data-access opinions.
- Deploy-shape cost, stated plainly: authenticated pages are per-user by definition, so they render on demand — the portal's routes join `/_actions/*` in the Worker and on the shared invocation budget. A portal inside a mostly-static site keeps the static pages static; only the gated routes move.

## The non-options

- HTTP Basic Auth in a Worker: Cloudflare publishes the example AND labels it not suitable for production, pointing to Access instead. It also needs `nodejs_compat` (the example uses Buffer). Acceptable for a five-minute demo; a client deliverable never ships it.
- Rolling your own session/cookie auth for rung-1-shaped problems: strictly dominated by Access on this stack — Access is free at this scale, audited, and maintained by someone else. Custom auth code is rung-3 territory and even there Supabase owns it.

## The billing trap of a custom gate

A hand-rolled gate in front of static assets means `run_worker_first` on the protected paths — and every matched request (every page, every subresource under the pattern) becomes a billed invocation on the shared 100k/day Free cap, with the 429 failure mode. That is edge-logic's trap 2 wearing an auth costume. Access does its check at the edge in front of the Worker; whether an Access-DENIED request still counts as an invocation is not documented either way — INFERRED that allowed requests to static assets stay on the free asset path when no worker-first pattern matches, but treat the billing interaction as a review-gate item, not a fact.

## Pins and review-gates

| Surface | Pinned fact (2026-08-18) | Review-gate |
|---|---|---|
| Worker-level Access | shipped 2026-08-14; destination types `worker`/`preview_worker`/`public` with narrow-over-broad precedence; `ctx.access.getIdentity()`; no WebSockets. First field burn 2026-08-18 (catalog fixture): path-scoped `public` app on a preview host, OTP end-to-end | MAXIMUM volatility — days old at authoring; plan gating, pricing, and semantics may all move; re-verify before EVERY client use |
| Access free plan | 50 users, $0 | seat definition and cap per plan page |
| Access IdPs | OTP is one explicit IdP add (not preinstalled); Cloudflare-as-IdP is the ONLY default for new orgs since 2026-06-18 (field-verified) | defaults may shift again |
| Service tokens | included with Access; header pair auth | plan-tier language is absent, availability inferred from Access docs |
| `@supabase/ssr` | 0.12.4; needs `nodejs_compat` + 2025+ compatibility_date on Workers | active package, near-monthly; re-pin at adoption |
| Supabase free tier | 50k MAU; projects pause after 1 week idle | pricing page moves; pause behavior bites portals |
| Basic Auth example | documented, labeled non-production | none — it stays a non-option |

## Limitations

- This skill does NOT cover: security headers and CSP (web-security-headers); RLS policy design and data contracts (data-layer); the CMS OAuth worker that cms-self-edit ships (that auth flow is Sveltia's, already solved); payment-gated content (a product decision, per-project).
- Everything above assumes the Workers Free plan and this catalog's mostly-static deploy shape; a fully on-demand app changes the invocation math and probably the auth conversation.
- First field burn: 2026-08-18, the catalog fixture — `/admin` of a Workers Builds branch preview gated via an account-level app (`public` destination with path, OTP policy, created 100% by API), full OTP login verified, sibling paths and CI untouched. The MAXIMUM review-gate stands: one burn is evidence, not stability.
