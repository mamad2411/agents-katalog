---
name: vibeops-db
description: >
  Run database migrations and schema changes safely, with automatic backups and protection
  against destructive changes in production. Use whenever the user mentions migrations,
  database changes, schema, adding or removing tables or columns, or 'I need to update the database'.
  Also triggers on: "new table", "alter table", "drop column", "run migrations".
---

# Vibeops — Database Migrations

You are running a database migration for the user's project. This skill has real side effects on data — it can be destructive if mishandled, so every step is wrapped in `scripts/safe_migrate.sh`, never run by hand.

**Required references:**
- The vibeops `references/safety-rules.md` — Rules 1 (Destructive Blocklist) and 2 (Production Lock)
- `references/railway.md` — load when `host: railway` in config

---

## Resolving the shared scripts (read this first)

Vibeops keeps its scripts as one shared source used by both Claude Code and Codex. This
skill folder is at `codex/skills/vibeops-db/`; the shared scripts live at the repo root
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
   `bash "$ROOT/scripts/safe_migrate.sh" dev .infra/config.yml`.

Never invoke a bare relative `scripts/<name>.sh` — Codex's working directory is not
guaranteed to be the skill folder. Always go through `$ROOT`.

---

## Step 1 — Read `.infra/config.yml`

If the file does not exist:
> "I need your project configured before I can run migrations. Run `vibeops-configure` first."
> Stop.

If there's no `database:` block in the config:
> "Your app isn't set up with a database yet — there's nothing to migrate."
> Stop.

---

## Step 2 — Identify the migration

Ask the user what changed, or check for pending migrations using the framework's own status command if one exists (e.g. `php artisan migrate:status`, `npx prisma migrate status`).

Explain in plain language what's about to happen before running anything:
> "This will add a new `email_verified` column to your users table."

If you can't tell what the migration does from the files, say so plainly and ask the user to describe it before continuing.

---

## Step 3 — Dry-run plan (Rule 5)

Print the plan before running anything:

```
Here's what I'm going to do:

1. Check your migration files for anything that deletes data or tables
2. Run the migration on your dev environment first
3. [If prod configured] Remind you to confirm a backup exists, then ask before touching production

Type 'yes' to continue, or tell me what you'd like to change.
```

Wait for explicit confirmation before proceeding.

---

## Step 4 — Run on dev

```bash
bash "$ROOT/scripts/safe_migrate.sh" dev .infra/config.yml
```

Translate the script's output to plain language as it runs. The script prints its own confirmation prompt ("Type 'yes' to run this") — relay it verbatim, do not pre-confirm on the user's behalf.

**If dev migration fails:** stop here. Report the error plainly. Do not touch production.

> "The migration didn't complete on dev. Here's what went wrong: [error]. Want me to run a full diagnosis? Say 'doctor'."

---

## Step 5 — Production (if configured)

If `environments` in config includes `prod`, offer to continue:
> "Dev migration looks good. Want me to run this on production too?"

If yes:

```bash
bash "$ROOT/scripts/safe_migrate.sh" prod .infra/config.yml
```

The script will, in order:
1. Remind the user to verify a recent backup exists (Railway's automatic backups, or a manual one) — relay this verbatim
2. If it found destructive statements (DROP/TRUNCATE/column-drop) in the migration files, show them and require the user to type **I UNDERSTAND THE RISK** before continuing — relay this prompt exactly, do not summarize it away
3. Require the standard production confirmation — type **DEPLOY** — relay this exactly too

**Never pre-confirm any of these prompts on the user's behalf.** Both gates exist independently — a destructive migration to prod must pass both.

---

## Step 6 — Report outcome

**Success:**
> "Migration complete on [dev/production]. Your database schema is up to date."

**Blocked by destructive-statement gate (user declined):**
> "Cancelled — no changes were made to production. The migration included statements that could delete data, so I held off until you confirm. Let me know if you want to review what would have changed."

**Failed:**
> "The migration failed on [dev/production]. Error: [error from script output]. Your database wasn't left half-migrated by this script — that depends on your migration tool's own failure handling. Say 'doctor' if you want a full diagnosis."

---

## What you must never do

- Never run a migration command directly via raw CLI — always go through `scripts/safe_migrate.sh`
- Never run a production migration without the Rule 2 confirmation (typed **DEPLOY**)
- Never suppress, skip, or auto-answer the destructive-statement gate (typed **I UNDERSTAND THE RISK**)
- Never claim a backup was taken if `safe_migrate.sh` only reminded the user to check Railway's automatic backups — it does not run `pg_dump` itself (it has no access to database credentials)
- Never proceed to production if the dev migration failed
