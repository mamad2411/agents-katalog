---
name: vibetime
description: Work with local VibeTime agent-coding activity data. Use when Codex needs to inspect VibeTime time tracking, agent activity, project/session/turn history, token usage, cost attribution, hook health, local SQLite data, data quality, dirty data, or safe database cleanup. Default to VibeTime CLI summaries for ordinary questions; use the bundled SQLite inspector for deep analysis, raw event access, audits, and repair plans.
---

# VibeTime

Use this skill to query, explain, audit, and carefully clean local VibeTime data.

VibeTime is local-first. The default database is `~/.vibetime/data.db`; the CLI binary is usually `~/.vibetime/bin/vibetime` or available as `vibetime` on `PATH`.

## Agent Scope

Activity hooks are supported for `claude-code`, `codex`, `cursor`, `gemini-cli`, and `opencode`.

Usage and cost analysis is currently supported for `claude-code`, `codex`, and `opencode` only. Usage facts are scanned from local transcripts/databases and stored as sanitized token/model rows; hook payloads are not treated as a usage source.

Cursor and Gemini CLI usage scanning is not enabled in the current product.

## Requirements

- Use the VibeTime CLI when it is available: `vibetime` or `~/.vibetime/bin/vibetime`.
- Use Python 3.10+ for `scripts/vibetime_data.py`.
- Do not install Python packages for the bundled script. It uses only the Python standard library, including `sqlite3`.

## Decision Path

1. For ordinary summaries, call the CLI first. It is the stable user-facing contract.
2. For raw facts, correlations, suspicious data, or questions the CLI cannot answer, use `scripts/vibetime_data.py` against SQLite in read-only mode.
3. For cleanup, run `audit` and `repair` as dry runs first. Never write unless the user explicitly asks to apply a safe repair.

## CLI First

Prefer CLI commands for quick answers:

```bash
vibetime status --json
vibetime today --json
vibetime history --days=30 --json
vibetime usage --days=30 --json
vibetime project <project-name> --json
vibetime export --format=json --from=2026-05-01 --to=2026-05-20
vibetime doctor --json
vibetime health --json
```

If `vibetime` is not on `PATH`, try `~/.vibetime/bin/vibetime`.

Read `references/cli.md` when choosing CLI commands or interpreting their JSON.

## Deep SQLite Access

Use the bundled script for agent-grade analysis:

```bash
python3 <skill-dir>/scripts/vibetime_data.py info
python3 <skill-dir>/scripts/vibetime_data.py app-info
python3 <skill-dir>/scripts/vibetime_data.py config
python3 <skill-dir>/scripts/vibetime_data.py health
python3 <skill-dir>/scripts/vibetime_data.py cli-status
python3 <skill-dir>/scripts/vibetime_data.py agents
python3 <skill-dir>/scripts/vibetime_data.py activity-live
python3 <skill-dir>/scripts/vibetime_data.py activity-summary --days 30
python3 <skill-dir>/scripts/vibetime_data.py events --days 7 --project <name>
python3 <skill-dir>/scripts/vibetime_data.py turns --days 30 --agent codex
python3 <skill-dir>/scripts/vibetime_data.py usage --days 30 --group-by project,model
python3 <skill-dir>/scripts/vibetime_data.py usage-summary --days 30 --agent codex
python3 <skill-dir>/scripts/vibetime_data.py usage-refresh-state
python3 <skill-dir>/scripts/vibetime_data.py audit
python3 <skill-dir>/scripts/vibetime_data.py repair
```

The functional read commands are:

- `activity-live`: current local-day completed activity and active turns.
- `activity-summary`: local-day calendar, trends, top projects, hourly matrix, turn durations, and period comparison.
- `usage-summary`: totals, daily trend, agent/model/project rankings, project-model matrix, efficiency, period comparison, data quality, audit rows, available filters, and matched pricing metadata.
- `agents`, `config`, `health`, `cli-status`, `app-info`: local status/config surfaces.
- `usage-refresh-state`: persisted scan-state approximation; in-flight refresh state lives in the running desktop process and is not fully reconstructable from SQLite.

The `usage` command is a flexible grouped query for ad hoc analysis.

Agent-only analysis is expected. When the user asks for deeper insight, do more than replay summaries:

- Cross-check CLI output, SQLite facts, and script summaries for disagreement.
- Explain whether a difference is caused by rolling-window vs local-calendar-day semantics.
- Find dirty data: stale `open_turns`, duplicate turn rows, missing starts, malformed JSON, token mismatches, unmatched usage, and missing project attribution.
- Diagnose usage/cost attribution: unknown pricing, provider/model ambiguity, Codex priority tier, cache hit rate anomalies, and project/model spend concentration.
- Detect outliers: unusually long turns, high cost per turn/hour, token spikes, idle-looking sessions, and low-confidence attribution.
- Produce safe cleanup plans with evidence and backups; never rewrite fact tables automatically.

The script emits JSON. All commands are read-only except:

```bash
python3 <skill-dir>/scripts/vibetime_data.py repair --apply --yes
```

That write path only deletes safe stale `open_turns` rows and creates a timestamped backup first.

Read `references/coverage.md` when checking whether a VibeTime module is covered. Read `references/schema.md` before writing custom SQL. Read `references/data-quality.md` before diagnosing dirty data or proposing cleanup.

## Safety Rules

- Do not write directly to `events`, `usage_records`, `usage_pricing_cache`, or `usage_scan_state`.
- Do not fabricate `turn_end` events, rewrite durations, rewrite project attribution, or change token counts.
- Do not run `repair --apply --yes` unless the user has explicitly requested applying safe cleanup.
- Prefer dry-run repair plans and evidence. Explain impact before changing local data.
- If the database is missing, report that VibeTime has not created local data yet; do not create it from the skill.

## Useful Patterns

- “What happened today?” → CLI `today --json`.
- “Why does this project look wrong?” → CLI `project`, then SQLite `events` and `turns`.
- “Summarize recent activity” → SQLite `activity-summary --days 30`.
- “Show raw Codex turns last week” → SQLite `turns --days 7 --agent codex`.
- “How much did Codex cost recently?” → SQLite `usage-summary --days 5 --agent codex`.
- “Rank spend by project/model” → SQLite `usage-summary --days 30`, then inspect `by_project`, `by_model`, and `project_model_matrix`.
- “Check agent hook install status” → CLI `agents --json`, then SQLite inspector `agents` if CLI is unavailable.
- “Check config/preferences” → SQLite inspector `config`.
- “Find dirty data” → SQLite `audit`, then inspect evidence.
- “Clean stale active turns” → SQLite `repair` dry run, then ask before apply.
