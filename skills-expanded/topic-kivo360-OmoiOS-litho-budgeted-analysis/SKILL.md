---
name: litho-budgeted-analysis
description: Profile a repository, inspect existing Litho/deepwiki-rs cache state, generate a repo-local Litho config that preserves the user's current global model/provider, and run deepwiki-rs within a target time budget. Use when Claude needs to analyze a repo quickly with Litho, auto-tune exclusions and boundary settings by repo size, reuse cache intelligently, or create a filtered local copy for very large repos.
---

# Litho Budgeted Analysis

Create a fast, repo-local Litho run plan without changing the user's global model choice.

## Workflow

1. Profile the repo.
2. Detect the effective global Litho config path if possible.
3. Inspect `.litho/cache` freshness.
4. Generate `litho.local.toml` in the target repo.
5. Prefer a direct run.
6. Use filtered-copy mode only when the repo is too large for the time budget.

## Scripts

### 0. Use the one-file local launcher

If you want the simplest possible local test, run exactly one file:

```bash
bash scripts/run_local_litho.sh /path/to/repo 15
```

That script:
- runs the full budgeted Litho workflow for the target repo
- streams progress in the current terminal
- writes `.litho/run.log`
- writes `.litho/run-status.json`

If you want a detached background run instead:

```bash
bash scripts/run_local_litho.sh /path/to/repo 15 --detach
```

Then watch progress with:

```bash
bash scripts/watch_litho_progress.sh /path/to/repo
```

### 1. Profile the repo

Run:

```bash
bash scripts/uv_run.sh scripts/profile_repo.py --repo-path /path/to/repo
```

This returns JSON including:
- tracked file count
- source-like file count
- total/source-like bytes
- largest directories
- cache presence/freshness
- detected global Litho config path
- repo class (`small`, `medium`, `large`, `very-large`)

### 2. Generate the local config

Run:

```bash
bash scripts/uv_run.sh scripts/generate_litho_config.py --repo-path /path/to/repo
```

Behavior:
- writes `/path/to/repo/litho.local.toml`
- preserves the user's existing provider/model settings
- only tunes safe runtime knobs like exclusions, boundary settings, chunking, and concurrency
- does not overwrite the global config

If automatic global-config detection is wrong or unavailable, pass it explicitly:

```bash
bash scripts/uv_run.sh scripts/generate_litho_config.py --repo-path /path/to/repo --global-config /path/to/global/litho.toml
```

### 3. Run Litho with a time budget

Run:

```bash
bash scripts/uv_run.sh scripts/run_litho_analysis.py --repo-path /path/to/repo --time-budget-minutes 15
```

Behavior:
- profiles first
- generates/refreshes `litho.local.toml`
- chooses direct vs filtered-copy mode
- chooses cache-aware flags (`--skip-preprocessing` when safe)
- executes through `zsh -ic` with alias-safe handling
- writes `.litho/run.log` and `.litho/run-status.json` in the target repo
- updates status with phase, command, PID, timestamps, and exit code

Use `--dry-run` first when you want to inspect the generated plan:

```bash
bash scripts/uv_run.sh scripts/run_litho_analysis.py --repo-path /path/to/repo --time-budget-minutes 15 --dry-run
```

Use `--detach` when you want the command to return immediately and monitor progress separately:

```bash
bash scripts/uv_run.sh scripts/run_litho_analysis.py --repo-path /path/to/repo --time-budget-minutes 15 --detach
tail -f /path/to/repo/.litho/run.log
cat /path/to/repo/.litho/run-status.json
```

### 4. Run through the uv fallback wrapper

Always prefer the wrapper in this skill:

```bash
bash scripts/uv_run.sh scripts/profile_repo.py --repo-path /path/to/repo
```

Behavior:
- uses `uv run` with the PEP 723 script metadata
- if the current repo's `.venv` is broken, falls back automatically to `uv run --python "$(which python3)" ...`
- keeps the logic self-contained inside this skill directory

### 5. Watch progress explicitly

Run:

```bash
bash scripts/watch_litho_progress.sh /path/to/repo
```

It prints:
- current phase
- PID
- start / last output / finish timestamps
- current exit code if finished
- tail of `.litho/run.log`

## Rules

- Never change `provider`, `model_efficient`, or `model_powerful` away from the user's current settings.
- Prefer direct runs with pruning before filtered-copy mode.
- Treat filtered-copy mode as a last resort for `very-large` repos or when the estimated runtime exceeds the budget.
- Do not auto-delete cache. Reuse it when fresh; ignore it when stale.
- Keep root configs, source files, migrations, schemas, and key architecture docs in filtered-copy mode.

## Heuristic Reference

Read `references/heuristics.md` when you need the exact repo-class thresholds, cache freshness logic, or filtered-copy inclusion rules.
