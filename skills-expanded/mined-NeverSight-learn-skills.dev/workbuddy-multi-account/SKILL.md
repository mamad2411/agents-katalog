---
name: workbuddy-multi-account
description: This skill should be used when the user wants to launch multiple WorkBuddy instances with different accounts simultaneously. It handles starting WorkBuddy with isolated user-data directories so each instance maintains its own login session, settings, and workspace state without interference.
---

# WorkBuddy Multi-Account Launcher

## Purpose

Enable running multiple WorkBuddy instances simultaneously, each logged in with a different account. This is achieved by launching each instance with a unique `--user-data-dir` argument, which isolates login sessions, settings, and workspace data.

## Key Concept

WorkBuddy is built on Electron. Each instance can be given an independent data directory via:

```
--user-data-dir="<path>"
```

- Default account data: `%APPDATA%\WorkBuddy`
- Additional accounts: `%APPDATA%\WorkBuddy-<AccountName>` (e.g., `WorkBuddy-Account2`)

## Workflow

### Launch an additional account (PowerShell)

Use the bundled script `scripts/launch_account.ps1`:

```powershell
# Launch with default second account name "Account2"
& "$env:USERPROFILE\.workbuddy\skills\workbuddy-multi-account\scripts\launch_account.ps1"

# Launch with a custom account name
& "$env:USERPROFILE\.workbuddy\skills\workbuddy-multi-account\scripts\launch_account.ps1" -AccountName "Work"
```

Or run inline directly:

```powershell
Start-Process -FilePath "C:\Program Files\WorkBuddy\WorkBuddy.exe" `
    -ArgumentList "--user-data-dir=`"$env:APPDATA\WorkBuddy-Account2`""
```

### Launch multiple accounts at once

```powershell
# Account 2
Start-Process -FilePath "C:\Program Files\WorkBuddy\WorkBuddy.exe" -ArgumentList "--user-data-dir=`"$env:APPDATA\WorkBuddy-Account2`""

# Account 3
Start-Process -FilePath "C:\Program Files\WorkBuddy\WorkBuddy.exe" -ArgumentList "--user-data-dir=`"$env:APPDATA\WorkBuddy-Account3`""
```

## Notes

- The default (first) account does NOT need `--user-data-dir`; it always uses `%APPDATA%\WorkBuddy`.
- Each additional account's data is persisted in its own folder and survives restarts.
- To remove an account profile entirely, delete the corresponding folder under `%APPDATA%`.
- If the user asks to "open another account", "多开账号", "用另一个账号", or similar phrasing — this skill applies.
