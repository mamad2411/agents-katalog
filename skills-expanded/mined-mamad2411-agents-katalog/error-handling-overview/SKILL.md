---
name: error-handling-overview
description: "Strategic overview of how a project handles errors: catch-type taxonomy (log/rethrow/swallow/recover/fallback), global handlers, error class hierarchy, clustered weaknesses. Read-only. Audience: Both. Trigger: /errors-overview"
trigger: /errors-overview
---

## What this is for

Per-file error analysis misses the gestalt. This skill builds a complete
taxonomy: every try/catch, .catch(), except:, global error middleware,
process.on('uncaughtException'), @ControllerAdvice, and custom error class.
The LLM clusters weaknesses by module and strategy - which errors are
swallowed, which global handlers eat everything, which retry patterns exist.

`error-handling-auditor` (quality/) finds anti-patterns per file.
This skill gives you the strategic map across the entire project.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/errors-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each module cluster:

### Step 5

- **Strategy**: what is the module's error-handling pattern (log-all,

### Step 6

rethrow-wrapped, swallow-trivial, recover-via-retry)?

### Step 7

- **Swallowed errors**: empty catch blocks or catches with only a comment.

### Step 8

Are they intentionally ignored or forgotten?

### Step 9

- **Global handlers**: do they log+rethrow, log+respond, or log+swallow?

### Step 10

A handler that catches everything and returns 200 is eating evidence.

### Step 11

- **Weakness cluster**: 3+ related weaknesses in one module or cross-module

### Step 12

pattern (e.g. "all services swallow DB errors").

### Step 13

5. Write `error-strategy-report.md` to the working directory.

## Usage

```
/errors-overview                          # interactive
/errors-overview <dir>                    # scan project
/errors-overview -help                    # show usage
```

Returns JSON with `handlers[]`, `globalHandlers[]`, `errorHierarchy[]`,
`counts{}` plus per-catch-type breakdown.
