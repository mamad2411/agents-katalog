---
name: deployment-frequency-tracker
description: "Deployment frequency tracker: compute DORA metrics from git history, LLM identifies bottlenecks and improvement opportunities. Read-only. Trigger: /deploy-freq"
trigger: /deploy-freq
---
# /deploy-freq

DORA metrics from local git history. No external API needed.

## What this is for

- Deployment frequency, lead time, change failure rate, time to restore
- Bottlenecks: long-running PRs, deployment batches, rollback patterns
- **Read-only skill.** No CI changes, no deployment automation.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/deploy-freq -help` or `/deploy-freq -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/dora-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each metric:

- How does it compare to DORA benchmarks (elite/high/medium/low)?
- What is the #1 bottleneck?
- Are deploys risky (high change failure rate + low freq) or healthy?

### Step 5 - Write report

File `deployment-frequency-report.md` in current working directory:

1. **Summary** - metrics vs DORA benchmarks, trend arrows.
2. **Bottleneck analysis** - blocking patterns with examples.
3. **Recommendations** - smaller batches, feature flags, faster CI, deployment automation.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight the #1 improvement opportunity.

## Usage

```
/deploy-freq               # interactive
/deploy-freq <dir>         # scan project
/deploy-freq -help
```


