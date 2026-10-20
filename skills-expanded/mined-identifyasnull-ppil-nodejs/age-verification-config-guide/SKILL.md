---
name: age-verification-config-guide
description: Configure site content to require age verification using mandatory AV gate and authenticated ACL routing in this architecture.
intent: >-
  Use this workflow when you need a regen-safe configuration guide that prevents unverified users from viewing site content by combining mandatory AV gate policy and route ACL hardening in site config fragments.
type: workflow
best_for:
  - "Locking down site content behind age verification"
  - "Converting public content routes from anon to authenticated"
  - "Applying mandatory AV gate changes that survive --regen"
scenarios:
  - "Make all Companions content inaccessible without age verification"
  - "Document mandatory AV gate + ACL enforcement as a repeatable config pattern"
  - "Fix bypass paths that still allow pre-verification content access"
license: MIT
metadata:
  version: 1.0.0
  author: Copilot
  category: architecture
  domain: age-verification
  updated: 2026-06-30
---

# Age Verification Config Guide (Regen-Safe)

This guide enforces: **no age verification = no content access**.  
It uses two controls together:
1. `ageVerification` at gateway level
2. `acl: "authenticated"` on content routes

## When to Use

- A site currently exposes content routes as `anon`.
- You need age-gated content enforcement that persists after `node .\launch.js --regen`.
- You need a repeatable config-only pattern (no shared-lib changes).

## Critical Rule: Edit Fragments, Not Assembled Config

Do **not** treat `sites/<site>/site-endpoint-config.json` as the source of truth for durable changes.  
Apply changes in:
- `sites/<site>/config/*/endpoint-config.json` fragments

Otherwise changes are overwritten on regen.

## Configuration Steps

## 1) Enable and tighten mandatory AV gate

File:
- `sites/<site>/config/gateway/endpoint-config.json`

Set:
- `gateway.ageVerification.enabled = true`
- `gateway.ageVerification.fallbackLoginPath` to the site login route
- `gateway.ageVerification.bypassPaths` to legal/public essentials only (for example `/terms-of-use`, `/dmca`)

Remove content/listing bypasses (example: `/ad/list`) so listing endpoints are gated.

## 2) Convert content routes from anon to authenticated

Update content surfaces in fragment configs:
- ads content pages (`config/ads/endpoint-config.json`)
- store pages (`config/store/endpoint-config.json`)
- spotlight/profile content where public today (`config/service-providers/endpoint-config.json`)

Typical route ACL conversions:
- `/search`: `anon` -> `authenticated`
- `/`: `anon` -> `authenticated` (listing/content roots)
- `/details/:id`: `anon` -> `authenticated`
- spotlight routes: `anon` -> `authenticated`

Keep auth/legal flows public (login/signup/recover/terms/dmca) unless business rules require otherwise.

## 3) Preserve auth entry points

Do not lock users out of verification/login:
- login
- signup (if applicable)
- recovery flows
- verification confirm routes

These routes may remain `anon` while content routes become `authenticated`.

## 4) Validate effective policy

Confirm there are no remaining `anon` ACLs on content pages and no bypass path that exposes listings/details pre-verification.

## Companions Reference Implementation

Applied pattern:
1. `sites/companions/config/gateway/endpoint-config.json`
   - `ageVerification.enabled: true`
   - removed `/ad/list` from `ageVerification.bypassPaths`
2. `sites/companions/config/ads/endpoint-config.json`
   - set `/search`, `/`, `/details/:id`, `/spotlight/article/:id` to `authenticated`
3. `sites/companions/config/store/endpoint-config.json`
   - set `/` and `/details/:id` to `authenticated`
4. `sites/companions/config/service-providers/endpoint-config.json`
   - set `/spotlight/profile/:id` routes to `authenticated`

## Troubleshooting

1. **Content still visible to unverified users**
   - Cause: one or more content routes still `acl: "anon"` in fragments.
   - Fix: scan fragment configs for `route` + `acl` pairs and convert remaining content endpoints.

2. **Works until --regen, then reverts**
   - Cause: edits made only to assembled `site-endpoint-config.json`.
   - Fix: apply same edits to `config/*/endpoint-config.json` source fragments.

3. **Unexpected redirect loops to login**
   - Cause: login/verification routes accidentally changed to authenticated or not in bypass/public set.
   - Fix: keep auth entry routes accessible and ensure fallback login path is correct.

4. **403 with AV gate code even when authenticated**
   - Cause: wallet trust bundle evidence missing/invalid for protected route.
   - Fix: ensure verification flow sets required trust evidence and passes it through request/session correctly.

## Anti-Pattern

Do not rely on splash gate alone for enforcement.  
Splash gate is UX; mandatory AV gate + authenticated ACL on content routes is enforcement.
