---
name: dokploy-ghcr-deploy
description: Set up automatic build + deploy of a Dockerized repo to a self-hosted Dokploy instance using GitHub Actions, GitHub Container Registry (GHCR), and the Dokploy MCP. Use when the user wants to auto-deploy a repo to Dokploy, set up CI/CD targeting Dokploy, ship a container to their own Dokploy server, configure a new app on Dokploy from an existing repo, or wire GitHub Actions to push an image and trigger a Dokploy redeploy — even if they don't mention "GHCR" or "GitHub Actions" explicitly. Triggers on phrasings like "deploy this to dokploy", "set up dokploy for this repo", "auto-build and deploy on my server", "ship this app to my dokploy", "I want CI/CD to my self-hosted Dokploy".
---

# Dokploy + GHCR auto-deploy

End-to-end recipe for turning a Dockerized GitHub repo into a Dokploy app that redeploys automatically on every push to `main`. Builds happen in GitHub Actions; images go to GHCR (private by default); Dokploy pulls and redeploys via a REST call from the workflow's final step.

Why this flow:
- **GHCR over Docker Hub** — Docker Hub's free tier caps at 1 private repo, GHCR gives unlimited private packages. Push-side auth is the built-in `GITHUB_TOKEN`, no extra PAT needed on the workflow side.
- **API-trigger over registry webhook** — GHCR doesn't fire push webhooks, so the workflow POSTs to Dokploy's `/api/application.deploy` instead of relying on a registry-side webhook (which is how Docker Hub → Dokploy would work).

Work through the phases in order. Each one has a clear stop condition; don't skip ahead if something's red.

## Prerequisites — check before anything else

Do these silently in parallel where possible; only surface problems to the user.

1. **Dockerfile exists and exposes a port.** Read it. Grep for `EXPOSE`. Capture the port number — you'll need it for the Dokploy domain. If there's no Dockerfile or no `EXPOSE`, stop and ask the user; do not fabricate one from framework defaults (that would be silent guesswork).
2. **`.dockerignore` exists.** If missing, offer to add a minimal one (`node_modules`, `.git`, `build`, `dist`, tests, `.env*`). Not a blocker.
3. **`gh` CLI authenticated.** `gh auth status` should show an active account. If not, stop and ask the user to run `gh auth login` first.
4. **Dokploy MCP is connected.** Call `mcp__dokploy-mcp__user-session`. If it errors, stop and ask the user to connect the Dokploy MCP before continuing — the skill can't do the Dokploy half without it.
5. **GitHub remote.** Parse `git remote get-url origin` to extract `owner/repo`. Lowercase it — GHCR rejects uppercase in image paths. If the remote isn't GitHub, this skill doesn't apply; tell the user.

## Inputs to gather from the user

Batch these into one `AskUserQuestion` call so the user answers once, not five times. Defaults in parentheses — pre-fill them and let the user override:

- **Dokploy project name** (default: the repo name)
- **Dokploy app name** (default: `web`)
- **Public domain** to attach (must already resolve to the Dokploy host; if they have a wildcard like `*.example.com`, suggest `<project>.example.com`)
- **Dokploy base URL** (e.g. `https://dokploy.example.com`) — you cannot infer this; always ask
- **Extra env vars** beyond `APP_ENV=production` — offer to skip; they can add more in the Dokploy UI later. Validate each entry matches `^[A-Z_][A-Z0-9_]*=` and reject values containing raw newlines before sending to `application-saveEnvironment`, so a stray newline in one value can't silently inject another variable.

## Phase A — Repo prep

1. Write `.github/workflows/docker-publish.yml` from `assets/docker-publish.yml.template`. The template uses `${{ github.repository }}` and lowercases it at runtime, so it works unmodified for most repos — you don't normally need to substitute anything.
2. Create a feature branch if not already on one (don't commit straight to `main` — we want the workflow to land atomically with a PR once secrets are in place).
3. Stage and commit the workflow. Don't push yet — we want Dokploy and GitHub secrets configured first, otherwise the very first workflow run will fire against an app that isn't ready and leave a failed deployment in the history.

## Phase B — Dokploy setup via MCP

Sequential, fail-fast. Each tool call produces IDs you'll need for the next one — capture them as you go.

1. **Resolve the organization** — call `mcp__dokploy-mcp__organization-active` and save `organizationId`.
2. **`mcp__dokploy-mcp__project-create`** with `name` and a short `description`. The response includes both a `projectId` and an auto-created default `environmentId` (named `production`) — save both.
3. **`mcp__dokploy-mcp__application-create`** with `name` (the app name) and `environmentId`. Save `applicationId`. The app starts with `sourceType: "github"`; it flips to `docker` when you save the Docker provider next.
4. **`mcp__dokploy-mcp__application-saveDockerProvider`** with:
   - `applicationId`
   - `dockerImage: "ghcr.io/<lowercase-owner>/<lowercase-repo>:latest"`
   - `registryUrl: "ghcr.io"`
   - `username: "<lowercase-owner>"`
   - `password: "PAT_PLACEHOLDER"` — this stub keeps the MCP call valid and is **left in place**. The real PAT is set by the user directly in the Dokploy UI in Phase E, so it never transits this conversation.
5. **`mcp__dokploy-mcp__application-saveEnvironment`** with:
   - `applicationId`
   - `createEnvFile: true`
   - `env: "APP_ENV=production\n..."` (plus whatever the user added)
   - `buildArgs: ""`, `buildSecrets: ""` — explicit empty strings, **not** undefined. See Gotchas.
6. **`mcp__dokploy-mcp__domain-create`** with:
   - `applicationId`
   - `host: "<domain-the-user-gave>"`
   - `port: <port-from-Dockerfile>`
   - `https: true`, `certificateType: "letsencrypt"`
   - `path: "/"`, `stripPath: false`, `domainType: "application"`
7. **`mcp__dokploy-mcp__user-createApiKey`** with `name: "github-actions-deploy-<repo>"` and `metadata: {"organizationId": "<from step 1>"}`. Save the `key` — it's shown once. Flag to the user that the default rate limit is 10 requests / 24h; offer to raise it via the Dokploy UI if they push to main a lot.

## Phase C — GitHub secrets via `gh`

Three secrets, set in one batched Bash call so the user approves once:

```sh
gh secret set DOKPLOY_URL --repo <owner>/<repo> --body "<dokploy-base-url>" && \
gh secret set DOKPLOY_API_KEY --repo <owner>/<repo> --body "<api-key-from-B7>" && \
gh secret set DOKPLOY_APPLICATION_ID --repo <owner>/<repo> --body "<applicationId-from-B3>"
```

Then smoke-test the API before pushing code. `read -s` keeps the key out of `~/.bash_history`; the `unset` at the end clears it from the shell so it doesn't linger in the process environment:

```sh
read -rsp "Paste DOKPLOY_API_KEY (not echoed): " DOKPLOY_API_KEY; echo
DOKPLOY_URL='https://your-dokploy.example.com'
APP_ID='<applicationId from B3>'
DOKPLOY_API_KEY="$DOKPLOY_API_KEY" \
  curl -fsS --max-time 30 -o /dev/null -w "%{http_code}\n" \
  -X POST "${DOKPLOY_URL%/}/api/application.deploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  --data "$(jq -cn --arg id "$APP_ID" '{applicationId:$id}')"
unset DOKPLOY_API_KEY
```

Expect `200`. Anything else means the URL, key, or app ID is wrong — fix before moving on. The deploy will fail (no image has been pushed yet) but the trigger should succeed; this is proof the auth path is good.

## Phase D — Push & PR

Push the branch, open a PR with `gh pr create`. PR body should call out:
- the three secrets that must be set (confirm they're in place)
- the Dokploy app details (project, app, domain, port)
- that merging triggers the first real deploy

## Phase E — GHCR PAT (the only manual step)

GitHub has no API for minting PATs, so the user has to do this in the UI. Don't pretend otherwise.

**The PAT must not transit this conversation.** A `read:packages` PAT in chat history is credential exposure — transcripts are routinely retained server-side, and the PAT can pull every private package the user can see. So the user pastes it straight into Dokploy, not into chat. Do **not** ask them to paste it here, and do **not** call `mcp__dokploy-mcp__application-saveDockerProvider` with the real value; the `PAT_PLACEHOLDER` stub from Phase B step 4 is replaced in-place via the Dokploy UI.

Tell the user verbatim:
> 1. GitHub → Settings → Developer settings → Personal access tokens (classic) → Generate new token → scope `read:packages` **only** → set expiration to **90 days** (GitHub's recommended max for machine credentials; do not pick "No expiration") → generate → copy the token to your clipboard.
> 2. Dokploy → Projects → *your project* → *your app* → General → Docker provider → paste the token into the **Password** field → Save.
> 3. Reply here with "saved" (no token, no paste).

Only when they confirm "saved" do you move to Phase F.

Rotation, if it's ever needed, follows the same path: revoke in GitHub, generate a new PAT, paste it into the Dokploy UI. No chat step.

Why this step isn't automated: the `gh` CLI token doesn't carry `read:packages` by default (scopes are typically `repo, read:org, gist, admin:public_key`), and running `gh auth refresh -s read:packages` would give you a user-scoped OAuth token with every other scope still attached — too much privilege to stash as a service password. A dedicated classic PAT scoped to `read:packages`, set via the Dokploy UI, is the cleanest answer.

## Phase F — First deploy

1. Merge the PR (or push to `main`). The workflow fires.
2. Watch the Actions tab: the build should push two tags (`latest` and `sha-<short>`) and the final step should return 2xx from Dokploy.
3. In Dokploy → app → Deployments, confirm a new deployment went from "Pulling" → "Running" → "Done".
4. Hit the domain; expect the app to respond on the port from the Dockerfile.

If the Dokploy deployment shows "denied: denied" from `ghcr.io/v2/`, the PAT is wrong or expired — go back to Phase E.

## Gotchas (learned the hard way)

- **MCP zod unions reject `undefined`.** `application-saveDockerProvider` requires all of `registryUrl, username, password` present (pass empty strings or real values, not omitted). `application-saveEnvironment` requires `buildArgs` and `buildSecrets` — pass `""`. Skipping them wastes a round trip on an opaque validation error.
- **GHCR image paths must be all-lowercase.** The workflow template handles this via `${IMAGE_NAME,,}`. If you hand-roll one, don't forget.
- **Don't suggest the Docker Hub webhook flow for GHCR.** GHCR doesn't support push webhooks. The Dokploy docs mention the webhook flow in the Docker Hub context only.
- **Docker Hub free tier = 1 private repo.** That's why this skill defaults to GHCR. Only mention Docker Hub to explain why you're not using it.
- **Package visibility.** GHCR packages inherit visibility from the source repo on first push — private repo → private package. No extra API call needed. If the repo is public, the package will be public too; mention that to the user once.
- **Dokploy API key default rate limit is 10/24h.** Fine for most `push to main` flows. Raise in the Dokploy UI if the user does many deploys per day (e.g., trunk-based with many merges).
- **`gh auth status` scopes aren't enough for GHCR pulls.** Typical `gh` tokens carry `repo, read:org, gist, admin:public_key` — no `read:packages`. That's why Phase E can't lean on the CLI token.
- **Don't rename `APP_ENV`.** Codebases that ship dual Vercel + Dokploy deploys often branch on `APP_ENV` specifically to avoid tangling with `VERCEL_ENV`. Set it to `production` unconditionally on Dokploy.

## What this skill deliberately doesn't do

- Doesn't migrate an existing Dokploy app's domains — if the user is replacing a GitHub-source Dokploy app, ask whether to create a new app in a new project (clean, no downtime on the old one) or reconfigure in place (needs domain cutover). Default to new project.
- Doesn't copy env vars from one app to another. Listing them is fine; blindly copying live Stripe/DB secrets between apps risks clobbering or double-writing.
- Doesn't set up preview deployments, healthchecks, or replicas. Scope creep; add when the user asks.
