---
name: subdomain-deploy
description: Spin up a new personal project at a subdomain of austinfox.com on Vercel. Use when the user says "deploy this", "ship this", "put it on austinfox.com", "set up <name>.austinfox.com", "spin up a new personal project", or anything that implies creating a new Vercel project on an austinfox.com subdomain. One Vercel project per subdomain, Bun+Vite+React+TypeScript default stack. Three access patterns (public, single-password, multi-user with cloud progress) — pick per project. Wildcard DNS for *.austinfox.com is already configured on Porkbun, so subdomain creation is Vercel-only.
user-invocable: true
disable-model-invocation: false
metadata:
  author: Austin Fox
  version: "1.1.0"
---

# Personal Subdomain Deploy (austinfox.com)

Stand up a new personal project at `<name>.austinfox.com` on Vercel with the right access pattern and storage strategy for the project. This skill is for Austin's personal projects only — not client work, not company projects.

## Non-Negotiables

These are the rules that distinguish this workflow from generic "deploy to Vercel":

1. **One Vercel project per subdomain.** Never combine multiple personal projects into a single Vercel project, never use path-based routing across them. Each subdomain gets its own GitHub repo, its own Vercel project, its own env vars, its own analytics.
2. **Default stack: Bun + Vite + React 19 + TypeScript.** Bun is the runtime/package manager; Vite is the dev server/bundler — they do different jobs and both are needed. Add Tailwind v4 (via `@tailwindcss/vite`) when styling is non-trivial. Don't reach for Next.js for static personal projects.
3. **Auth is custom Edge middleware**, never Vercel's built-in Password Protection. Vercel's feature requires the Advanced Deployment Protection add-on (~$150/mo). The middleware patterns in `references/` are no-ops when their env vars are unset, so they cost nothing during local dev.
4. **Wildcard DNS is already set on Porkbun** (`*.austinfox.com → cname.vercel-dns.com`). New subdomains require zero DNS work — `vercel domains add` is sufficient.
5. **Private GitHub repo by default.** Personal projects are private unless the user explicitly says otherwise.

## When to Use This Skill

Activate when the user's request implies creating a brand-new project on an austinfox.com subdomain. Strong signals:

- "deploy this" / "ship this" + the project is local-only and has no Vercel link yet
- "put it on austinfox.com" / "set up `<name>`.austinfox.com"
- "spin up a new personal project"
- Mentions of austinfox.com or a subdomain like `lettera.austinfox.com`

Do NOT use this skill when:

- The project is already linked to a Vercel project — in that case use the generic `deploy-to-vercel` skill.
- The user wants to deploy to a non-austinfox.com domain — use the generic flow.
- The user is deploying a redeploy / preview / hotfix to an existing project — use the generic flow.

## Step 0: Pick the Access Pattern

Decide this BEFORE writing code. Ask the user if it isn't obvious from context.

| Pattern | Use when | Auth | Per-user storage |
|---|---|---|---|
| **Public** | Portfolio, demo, anything not sensitive | None — no middleware | localStorage if needed |
| **Single password** | One viewer, or a small trusted group sharing one password; same device per visit | `SITE_PASSWORD` + `references/middleware.ts` | localStorage |
| **Multi-user** | Multiple distinct users; cross-device sync; "I cleared my cache and lost everything" must not be possible | `USERS` (named accounts) + `references/middleware-multi-user.ts` | Upstash Redis via `references/cloud-progress.md` |

**Heuristics:**
- One viewer + one device → **single password**. Cheapest, simplest.
- One viewer + multiple devices → **single password + cloud progress**. Storage keyed by a constant (since "the user" is one identity) — see `references/cloud-progress.md`.
- Multiple humans need separate progress → **multi-user**. Per-user identity in cookies; storage keyed by username.
- Nothing private about the project → **public**.

Default if unclear: **single password + localStorage**. It's right ~80% of the time.

## Step 1: Confirm Project Identity

Before writing any code or running any CLI commands:

1. **Confirm the subdomain.** If the user said "ship this" without naming the subdomain, ask. The subdomain becomes the GitHub repo name, Vercel project name, and live URL.
2. **Confirm the access pattern** from Step 0.
3. **Confirm the password(s).** For single-password: ask for `SITE_PASSWORD`. For multi-user: ask for `<username>:<password>` pairs. Never invent passwords. Never echo them in chat history if avoidable — they go in via `vercel env add` at the prompt.
4. **Confirm the Vercel scope.** `vercel link` defaults to a team scope, not the personal account. Ask explicitly: "Personal scope (`afox`) or a team like `wiz-dev`?" Don't assume. (If the user has a Pro subscription on a team and wants personal projects there, that's normal — just confirm.)
5. **Confirm Tailwind.** If the project has more than two screens or a custom visual identity, default Tailwind v4 to enabled. Otherwise ask once.

## Step 2: Stack Setup

Use Bun for everything (install, dev, build). Do not generate a `package-lock.json` or `yarn.lock`.

```bash
bun create vite . --template react-ts
bun install
```

If Tailwind v4:

```bash
bun add tailwindcss @tailwindcss/vite
```

In `vite.config.ts`:

```ts
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Replace `src/index.css` with:

```css
@import "tailwindcss";
```

Tailwind v4 uses no `tailwind.config.js` by default — configuration goes in CSS via `@theme`.

Remove the starter assets you won't use: `src/App.css`, `src/assets/`, `public/vite.svg`.

## Step 3: Add the Auth Middleware

Pick the template that matches Step 0:

- **Public:** skip this step entirely. No middleware.
- **Single password:** copy `references/middleware.ts` to the project root (sibling to `vite.config.ts`, NOT in `src/`).
- **Multi-user:** copy `references/middleware-multi-user.ts` to the project root, renamed to `middleware.ts`.

Either middleware needs the Edge package:

```bash
bun add @vercel/edge
```

Vercel auto-detects `middleware.ts` at the project root and deploys it as an Edge Function for any framework — no `vercel.json` needed.

Both templates:
- Are no-ops when their env vars are unset (so local dev works without setup).
- Serve a custom-styled login page on every unauthenticated request.
- Set 1-year `HttpOnly`, `Secure`, `SameSite=Lax` cookies on successful login.
- Store hashes in cookies, never raw passwords.

If the project has a custom visual identity, edit the `loginHtml()` function in the chosen template to match — colors, fonts, heading text. The default styling matches Lettera's cream + Lora + Outfit aesthetic; replace it for other projects.

### Generating password hashes (multi-user)

`USERS` env var format: `alice:HASH1,bob:HASH2`. Each `HASH` is `SHA-256(password)`:

```bash
echo -n "alice-password" | shasum -a 256 | cut -d' ' -f1
```

Build the `USERS` value once and paste it at `vercel env add` time.

## Step 4: Add Cloud-Synced Progress (optional)

Skip if Step 0 chose localStorage. Otherwise see `references/cloud-progress.md` — it covers:

- Provisioning Upstash Redis through Vercel Marketplace (free tier).
- The `api/progress.ts` Vercel Function template.
- Wiring the React side to use cloud + localStorage as a write-through cache.
- Storage keying for both single-password (one shared key) and multi-user (key per username from cookie) modes.

## Step 5: Deploy Flow

Run these in order. Each command is a single line — no chaining `&&` so failures are easy to spot.

```bash
# 1. Initialize git and create private GitHub repo
git init
git add .
git commit -m "Initial commit"
gh repo create austinfox/<name> --private --source=. --push

# 2. Link to a new Vercel project
vercel link --yes --project <name>
# Defaults to a team scope, NOT personal. If wrong scope was picked,
# delete .vercel/ and re-run with `vercel switch` first to pick the
# right scope, OR pass --scope <team-slug> explicitly.
# Note: --scope <personal-account-slug> is rejected ("cannot set Personal
# Account as scope") in some CLI versions; use `vercel switch` instead.

# 3. Set env vars for all environments (see gotcha below)
vercel env add SITE_PASSWORD production --value "<password>" --yes
vercel env add SITE_PASSWORD preview '' --value "<password>" --yes
vercel env add SITE_PASSWORD development --value "<password>" --yes
# For multi-user, replace SITE_PASSWORD with USERS and pass the
# alice:hash,bob:hash string as the value.

# 4. Add the custom subdomain to THIS project
vercel domains add <name>.austinfox.com
# Equivalent UI path: this project's Settings → Domains → add <name>.austinfox.com.
# Do NOT use the team-level "Domains → Add Domain" dialog (that one binds the
# apex austinfox.com to a single project). Subdomains attach per-project.

# 5. Deploy to production
vercel --prod
```

After deploy, smoke-test against the **custom domain**, not the `*.vercel.app` URL — see Gotchas. If your local resolver hasn't picked up the new subdomain yet, force it via curl `--resolve`:

```bash
VERCEL_IP=$(dig @1.1.1.1 +short cname.vercel-dns.com | head -1)
curl -sI --resolve "<name>.austinfox.com:443:$VERCEL_IP" https://<name>.austinfox.com/
```

Expect `HTTP/2 401` and the custom login HTML for unauthenticated requests; `303` to `/` with a `Set-Cookie` for the right password.

## Step 6: Verify Wildcard DNS (one-time, only if it's missing)

The wildcard `*.austinfox.com → cname.vercel-dns.com` should already be set at Porkbun. If `vercel domains inspect <name>.austinfox.com` shows a misconfiguration, or if `dig @<porkbun-ns> probe.austinfox.com CNAME +short` returns nothing:

1. Verify nameservers actually point to **Porkbun** (`whois austinfox.com | grep -i 'name server'`). If they point elsewhere (e.g. `ns-cloud-*.googledomains.com`), records added in Porkbun's UI won't resolve until nameservers are switched. Switch in Porkbun → domain → Authoritative Nameservers → "Use Porkbun's defaults".
2. In Porkbun's DNS Records: add `Type=CNAME, Host=*, Answer=cname.vercel-dns.com, TTL=600`.
3. Wait 1–5 minutes, then re-run `vercel domains inspect`.

This is a one-time fix per domain. Once set, every future subdomain works with zero DNS work.

## Step 7: Hand Off

Tell the user:
- The live URL.
- The repo URL.
- Where to rotate secrets: `https://vercel.com/<scope>/<project>/settings/environment-variables`.
- That `git push` to `main` triggers an auto-deploy via the Vercel GitHub integration — no need to run `vercel --prod` again unless they want a manual deploy.
- For multi-user: the username:password pairs and how to add a new user (regenerate `USERS` value, rotate the env var).
- For cloud progress: that progress now syncs across devices for the same user; clearing the browser doesn't lose data.

## Gotchas We've Learned

Concrete failure modes encountered in real deploys. Apply these proactively.

**`vercel env add NAME preview --value X --yes` is broken in non-interactive mode.** It prints "Pass branch as third argument, or omit for all Preview branches" — but errors when you do omit. **Fix:** pass an empty string for the branch positional: `vercel env add NAME preview '' --value X --yes`. Production and development don't have this issue.

**`vercel link --scope <personal-account>` fails** with "You cannot set your Personal Account as the scope." Pass `--scope` only for teams. For personal account, run `vercel switch` interactively first or just let `vercel link --yes` pick the scope and confirm with the user.

**Vercel Pro's Standard Deployment Protection blocks `*.vercel.app` URLs.** A 401 with a `_vercel_sso_nonce` cookie is the team's SSO wall, NOT your middleware — Vercel's protection runs *before* Edge middleware on those URLs. The custom domain (`<name>.austinfox.com`) is public on Pro, so smoke-test there. If you must test the `vercel.app` URL, disable protection in Project Settings → Deployment Protection.

**Domain registered at Porkbun does not mean DNS is hosted at Porkbun.** Always verify nameservers with `whois <domain> | grep -i 'name server'` before assuming DNS records added at Porkbun will resolve. If nameservers point elsewhere (Google Cloud DNS, Cloudflare, etc.), either switch them or add records at the actual nameserver provider.

**Local resolver cache lags behind Porkbun's authoritative nameservers.** When verifying DNS or smoke-testing right after `vercel domains add`, query Porkbun directly (`dig @curitiba.ns.porkbun.com ...`) or bypass with curl `--resolve`. Don't get fooled by a stale local cache showing nothing.

## Vercel UI Gotcha: Two Different "Domains" Screens

Vercel has two domain UIs that look similar and confuse newcomers:

| UI | Purpose | Use it when |
|---|---|---|
| **Team → Domains** (account-level) | Claims an apex domain (e.g. `austinfox.com`) and binds it to one project for SSL/nameserver bookkeeping | Only if you want the apex itself to serve a project (e.g. a landing page) |
| **Project → Settings → Domains** | Attaches a specific (sub)domain to that project | **Every subdomain** — `lettera.austinfox.com`, `foo.austinfox.com`, etc. |

Subdomains of the same apex can live on different Vercel projects independently — Vercel verifies each via a DNS lookup against the wildcard CNAME on Porkbun. You do **not** need to claim `austinfox.com` at the team level to attach subdomains to projects. If the user lands on the team-level "Add Domain" dialog asking to assign `austinfox.com` to a project, tell them to back out and use the project-level Domains screen (or the `vercel domains add` CLI from inside the project directory).

## What NOT to Do

- **Don't** enable Vercel's built-in Password Protection (Settings → Deployment Protection) for auth. It requires Advanced Deployment Protection (~$150/mo). The custom middleware achieves the same UX for free.
- **Don't** deploy without setting the auth env var first when one is required — the middleware is a no-op when unset, which would publish the project unprotected.
- **Don't** combine multiple personal projects into one Vercel project. The cost of a separate project is zero; the cost of disentangling later is high.
- **Don't** add Next.js for static personal projects. Vite + React is faster and simpler.
- **Don't** create the GitHub repo as public unless the user explicitly asks.
- **Don't** check passwords or `USERS` strings into the repo (no `.env`, no fallback default in code).
- **Don't** use cloud progress when localStorage suffices. Adds API surface, fail modes, and Marketplace setup for no real-world benefit on a single-device app.

## References

- `references/middleware.ts` — Edge middleware for the **single-password** pattern. Default for most projects.
- `references/middleware-multi-user.ts` — Edge middleware for the **multi-user** pattern (named accounts via `USERS` env var). Use when distinct humans need distinct progress.
- `references/cloud-progress.md` — How to add Upstash Redis-backed cross-device progress. Covers Marketplace setup, the `api/progress.ts` template, and React-side wiring.
