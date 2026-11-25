---
name: codex-reset-credit
description: Check Codex reset credit status on demand from local Codex auth. Use when the user asks to show, inspect, or check Codex reset credits, reset-credit expiries, or available reset credits without modifying Codex Desktop.
---

# Codex Reset Credit

Use the bundled script to check reset credit status on demand.

## Workflow

1. Run:

```bash
python3 scripts/check_reset_credits.py
```

2. Report the readable output to the user.
3. Do not print or reveal access tokens, account IDs, credit IDs, email addresses, or profile image URLs.
4. If auth is missing or the endpoint fails, report the plain error message.

## Notes

- The script reads `~/.codex/auth.json`.
- The script calls the ChatGPT reset credit endpoint with the local Codex access token.
- Expiry times are shown in this machine's local timezone by default.
- Do not edit `Codex.app`, bundled app files, auth files, or session files.
