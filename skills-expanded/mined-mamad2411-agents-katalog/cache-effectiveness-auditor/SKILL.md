---
name: cache-effectiveness-auditor
description: "Cache effectiveness auditor: inventory every caching pattern, extract strategy (TTL/invalidation/key design), LLM judges if each cache is effective or harmful. Read-only. Trigger: /cache-audit"
trigger: /cache-audit
---
# /cache-audit

Caches are supposed to make things faster. This skill finds caches that don't.

## What this is for

- TTL too short (miss every time) or too long (serve stale data)
- Missing invalidation (stale data forever)
- Cache cost exceeds recompute cost
- **Read-only skill.** No configuration changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/cache-audit -help` or `/cache-audit -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/cache-harvest.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each cache:

- **Effective**: appropriate TTL, has invalidation, benefits outweigh cost
- **Too-short TTL**: expires before meaningful reuse
- **Too-long TTL**: stale data risk
- **Missing invalidation**: data changes but cache never cleared
- **Cost exceeds benefit**: checking cache is more expensive than recomputing
- **Scope mismatch**: in-memory cache in multi-instance deployment

### Step 5 - Write report

File `cache-effectiveness-report.md` in current working directory:

1. **Summary** - caches by classification.
2. **Cache table** - problematic first. Per cache: mechanism, key pattern, TTL, invalidation, assessment, recommendation.
3. **Missed opportunities** (frequently accessed data without caching).
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight caches doing more harm than good.

## Usage

```
/cache-audit               # interactive
/cache-audit <dir>         # scan project
/cache-audit -help
```


