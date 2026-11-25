---
name: health-check
description: Verify env, DB schema, allowlist config, today's token budget, and Telegram bot reachability. Returns JSON status; DMs admin on failure.
user-invocable: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB", "TELEGRAM_BOT_TOKEN", "ADMIN_TG_USER_ID"]
      os: ["linux", "darwin"]
---

Run `python3 -m core.skills.health_check`. Output is JSON `{ok, checks: {...}, errors: []}`.

Hard rules:
- Never reads/loads `MEMORY.md` or `USER.md` (callable from any session).
- On any check failure, sends an admin DM via `post-telegram --kind admin` and
  exits non-zero. The pipeline checklist treats non-zero as "skip this tick".
