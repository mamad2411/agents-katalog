---
name: refresh-catalogs
description: "Manually regenerate catalog indexes with support for --force, --dry-run, and --only flags"
---

# Refresh Catalogs

Manually regenerate catalog indexes for memory, shared memory banks, diary, and skills. This skill invokes the catalog dispatcher (`generate_catalogs` via `"${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py"`) to rebuild catalog files used by the context manager for fast routing.

## Usage

By default (no arguments), all enabled catalogs are regenerated using state-aware skipping — only catalogs whose source content has changed since the last run are rebuilt. Memory and diary catalogs are always processed (mandatory). The skills catalog only runs if enabled in the plugin configuration. There is no resources catalog — a resources corpus is retrieved through qmd at prompt time, never summarised into a catalog.

### Flags

- **`--force`** — Force regeneration of all enabled catalogs, bypassing state-aware skipping. Ignores content hash state and regenerates regardless of whether sources have changed. Pass `--force` flag through to the dispatcher.
- **`--dry-run`** — Preview mode. Reports what catalogs would be regenerated or skipped without writing any files, modifying `.generation-state.json`, or making LLM calls. Dry-run output shows which generators would run and which would be skipped. No side effects.
- **`--only <generators>`** — Selectively regenerate specific catalogs. Provide a comma-separated list of generator names: `memory`, `banks`, `diary`, `skills`. Example: `--only memory,diary` runs only those two generators. **`--only` is an explicit override: a generator named here runs even if its `enable_*` config flag is off** (e.g. `--only skills` rebuilds the skills catalog while `enable_skills` stays `false`, so you can keep a fresh index without turning on injection).

### Combinations

- `--dry-run --force` — Shows all enabled catalogs as pending (since force bypasses skip logic).
- `--only diary --force` — Force-regenerates only the diary catalog.
- `--only skills --dry-run` — Preview what the skills catalog generator would do.

## Steps

1. **Parse flags** from the user's invocation to determine mode (default, force, dry-run) and any generator filter.

2. **Invoke the catalog dispatcher:**
   Run `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py"` with the appropriate flags:
   - Default: `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py"`
   - Force: `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py" --force`
   - Dry-run: `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py" --dry-run`
   - Selective: `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py" --only memory,diary`
   - Combined: `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/generate_catalog.py" --force --dry-run`

3. **Report per-catalog status** as a summary table:
   - Each catalog gets its own status line: **regenerated** (success), **skipped** (unchanged), or **failed** (with error reason).
   - Show counts: sources processed, entries generated, entries skipped, entries pruned.
   - On first run or with a missing/corrupt state file, all catalogs are regenerated since no prior state exists. The dispatcher handles graceful recovery from corrupt or invalid `.generation-state.json`.

## Error Handling

- If a generator fails, other generators still run — failures are isolated per catalog.
- Missing source directories (e.g., diary directory doesn't exist) cause that catalog to be skipped gracefully with a clear message, not a crash.
- Missing or corrupt `.generation-state.json` triggers full regeneration for all catalogs (equivalent to `--force` for the first run).
- All LLM calls go through `model_client` using the configured `catalog_model` (and `catalog_model_diary` for the diary generator). No direct API calls or new external dependencies.

## Configuration

The dispatcher respects these `plugin.json` userConfig settings:
- `catalog_model` — Model for LLM-based catalog generation (default: `claude-sonnet-5`)
- `catalog_model_diary` — Optional model override for the diary generator (default: inherit `catalog_model`)
- `enable_skills` — Whether to include the skills catalog generator (default: false)

## Operational Notes

- **Interpreter:** ALWAYS invoke via `uv run --project` exactly as shown above — `scripts/pyproject.toml` is a member of the repo-root uv workspace and declares the dependencies (`multiplai-core`, `claude-agent-sdk`) for every script in that directory. Bare `python`/`python3` fails with `ModuleNotFoundError: multiplai_core`. Do not switch this back to project-less resolution with an inline PEP 723 header: that re-resolves the dependency on every run, which is what made the prompt hooks time out.
- **Exit code 1 means partial errors, not total failure.** The catalog is still written for every source that succeeded; re-run to fill gaps. A common per-file error is a `429 "usage credits are required for long context requests"` on very large files — trim/split those or re-run when credits allow.
- **Do not background-detach or pattern-kill the run.** It spawns bounded `claude` CLI subprocesses (concurrency = `catalog_concurrency`, default 5), which is fine in-container. `pkill -f generate_catalog` will also match the calling shell and kill the job — kill the specific python PID if you must stop it.
- **Concurrency:** raise/lower with the `catalog_concurrency` userConfig (default 5) if you hit rate limits or want faster throughput.
