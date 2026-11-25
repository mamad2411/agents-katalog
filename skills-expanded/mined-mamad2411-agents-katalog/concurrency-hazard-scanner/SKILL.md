---
name: concurrency-hazard-scanner
description: "Concurrency hazard scanner: map shared mutable state across async boundaries, LLM judges each pattern as safe/racy/deadlock-prone. Read-only. Trigger: /concurrency"
trigger: /concurrency
---
# /concurrency

Race conditions, deadlocks, data races - found statically before they manifest at runtime.

## What this is for

- Shared state modified from two async handlers without sync
- Nested locks in inconsistent ordering (deadlock-prone)
- TOCTOU patterns (read-check-then-write without atomicity)
- **Read-only skill.** No code modification.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/concurrency -help` or `/concurrency -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/shared-state-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each shared state access:

- **Safe**: properly synchronized or single-threaded context
- **Racy**: unsynchronized write after async boundary
- **Deadlock-prone**: nested locks in inconsistent order
- **TOCTOU**: read-check-then-write without atomicity

### Step 5 - Write report

File `concurrency-report.md` in current working directory:

1. **Summary** - access paths by classification.
2. **Hazard table** - racy/deadlock first. Per path: state variable, access type, sync mechanism, async boundary, recommendation.
3. **Safe patterns** in appendix.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight confirmed hazards.

## Usage

```
/concurrency               # interactive
/concurrency <dir>         # scan project
/concurrency -help
```


