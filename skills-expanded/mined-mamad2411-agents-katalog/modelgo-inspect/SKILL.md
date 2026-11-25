---
name: modelgo-inspect
version: 0.1.4
description: "Inspect tenant balance, permissions, and call logs. Use when the user asks about billing, balance, quotas, permissions, access control, call history, usage, API costs, or model consumption. Triggers: 余额, 账单, 权限, 调用日志, 用量, balance, billing, permissions, call logs, usage, cost."
metadata:
  requires:
    bins: ["modelgo"]
  cliHelp: |
    modelgo balance [--json]
    modelgo balance transactions [--type TYPE] [--limit N] [--json]
    modelgo balance grant [--json]
    modelgo permissions [--json]
    modelgo logs [--limit N] [--preset 1h|24h|7d] [--status STATUS] [--model MODEL] [--json]
    modelgo logs <request-id> [--json]
    modelgo logs <request-id> payload [--kind request|response] [--json]
    modelgo logs stats [--group-by MODEL|provider|workspace] [--granularity hour|day] [--json]
    modelgo logs usage [--from DATE] [--to DATE] [--json]
---

# modelgo inspect — balance, permissions, and logs

This skill lets users inspect their tenant's financial status, access permissions, and API call history via the `modelgo` CLI.

> **Setup & version check:** install, login, env/tenant selection, and the
> skill/CLI version-check protocol live in the `modelgo-shared` skill. Align
> versions there before relying on the flags below.

## Command reference (authoritative)

Per-command flags, usage, and examples are auto-generated from the CLI's own
`--help`:

- [`reference/index.md`](reference/index.md) — index + global conventions + exit codes
- [`reference/balance.md`](reference/balance.md), [`reference/permissions.md`](reference/permissions.md), [`reference/logs.md`](reference/logs.md)

Don't guess flags — read the reference file or run `modelgo <command> --help`.

## When to use

When the user asks about any of:
- **Balance/billing**: "What's my balance?", "How much credit do I have?", "Show me my transactions", "Is my grant depleted?"
- **Permissions**: "What can I access?", "Do I have billing permissions?", "Show my access rights"
- **Call logs**: "Show my recent API calls", "Why did my request fail?", "What's my latency?", "How much did gpt-4o cost me?"
- **Usage**: "How many tokens did I use?", "What's my spend this week?", "Give me a usage summary"

## How to use

### Balance

```bash
modelgo balance                # Overview: available balance, frozen, currency, status
modelgo balance transactions   # Billing transaction list
modelgo balance grant          # Registration grant status
```

Common flags: `--json` for machine-readable output, `--type` to filter transactions (consumption/recharge/refund/grant), `--limit N` to cap results.

### Permissions

```bash
modelgo permissions            # Granted permissions + accessible menus
```

### Call Logs

```bash
modelgo logs                            # Recent 20 calls
modelgo logs --preset 7d                # Last 7 days
modelgo logs --model gpt-4o --status error  # Filtered
modelgo logs <request-id>               # Single call detail
modelgo logs <request-id> payload       # Response payload
modelgo logs <request-id> payload --kind request  # Request payload
modelgo logs stats                      # Statistics grouped by model
modelgo logs stats --group-by provider  # Group by provider
modelgo logs usage                      # Usage summary
modelgo logs usage --from 2026-05-01 --to 2026-06-01  # Date range
```

## Notes

- All commands require login first (`modelgo auth login`).
- Commands operate on the active tenant by default. To target a different tenant for one call, use the global `--tenant <slug|id>` flag *before* the subcommand: `modelgo --tenant <slug|id> balance`. An unknown tenant errors (exit 1) instead of silently using the active one.
- Add `--json` to any command for structured output suitable for scripting or further processing.
- On error the CLI prints a plain-text message to stderr and exits non-zero (`1` runtime, `2` usage). `session expired` → re-login; `permission denied` → check `modelgo permissions`.
- If a command looks like a CLI bug (crash, empty/malformed output, malformed `--json`), see `modelgo-shared/assets/issue-reporting.md` before filing an issue.
