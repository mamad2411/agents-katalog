---
name: vibeops-doctor
description: >
  Diagnose and fix a broken or misbehaving deployment by checking the most common causes in
  order. Use whenever the user says the app is down, broken, erroring, won't start, showing
  a blank page, or 'works locally but not in production'.
  Also triggers on: "500 error", "502 bad gateway", "app crashed", "deployment failed",
  "can't connect", "logs show error", "my site is down".
---

# Vibeops — Doctor

You are diagnosing a broken or misbehaving deployment. Run the fixed runbook below in exact order — every time, no skipping, no reordering. Predictability matters more than cleverness for a triage tool: the user is stressed, and a consistent process builds trust.

**Required references:** the vibeops `references/safety-rules.md` Rule 1 (Destructive Blocklist — never run destructive commands while diagnosing). Load `references/railway.md` if `host: railway`.

---

## Resolving the shared scripts (read this first)

Vibeops keeps its scripts as one shared source used by both Claude Code and Codex. This
skill folder is at `codex/skills/vibeops-doctor/`; the shared scripts live at the repo root
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
   `bash "$ROOT/scripts/detect_stack.sh" /path/to/project`.

Never invoke a bare relative `scripts/<name>.sh` — Codex's working directory is not
guaranteed to be the skill folder. Always go through `$ROOT`.

---

## Pre-check

Read `.infra/config.yml`. If missing:
> "I don't see a vibeops config for this project yet. Run `vibeops-configure` first, then come back if something's still broken."
> Stop.

Determine target environment (ask if ambiguous: "Is this happening on dev, production, or both?").

---

## The runbook (always run all 6 steps, in this order)

Run every step even if an earlier one finds the cause — the report should be complete. Exception: if the user explicitly asks to stop and fix immediately after a finding, you may pause the runbook there.

### 1. Runtime version

Run a fresh `detect_stack.sh` to get the expected runtime:
```bash
bash "$ROOT/scripts/detect_stack.sh" /path/to/project
```

Compare the `runtime` field against what's actually deployed (build logs show the installed runtime version — `railway logs --environment [env]` near the start of the build).

Report: "Your app expects [runtime] — the platform is using [X]." or "Runtime version looks fine."

### 2. Dependencies

Check the most recent build log for install failures:
```bash
railway logs --environment [env]
```

Look for non-zero exits from `npm install`, `composer install`, `pip install`, `bundle install`, `go mod download`, etc.

Report: "Your dependency install failed during the build — here's the error: [translated]." or "Dependencies installed fine."

### 3. Secrets

```bash
railway variables --environment [env]
```

Diff against the `secrets:` list in config. Report missing names only — never values.

Report: "These secrets aren't set: [names]. A missing secret is the most common reason an app works locally but not when deployed." or "All required secrets are set."

### 4. Database and cache connectivity

If config has a `database:` block (or cache dependency from a fresh `detect_stack.sh` run), check recent logs for connection-refused, timeout, or auth-failure patterns:
```bash
railway logs --environment [env] | grep -iE "connection refused|could not connect|timeout|ECONNREFUSED|authentication failed"
```

Report: "Your app can't reach its database — [translated reason]." or "Database connection looks fine." Skip this step's findings (not the step) if no database/cache configured.

### 5. Ports and health endpoint

Check whether the app's start command binds to `$PORT` rather than a hardcoded port (grep source/start command for literal port numbers like `3000`, `8000`, `5000`).

Then curl the live URL the same way `deploy.sh` does — try `/health` first, fall back to `/`:
```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$URL/health"
curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$URL/"
```

Report: "Your app is hardcoded to port [X] instead of using the platform's \$PORT — that'll cause it to never come up." or "App is listening correctly but not responding (HTTP [code])." or "App responds normally (HTTP 200)."

### 6. Recent logs

```bash
railway logs --environment [env] -n 50
```

Find the **first** ERROR line (not the last — the first error is usually the root cause; later ones are often downstream noise).

Report the translated first error line in plain language.

---

## After the runbook — propose a fix

Summarize all 6 findings together, even the "looks fine" ones, so the user sees the full picture. Then identify the single most likely root cause and propose one fix.

**Apply nothing without confirmation.** Print the proposed fix, then ask:
> "Want me to fix this now?"

Route based on the fix type:

| Root cause | Route to |
|---|---|
| Missing secret | "Say 'set up secrets' and I'll walk you through it" → `vibeops-secrets` |
| Bad/stale deploy, needs rebuild | "Say 'deploy' to redeploy with the fix" → `vibeops-deploy` |
| Schema/migration issue | "Say 'fix the database' and I'll run a safe migration" → `vibeops-db` |
| Something doctor can't resolve (e.g. third-party outage, platform issue) | Explain plainly, suggest checking Railway's status page |

---

## What you must never do

- Never skip a runbook step, even if you're confident you've already found the cause
- Never apply a fix without explicit user confirmation
- Never run a destructive command as part of diagnosis (Rule 1) — this skill only reads (logs, variables list, curl checks), it never writes
- Never show a raw `railway logs` dump untranslated — extract the relevant lines and explain them in plain language
- Never claim a fix worked without re-checking (e.g. re-running the health check after a redeploy)
