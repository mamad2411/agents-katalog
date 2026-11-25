---
name: auto-research-codex
description: Run an autonomous experimentation loop for Codex based on github/awesome-copilot autoresearch, adapted to native hooks for persistence. Use when a repo needs repeated measurable experiments with baseline capture, one commit per experiment, automatic discard of regressions, strict scope control, and uninterrupted iteration until stopped.
---

# Auto Research Codex

Use `$auto-research-codex` for metric-driven autonomous experimentation, not for open-ended coding.

This skill is based on the public `awesome-copilot/autoresearch` workflow, but uses Codex native hooks to keep the loop alive between turns.

Default mode is one repo. Multi-repo tracking is optional and only turns on when you explicitly pass extra `--repo` flags.

Prefer absolute paths for `--in-scope` and `--out-of-scope`. The script will map each absolute path to the correct tracked repo automatically.

## Phase 1: Setup

Before the loop starts, collect and confirm every item below. Do not skip any.

1. Goal
   - Ask what the user wants to improve or optimize.
2. Metric
   - Ask for the exact command to run.
   - Ask how to extract one numeric value from the output.
   - Ask whether lower is better or higher is better.
3. Scope
   - Ask which files or directories are in scope.
   - Ask which files or directories are off limits.
4. Constraints
   - Ask for constraints such as test requirements, API stability, no new dependencies, time budget, or memory limits.
5. Experiment budget
   - Ask for a number of experiments or `unlimited`.
6. Simplicity policy
   - Default policy: all else equal, simpler is better.

Summarize the full setup back to the user and wait for confirmation before starting.

## Phase 2: Start the loop

From the skill directory, run:

```bash
bash scripts/autoresearch_loop.sh setup \
  --goal "<goal>" \
  --metric-command "<command>" \
  --metric-regex "<regex>" \
  --direction higher|lower \
  --in-scope /absolute/path/in/this/repo \
  --out-of-scope /absolute/path/to/avoid \
  --constraint "<constraint>" \
  --max-experiments <number|unlimited> \
  --simplicity-policy "<policy>"
```

What setup does:

- re-installs this skill's native hook entries automatically
- creates or switches to `autoresearch/YYYYMMDD`
- initializes root-level `results.tsv` and `run.log`
- adds `results.tsv`, `run.log`, and `.codex-autoresearch/` to `.git/info/exclude`
- runs the baseline measurement and records experiment `0`

Optional multi-repo extension:

```bash
bash scripts/autoresearch_loop.sh setup \
  --repo /path/to/primary-repo \
  --repo /path/to/second-repo \
  --metric-repo /path/to/primary-repo \
  --goal "<goal>" \
  --metric-command "<command>" \
  --metric-regex "<regex>" \
  --direction higher|lower \
  --in-scope /path/to/primary-repo/src \
  --in-scope /path/to/second-repo/Sources \
  --out-of-scope /path/to/second-repo/Examples
```

Rules for multi-repo mode:

- If you omit `--repo`, it stays single-repo.
- Absolute scope paths are preferred and are mapped to the matching tracked repo automatically.
- Unqualified relative scope paths still apply to the primary repo.
- The Stop hook evaluates one experiment across all tracked repos atomically.

## Phase 3: Experiment loop

Once active, keep iterating without asking whether to continue.

For each experiment:

1. Think
   - Analyze the current best result and propose one focused hypothesis.
2. Edit
   - Modify only in-scope files.
3. Commit
   - Commit every experiment before the turn ends.
   - Use `experiment: <short description>`.
4. Stop
   - Let the native `Stop` hook measure the result.

The hook enforces the autoresearch protocol:

- baseline is preserved
- every touched tracked repo must be committed before evaluation
- out-of-scope changes are rejected
- crashes and parse failures are logged and reverted
- same-or-worse results are discarded by resetting every changed tracked repo to the previous kept commit
- improvements are kept and become the new best result
- every evaluated experiment is appended to `results.tsv`
- if the work expands beyond what one repo-local native loop can safely track, switch to manual fallback instead of letting the loop mis-track state

## Phase 4: End the loop

End cleanly by either:

- running `bash scripts/autoresearch_loop.sh stop`
- or emitting a line that is exactly `AUTORESEARCH_DONE` only after the result is actually verified

Both paths remove this skill's hook entries automatically.

## Manual fallback

If the work expands beyond one repo-local native loop, do not keep pretending the native keep/discard logic is still authoritative.

If even tracked multi-repo mode is not enough, switch to manual fallback:

```bash
bash scripts/autoresearch_loop.sh manual-fallback --reason "<why native tracking is no longer safe>"
```

What manual fallback does:

- keeps the hook and state alive
- stops native keep/discard automation
- continues injecting the autoresearch protocol on every turn
- prevents the loop from silently collapsing just because the topology changed

Return to native mode only when the work is back inside one safely tracked repo:

```bash
bash scripts/autoresearch_loop.sh resume-native
```

## Outputs

Repo root:

- `results.tsv`
- `run.log`

Repo-local state:

- `.codex-autoresearch/state.json`

## Key rules

- No experiment without a measurement.
- Commit every experiment before it is evaluated.
- Regressions are not kept unless the user explicitly changes the policy.
- Do not modify off-limits files.
- Do not install new dependencies unless the user approved it.
- Stay autonomous once the loop starts.
