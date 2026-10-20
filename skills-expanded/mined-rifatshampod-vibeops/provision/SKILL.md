---
name: vibeops-provision
disable-model-invocation: true
description: >
  Create and set up all the cloud infrastructure an app needs — hosting environment, database,
  and cache — according to the project's .infra/config.yml. Only runs when the user explicitly
  asks to provision or set up infrastructure. Never triggers on ambient mentions of provisioning.
  Requires .infra/config.yml to exist before running.
---

# Vibeops — Provision

You are creating the user's cloud infrastructure: their Railway project, environments, and any managed database or cache. This skill has real side effects and costs money — it only runs when the user explicitly asks.

**Required references:** `references/safety-rules.md` Rules 4 (Cost Interstitial), 5 (Dry-Run First), 6 (Idempotency). Load `references/railway.md` if `host: railway`.

**This skill only runs when the user explicitly asks to provision or set up infrastructure.** Ambient mentions ("I'll need a database eventually") do not trigger it.

---

## Step 1 — Pre-flight checks

Read `.infra/config.yml`. If missing:
> "I need your project configured before I can set anything up. Run `vibeops-configure` first."
> Stop.

Check Railway CLI installed and authenticated (same checks as `vibeops-deploy` step 1b — `railway whoami`, prompt `railway login` if needed).

---

## Step 2 — Cost interstitial (Rule 4)

Run `scripts/provision.sh`, which prints its own cost estimate before creating anything. Relay it verbatim, translated to plain language — never say "Postgres," say "a database"; never say "Redis," say "a way to speed up repeated requests."

Example translation:
> "This will cost approximately $15-25/month: about $5-10 for running your app, plus $5-10 for your database."

---

## Step 3 — Dry-run plan (Rule 5)

The script also prints a numbered plan before doing anything, marking what's skipped because it already exists (Rule 6). Relay this verbatim — do not hide the "already exists, skipping" lines, they're proof nothing gets duplicated.

Wait for the script's own "Type 'yes'" prompt. Never pre-confirm.

---

## Step 4 — Execute and translate output

Run the provision script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/provision.sh" .infra/config.yml
```

Stream `scripts/provision.sh`'s output, translated line by line, same approach as `vibeops-deploy`:
- "Creating Railway project..." → "Setting up your project..."
- "Creating dev environment..." → "Setting up your dev environment..."
- "Adding a managed database..." → "Setting up your database..."
- Keep error messages verbatim — they carry information the user may need to share.

---

## Step 5 — Report outcome

Translate the script's Created/Already set up/Failed summary into plain language:

```
Here's what's set up now:
- Your project: [created / already there]
- Dev environment: [created / already there]
[If prod configured] Production environment: [created / already there]
[If database] Your database: [created, backed up daily / already there]
[If cache] A way to speed up repeated requests: [created / already there]

Next step: say "set up secrets" to collect your API keys, or "deploy" if secrets are already set.
```

If anything failed, report it plainly with the raw error, and suggest retrying provision once the issue is fixed — re-running is always safe (Rule 6).

---

## What you must never do

- Never create a resource without first checking it doesn't already exist (Rule 6) — this is handled by `provision.sh`, but never bypass it by running raw `railway add`/`railway init` commands yourself
- Never skip the cost interstitial (Rule 4)
- Never skip the dry-run plan (Rule 5)
- Never run this skill from an ambient mention — only on explicit request
- Never claim something was created if the script reported it as skipped or failed
