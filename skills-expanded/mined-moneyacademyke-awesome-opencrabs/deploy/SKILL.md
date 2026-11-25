---
name: deploy
description: Build, test, and deploy the current project to Cloudflare Workers/Pages via Wrangler.
output_contract: |
  - `wrangler deploy` exits 0
  - live URL returns HTTP 200
  - verification witness written to `verification/witnesses/`
---

# deploy

Use this skill when the user wants to ship the current project to Cloudflare.

## Goal

Run a clean build, verify tests pass, and deploy the production artifacts to Cloudflare — then confirm the live site is healthy.

## Preconditions

- A `wrangler.toml` (or `wrangler.json`) exists in the project root
- Wrangler is authenticated (`bunx wrangler whoami` returns an account)
- The build command is defined in `package.json`

## Steps

### 1. Pre-flight checks

- Confirm `wrangler.toml` exists in the project root. If missing, stop and tell the user.
- Run `bunx wrangler whoami` to confirm authentication. If not authenticated, tell the user to run `bunx wrangler login` first.
- Determine the **Cloudflare account ID**:
  1. Check if `account_id` is set in `wrangler.toml`. If yes, use it.
  2. Otherwise, read it from `CLOUDFLARE_ACCOUNT_ID` env var.
  3. Otherwise, extract it from `bunx wrangler whoami` output.
- Read `package.json` to find the build script (`build`, `build:prod`, etc).

### 2. Run tests

- Run the project's test suite before deploying. Typically `bun run test`.
- If tests fail, **stop**. Report the failures. Do not deploy broken code.

### 3. Build

- Run the production build. Typically `bun run build`.
- Confirm the output directory (from `wrangler.toml` `[assets] directory` — usually `./dist`) is populated.
- If the build fails, **stop**. Report the error.

### 4. Deploy

- Run `bunx wrangler deploy` with the resolved account ID:
  ```bash
  CLOUDFLARE_ACCOUNT_ID="<resolved-id>" bunx wrangler deploy
  ```
- If the user provides `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_KEY`, or `CLOUDFLARE_EMAIL` env vars, pass them through. Otherwise rely on Wrangler's cached OAuth token.
- Capture the deployed URL from Wrangler's output.

### 5. Verify

- After deploy completes, fetch the live URL with `http_request` (GET) to confirm it returns HTTP 200 and the expected HTML.
- If the page loads but shows a runtime error, investigate and fix before reporting success.
- Report the deployed URL and a one-line summary of what shipped.

## Constraints

- Never deploy if tests fail.
- Never deploy if the build fails.
- Never echo credentials (API tokens, API keys) in output — reference them as "the token" or "the key".
- If wrangler is not authenticated and no API token is provided, stop and tell the user to authenticate.
- Always verify the live site after deploy — a successful `wrangler deploy` does not guarantee the app boots in the browser.

## Outputs

- Deployed URL
- Confirmation that tests passed and build succeeded
- Any changed assets that were uploaded
