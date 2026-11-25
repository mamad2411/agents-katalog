---
name: fleet-witness
description: >-
  Run weekly SLI and trust witnesses in one command.
  Use for WCE continuity eval, W8 census, retrieval gold, LoCoMo pilot, or CI smoke —
  instead of hunting for wce_witness.py, w8_census_witness.py, retrieval_gold_check.py, etc.
---

# Fleet witness sweep

**One command. All SLI witnesses. Separate from session ingest.**

Default: `retrieval`, `wce` (check-first), `w8`. Heavy phases (`locomo`, `smoke`) are opt-in.

## Run it

```bash
cd ~/github/willow-2.0
WILLOW_AGENT_NAME=willow python3 scripts/fleet_witness_sweep.py
```

Force WCE when interval not elapsed:

```bash
python3 scripts/fleet_witness_sweep.py --force
python3 scripts/fleet_witness_sweep.py --only retrieval
python3 scripts/fleet_witness_sweep.py --only locomo --locomo-conv 0
python3 scripts/fleet_witness_sweep.py --only smoke
python3 scripts/fleet_witness_sweep.py --list-phases
```

## Phases

| Phase | Script | Schedule |
|-------|--------|----------|
| `retrieval` | `scripts/retrieval_gold_check.py` | PR / smoke |
| `wce` | `scripts/wce_witness.py` | weekly (`willow-wce.timer`) |
| `w8` | `scripts/w8_census_witness.py` | weekly (`willow-w8-census.timer`) |
| `locomo` | `willow/bench/locomo/path_a_locomo_pilot.py` | manual / weekly pilot |
| `smoke` | `scripts/smoke_scorecard.sh` | CI (pytest + retrieval) |

Report: `$WILLOW_HOME/reports/fleet_witness_sweep_report.json`

## Read results

| Artifact | Path |
|----------|------|
| WCE runs | `willow/bench/continuity/runs/wce_*.json` |
| Retrieval baseline | `willow/bench/scorecard.json` |
| W8 census | `sandbox/stone_soup/reports/recon-canonical.json` |

## Agent rules

1. **Never** fold WCE into `fleet-session-sweep` — witnesses live here.
2. Default WCE uses `--check-first` — use `--force` only when operator asks.
3. `locomo --all` is expensive — prefer `--locomo-conv N` for spot checks.
4. `smoke` runs full pytest — CI / pre-release only.
