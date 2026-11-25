---
description: Audit the whole git history and working tree for leaked secrets and unsafe files before sharing or publishing the repo
disable-model-invocation: true
---

Scan output (secret values are never printed):

!`bash ${CLAUDE_SKILL_DIR}/scan.sh`

Interpret the result:

1. **Files ever tracked** must not include `.env`, `.env.*` (other than `.env.example`), `*.local.json`, `*.pem` or `*.key`. Any such file in history is a leak.
2. **Pattern hits** (Discord bot tokens, Apify tokens, GitHub tokens, private keys, cloud keys, long values assigned to `*_KEY`/`*_TOKEN`/`*_SECRET`/`*_PASSWORD`): open each hit with `git show <rev>:<path>` only to decide whether it is a real secret or a placeholder. Do not paste real values into the conversation.
3. **Known-secret hits** compare the values in your current environment (`MCP_API_KEY`, `DISCORD_BOT_TOKEN`, `APIFY_TOKEN`, `GMAIL_APP_PASSWORD`) against every revision. Any count above 0 is a confirmed leak.
4. Check GitHub too: `gh api repos/<owner>/<repo>/commits/<old-sha>` returning a commit means orphaned commits are still fetchable even if no branch reaches them.

If a real secret is in history:

1. Rotate it at the provider now (Discord: Reset Token; Apify: regenerate; Google: revoke the app password; new `MCP_API_KEY` via Vercel env and redeploy).
2. Deleting the secret from history is not enough. Create a fresh repository, push the cleaned history there, and delete the old repository (`gh auth refresh -s delete_repo` then `gh repo delete`).
3. Delete old Vercel deployments or the project if their uploaded source contained the secret.
4. Re-run this audit and confirm zero hits.

Also confirm: `.gitignore` still covers `.env*` (except the example), `.capes.local.json` and `.claude/settings.local.json`; `git status` shows nothing sensitive untracked.
