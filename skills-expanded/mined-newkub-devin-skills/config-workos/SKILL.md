---
name: follow-service-workos-config-workos
description: Set/edit WorkOS configuration — AuthKit, SSO connections, Directory Sync, redirect URIs, and session config — without clobbering existing settings
related:
  - follow-service-workos
---

## Goal

Set/edit WorkOS configuration — AuthKit, SSO connections, Directory Sync, redirect URIs, and session config — without clobbering existing settings

## Scope

- Define env vars and redirect URIs
- Configure AuthKit/User Management or the legacy `sso.*` flow
- Create organizations, connections (SAML/OIDC), and Directory Sync webhooks
- Does not cover first-time SDK install → use `workflows/setup-workos/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Know the current state before editing

1. Read `.env*` and the existing auth module to identify the flow in use (AuthKit vs `sso.*`)
2. Do `/check-secrets env-vars` to identify missing vars
3. Check the redirect URIs and connections already configured in the dashboard — use `/open-web-for-config-secret` (service workos)
4. If the SDK/credentials are not there yet → do `workflows/setup-workos/SKILL.md` instead

### 2. Configure Env And Redirects

> Goal: Set env vars and redirect URIs completely

1. Define `WORKOS_API_KEY`, `WORKOS_CLIENT_ID` (API key is server-only)
2. If using AuthKit sessions → define a cookie password env such as `WORKOS_COOKIE_PASSWORD` (long random value, stored in `/follow-secret-manager`)
3. Set the redirect URI and allowed origins in the dashboard to match app routes such as `/callback`
4. Merge only the necessary keys — never overwrite the existing env/config

### 3. Configure AuthKit Or SSO

> Goal: Enable the auth flow that matches the product

1. AuthKit (modern path): enable AuthKit in the dashboard and use User Management APIs for authorization URL, code exchange, and sessions
2. Legacy SSO: use `workos.sso.getAuthorizationURL` and `workos.sso.getProfileAndToken`
3. Create organizations and connections per provider (SAML, OIDC, Google, Microsoft)
4. Set `state` and PKCE (`code_challenge`) for flows that support them

### 4. Configure Directory Sync And Webhooks

> Goal: Receive user/group events securely

1. Create a directory for the connection that needs sync
2. Set a webhook endpoint in the dashboard and store the webhook secret in `/follow-secret-manager`
3. Verify the webhook signature every time per the official docs
4. Map `dsync.*` events to the app's user/group handlers

### 5. Verify

> Goal: Confirm the auth flow works end-to-end

1. Test authorization URL → callback → session in dev
2. Do `/run-verify` and test webhook delivery if present
3. If it fails → revert the changed keys, do `resolve-errors`, then report the diff

## Rules

- Use environment-based config — never hardcode keys or commit secrets
- AuthKit/User Management API is the modern path — use `sso.*` only for existing legacy flows
- Validate webhook signatures every time
- Redirect URIs in the dashboard must match the real routes in every environment
- If unsure about an option/method → check official docs or `learn` (web)

## Expected Outcome

- AuthKit/SSO flow works from authorize through session
- Redirect URIs, connections, organizations correct per environment
- Directory Sync webhook is secure and receives events
- Config merged without clobbering existing settings
