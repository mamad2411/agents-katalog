---
name: vibeops-deploy
description: >
  Build and deploy the app to its live environment, with health checks and one-command rollback.
  Only runs when the user explicitly asks to deploy, ship, go live, push to production, or
  update the live site. Never triggers on ambient or future-tense mentions of deploying.
  Requires .infra/config.yml to exist before running.
---

# Vibeops — Deploy

You are deploying the user's app to Railway. This skill has real side effects: it builds code, creates live deployments, and if production is configured, makes changes that real users will see.

**This is a gated skill.** In Codex it is marked `allow_implicit_invocation: false` — it must be invoked explicitly (e.g. `$vibeops-deploy`). Do not run it from an ambient mention.

**Required references:**
- The vibeops `references/safety-rules.md` — Rules 1 (Destructive Blocklist), 2 (Production Lock), 3 (Leak Gate), 5 (Dry-Run First)
- `references/railway.md` — load when `host: railway` in config

**This skill only runs when the user explicitly says to deploy.** It does not trigger on "I want to deploy someday" or "we'll need to deploy later." Ambient mentions = do not run.

---

## Resolving the shared scripts (read this first)

Vibeops keeps its scripts as one shared source used by both Claude Code and Codex. This
skill folder is at `codex/skills/vibeops-deploy/`; the shared scripts live at the repo root
under `scripts/`. Before running any script, establish the absolute vibeops root **once**:

1. Find the absolute path of **this skill's own directory** on disk (the folder containing
   this `SKILL.md`). Call it `SKILL_DIR`.
2. Run the locator and capture its output — it prints the canonical absolute root (it prefers
   `$CLAUDE_PLUGIN_ROOT` if set, otherwise derives the root from its own location, so it is
   correct regardless of the current working directory):

   ```bash
   ROOT="$(bash "$SKILL_DIR/../../../scripts/vibeops_root.sh")"
   ```

3. Call every shared script through that absolute `ROOT`, for example
   `bash "$ROOT/scripts/deploy.sh" .infra/config.yml`.

Never invoke a bare relative `scripts/<name>.sh` — Codex's working directory is not
guaranteed to be the skill folder. Always go through `$ROOT`.

---

## Step 1 — Pre-flight checks

Before doing anything else, verify the project is ready to deploy.

### 1a. Read `.infra/config.yml`

If the file does not exist:
> "I need your project configured before I can deploy. Run `vibeops-configure` first."
> Stop.

Parse: `app.name`, `stack.build`, `stack.start`, `host`, `environments`, `secrets`

### 1b. Check Railway CLI

Run `railway whoami`. If not authenticated:
> "You need to be logged in to Railway first. Run `railway login` and then come back."
> Stop.

Run `railway status`. If no project linked:
> "Your project isn't linked to a Railway project yet. Run `railway link` to connect, or `railway init` to create a new one."
> Stop.

### 1c. Check secrets are set

Run `railway variables --environment dev` and compare the output against the `secrets:` list in config.

If any secrets are missing:
> "Some secrets aren't set yet. Before deploying, I need to collect them — otherwise your app will fail to start.
>
> Missing: [SECRET_NAME_1], [SECRET_NAME_2]
>
> Say 'set up secrets' and I'll walk you through it, or run `vibeops-secrets` directly."
> Stop.

---

## Step 2 — Leak gate (Rule 3)

Run `scripts/leak_scan.sh` on staged files:

```bash
bash "$ROOT/scripts/leak_scan.sh" --staged /path/to/project
```

If leaks found:
> "I found exposed secrets in your staged files — I can't deploy until these are fixed."

Translate each finding to plain language. Point to `vibeops-secrets` to resolve.

**Do not proceed if the leak gate fails.**

---

## Step 3 — Dry-run plan (Rule 5)

Print the deployment plan before running anything:

```
Here's what I'm going to do:

1. Run your build: [stack.build from config]
2. Deploy to your dev environment on Railway
3. Wait for the app to start and check it's responding
[If prod in environments:]
4. Ask for your confirmation before pushing to production
5. Deploy to production with a second health check
6. Give you the live URL

[If prod:] I'll keep the previous version pinned — if anything goes wrong, one command reverts it.

Type 'yes' to run this, or tell me what you'd like to change.
```

Wait for explicit confirmation. Do not proceed without it.

---

## Step 4 — Execute `scripts/deploy.sh`

Run the deploy script:

```bash
bash "$ROOT/scripts/deploy.sh" .infra/config.yml
```

Relay its output in plain English. Do not show raw Railway CLI output — translate each step as it completes:

- "Running your build..." → "Build finished successfully." or "Build failed — see errors above."
- "Deploying to dev..." → "Deployed to dev. Checking it's working..."
- "Health check passed" → "Dev is up and responding."
- "Health check failed" → "Dev didn't start correctly. I've rolled it back automatically. Here's what to check: [translated reasons]"

### Translate `deploy.sh` output

Stream `deploy.sh` output to the user with this translation approach:
- Replace technical Railway CLI status messages with plain-English equivalents
- Keep error messages verbatim (they contain important technical info the user may need to share)
- Prefix each translated line with the current step number from the plan

### Production confirmation (Rule 2)

When `deploy.sh` prompts for production confirmation, relay the prompt exactly:

> "Dev deployment looks good.
>
> I'm ready to push to production. **This will update your live app** — real users will see the new version immediately.
>
> Type **DEPLOY** to continue, or anything else to cancel."

This confirmation is required by Rule 2 (Production Lock). Do not skip it, do not pre-confirm on the user's behalf.

---

## Step 5 — Report outcome

### Success

```
Your app is live!

Dev:        https://your-app-dev.up.railway.app
[If prod:]
Production: https://your-app.up.railway.app

If anything goes wrong, say "rollback" — I'll revert to the previous version instantly.
```

### Dev-only success (no production configured)

```
Deployed to dev!

Dev URL: https://your-app-dev.up.railway.app

When you're ready to go live with real users, run vibeops-configure to add
a production environment, then deploy again.
```

### Health check failure (auto-rollback ran)

```
The deployment didn't pass the health check — something went wrong when the app started.

I've automatically rolled back to the previous version, so your live app is still running normally.

Here's what to check:
1. Are all secrets set correctly? (Say "check secrets" to verify)
2. Did the build succeed? (Check the build output above for errors)
3. Is your app listening on $PORT? Railway sets this automatically — your app must use it
4. Check your app logs: railway logs --environment [dev/production]

Say "doctor" to run a full diagnosis, or fix the issue and say "deploy" again.
```

### Build failure

```
The build failed before anything was deployed. No changes were made to your live app.

Build error: [the error from deploy.sh output]

Fix the build error above and say "deploy" again when ready.
```

---

## Rollback (if user says "rollback" after this skill ran)

Route immediately to `scripts/rollback.sh`:

```bash
bash "$ROOT/scripts/rollback.sh" [env] .infra/config.yml
```

Relay the rollback script's confirmation prompt verbatim. Translate its output to plain English.

---

## What you must never do

- Never skip the dry-run plan (Step 3)
- Never skip the production confirmation prompt (Rule 2)
- Never run deploy.sh without first passing the leak gate (Step 2)
- Never attempt a `git push --force` to main or any destructive command (Rule 1)
- Never tell the user "I deployed" if deploy.sh did not confirm success
- Never show raw Railway CLI output without translation
- Never deploy if pre-flight checks (Step 1) failed — always stop and explain what's missing
