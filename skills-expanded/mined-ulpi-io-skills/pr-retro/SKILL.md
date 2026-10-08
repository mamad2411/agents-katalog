---
name: pr-retro
version: 2.0.0
description: |
  Read a feature branch's merge-readiness from its actual git data — measured metrics, not vibes:
  collect raw git output for the branch vs base, compute branch-health metrics (size class, test ratio,
  focus, drift, sessions, hotspots), scan the diff for pre-PR artifacts (secrets, `.only`, conflict
  markers, debug lines, TODOs), then render a GREEN / YELLOW / RED verdict with per-signal
  recommendations — runs as a forked analysis workflow with its own reasoning budget, isolated from the
  main flow. Every metric is derived from concrete git data, never estimated; the verdict follows the
  documented signal thresholds and never reports GREEN while a blocking finding stands; read-only apart
  from the optional JSON snapshot, never touching code or git state. Use when the user asks for branch
  health, pre-PR analysis, or `/pr-retro`.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
context: fork
agent: general-purpose
effort: high
argument-hint: "[--quick] [--base <branch>]"
arguments:
  - request
when_to_use: |
  Use when the user asks for a branch retrospective, pre-PR check, branch health audit, or
  merge-readiness review. Examples: "pr retro", "branch health check", "pre-PR analysis",
  "/pr-retro --quick", or "/pr-retro --base dev". Do NOT use for code fixing (that's bugfix), deep bug
  hunting (that's find-bugs), or for creating the PR itself — pr-retro measures and reports, it changes
  nothing.
---

<EXTREMELY-IMPORTANT>
This skill is a read-heavy analysis workflow with metric integrity requirements.

Non-negotiable rules:
1. Verify the branch is a feature branch and actually has commits relative to base.
2. Compute metrics from git data, never by estimation.
3. Form the verdict only after the full metric and self-review pass is complete.
4. Stay read-only with respect to code and git state; the only allowed write is the JSON snapshot.
5. Keep the heavy metric tables, scan patterns, and JSON schema in references, not inline in every invocation.
</EXTREMELY-IMPORTANT>

# PR Retro

## Inputs

- `$request`: Optional flags or guidance such as `--quick` or `--base <branch>`

## Goal

Produce a credible branch retrospective that:

- measures the actual branch diff
- identifies contributors and hotspots
- scans for common pre-PR artifacts
- evaluates merge readiness with explicit signals
- optionally saves a JSON snapshot under `.history/pr-retros/`

## Step 0: Resolve mode and branch scope

Determine:

- whether the request is standard mode or `--quick`
- whether a custom base branch was specified
- current branch name
- whether the branch is a feature branch
- whether commits exist relative to base

Stop early if:

- on `main`, `master`, or `develop`
- no commits exist relative to base

Use `references/retro-metrics.md` for base-branch resolution rules and mode behavior.

**Success criteria**: The retro mode and review base are explicit, and there is real branch data to analyze.

## Step 1: Gather raw branch data

Collect the raw git data needed for the retro:

- commit list with author and timestamps
- per-commit stats
- machine-readable numstat
- aggregate diff stat
- branch divergence info

Rules:

- prefer raw git output over prose or inference
- if a metric cannot be derived from the collected data, say so explicitly
- do not skip this step and jump directly to a verdict

**Success criteria**: All downstream metrics can be derived from collected branch data.

## Step 2: Compute branch metrics

Compute the core branch metrics from raw data:

- total commits
- contributors
- files changed
- insertions
- deletions
- net LOC
- test LOC ratio
- PR size class
- branch age
- base drift
- focus score
- session count and timeline

If in `--quick` mode, stop after computing the dashboard-grade metrics and verdict inputs.

Load `references/retro-metrics.md` for:

- metric formulas
- PR size buckets
- focus score rules
- session detection rules

**Success criteria**: Every displayed metric is derived from concrete git data.

## Step 3: Analyze contributors, hotspots, and hygiene

Build the branch-health view:

- contributor breakdown
- commit type distribution
- hotspot files
- hygiene signals such as WIP/fixup or weak commit messages

Rules:

- attribute commits per author from commit data, not local git config
- treat conventional-commit compliance as a metric, not a moral judgment
- use hotspot analysis to explain risk concentration, not to imply a bug by itself

**Success criteria**: The retro explains who changed what and where the branch is concentrated.

## Step 4: Run the self-review scan

Use `references/retro-metrics.md` to scan the branch diff for:

- hardcoded secrets
- `.only` test markers
- conflict markers
- debug statements
- TODO or FIXME artifacts
- commented-out code
- large file additions
- binary files
- notable config changes

Rules:

- never include actual secret values in output
- distinguish between `BLOCK`, `WARN`, and `INFO`
- this is not a full security audit; use it as merge-readiness evidence

**Success criteria**: The retro captures branch hygiene issues that affect merge readiness.

## Step 5: Determine merge-readiness verdict

Evaluate the configured signals:

- hygiene
- size
- test ratio
- focus
- self-review findings
- drift

Then produce:

- `GREEN`
- `YELLOW`
- `RED`

Generate recommendations for every non-green signal.

Load `references/retro-metrics.md` for the verdict rules and signal thresholds.

**Success criteria**: The verdict follows the documented signal rules and is explainable from the metrics.

## Step 6: Render output and save snapshot

Always render the dashboard summary.

In standard mode, also render:

- contributors
- commit type breakdown
- hotspots
- self-review findings
- time distribution
- recommendations

In standard mode, save the JSON snapshot to:

- `.history/pr-retros/<branch-slug>.json`

Skip the snapshot in `--quick` mode.

Use `references/retro-metrics.md` for:

- output sections
- JSON schema
- branch slugging rules

**Success criteria**: The retro output is internally consistent, and the snapshot is written only when appropriate.

## Guardrails

- Do not fabricate metrics.
- Do not change code or git state.
- Do not add `disable-model-invocation`; this skill should remain callable when the user asks for branch analysis.
- Do not add `paths:`; this is a generic workflow skill.
- Do not keep the metric tables, signal thresholds, and JSON schema inline in `SKILL.md`.
- Do not report a `GREEN` verdict when blocking findings exist.

## When To Load References

- `references/retro-metrics.md`
  Use for metric formulas, signal thresholds, self-review scan patterns, output layout, and JSON snapshot schema.

## Output Contract

Report:

1. branch and base
2. key dashboard metrics
3. overall verdict and per-signal status
4. notable findings and recommendations
5. snapshot path when written, or explicit quick-mode skip
