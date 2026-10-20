---
name: vibeops-teardown
disable-model-invocation: true
description: >
  Permanently delete a project's hosted infrastructure — project, environments, database,
  cache — to stop all billing. Only runs when the user explicitly asks to tear down, delete,
  remove, shut down, or stop paying for their hosted app. Never triggers on ambient mentions.
  Irreversible — requires two separate typed confirmations.
---

# Vibeops — Teardown

You are permanently deleting the user's hosted infrastructure. This is the most destructive action vibeops can take — there is no rollback. Treat it as always-prod-locked, regardless of which environments exist.

**Required references:** `references/safety-rules.md` Rule 1 (Destructive Blocklist) and Rule 2 (Production Lock).

**This skill only runs on explicit request.** "I don't need this anymore" is not enough on its own — confirm the user actually wants to tear down and delete, not just stop working on it for now.

---

## Step 1 — Confirm intent in plain language

Before running anything, make sure the user understands what's about to happen:
> "This will permanently delete [app name]'s hosting, database, and all its data. This cannot be undone. Are you sure you want to do this?"

If there's any hesitation, stop and clarify rather than proceeding.

---

## Step 2 — Run `scripts/teardown.sh`

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/teardown.sh" .infra/config.yml
```

The script enforces two separate confirmation gates — relay both verbatim, never pre-confirm on the user's behalf:

1. **Type the app name** — proves the user is targeting the right project
2. **Type `DELETE EVERYTHING`** — the final irreversible confirmation

Because the Railway CLI has no command to fully delete a project, the script then walks the user through the exact Dashboard steps (Settings → Danger Zone → Delete Project) and waits for them to type `DONE` after they've done it. Relay these steps exactly as the script prints them — never invent a faster CLI shortcut that doesn't exist.

---

## Step 3 — Report outcome

**Confirmed:**
> "Done — your project has been removed. One more thing: check your Railway billing page to make sure no further charges show up: https://railway.app/account/billing"

**Cancelled at either gate:**
> "Cancelled — nothing was deleted."

**Stopped before confirming dashboard deletion:**
> "Okay, I've stopped here. Your project hasn't been confirmed as deleted yet. Let me know when you're ready to finish."

---

## What you must never do

- Never run this skill from an ambient mention — only on explicit request to tear down, delete, remove, or stop paying for hosting
- Never skip either confirmation gate
- Never claim deletion succeeded without the user confirming they completed the Dashboard step
- Never fabricate a one-shot CLI delete command — Railway doesn't expose one; always route to honest Dashboard guidance
- Never treat "dev only, no prod" as lower-risk — teardown is irreversible regardless of environment
