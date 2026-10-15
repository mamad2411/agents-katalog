---
name: make-app-auth
description: Use when generating, modifying, reviewing, or debugging Make App unified login and authenticated /api/make requests with @qfeius/make-app-auth. Covers unified login, OAuth/ngrok mode, 401/403 handling, logout, current-user menu logout wiring, cookies, sessions, redirect callbacks, and Make App auth troubleshooting. Does not cover UI layout, account menu placement, page structure, build output, Service API contracts, DSL modeling, or canvas-table internals; use makeui for the current-user header menu surface.
---

# make-app-auth

Use this skill for **Make App authentication and authenticated Make API access**.

## Scope

This skill covers:

- `@qfeius/make-app-auth` SDK integration
- unified login as the default generated/published Make App auth mode
- unified login, OAuth, SSO, ngrok, cookie, logout, and callback testing
- direct Make gateway `/api/make/**` authenticated requests
- Service-fronted published App auth under the deployed App Service prefix, normally `/api/auth/**`
- 401, 403, and logout behavior
- cookie, session, redirect, and callback troubleshooting

This skill does not cover:

- UI layout, component design, or Make App page structure; use `makeui`.
- Service build output, packaging, image entrypoints, or publish runtime readiness; use `make-app-runtime`.
- runtime schema normalization, object-field mapping, table rendering, blank-page diagnosis, or business data correctness; use `makeui` and the host app tests.
- DSL modeling or Make resource definitions; use `makedsl`.
- makecli command execution; use `makecli`.
- make-gateway or Org server implementation changes.

## Default Behavior

Default generated and published Make Apps use **unified login** with `unifiedLogin: true`, `apiAuthRedirect: true`, and `auth.init({ redirect: true })`.

This skill only supports unified login for generated and reviewed Make Apps. Missing unified-login prerequisites are blockers, not reasons to switch modes. Do not generate token mode, mock mode, or any no-login bypass from this skill.

## Hard Rules

- Always use `@qfeius/make-app-auth`; do not fork a separate auth implementation.
- Direct-gateway business requests to Make backend must go through `auth.api` under `/api/make/**`.
- All frontend requests to Make backend must go through `auth.api`, including schema/meta, list, get, create, update, delete, attachment/file, lookup, user, and department candidate requests.
- Generated Apps must centralize Make backend access in a shared API adapter or data-source layer that wraps `auth.api`.
- Service-fronted Apps must preserve the `UI -> Service -> make-gateway` contract; do not let UI bypass Service for meta/data calls.
- Service-fronted published Apps behind Make Deploy's default route split use `gatewayBaseUrl: "/api"` in UI. UI calls `auth.api("/app/**")`, which becomes browser requests to `/api/app/**`; auth bootstrap becomes `/api/auth/**`. Do not generate `gatewayBaseUrl: "/api/make"` or `/api/make/app/**` for this mode.
- Do not generate raw `window.fetch('/api/make/...')` for Make backend calls.
- Do not hand-write `Authorization`.
- Browser resource requests such as `<img src>`, `<object data>`, and plain `<a href>` cannot attach custom `Authorization` headers. If a Make file download requires a bearer token, UI must use a same-origin Service download proxy URL, and the Service must validate the current App session before using any deployment-injected download token.
- `gatewayBaseUrl` is the SDK option for the Make backend API base. Reuse the host Make backend config first, especially the `makecli` `server-url` value; do not create a second environment concept for the same URL.
- `gatewayBaseUrl` is not the unified login or account-center URL. Prefer `/api/make` only for direct-gateway same-origin Apps; prefer `/api` for Service-fronted published Apps using Make Deploy's `/api -> service`, `/ -> ui` route split.
- Do not configure or hard-code unified login, Org, or account-center URLs in generated App code; make-gateway returns those URLs.
- Do not read, write, persist, or delete `zs_session` or `make_app_session` in App code.
- Do not construct Org OAuth URLs, `redirect_uri`, `state`, `code_challenge`, token exchange, or Org logout URLs in generated App code.
- Browser code cannot read `~/.make/credentials`.
- Do not generate `unifiedLogin: false`, `accessToken`, `token`, `tokenProvider`, local credential loading, `VITE_MAKE_AUTH_MODE=token`, or equivalent token-mode switches.
- Do not silently downgrade generated Apps from unified login because local OAuth prerequisites are missing; report the blocker.
- Published/vibe Apps must be auth-ready before reporting success: the agent or platform performs the auth checks. Do not leave domain access, DevTools, k8s logs, or cookie inspection as user-only validation steps.
- For Service-fronted Apps, `/api/auth/**` is a required Service proxy contract under the published App Service prefix, not an optional convenience route.
- For Service-fronted Apps, Service must preserve the App host context for every make-gateway call: derive `X-Forwarded-Host` from inbound `Host`, do not trust client-supplied `X-Forwarded-Host`, add `X-Forwarded-Proto`, and share the same helper for auth and business proxy requests.
- Generated authenticated App shells must expose a visible logout action in the current-user menu or the host's established account area, and that action must call `auth.logout()`. The visual menu surface belongs to `makeui`; this skill owns the auth handler and logout behavior. Do not implement logout by clearing cookies, rewriting Org URLs, or hiding logout in page-specific controls.
- Generated Apps must handle recoverable unified-login expiry: when SDK init returns `reason: "state_expired"` or `reason: "challenge_expired"`, show a relogin prompt and call `auth.login({ redirect: true })` from user action.

## Pre-flight Workflow

1. Use unified login. If unified-login prerequisites are missing, report the blocker instead of switching modes.
2. Read `references/sdk-integration.md` before generating or changing auth code.
3. Read the relevant mode reference unless troubleshooting requires more.
   - Default unified login: `references/unified-login-mode.md`
   - 401, 403, logout: `references/logout-and-401.md`
   - Incident/debugging: `references/troubleshooting.md`
4. Read `references/service-fronted-mode.md` when the App keeps a Service layer between UI and make-gateway.
5. Read `references/request-adapter.md` whenever generating or reviewing Make backend requests.
6. Keep auth bootstrap thin. Business features must consume the project Make API adapter and auth state, not auth internals.
7. For published or vibe Apps, verify auth readiness before claiming the app is usable: current-context route, unified redirect, session callback, cookie-preserving business requests, and Service-fronted auth proxy when applicable.
8. Run `scripts/audit-auth-contract.mjs <project-root> --published` for generated Apps when a project tree is available; use `--mode service-fronted` when the App keeps a Service layer.
9. When changing generated code, add or update tests for the touched auth path: unauthenticated session, expired session, 403, logout, unified-login redirect, callback proxy, or business-request 401 handling.

## Reference Selection

- SDK contract and request wrapper: `references/sdk-integration.md`
- Shared request adapter and 401/403 handling: `references/request-adapter.md`
- Default unified login mode: `references/unified-login-mode.md`
- Service-fronted unified-login mode: `references/service-fronted-mode.md`
- 401, 403, and logout behavior: `references/logout-and-401.md`
- Auth incident diagnosis: `references/troubleshooting.md`
- Minimal Service-fronted sample project: `examples/service-fronted-node/`; use only as a reference shape after reading `references/service-fronted-mode.md`.

## Deterministic Checks

Use `scripts/audit-auth-contract.mjs` on generated App projects to catch contract drift before publish:

```bash
node skills/make-app-auth/scripts/audit-auth-contract.mjs <project-root> --published
node skills/make-app-auth/scripts/audit-auth-contract.mjs <project-root> --mode service-fronted --published
```

The audit is auth-scoped. It checks unified-login readiness, raw `/api/make` fetch usage, Service-fronted `/api/auth/**` proxy presence, and obvious direct-vs-Service route mismatches. It does not verify schema rendering or UI blank-page behavior.

## Collaboration With makeui

When `makeui` is generating or editing Make App frontend code, this skill owns all authentication decisions. `makeui` may design UI states around auth results, but it must not invent OAuth, cookie, token, logout, or `/api/make/**` request logic.

`make-app-auth` reports whether the user is authenticated, unauthenticated, forbidden, expired, or blocked by an auth proxy/callback problem. It should not diagnose schema shape mismatches, missing fields, render crashes, white screens, or record-table behavior after authenticated Make requests are already reaching the backend.
