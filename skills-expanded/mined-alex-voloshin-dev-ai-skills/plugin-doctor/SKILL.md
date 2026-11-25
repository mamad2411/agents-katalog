---
name: plugin-doctor
description: Use this skill when installing the plugin, upgrading to a new version, or troubleshooting unexpected plugin behavior — a self-diagnostic for the ai-skills plugin that validates skill frontmatter, hook executability, run-log parseability, and judge calibration. Default mode is fast and cost-free; `--calibrate-judge` is opt-in.
context: fork
argument-hint: "[--calibrate-judge]"
---

# /plugin-doctor — Plugin Self-Diagnostic

Check that the plugin is installed correctly and operating within healthy bounds. Default mode is fast (linter-only, no LLM cost) and always passes on a clean install.

## Invocation

Shipped commands:

```
/plugin-doctor                          # default smoke test (Tier 1 linters)
/plugin-doctor --calibrate-judge        # opt-in: judge calibration vs samples
/plugin-doctor --show-recent-errors     # top-5 hooks by ERROR/WARN count (audit WP-4.2)
```

Planned (not yet shipped):

```
/plugin-doctor --runs --last N          # summarize last N workflow runs
/plugin-doctor --health-trends          # context-health metrics summary (G8)
```

Both `--runs` and `--health-trends` will land once `.ai-skills-memory/runs.jsonl` accumulates enough entries to make the summary meaningful. Track progress in the plugin issue tracker.

## Two-step boot model

### Default mode (`/plugin-doctor`)

Wraps `plugin/eval/runner.py --tier 1` — runs and reports on:
- **Skill frontmatter** — `name` + `description` present, kebab-case `name` matches parent dir, recognizable `Use when` trigger phrase (H5 regex from `runner.py`).
- **Hook references** — every entry in `plugin/hooks/hooks.json` resolves to an existing script under `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/`. Both bare-path and the v0.3.3 `python3 ${CLAUDE_PLUGIN_ROOT}/...` wrapper form accepted.
- **Hook scripts** — Python syntax valid (`py_compile` in the runner).
- **Run logs** — `.ai-skills-memory/runs.jsonl` parses (JSON-syntax check; richer summaries are planned via `--runs --last N`, see Planned section above).
- **JSON validity** — `plugin/schemas/*.json` + `eval/config.json` + `monitors/monitors.json` + `.claude-plugin/plugin.json` parse cleanly.

Note: schema files are checked for valid JSON syntax, not full JSON Schema draft 2020-12 validation; the `$schema` URI declares draft 2020-12 but the runner does not currently re-validate against it.

Reports calibration as `not yet run; use /plugin-doctor --calibrate-judge to run`.

### `--calibrate-judge` (explicit opt-in)

Delegates to the Tier 2 smoke runner — `plugin/eval/runner.py --tier 2` — which performs a **score-band tolerance check** against `plugin/eval/calibration/<rubric>/` samples. For each sampled rubric, the Haiku judge scores known good + known bad samples and the result must land within ±0.5 of the expected score encoded in the filename (`<scenario>.score-X.X.md`).

Catches three drift classes: rubric edits that break scoring, judge-model version changes, and calibration-sample edits that move them out of band.

Errors clearly when samples are missing or count too low (< 4 per rubric):

```
ERROR: Insufficient calibration samples at plugin/eval/calibration/<rubric>/.
       Expected ≥ 4 (good + bad pairs). Found N.
       See plugin/docs/concepts/eval.md for guidance.
```

Requires `ANTHROPIC_API_KEY` and the `anthropic` Python SDK; without them the run reports `DRY-RUN ONLY` and skips real judge calls. Default sample plan (seed 42): 10 rubrics × 2 samples = 20 judge calls. Override with `--seed`, `--sample-rubrics`, `--samples-per-rubric` on `runner.py`.

### `--show-recent-errors` (recent-errors dashboard)

Surfaces the top hooks ranked by `ERROR + WARNING` count in `.ai-skills-memory/errors.log` over the last 7 days (default window). Ranking is `ERROR * 10 + WARNING` so a hook with a few ERRORs ranks above a hook with many INFO-level WARNINGs. For each hook the dashboard shows the top 3 `issue` strings and counts so the root cause of a noisy hook is one glance away.

Invocation:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/dev/recent-errors.py [--days N] [--top K] [--json]
```

Run from the project root (the script defaults to `<cwd>/.ai-skills-memory/errors.log`). No LLM cost; fail-open on missing log or parse errors. Typical output (real f4ai data, 7-day window):

```
Recent errors — last 7 day(s) (since 2026-05-06T13:40:33Z)
  Total events: 5918
  Distinct hooks: 7

Top 5 hooks by severity (ERROR weighted 10x):
  1. tool-output-normalize             ERR=0    WARN=5356 INFO=0
       └ wrap_marker_missing_before_normalize     x 5356
  2. subagent-stop-learnings           ERR=351  WARN=0    INFO=0
       └ return_contract_validation_failed        x 351
  …
```

Use `--json` for machine-readable output (e.g. CI dashboards). Use `--days 1` for a same-day triage view.

## Other modes (planned, not yet shipped)

`--runs --last N` and `--health-trends` are documented for design continuity. The runner does not currently expose these flags; invoking them will fall through to the default Tier 1 path (or error on the unknown flag depending on shell). Track shipping in the plugin issue tracker.

## Output

- stdout: human-readable report
- `.ai-skills-memory/plugin-doctor.log` — append-only audit log

## Failure modes

- **No `.ai-skills-memory/`:** report as "first run — no history yet"; suggest `/ai-skills-init`
- **Hook script missing executable bit:** **expected** since v0.3.3. Hooks are invoked via the wrapper form `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/<name>.py` (commit `4ea3347`), which does not need the exec bit. Reverting to the bare `${CLAUDE_PLUGIN_ROOT}/...` form would re-introduce the v0.3.2 "Permission denied" install bug. Report this as `INFO` only, not as a warning.
- **`hooks.json` command starts with `python3 ${CLAUDE_PLUGIN_ROOT}/...` rather than `${CLAUDE_PLUGIN_ROOT}/...`:** **expected** since v0.3.3 — same reason as above. The Tier 1 linter (`plugin/eval/runner.py`) accepts both forms by searching for the placeholder substring rather than requiring it at position 0. If a third-party validator still flags the wrapper form, treat it as a linter-bug, not a plugin-bug.
- **`marketplace.json` missing at the cache root (`~/.claude/plugins/cache/<owner>/<plugin>/.claude-plugin/marketplace.json`):** **expected** in `claude --plugin-dir` install mode. The repo-level `/<repo>/.claude-plugin/marketplace.json` is the source-of-truth and is consumed only by `/plugin marketplace add`. `--plugin-dir` is the supported install mode for local development of this repo (per repo `README.md` and `CLAUDE.md`); the cache-root warning can be ignored unless distributing via marketplace.
- **Run log too large to parse fully:** stream-parse last 1000 lines; report partial stats with "(last 1000 events)" note

## Integration

- **Reads**: every file under `plugin/` for lints; `.ai-skills-memory/runs.jsonl`, `plugin-doctor.log` for summaries
- **Calls**: `eval/runner.py --tier 1` (Tier 1 linters); `eval/runner.py --tier 2` if `--calibrate-judge`
- **Memory writes**: `.ai-skills-memory/plugin-doctor.log` (audit trail)
- **Used by**: developers post-install, CI smoke before merge
