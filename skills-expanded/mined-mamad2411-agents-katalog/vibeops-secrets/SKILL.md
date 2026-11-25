---
name: vibeops-secrets
description: >
  Collect and securely set the environment variables and secrets an app needs, and check the
  project for accidentally exposed secrets. Use before any deploy, or whenever the user mentions
  API keys, passwords, tokens, .env files, or says 'it works locally but not deployed'.
  Also triggers on: "my app can't connect", "where do I put my API key", "secret", "credentials",
  "environment variables", "set up my keys", "I need to add my stripe key".
---

# Vibeops — Secrets

You are setting up or auditing secrets for the user's project. Your goals in order:
1. Find any secrets accidentally exposed in the codebase and stop them
2. Make sure the project is configured to keep secrets out of git
3. Set all required secrets securely on the hosting platform

Reference the vibeops `references/safety-rules.md` Rule 3 (Leak Gate) throughout this skill.
If `host: railway` is in the config, load `references/railway.md` for platform details.

**What you must never do:**
- Ask the user to paste a secret value into the chat
- Write any secret value to a file, to the config, or to your response
- Display a secret value the user has already pasted (acknowledge it was received; do not echo it)
- Proceed past Step 3 if leaks are found

---

## Resolving the shared scripts (read this first)

Vibeops keeps its scripts as one shared source used by both Claude Code and Codex. This
skill folder is at `codex/skills/vibeops-secrets/`; the shared scripts live at the repo root
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
   `bash "$ROOT/scripts/leak_scan.sh" --all /path/to/user/project`.

Never invoke a bare relative `scripts/<name>.sh` — Codex's working directory is not
guaranteed to be the skill folder. Always go through `$ROOT`.

---

## Step 1 — Read the config

Read `.infra/config.yml` from the user's project root.

**If the file does not exist:**
> "I need your project config before I can set up secrets. Run `vibeops-configure` first — it only takes a few minutes."
> Stop here.

Parse:
- `secrets:` — list of secret names (never values)
- `host:` — platform (railway or render)
- `environments:` — which environments are active

Show the user what secrets their app needs (names only):
> "Your app needs these secrets set before it can run:
> - APP_KEY
> - DATABASE_URL
> - [etc.]
>
> I'm going to walk through setting each one up."

---

## Step 2 — Inventory check

Cross-reference the `secrets:` list in config against a fresh run of `detect_stack.sh` on the user's project:

```bash
bash "$ROOT/scripts/detect_stack.sh" /path/to/user/project
```

Compare `env_vars_referenced` from the JSON output against the names in `secrets:`. If any variable is referenced in code but missing from the `secrets:` list, flag it:

> "I noticed your code also references [VAR_NAME] — should I add that to your secrets list? (I'll update `.infra/config.yml` if you say yes.)"

Do not add variables automatically — ask first.

---

## Step 3 — Leak scan (MUST complete before any further steps)

Run `scripts/leak_scan.sh` on the full project:

```bash
bash "$ROOT/scripts/leak_scan.sh" --all /path/to/user/project
```

**If leaks are found — STOP. Do not proceed to Steps 4–7.**

Report each finding in plain language. Do not show the raw script output verbatim — translate it:

> "I found what looks like a secret hardcoded in your project:"
>
> - `src/config.js` line 14: a value that looks like an API key
> - `.env` file: this file is committed to git and should not be
>
> "I need you to fix these before I set up your secrets. Here's how:"

Resolution steps to offer:
1. For committed `.env` files: "Remove it from git tracking: `git rm --cached .env` then add `.env` to `.gitignore`"
2. For hardcoded values in source files: "Replace the hardcoded value with a reference to the secret setting (e.g., `process.env.MY_KEY`), then commit the change"
3. For values already in git history: "The secret may need to be rotated at the source (change the password/key on the service that issued it), since git history is hard to scrub"
4. After fixing: "Re-run secrets setup and I'll scan again to confirm everything is clean"

**If scan is clean:**
> "No exposed secrets found — your codebase is clean."

---

## Step 4 — Ensure `.gitignore` covers `.env`

Check the user's project `.gitignore` file for `.env` or `.env*` entries.

**If missing:** Add `.env` to `.gitignore` by instructing the user:
> "I've noticed `.env` isn't in your `.gitignore`. Let me add it now."

Run:
```bash
echo ".env" >> /path/to/project/.gitignore
echo ".env.*" >> /path/to/project/.gitignore
```

Then tell the user: "Added `.env` to your `.gitignore` — your secret files won't be committed by accident now."

**If already present:** "Your `.gitignore` already covers `.env` — good."

---

## Step 5 — Ensure `.env.example` exists

Check if `.env.example` exists in the project root.

**If missing:** Generate one from the `secrets:` list — names with empty values only:

```
# .env.example — copy to .env and fill in your values
# Never commit .env — only commit this template file

APP_KEY=
DATABASE_URL=
REDIS_URL=
# ... all secret names from config
```

Tell the user:
> "I've created `.env.example` as a template for your team. It lists all the secret names your app needs, with no values. It's safe to commit — go ahead and add it to git:
> ```
> git add .env.example && git commit -m 'chore: add .env.example template'
> ```"

**If already present:** Check that all names in `secrets:` are listed in the file. Add any missing ones (names only).

---

## Step 6 — Set secrets on the platform

### Check Railway CLI

If `host: railway`:
1. Verify Railway CLI is installed: if `railway: command not found`, guide install:
   > "You'll need the Railway CLI to set secrets from here. Install it: `npm install -g @railway/cli` then `railway login`"
2. Verify authentication: `railway whoami` — if fails, prompt `railway login`
3. Verify project is linked: `railway status` — if not linked, prompt `railway link`

### Run set_secrets.sh

Tell the user what's about to happen:
> "Now I'll collect your secret values. You'll type each one — the input will be hidden, like a password field. Nothing gets saved to your computer."

Run for the `dev` environment:
```bash
bash "$ROOT/scripts/set_secrets.sh" dev .infra/config.yml
```

The script handles all prompting and Railway CLI calls. Relay its output to the user, translated to plain language.

If `environments: [dev, prod]` in config, offer to repeat for production:
> "Dev secrets are set. Want me to set the same secrets for your production environment too? You can use different values if needed (e.g., a separate database)."

If yes:
```bash
bash "$ROOT/scripts/set_secrets.sh" prod .infra/config.yml
```

### Manual fallback (if Railway CLI unavailable)

If Railway CLI cannot be installed or authenticated, guide the user through the Dashboard:
1. Go to your Railway project
2. Click on your app service
3. Click "Variables"
4. Click "New Variable" for each secret name — paste the value in the value field
5. Railway will automatically restart your app with the new variables

---

## Step 7 — Post-completion summary

After all steps complete:

```
Here's what I did:

Leak scan:        [✓ Clean / ✗ Found issues — see above]
.gitignore:       [✓ .env already excluded / ✓ Added .env exclusion]
.env.example:     [✓ Already existed / ✓ Created with N secret names]
Secrets on dev:   ✓ N secret(s) set
[If prod] Secrets on prod: ✓ N secret(s) set

You're ready to deploy. Say "deploy" whenever you want to go live.
```

---

## Jargon rules (same as assess)

- Never call them "environment variables" — say "secrets" or "secret settings"
- Never say "set env vars" — say "set your secrets"
- Never expose values in output — only names
- Do say what each secret is for if you know: "DATABASE_URL is the connection string for your database"
