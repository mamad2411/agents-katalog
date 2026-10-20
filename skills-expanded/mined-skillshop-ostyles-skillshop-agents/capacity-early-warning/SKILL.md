---
name: capacity-early-warning
description: "Capacity early warning: find hardcoded limits, pool sizes, timeouts, quotas, then LLM judges each as adequate/approaching/critical. Read-only. Trigger: /capacity"
trigger: /capacity
---
# /capacity

Production outages from exceeded capacity always seem sudden. This skill finds limits before they break.

## What this is for

- Connection pool of 10 for a service that grew 3x
- 30-second timeout that fires daily
- Hardcoded limits with no monitoring
- **Read-only skill.** No config changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/capacity -help` or `/capacity -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/limit-harvest.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each limit:

- Given the service domain and typical workload, is the limit adequate?
- What happens if traffic grows 2x/5x/10x?
- Is there monitoring before the limit is hit?

### Step 5 - Write report

File `capacity-report.md` in current working directory:

1. **Summary** - total limits, adequate, approaching, critical.
2. **Limit table** - critical first. Per limit: value, unit, config mechanism, growth risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight critical limits.

## Usage

```
/capacity               # interactive
/capacity <dir>         # scan project
/capacity -help
```


