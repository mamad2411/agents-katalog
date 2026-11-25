---
description: Deploy this rephonic-mcp Cloudflare Worker. Use when the user asks to deploy, ship, or push the MCP server from this repo. Handles the CLOUDFLARE_API_TOKEN env conflict and verifies prod afterwards.
user-invocable: true
---

# /deploy

Deploy the Rephonic remote MCP server to Cloudflare Workers.

Worker name: `rephonic-mcp`. Prod domain: `https://mcp.rephonic.com`.

## Gotcha: unset CLOUDFLARE_API_TOKEN

If `CLOUDFLARE_API_TOKEN` is exported in the shell (for example, set by another Cloudflare-scoped skill or tool), wrangler uses that token instead of the stored OAuth login. When the token lacks Workers deploy scope the deploy fails with `Authentication error [code: 10000]`.

Always run wrangler with the token unset:

```bash
env -u CLOUDFLARE_API_TOKEN npm run deploy
```

Same pattern for `wrangler login` when OAuth is stale:

```bash
env -u CLOUDFLARE_API_TOKEN npx wrangler login
```

Login is interactive (browser), so ask the user to run it with the `!` prefix.

## Deploy steps

1. Check what's changing and surface anything surprising before deploying:
   ```bash
   git status && git diff
   ```

2. Type-check:
   ```bash
   npm run type-check
   ```

3. Deploy:
   ```bash
   env -u CLOUDFLARE_API_TOKEN npm run deploy
   ```
   Success output ends with `Uploaded rephonic-mcp`, `Deployed rephonic-mcp triggers`, and a version ID.

4. Smoke test prod. The MCP route is OAuth-gated, so unauthenticated requests should return `401`:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://mcp.rephonic.com/mcp
   ```
   Expect `401`. Anything else (5xx, timeout, 404) means the deploy broke something.

5. If the change touched a tool that wraps a Rephonic API endpoint, verify the backend end-to-end. Ask the user for a prod API key if needed, and call the underlying `api.rephonic.com` endpoint directly. Do not write API keys into this file or anywhere else in the repo.

## If wrangler login is stale

Symptom: `Failed to fetch auth token: 400 Bad Request`, followed by `In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN environment variable`.

Fix: ask the user to run `!env -u CLOUDFLARE_API_TOKEN npx wrangler login`, then retry the deploy.

## First-time setup (reference only)

One-time steps, already done for the live worker. Only relevant when recreating from scratch or forking to a new Cloudflare account:

1. Log in: `npx wrangler login`
2. Create the OAuth KV namespace: `npx wrangler kv namespace create OAUTH_KV`, then paste the `id` into `wrangler.jsonc`.
3. Set the cookie encryption secret: `npx wrangler secret put COOKIE_ENCRYPTION_KEY` (any random string, e.g. `openssl rand -hex 32`).
4. Add a Custom Domain in the Cloudflare dashboard: Workers & Pages → `rephonic-mcp` → Settings → Domains & Routes.

## Scope

This skill is specific to `rephonic-mcp`. Do not use it for other Rephonic services (rephonic-app, rephonic-web, selfserve-web), which have their own pipelines.
