---
name: mimir-help
description: Show all Mimir commands and the recommended workflow.
allowed-tools: []
---

Print the following help text verbatim. Do not execute any commands.

---

⚡ **Mimir** — Claude Code preflight checker

**Commands:**

| Command | Description |
|---|---|
| `/mimir "<task>"` | Estimate token cost + risk before running |
| `/mimir "<task>" --files f1 f2` | Include specific files in estimate |
| `/mimir "<task>" --git-diff` | Include current git diff in estimate |
| `/mimir "<task>" --turns N` | Include N conversation turns in estimate |
| `/split-task "<task>"` | Split large task into safer sub-tasks |
| `/mimir-config` | Show active configuration |
| `/mimir-help` | Show this help |
| `/mimir-update` | Update Mimir to latest version |

**Risk levels:** `LOW ✅` `MEDIUM ⚠️` `HIGH 🔴` `CRITICAL 🚨`

**Workflow:**
1. `/mimir` — if LOW or MEDIUM, proceed
2. If HIGH or CRITICAL → `/split-task` to break it down
3. Run sub-tasks one at a time
