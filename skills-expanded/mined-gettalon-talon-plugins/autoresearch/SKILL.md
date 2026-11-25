---
description: "Autonomous research loop — iteratively edit, test, measure, keep/discard. Usage: /autoresearch <file> <metric> [--budget 5m] [--provider ark]"
---

# Autoresearch — Autonomous Experiment Loop

Inspired by Karpathy's autoresearch. Iteratively modify a target file, run an experiment, measure a metric, and keep improvements or discard failures. Runs forever until stopped.

## Arguments

Parse `$ARGUMENTS` for:
- `<file>` — The file to modify (e.g., `train.py`, `src/lib.rs`, `index.tsx`)
- `<metric>` — What to optimize (e.g., "minimize val_bpb", "minimize bundle size", "maximize test coverage", "minimize compile time", "minimize response time")
- `--budget <duration>` — Time budget per experiment (default: 5m)
- `--provider <name>` — AI provider for iterations (default: current session)
- `--max-runs <n>` — Max experiments before stopping (default: unlimited)
- `--branch <name>` — Git branch name (default: autoresearch/<timestamp>)

If arguments are missing or unclear, ask the user.

## Setup Phase

1. Verify the target file exists
2. Create a git branch: `autoresearch/<file>-<YYYYMMDD-HHMM>`
3. Read the target file completely to understand the codebase
4. Determine the run command and metric extraction:
   - Ask the user: "How do I run the experiment and measure the result?"
   - Or infer from context (e.g., `cargo test`, `npm test`, `python train.py`)
5. Run baseline experiment, record initial metric value
6. Create `autoresearch-results.tsv` with columns: `commit | metric | memory | status | description`
7. Log baseline as first row

## Experiment Loop

Run this loop **forever** (or until `--max-runs` reached):

```
Step 1: THINK
- Review the current state of <file>
- Review past experiment results in autoresearch-results.tsv
- Think of ONE specific improvement to try
- Prefer: small, focused, reversible changes
- All else equal, simpler is better

Step 2: EDIT
- Modify <file> with the improvement
- git add <file> && git commit -m "autoresearch: <brief description>"
- Record the commit hash

Step 3: RUN
- Execute the run command with a timeout of <budget>
- Capture stdout+stderr to run.log
- If it crashes: read the error, attempt ONE fix, re-run. If still crashes, mark as "crash" and skip.

Step 4: MEASURE
- Extract the metric from run.log (grep, parse, etc.)
- Compare to the best known value

Step 5: DECIDE
- BETTER (metric improved): Keep the commit. Update best known value. Log "keep".
- SAME or WORSE: git reset --hard HEAD~1. Log "discard".
- CRASH: git reset --hard HEAD~1. Log "crash".

Step 6: LOG
- Append to autoresearch-results.tsv
- Print a one-line summary: [run #N] <metric_value> (<delta>) — <keep/discard/crash> — <description>

Step 7: REPEAT
- Go to Step 1. Do NOT stop. Do NOT ask the user. The human might be asleep.
```

## Simplicity Rules

- A tiny improvement from deleting code? Definitely keep.
- A tiny improvement from adding 20 lines of hack? Probably discard.
- If unsure, bias toward keeping the codebase simple.
- Never add external dependencies without explicit user approval.

## Output Format

After each experiment, print exactly one line:
```
[#001] metric=3.142 (delta=-0.015) KEEP — replaced relu with gelu in attention
[#002] metric=3.148 (delta=+0.006) DISCARD — tried larger batch size
[#003] metric=ERROR CRASH — OOM with 4x model width
```

## Stopping

The loop stops when:
- `--max-runs` is reached
- The user interrupts (Ctrl+C)
- No improvement in 20 consecutive runs (suggest stopping, but continue if user doesn't respond)

## Provider Delegation

If `--provider` is specified, each experiment's THINK+EDIT phase is delegated to that provider via:
```bash
env $(~/.claude/scripts/switch-provider.sh <provider> --export) \
  claude -p "<think and edit prompt>" --max-turns 3
```

The RUN+MEASURE+DECIDE phases always run locally (no provider needed).
