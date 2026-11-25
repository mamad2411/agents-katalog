---
name: system
description: Execute allowlisted shell commands and inspect running processes.
module: builtin_tools.sys_ops
tools:
  - shell_command
  - process_list
---

# System Skill

System-level execution with strict-default guardrails.

## `shell_command`

- Required: `command`
- Optional: `cwd`, `timeout` (seconds, clamped to 1..120)
- Security model:
  - command allowlist enforced
  - blocked commands take precedence
  - command chains are parsed and validated segment-by-segment
  - output length capped

## `process_list`

- Optional: `filter` (substring match)
- Returns top process list (platform-specific fields)

## Policy

Use system commands only when needed for user tasks.
Avoid risky mutations unless explicitly requested by the user.

## PowerShell Notes

- Prefer explicit cmdlets for inspection workflows:
  `Get-ChildItem`, `Get-Content`, `Select-String`, `Where-Object`,
  `Select-Object`, `Sort-Object`, `Measure-Object`, `Test-Path`,
  `Join-Path`, `Get-FileHash`.
- Keep scripts ASCII-safe and avoid inline interpreters for security.
