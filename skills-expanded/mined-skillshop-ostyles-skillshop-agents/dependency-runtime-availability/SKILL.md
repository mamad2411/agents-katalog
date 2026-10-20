---
name: dependency-runtime-availability
description: "Dependency runtime availability checker: find dynamic imports and runtime resource references that fail in production. Read-only. Trigger: /runtime-deps"
trigger: /runtime-deps
---
# /runtime-deps

The build passed. npm install succeeded. But will your app actually load at runtime? This skill finds dynamic loading patterns that fail in production.

## What this is for

- Dynamic require/import with computed paths (wrong path = crash)
- Native modules missing on target platform
- Files referenced that aren't bundled
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/runtime-deps -help` or `/runtime-deps -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/runtime-load-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each reference:

- **Will-fail**: file doesn't exist in project, missing native module, devDependency at runtime
- **Might-fail**: platform-specific, path computed from runtime value
- **Safe**: deterministic path, bundled, cross-platform

### Step 5 - Write report

File `runtime-dependency-report.md` in current working directory:

1. **Summary** - references by risk level.
2. **Reference table** - will-fail first. Per reference: file, line, type, target, risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight references that will crash at startup.

## Usage

```
/runtime-deps               # interactive
/runtime-deps <dir>         # scan project
/runtime-deps -help
```


