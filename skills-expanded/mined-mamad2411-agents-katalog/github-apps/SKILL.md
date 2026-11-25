---
name: github-apps
description: >
  Implement, debug, and secure GitHub authentication for xbp.app (apps/web): classic
  OAuth App for user login (preferred, minimal surface) and GitHub App for install /
  webhooks / automation. Covers web + device OAuth flows, PKCE/state, token exchange,
  scopes vs fine-grained permissions, user access tokens (UAT) vs installation tokens
  (IAT), and the dual credential model (GITHUB_OAUTH_* vs GITHUB_APP_*). Use when the
  user runs /github-apps or /github-apps-oauth-and-normal, or mentions GitHub OAuth,
  OAuth App, GitHub App login, authorize callback, device flow, xbp.app sign-in,
  /auth/sign-in/github, /api/callback/github, or GitHub App user OAuth.
---

# GitHub OAuth App + GitHub App (xbp.app)

## Product policy (non-negotiable)

1. **Prefer the classic GitHub OAuth App for user login** on `xbp.app` / `apps/web`.
2. Keep the OAuth App surface **as small as possible** — identity + the dashboard scopes
   already required for product features (`repo`, `read:org`, `user:email`). Do not add
   new scopes or new OAuth App features without an explicit product reason.
3. Use the **GitHub App** for installation, webhooks, bot/automation, and short-lived
   app/installation tokens — not as the primary “Sign in with GitHub” identity path.
4. Never mix credential sets: OAuth App client id/secret ≠ GitHub App client id/secret.

| Concern | App type | Env (apps/web Worker) | D1 `account.providerId` |
|---------|----------|------------------------|-------------------------|
| Browser login / session | **OAuth App** | `GITHUB_OAUTH_CLIENT_ID`, `GITHUB_OAUTH_CLIENT_SECRET` | `github` |
| App user OAuth (setup) | **GitHub App** | `GITHUB_APP_CLIENT_ID`, `GITHUB_APP_CLIENT_SECRET` | `github-app` |
| Install / JWT / IAT | **GitHub App** | `GITHUB_APP_ID`, `GITHUB_APP_PRIVATE_KEY`, `GITHUB_APP_SLUG` | n/a (installation) |
| Webhooks | **GitHub App** | `GITHUB_WEBHOOK_SECRET` | n/a |

Callback path for login OAuth App: **`/api/callback/github`** (`GITHUB_OAUTH_CALLBACK_PATH`).
Register that exact path (and local/dev variants) on the OAuth App’s callback URL list.

## When to load which reference

| Topic | Read |
|-------|------|
| Web application OAuth (authorize → code → token) | [references/oauth-web-flow.md](references/oauth-web-flow.md) |
| Device flow (CLI / headless) | [references/oauth-device-flow.md](references/oauth-device-flow.md) |
| GitHub App vs OAuth App, UAT vs IAT | [references/github-app-vs-oauth.md](references/github-app-vs-oauth.md) |
| Concrete `apps/web` routes and modules | [references/xbp-apps-web-map.md](references/xbp-apps-web-map.md) |

Prefer live GitHub docs via Context7 / docs.github.com when APIs change; keep this skill’s
**xbp wiring** as the monorepo source of truth.

## Agent workflow

### A. Login / session work (default)

1. Confirm change is **login identity**, not installation automation.
2. Use **OAuth App** credentials only (`getGitHubOAuthConfig` / D1 auth path).
3. Entry: `GET /auth/sign-in/github` → social sign-in proxy → GitHub authorize →
   `GET /api/callback/github` → Better Auth / D1 session.
4. Default scopes live in `DEFAULT_GITHUB_OAUTH_SCOPES`:
   `repo`, `read:org`, `user:email`.
5. Always preserve **`state`** CSRF and match **`redirect_uri`** on code exchange.
6. Prefer **PKCE** (`code_challenge` S256 + `code_verifier`) for new or hardened flows.
7. Tokens from OAuth App are long-lived classic user tokens (`gho_…`); store in D1
   `account` with `providerId = "github"`. Never log raw tokens.

### B. GitHub App install / user-to-server OAuth

1. Require an existing session first (user already logged in via OAuth App).
2. Use `/api/github/app/authorize` + `/api/github/app/callback` with cookies
   `github_app_oauth_state` / `github_app_oauth_return_to`.
3. Exchange with **GitHub App** client id/secret; persist as `providerId = "github-app"`.
4. Expect **expiring** user access tokens + refresh tokens; refresh before use.
5. Installation tokens (IAT) are issued via app JWT + installation id — separate path
   from browser login.

### C. Debugging checklist

- Wrong client id on authorize URL → user lands on wrong app consent screen.
- Callback URL not registered → `redirect_uri` mismatch / GitHub error page.
- State cookie missing / mismatch → `invalid-state` (app) or aborted login.
- Mixing `GITHUB_OAUTH_*` into app exchange (or reverse) → token works for wrong API
  surface or fails refresh.
- Missing `user:email` → cannot resolve verified email for local user row.
- CLI browser handoff: `GET /auth/sign-in/github?redirect=/cli/login/<id>` must keep
  redirect through `/api/callback/github?redirect=…`.

## Security rules

- `client_secret` and `GITHUB_APP_PRIVATE_KEY` are **server-only** (Worker secrets /
  `cloudflare:workers` env). Never ship to the client bundle.
- Use HttpOnly + SameSite=Lax cookies for OAuth `state` (and return-to).
- Temporary `code` expires in **~10 minutes**; single-use.
- Device flow: poll with exponential backoff; stop on `slow_down` / expiry.
- Redact `code`, `state`, `access_token`, `refresh_token` in logs/telemetry
  (see `auth-telemetry` helpers).
- Implicit grant is **not** supported by GitHub.

## Do not

- Replace OAuth App login with GitHub App user OAuth without an explicit migration plan.
- Expand OAuth scopes “just in case.”
- Commit secrets from `.env.local` / Wrangler secrets into skill docs or commits.
- Use installation tokens as if they were the signed-in end-user session.
- Document real production client secrets or private keys in this skill.

## Validation

After auth changes in `apps/web`:

1. Unit tests under `apps/web/src/lib/auth-*.test.ts`, `github-callback` tests if present.
2. Manual happy path: sign-in → callback → session cookie → API call with linked token.
3. App setup path (if touched): logged-in user → app authorize → callback →
   `providerId=github-app` row.
4. Confirm Wrangler / Worker env has both credential pairs when both flows are enabled.

## Official docs (anchors)

- [Authorizing OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)
- [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps)
- [Differences between GitHub Apps and OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps)
- [Authenticating with a GitHub App on behalf of a user](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-with-a-github-app-on-behalf-of-a-user)
- [Permissions required for GitHub Apps](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps)
