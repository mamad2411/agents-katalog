---
name: training-data-leakage-detector
description: "Training data leakage detector: find cross-contamination between train/test splits in ML pipelines. Read-only. Trigger: /train-leak"
trigger: /train-leak
---
# /train-leak

Test data leaking into training is the most common ML failure. This skill finds pipeline order issues that cause leakage.

## What this is for

- Feature engineering before train/test split (leaks test info into training)
- Group leakage (same user in train and test)
- Temporal leakage (future data used for past predictions)
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/train-leak -help` or `/train-leak -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/leak-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each pipeline:

- **Clean**: split before any transformation
- **Leakage-risk**: transformation before split
- **Temporal-leak**: future data used for past predictions
- **Group-leak**: same entity in both splits

### Step 5 - Write report

File `data-leakage-report.md` in current working directory:

1. **Summary** - pipelines by classification.
2. **Pipeline table** - leaks first. Per pipeline: file, line, split type, operations order, risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight pipelines with data leakage.

## Usage

```
/train-leak               # interactive
/train-leak <dir>         # scan project
/train-leak -help
```


