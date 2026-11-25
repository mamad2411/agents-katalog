---
name: fleet-metabolic
description: >-
  Run the fleet nightly metabolism (Norn pass) and optional sibling passes in one command.
  Use for signal promote, intake promote, sleep consolidation, session quality, or gap detection —
  instead of hunting for run_norn.py, sleep_consolidation.py, promote_corrections.py, etc.
---

# Fleet metabolic sweep

**One command. Norn + optional passes. No scavenger hunt.**

Default is **`norn` only** — the full nightly metabolic cycle (`run_norn.py` → `core.metabolic.norn_pass`).

## Run it

```bash
cd ~/github/willow-2.0
WILLOW_AGENT_NAME=willow python3 scripts/fleet_metabolic_sweep.py
```

Via Kart:

```
agent_task_submit(
  app_id="willow",
  task="cd ~/github/willow-2.0 && WILLOW_AGENT_NAME=willow python3 scripts/fleet_metabolic_sweep.py",
)
kart_task_run(app_id="willow")
```

Extended pass (norn + siblings not wired inside norn):

```bash
python3 scripts/fleet_metabolic_sweep.py --only norn,sleep,corrections,quality,gaps
python3 scripts/fleet_metabolic_sweep.py --dry-run --list-phases
```

## Phases

| Phase | Script | Default? |
|-------|--------|----------|
| `norn` | `scripts/run_norn.py` | yes |
| `sleep` | `scripts/sleep_consolidation.py` | optional |
| `corrections` | `scripts/promote_corrections.py` | optional |
| `quality` | `scripts/session_quality_scorer.py` | optional |
| `gaps` | `scripts/cross_session_gap_detector.py` | optional |

**Inside norn already:** signal promote/archive, intake promote, filesystem groom (dry), dream/WCE schedule checks.

Report: `$WILLOW_HOME/reports/fleet_metabolic_sweep_report.json`

Timer: `systemd/willow-metabolic.timer` (daily)

## Agent rules

1. Nightly metabolism → this sweep, not ad-hoc `promote_signals.py`.
2. `--dry-run` on sweep = inventory only; `run_norn.py --dry-run` = norn without writes.
3. Session ingest → `fleet-session-sweep`. Hygiene audits → `fleet-hygiene`. Witness SLIs → `fleet-witness`.
