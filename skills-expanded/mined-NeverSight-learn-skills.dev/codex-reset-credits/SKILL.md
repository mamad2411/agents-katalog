---
name: codex-reset-credits
description: 查询并用中文展示 Codex 重置次数、每次重置的剩余时间、过期时间，以及过期前 1 天和过期前 1 小时的提醒时间。Use when the user asks how many Codex reset credits, reset次数, rate-limit reset credits, credits expiry times, reminder times, or how long each Codex reset credit has before expiration.
---

# Codex Reset Credits

## Workflow

1. Run `scripts/query_reset_credits.py` with a Python 3 interpreter.
2. Use Chinese for the user-facing result.
3. Report `available_count` as `Codex 重置次数`.
4. For each credit, report:
   - `remaining`: remaining time before expiry, formatted in Chinese.
   - `expires_at_china`: expiry time in `Asia/Shanghai` / UTC+8.
   - reminder time at `expires_at - 1 day`.
   - reminder time at `expires_at - 1 hour`.
5. Do not print or expose the access token from `auth.json`.

## Script

Use the script from this skill directory:

```powershell
python .\scripts\query_reset_credits.py
```

If `python` is not in PATH, use the bundled Codex Python when available:

```powershell
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\scripts\query_reset_credits.py
```

The script reads:

- `%CODEX_HOME%\auth.json` when `CODEX_HOME` is set.
- Otherwise `%USERPROFILE%\.codex\auth.json`.

It calls `https://chatgpt.com/backend-api/wham/rate-limit-reset-credits` with the stored access token and formats the returned `credits[].expires_at` values.

Text output should look like:

```text
Codex 重置次数：2
第 1 次重置：
  剩余时间：23天 15小时 58分钟 18秒
  过期时间：2026-07-27 07:45:22（中国时间）
  提醒时间：
    - 过期前 1 天：2026-07-26 07:45:22（中国时间）
    - 过期前 1 小时：2026-07-27 06:45:22（中国时间）
```

## Reminder Handling

When the user asks to add expiry reminders, first run the script for fresh expiry times. Create reminders at:

- `expires_at - 1 day`
- `expires_at - 1 hour`

Use China time for user-facing wording. When reminders have already been created, still display the reminder schedule in the query result so the user can see it directly.
