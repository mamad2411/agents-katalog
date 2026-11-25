---
name: calcom-selfhosted-ops
description: Use when operating self-hosted Cal.com/cal.diy bookings.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cal.com, cal.diy, bookings, self-hosted, stripe, google-calendar]
    triggers: [cal.com, cal.diy, self-hosted bookings, booking calendar, cal.your-domain.example]
    related_skills: [self-hosted-communication-server, gateway-troubleshooting]
---

# Self-Hosted Cal.com / cal.diy Operations

Use when working with a self-hosted Cal.com (or cal.diy — the community-edition branding of Cal.com) scheduling instance: connecting Stripe for paid events, connecting Google Calendar/Meet, embedding booking pages in a site, or diagnosing connection errors. Covers the operator's instance at `cal.your-domain.example` (docker container `agency-stack-agency-calcom-1`, image `agency-calcom-custom:v6.2.0`, managed from `${MY_REPOS}\Documents\github\ghl\compose.yaml` + `.env`).

## Key facts

- **cal.diy IS Cal.com** (open-source community edition). Docs: `https://cal.diy` (routes: `/apps/stripe`, `/apps/google`, `/troubleshooting`). Any Cal.com issue applies.
- The Stripe app requires **4 env vars** — if missing, the app shows as "not installed" and connect fails with HTTP 400 on `/api/integrations/stripepayment/add`:
  - `NEXT_PUBLIC_STRIPE_PUBLIC_KEY` = `pk_...` (Stripe Dashboard → Developers → API keys)
  - `STRIPE_PRIVATE_KEY` = `sk_...`
  - `STRIPE_CLIENT_ID` = `ca_...` — REQUIRES activating "OAuth for Standard Accounts" in Stripe Connect settings (most-missed step)
  - `STRIPE_WEBHOOK_SECRET` = `whsec_...` — webhook endpoint `<CAL_URL>/api/integrations/stripepayment/webhook`, subscribe to **all `payment_intent.*` and `setup_intent.*` events**
  - API v2 service additionally wants `STRIPE_API_KEY` (only if a `calcom-api` service exists — plain stacks may not have one)
- **Google Calendar/Meet** requires `GOOGLE_API_CREDENTIALS` = the **full OAuth client JSON** (client_id, client_secret, redirect_uris). An empty `{}` default (compose `:-{}` fallback) means Google connect fails at the handshake. Required pieces:
  - Enable Google Calendar API in Google Cloud Console
  - OAuth Client ID, type **Web Application**
  - Authorized redirect URIs: `<CAL_URL>/api/integrations/googlecalendar/callback` AND `<CAL_URL>/api/auth/callback/google`
  - Scopes: `.../auth/calendar.events`, `.../auth/calendar.readonly`
  - Set `GOOGLE_LOGIN_ENABLED=false` for an internal app
  - Re-seed app store after adding (`pnpm db-seed`) or use the stack's sync script
- **NEXTAUTH_URL must be the bare base URL** (`https://cal.your-domain.example`, no trailing slash, NO `/api/auth` suffix) — a `/api/auth` suffix breaks OAuth callback redirects.
- **Stripe Payment Links (`buy.stripe.com/...`) CANNOT be embedded in an iframe** — Stripe refuses with "Stripe Checkout is not able to run in an iFrame. Please redirect to Checkout at the top level." Use a top-level redirect / new-tab button, or better: make the Cal.com event type a **paid event** so Cal handles payment in its own flow (the operator's preferred pattern).
- **Cal.com booking pages CAN be iframed** (no X-Frame-Options/CSP frame-ancestors block) — `https://cal.your-domain.example/the operator/assessment` embeds fine at ~440px min-height.

## Diagnosis workflow (connection errors)

1. **Check container env** (values redacted): `docker exec <calcom-container> env | grep -iE 'STRIPE|GOOGLE|NEXTAUTH|CALENDSO'` — look for MISSING vars and value SHAPES: `echo "len: ${#GOOGLE_API_CREDENTIALS}"` — a 2-char length means `{}` (empty JSON default).
2. **Check compose wiring**: grep the service's `environment:` block in `compose.yaml`; env vars with `:-}` defaults silently become empty strings.
3. **Check DB state** (what's actually connected): `docker exec <postgres> psql -U calcom -d calcom -c 'select slug, enabled, "dirName" from "App" where slug in (''stripe'',''google-calendar'');'` and `select "appId", count(*) from "Credential" group by "appId";` — a missing Stripe `Credential` row + enabled App row = UI shows connectable but backend has no keys.
4. **Validate compose after edits**: `docker compose config --quiet` (warnings about unset vars are harmless).
5. Check the stack's own docs — the ghl repo documents known Cal.com corrections (`docs/public-stack-startup-and-calcom-app-sync-2026-04-19.md`) and has a sync script `scripts/sync-calcom-apps-from-env.ps1` that enables/disables apps based on env validity (run after adding Google creds).

## Booking modal pattern (static site, calendar-first)

the operator's approved funnel for paid assessments on a static page (<you> index.html):
1. Pricing CTA opens an **on-page modal** (no new page).
2. Phase 1: iframe the Cal.com booking page (`calDiyUrl`) — captures lead name/email/phone at booking. This is the lead-capture play: **calendar first, payment second**; a no-pay booker leaves contact info + a reserved slot for email/SMS/call follow-up.
3. Phase 2: payment. Either a Stripe Payment Link opened **in a new tab** (never iframe), or — the operator's preference — make the Cal.com event type a **paid event** so Cal collects payment during booking, no second phase needed.
4. Config lives in a `TBA_CONFIG` object (or SITE_CONFIG) at the top of the page script: `calDiyUrl`, `stripePayUrl`, with empty-string fallbacks that swap in graceful email fallbacks so the page never looks broken mid-setup.
5. Pitfall: modal HTML must be inserted BEFORE the `<script>` tag or `getElementById` returns null at IIFE execution (script runs at parse time).
6. NO "no payment needed" copy — the flow must read as active ("Payment completes your reservation"), per the operator's instruction.

See `references/<you>-calcom-setup.md` for the <you>-specific state and exact URLs.
