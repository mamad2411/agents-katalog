---
name: weekly-system-health-check
description: Weekly full system health check — tests all Eidetic OS subsystems and emails a report.
---

Run a full system health check on your Eidetic OS infrastructure and email
yourself a report.

> Placeholders: `{{USER_EMAIL}}` = recipient, `{{EIDETIC_OS}}` = repo path,
> `{{VAULT_PATH}}` = vault path. The health-check script reads all hosts/ports
> from env vars (see `.env.example`).

**Preferred path — run the script:**
```bash
EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic health --json
```
It probes every subsystem and returns structured JSON. Use that as the basis for
the email. The subsystems it checks:

1. **Vault** — count `.md` files; verify `.claude-index.md`, `wiki/index.md`, `wiki/hot.md`, `wiki/log.md` exist and are recent
2. **RAG Pipeline** — check `vectors.json` size, `last_embed.txt` timestamp, and that the embeddings endpoint (`EMBED_HOST:EMBED_PORT`) is reachable
3. **TTS** — check the TTS endpoint (`TTS_HOST:TTS_PORT`) responds (optional component)
4. **Email** — verify `send_email.py` exists and `SMTP_APP_PASSWORD` is set
5. **Git** — check for a stale `.git/index.lock`, run `git status`, check recent commits
6. **Scheduled Tasks** — list tasks, verify `SKILL.md` files exist
7. **Dashboard** — check frontend (`DASHBOARD_FRONTEND_PORT`) and backend (`DASHBOARD_BACKEND_PORT`) respond
8. **Frontmatter Schemas** — check `.schemas/` and `schemas/enforce_schemas.py` exist
9. **Wiki System** — verify the wiki folder and index files

**For each system:** Report ✅ Working | ⚠️ Degraded | ❌ Down with specifics.

**Auto-fix what you safely can:**
- If `.git/index.lock` exists: `git worktree prune && rm -f {{VAULT_PATH}}/.git/index.lock`
- If the working tree is dirty: commit with `EIDETIC_TRIGGER=scheduled eidetic commit`

**Email the report** using `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited):
- To: `{{USER_EMAIL}}`
- Subject: `🏥 Eidetic Weekly Health Check — [date]`
- Include every subsystem status and any action items.
