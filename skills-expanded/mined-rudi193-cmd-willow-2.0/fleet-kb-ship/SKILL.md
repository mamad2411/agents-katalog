---
name: fleet-kb-ship
description: >-
  Run KB ship-shape gates before merge or release in one command.
  Use for kb_preflight, embedding completeness, bitemporal audit, retrieval gold,
  or dry-run repairs — instead of hunting for kb_preflight.py, pg_completeness_gate.py, kb_repair.py, etc.
---

# Fleet KB ship sweep

**One command. All ship gates. Read-only by default.**

## Run it

```bash
cd ~/github/willow-2.0
WILLOW_AGENT_NAME=willow python3 scripts/fleet_kb_ship_sweep.py
```

Via Kart:

```
agent_task_submit(
  app_id="willow",
  task="cd ~/github/willow-2.0 && WILLOW_AGENT_NAME=willow python3 scripts/fleet_kb_ship_sweep.py",
)
kart_task_run(app_id="willow")
```

Subset / inventory:

```bash
python3 scripts/fleet_kb_ship_sweep.py --only preflight,completeness,retrieval
python3 scripts/fleet_kb_ship_sweep.py --dry-run --list-phases
```

Writes (operator consent required):

```bash
python3 scripts/fleet_kb_ship_sweep.py --apply-embed --embed-limit 500
python3 scripts/fleet_kb_ship_sweep.py --apply-repair --consent
python3 scripts/fleet_kb_ship_sweep.py --only bitemporal_repair --apply-bitemporal
python3 scripts/fleet_kb_ship_sweep.py --only binder_edges --apply-binder
```

## Default phases (6)

| Phase | Script | Notes |
|-------|--------|-------|
| `preflight` | `kb_preflight.py` | PASS/WARN/FAIL rollup (embed health) |
| `completeness` | `pg_completeness_gate.py` | embedding % gate |
| `bitemporal` | `audit_bitemporal.py` | supersede invariant |
| `retrieval` | `retrieval_gold_check.py` | regression gate |
| `repair_dangling` | `kb_repair.py delete-dangling` | dry-run |
| `repair_dedup_title` | `kb_repair.py dedup-title` | dry-run |

Opt-in: `embed` (`--only embed` or `--apply-embed --embed-limit N`)

Optional: `binder_edges`, `bitemporal_repair` (see `--list-phases`)

Report: `$WILLOW_HOME/reports/fleet_kb_ship_sweep_report.json`

## Agent rules

1. Pre-merge KB check → this sweep, not scattered scripts.
2. Repairs and embed backfill need explicit `--apply-*` flags.
3. Edge writes need `--consent` or `WILLOW_HUMAN_CONSENT=1`.
4. Exit `1` on any failed phase — treat as ship blocker.
