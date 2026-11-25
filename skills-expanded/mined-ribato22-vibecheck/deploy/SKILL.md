---
name: deploy
description: Pre-deploy check for "it works on my machine but breaks in production". Finds env vars missing on the host, hardcoded localhost URLs, imports whose letter case only works on Mac/Windows, packages missing from package.json, servers that ignore $PORT or only listen on localhost inside a container, SQLite and file writes on serverless hosts, Prisma clients that never get generated, and the host-side steps people forget (migrations, auth redirect URLs, live webhooks). Use before a first or big deploy, when a build or deploy fails, when something is "undefined" or broken only in production, or when the user asks if the app is ready to deploy to Vercel, Netlify, Cloudflare, Railway, Render, Fly, Heroku or Docker.
argument-hint: "[path] [--host vercel|netlify|cloudflare|railway|render|fly|heroku|docker|local]"
---

# vibecheck deploy: will it run in production?

`/vibecheck:check` asks "is it safe?". This asks "will it still work after I deploy?" Most "works on my machine" failures come from a short list: an env var that only exists in your local `.env`, a URL that points at localhost, a file name whose letter case your Mac ignores, a package that was never added to package.json, a server on the wrong port, a database file on a host that wipes its disk. Find them before your users do.

## Ground rules

- **Read-only.** Don't deploy, don't change host settings, don't edit code. Offer fixes; `/vibecheck:fix` or the user applies them.
- **Never print env var values.** Work with names only, in chat, in files and in commands. Avoid commands that print or download values, such as `vercel env pull`, `heroku config` or `railway variables`.
- **Ask before running a host CLI.** Even a read-only listing talks to the user's account.
- **Reply in the user's language.**

## Step 1: Where and how does it deploy?

Find the host. The preflight detects `vercel.json`, `netlify.toml`, `wrangler.toml`, `amplify.yml`, `railway.json`, `render.yaml`, `fly.toml`, `Procfile`, a `Dockerfile` and a linked `.vercel/` folder. Many Vercel and Netlify projects have no config file at all, so if nothing is detected, check the README or ask the user. Also find out how it deploys (git push, CLI, Docker image) and, in a monorepo, which folder is the app root on the host.

If the app only ever runs on this machine (a local demo or internal tool started with `npm start`), the host is `local`. Pass `--host local`: localhost URLs, loopback binds and fixed ports are correct there and aren't flagged, and host-dashboard reminders are skipped. The verdict becomes "READY (local only)". If the target later changes, run again with the real host.

## Step 2: Run the preflight

```bash
node "${CLAUDE_SKILL_DIR}/scripts/preflight.mjs" "<path>" --json --host <host>
```

`${CLAUDE_SKILL_DIR}` is the folder containing this SKILL.md. Leave out `--host` if you don't know it yet. The script is read-only, has no dependencies, makes no network calls, never reads env values and needs Node 18+.

It returns `findings`, `env` (names only: `used` with where and whether the code has a fallback, `defined_locally`, `documented`, `on_host`, and `set_on_host`: the names the host needs), `reminders` (host-side steps derived from the stack) and `notes`.

## Step 3: Compare env vars with the host (ask first)

Get the list of names set on the host for **production**:

| Host | Names-only source |
|---|---|
| Vercel | `vercel env ls production` |
| Fly | `fly secrets list`, plus `[env]` in fly.toml |
| Cloudflare Workers/Pages | `wrangler secret list`, plus `[vars]` in wrangler.toml |
| Supabase Edge Functions | `supabase secrets list` |
| Netlify, Railway, Render, Heroku, Amplify | the dashboard's environment variables page: ask the user to paste the **names only** |

Save the names to `.vibecheck/host-env.txt`, one per line. Create `.vibecheck/` with a `.gitignore` containing `*` if it doesn't exist. Then re-run the preflight with `--host-env .vibecheck/host-env.txt`.

## Step 4: Verify, then cover what code can't show

- Confirm every finding by reading the code, and drop false positives. Check that a "missing" env var really has no default (a default can hide inside a helper, like `parseScale(process.env.SCALE)`), and that an undeclared package isn't a framework built-in or a path alias the script didn't know about. Env vars and URLs in `scripts/`, `tools/` and `seeds/` folders are treated as dev tooling and skipped; if one of those actually runs in production, check it by hand.
- Read the matching section of [references/hosts.md](references/hosts.md) and check its items.
- Turn `reminders` into a checklist. Ask the user about each dashboard step you can't verify, such as auth redirect URLs, live webhooks or migrations applied to the production database.

## Step 5: Verdict and report

- 🛑 **WILL BREAK**: any verified high or critical finding.
- ⚠️ **FIX FIRST**: verified medium findings.
- 🚀 **READY TO DEPLOY**: neither. If env vars weren't compared with the host, say "ready once the N env vars below are set on the host". For `--host local`, say "READY (local only)".

Write `.vibecheck/deploy.md`. Rename an existing one to `deploy.prev.md` first, and create `.vibecheck/` with its `.gitignore` if needed. Include:
1. the verdict, the host, and how it deploys
2. each finding: what will happen in production, where (`file:line`), the fix, and a fix prompt the user can paste into any AI tool
3. an env table: `Variable | Used in | In local .env | In .env.example | On host | Action`, with names only
4. the host checklist from `reminders` and references/hosts.md
5. after the deploy: where the logs are, and the 3–5 flows to click through once

## Step 6: Tell the user

```
🚀 vibecheck deploy: 🛑 WILL BREAK on Vercel
2 high · 1 medium · 5 env vars to set on the host

1. 🛑 `import Button from '../components/button'`: the file is Button.tsx. Works on your Mac, fails on Vercel's Linux build. (src/app/page.tsx:3)
2. 🛑 STRIPE_SECRET_KEY isn't set on Vercel: checkout will fail.
3. ⚠️ Falls back to http://localhost:3000 if NEXT_PUBLIC_API_URL is missing. (src/lib/api.ts:2)

Set on the host: OPENAI_API_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL
Then: prisma migrate deploy · Supabase redirect URLs · Stripe live webhook
Full list: .vibecheck/deploy.md · /vibecheck:fix can fix the code items
```

If `/vibecheck:check` hasn't been run, suggest it too: this skill checks that the app will run, not that it's safe.
