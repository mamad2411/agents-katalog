---
name: fleet-session-sweep
description: >-
  Run the complete fleet session memory + benchmark pipeline in one command.
  Use when backfilling sessions, filling the memory tracker, running Nest benchmarks,
  Sonnet 5 cohort comparison, token efficiency, or Willow SLI retrieval gold —
  instead of hunting for session_indexer, parse_benchmark_sessions, fold_pr_outcomes, etc.
---

# Fleet session sweep

**One command. All layers. No scavenger hunt.**

## Run it

```bash
cd ~/github/willow-2.0
WILLOW_AGENT_NAME=willow python3 scripts/fleet_session_sweep.py --since 2026-07-03
```

Via Kart (preferred in agent sessions):

```
agent_task_submit(
  app_id="willow",
  task="cd ~/github/willow-2.0 && WILLOW_AGENT_NAME=willow python3 scripts/fleet_session_sweep.py --since 2026-07-03",
)
kart_task_run(app_id="willow")
```

Dry-run / inventory:

```bash
python3 scripts/fleet_session_sweep.py --list-phases
python3 scripts/fleet_session_sweep.py --since 2026-07-03 --dry-run
```

Subset:

```bash
python3 scripts/fleet_session_sweep.py --only index,benchmark,sonnet5,fold,analyze,sli
python3 scripts/fleet_session_sweep.py --skip atoms,promote,intake,edges
```

## What it runs (13 phases)

| Phase | Script | Output |
|-------|--------|--------|
| `index` | `scripts/session_indexer.py --fleet` | Postgres `session_index` / `session_messages` → `session_query` |
| `jeles` | `scripts/register_jeles_sessions.py` | Postgres `jeles_sessions` |
| `bridge` | `scripts/bridge_cross_runtime.py` | `$WILLOW_HOME/handoffs/cross-runtime.json` |
| `atoms` | `scripts/extract_atoms_from_sessions.py --fleet` | `~/.willow/willow-2.0.db` atom staging |
| `promote` | `scripts/promote_candidates.py` | KB `session_promote` atoms |
| `intake` | `scripts/promote_intake.py --fleet --no-llm` | intake JSONL → KB |
| `edges` | `scripts/propose_edges.py propose` | proposed edges (not auto-applied) |
| `handoff` | `sap/tools/build_handoff_db.py` | handoffs.db index |
| `benchmark` | `$NEST/parse_benchmark_sessions.py` | `claude_benchmarks.db` token/tool metrics |
| `sonnet5` | `$NEST/normalize_sonnet5_sessions.py` | Sonnet 5 + Cursor cohort report |
| `fold` | `$NEST/fold_pr_outcomes.py` | `benchmark_sessions_full.md` comparison chart |
| `analyze` | `$NEST/benchmark_analyze.py` | efficiency / model pattern findings |
| `sli` | `scripts/retrieval_gold_check.py` | Willow improvement gate (retrieval gold) |

Report: `$NEST/fleet_session_sweep_report.json`

## Fleet repos (shared config)

`scripts/fleet_repos.py` — four repos, Claude + Cursor roots:

- `willow`, `willow-2.0`, `safe-app-store-public`, `DispatchesFromReality`

Do not duplicate these paths in one-off Kart scripts.

## Environment

| Var | Default |
|-----|---------|
| `NEST` | `~/Desktop/Nest` |
| `WILLOW_20_DB` | `~/.willow/willow-2.0.db` |
| `WILLOW_AGENT_NAME` | required for jeles + bridge |

## Read results

| Artifact | Path |
|----------|------|
| Session query | MCP `session_query` |
| Benchmark chart | `$NEST/benchmark_sessions_full.md` |
| Sonnet 5 cohort | `$NEST/sonnet5_selected_sessions.json` |
| Analysis | `$NEST/benchmark_analysis_report.json` |
| SLI scorecard | `willow/bench/scorecard.json` |

## Not in default sweep (weekly / sidecar)

Run separately when needed — listed in `--list-phases` under `optional_related`:

- `normalize_fable_sessions.py`, `normalize_sonnet46_sessions.py` — model cohort sidecars
- `willow/bench/locomo/path_a_locomo_pilot.py` — weekly external memory SLI
- `willow/bench/continuity/run_wce.py` — weekly handoff continuity SLI
- `scripts/smoke_scorecard.sh` — full pytest + retrieval (CI smoke)
- `benchmarks/sidecars/cartographer_code_memory/` — controlled CBM prompt bench

## Agent rules

1. **Never** ad-hoc scrape `~/.claude/projects/*.jsonl` into scratch markdown for fleet memory — use this sweep.
2. **Never** run `parse_benchmark_sessions` without going through sweep or documenting why a subset is enough.
3. Atom extraction (`atoms` phase) is optional for benchmark-only refreshes (`--only benchmark,sonnet5,fold,analyze`).
4. `edges` proposes only — does not apply without human consent.
5. After sweep, skim `benchmark_sessions_full.md` and `fleet_session_sweep_report.json` for failures.
