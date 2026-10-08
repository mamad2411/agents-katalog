---
name: emergency-priority2-receipt
description: Send a Pushover EMERGENCY (priority 2) alert that repeats until acknowledged, then poll the receipt until the user acks or it expires. Use when something is urgent and must not be missed - production breakage, a blocked autonomous loop needing immediate input, an alarm-until-acknowledged notification. For routine notifications use send-notification. TRIGGERS - emergency alert, urgent pushover, alarm until acknowledged, priority 2, wake me up.
---

# emergency-priority2-receipt

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Priority-2 emergency notification with receipt polling, via the TS core `pushover_core.ts emergency`.

```bash
env -u HTTPS_PROXY -u HTTP_PROXY bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_core.ts" emergency \
  --title "Title" --message "what happened + the one action needed" \
  [--retry 30] [--expire 300] [--sound piano] [--attach report.png] [--app main|test]
```

## Behavior (verified on a physical device 2026-05-30)

- priority 2 **requires** `retry` (≥ 30 s) and `expire` (≤ 10800 s) — Pushover returns HTTP 400 without them. The core supplies defaults (30 / 300) automatically.
- The response returns a `receipt`; the core polls `/1/receipts/{receipt}.json` every 5 s and prints `{acknowledged, acknowledged_at, expired}` when you ack (verified ack at t+35 s) or it expires.
- `sound=piano` is a custom sound on this account; `pianobar` is the built-in fallback — use `custom-sounds resolve piano pianobar`.
- Attach a `render-incident-report-image` PNG for full detail; keep `--message` ≤ 1024.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the priority-2 alert repeat until acknowledged?** If it stopped early or never fired, fix the retry/expire handling.
2. **Did the receipt poll detect the ack or expiry?** If polling hung or missed the ack, fix the poll loop.

Only update if the issue is real and reproducible — not speculative.
