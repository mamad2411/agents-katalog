---
name: performance-anti-pattern-detector
description: "Performance anti-pattern detector: statically finds 8 families of structural performance problems (N+1 queries, sync-over-async, hot-loop allocation, listener leaks, unnecessary serialization, large closure captures, string concat in loop, redundant computation). Evidence-based report with severity and LLM impact assessment. Read-only. Audience: Senior. Trigger: /perf"
trigger: /perf
---
## What this is for

Performance problems rarely come from one slow function - they come from
recurring structural patterns: database queries inside loops, blocking calls
in async contexts, object allocation in hot paths, listeners that are never
cleaned up, and string concatenation in loops.

This skill finds those patterns statically. It combines a deterministic
collector (regex-based heuristics for 8 pattern families) with LLM context
analysis that validates reachability, assesses impact, and filters false
positives.

**Audience:** Senior - the findings require understanding of async/await,
event loops, and database access patterns.

### Trigger: `/perf`

Read-only static analysis. Never executes the target code.

## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

### Step 1 - `-help`/`-h` check
If invoked with `-help` or `-h`, print the usage block below and stop.

### Step 2 - Confirm `-ProjectDir`
If not provided, prompt user. Confirm path exists.
Print: `Performance anti-pattern scan on <path> ...`

### Step 3 - Run Collector
```powershell
& .\scripts\perf-scan.ps1 -ProjectDir "<path>"
```

Parse JSON output. If exit code ? 0, report error and stop.

### Step 4 - LLM Context Analysis
For each finding:
1. Read `context` snippet.
2. Determine **reachability**: is this code path called from a request handler, event consumer, cron job, or hot loop?
3. Validate pattern: e.g., is the N+1 actually a DataLoader-batched query? Is sync-over-async in a known sync-only context?
4. Assign confidence: `proven`, `likely`, `suspected`.
5. Impact estimate: low/medium/high based on call frequency and data volume.

### Step 5 - Produce Report
Write `perf-report.md` to the working directory:

```
# Performance Anti-Pattern Report - <project>

## Executive Summary
<n> findings: <h> high, <m> medium, <l> low. Estimated impact: <level>.

## Hot Path Findings (high severity, confirmed reachable)
| # | File | Line | Pattern | Impact | Fix |
|--|---|---|-----|----|---|
...

## Medium Findings (grouped by pattern)
...

## Low / Informational
...

## False Positives (dismissed by context)
...

## Open Questions
...
```

### Step 6 - Console Summary
```
=== Performance Anti-Pattern Scan Complete ===
  Findings: <n> (high: <x>, medium: <y>, low: <z>)
  Report: perf-report.md
```

## Usage

```
/perf                   # interactive
/perf /path/to/project  # scan directory
/perf -help
```
