---
name: ml-pipeline-determinism-check
description: "Find sources of non-determinism in ML training pipelines. Trigger: /ml-determinism"
trigger: /ml-determinism
---
# /ml-determinism

Non-deterministic pipelines produce unreproducible results. This skill finds missing seeds, GPU non-determinism, and data ordering issues.

## What this is for

- Missing random seeds across frameworks
- GPU non-determinism (CUDA, cuDNN)
- Data loading with shuffle but no seed
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/ml-determinism -help` or `/ml-determinism -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/determinism-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each pipeline:

- **Deterministic**: seeded + configured
- **Mostly-deterministic**: seed set but GPU not configured
- **Non-deterministic**: no seed, random order
- **Chaotic**: multiple uncontrolled randomness sources

### Step 5 - Write report

File `ml-determinism-report.md` in current working directory:

1. **Summary** - pipelines by determinism level.
2. **Issue table** - chaotic first. Per issue: file, line, type, has global seed, has GPU config, severity, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight non-deterministic and chaotic pipelines.

## Usage

```
/ml-determinism               # interactive
/ml-determinism <dir>         # scan project
/ml-determinism -help
```


