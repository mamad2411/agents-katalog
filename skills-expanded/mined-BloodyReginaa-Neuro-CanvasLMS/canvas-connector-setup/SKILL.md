---
name: canvas-connector-setup
description: Install, update, reconnect, uninstall or troubleshoot this repo's read-only Canvas LMS connector (a remote MCP server on the user's own Cloudflare account) so Claude (web, desktop, mobile, Claude Code) or ChatGPT can read their Canvas. Use when the user asks to set up / install / deploy the Canvas connector, connect Canvas to Claude or ChatGPT, renew an expired Canvas token, update or remove the connector, use it at their school, or fix connector errors.
---

# Canvas connector setup

The user runs **their own copy** of this connector in their own Cloudflare account. The
installer (`npm run setup`, same as `npx -y neuro-canvas-lms`) does all the
technical work. Most users are not developers: explain each step in one plain sentence, **in the
user's language**.

## Hard rules

1. **Never ask for, read, type, store or print the user's Canvas access token.** They paste it only
   into the connector's authorization page in their browser. If they paste one into chat, tell
   them not to, do not use it, and suggest deleting it in Canvas and making a new one.
2. Never print, copy or commit Cloudflare credentials.
3. Do not describe this project as official or endorsed by any school or by Instructure.
4. Keep it read-only: no write/POST routes, no generic URL-fetch tools.
5. The user clicks the Cloudflare "Authorize" button and authorizes the connector themselves.

## Install

Works from any AI agent that can run terminal commands (Claude Code, Codex and others), **with or
without a clone of this repo**. Run without an interactive terminal (as agents do), the installer
never asks questions: everything comes from flags, and when something is missing it stops with a
message (in the user's language) naming exactly what to add. Nothing is lost when it stops; run the
same command again.

1. Check `node -v`: it needs 22 or newer. Otherwise send the user to https://nodejs.org and stop.
2. Ask the user for their school's **Canvas address**: what the browser's address bar shows when
   they use Canvas (e.g. `canvas.example.edu` or `<school>.instructure.com`, not the school portal
   or login page). Never guess the address.
3. **Cloudflare sign-in comes first, in the user's own browser.** Run `npx -y wrangler whoami`.
   If it shows an email, they are signed in: go on. If not, ask the user to run
   `npx -y wrangler login` **themselves, in their own terminal** (PowerShell on Windows,
   Terminal on macOS). Their usual browser opens Cloudflare: they sign in (or sign up for free)
   and click the blue **Authorize** button; the terminal then says "Successfully logged in".
   Wait until they confirm, then check `wrangler whoami` again.
   - Do not do this sign-in in a browser built into your own app or sandbox: the user is not
     signed in to Cloudflare there ("Authentication error", "Application authorization failed").
   - Never start a second sign-in while one is pending. Each attempt has its own callback; an
     Authorize click on an older tab fails with "callback does not match the pending login".
     If that happens: the user closes every Cloudflare tab and runs `npx -y wrangler login` once.
   - Only if the user wants you to run the sign-in yourself: tell them first that a Cloudflare page
     opens and they click **Authorize** within about 2 minutes, and give the command a long
     timeout (5 minutes or more).
4. Run, **without a clone** (`-y` only skips npm's own download prompt):
   ```bash
   npx -y neuro-canvas-lms --canvas-host "<address>"
   ```
   From a clone instead: `npm install`, `npm test` (all must pass), then
   `npm run setup -- --canvas-host "<address>"`.
   Give it a timeout of 10 minutes. A new Cloudflare account gets a free workers.dev subdomain from
   the installer itself (a random `neuro-xxxxxx` name). On a brand-new workers.dev address the HTTPS
   certificate can take a few minutes; the installer then says it is waiting for it, keeps
   checking for up to 5 minutes and meanwhile opens Canvas so the user can create their token: tell
   the user. Let it finish; do not restart it.
5. If it stops, do what its message says, then run the same command again:
   - **Several Cloudflare accounts:** it lists them as `--account-id <id>  <name>`. Ask the user
     which account to use and add that flag. Never pick one yourself.
   - **Cloudflare email not verified:** the user opens the verification email from Cloudflare
     (spam folder too) and clicks the link.
   - **New Cloudflare account without a workers.dev subdomain** (only if the installer could not
     create one itself): give the user the printed dashboard link; they choose a name (e.g. their
     name plus a number) and save it.
   - **Deployed, but not confirmed online yet (exit code 2):** the deploy worked; the new address did
     not answer correctly in time (usually its HTTPS certificate). Do not install again: wait a few
     minutes, then run the check it prints, `npx -y neuro-canvas-lms check` (with the same
     `--name` if one was used). It deploys nothing; exit code 0 means ready.
   - **"does not look like a Canvas site":** the address is wrong (school portal or SSO page).
     Ask the user again.
   - **Cloudflare sign-in failed or timed out:** see step 3 (the user signs in once, in their own
     terminal and browser).
6. On success it prints the connector URL (`https://<name>.<subdomain>.workers.dev/mcp`, also copied
   to the clipboard) and the next steps. Relay them; **the user does these in their browser, never
   you**:
   - Canvas → Account → Settings → **+ New Access Token**, unless they already made it while the
     installer waited (schools may cap it, e.g. 30 days at UMass Amherst; copy it right away,
     Canvas shows it once). The connector's page also has an **Open Canvas settings** button.
   - Claude: Settings → Connectors → **Add custom connector** → the `…/mcp` URL → **Connect** →
     paste the Canvas token on the connector's own page → Authorize. Works on every device with the
     same account, including Claude Code (check with `/mcp`).
   - ChatGPT: custom connector in developer mode, same URL. Menu names change; follow the UI.
7. Test in a **new chat**: "What assignments do I have due this week?"

Connect right after installing: until the first authorization, whoever authorizes first becomes
the owner. (To pin the owner, add `OWNER_CANVAS_ID` to the vars in
`~/.neuro-canvas-lms/<name>/wrangler.jsonc` and deploy that file with wrangler.)

## Update / reinstall / uninstall

- **Update:** run `npx -y neuro-canvas-lms` again (from a clone: `git pull`,
  then `npm run setup`). It reuses the saved settings; without a terminal it does not ask first.
  Then tell ChatGPT users to refresh the connector in ChatGPT's settings (ChatGPT keeps its own copy
  of the tool list); in Claude a new chat is enough.
  It reuses the storage, so connections keep working. Start a new chat afterwards (clients cache
  tool lists).
- **Uninstall:** `npm run setup -- uninstall --yes` (deletes the Worker and its storage), then the
  user deletes the Canvas token and the connector in their AI app.

## Renewing an expired token

Symptom: "Canvas authorization expired; reconnect." The user makes a new Canvas token, then in
their AI app: connector → Disconnect → Connect → paste it. No reinstall needed.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "bound to a different Canvas account" | Someone else authorized first, or the user changed accounts. Reset: `npx wrangler kv key delete --namespace-id <id> --remote owner:canvas_user_id` (id in `~/.neuro-canvas-lms/<name>/state.json`), then connect again. |
| Installer: "email address is not verified" / `email_verification_required` | A new Cloudflare account must verify its email first: the user clicks the link in Cloudflare's email (or requests a new one in the dashboard), then runs the installer again. |
| Installer: "does not look like a Canvas site" | They pasted the school portal or SSO page. Find the real Canvas host (often `<school>.instructure.com`). |
| Cloudflare sign-in failed: "Authentication error", "authorization failed", "callback does not match the pending login", or timed out | The consent page opened in a browser without the user's Cloudflare session, or an older attempt's tab was used. Stop any running installer, close every Cloudflare tab; the user runs `npx -y wrangler login` once in their own terminal and clicks Authorize in their usual browser. Then run the installer again. |
| Homepage says "not configured" / `/healthz` not ok | `CANVAS_HOST` var missing: run the installer again. |
| Verification failed, HTTP 401 | Token wrong, incomplete or expired → new token. |
| "denied access to this resource" | Canvas permission for that item (e.g. the instructor hid it). The token is fine; don't reconnect. |
| New connector address fails with `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`, a TLS handshake error or "not found" right after the first deploy | The new workers.dev subdomain is still getting its certificate/DNS (minutes). The installer waits up to 5 minutes, then exits with code 2 ("deployed, not confirmed online yet"). Nothing is broken and nothing needs redeploying: wait a few minutes and run `npx -y neuro-canvas-lms check`. |
| HTTP 406 / HTML error pages from Canvas | Something in front of Canvas rejected the request. API calls already retry over a raw TLS socket (`canvas-transport.mjs`). Debug with the `CANVAS_TRANSPORT` var (`fetch` / `socket`) and `npx wrangler tail`. |
| File download 403 (`text/html`) while metadata works | A firewall rejects the download's User-Agent (none, or one containing `UMassCanvas`). Keep `DOWNLOAD_UA` in `file-content.mjs` as shipped. |
| "not shared as Anyone with the link" on a linked file | The Google/Dropbox file is private. Only the teacher can change that; give the user the link to open it signed in. |
| HTTP 403/404 on Files, Pages or Quizzes | The course hides that list. Files are still found with `canvas_find_files` (searches front page, syllabus, modules, assignments, announcements and linked pages); quizzes stay hidden. |
| File "exceeds 15 MiB" | Worker memory limit. Download it and open it with Claude Code locally. |
| Handwritten/scanned PDF has no text | Expected. Use `canvas_file_original` (any file id) or `canvas_module_file`; the AI reads pages as images (ask for ~150 dpi for formulas). |

## Logs

Persistent Workers Logs are on, with automatic invocation logs OFF (request headers are never
stored). The Worker writes only `{http: {path, method, status}}`, `{mcp_method}`,
`{mcp_resource_read: ok|error}` and `{canvas_transport: {via, status, reason}}`. Cloudflare
dashboard → Workers → the Worker → Logs, or live with `npx wrangler tail <name>`.
