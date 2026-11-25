---
name: fleet-hygiene
description: >-
  Run the complete fleet hygiene / audit sweep in one command.
  Use for repo litter, hook wiring, hardening scans, Kart sandbox audit closure,
  MCP inventory, SAFE path checks, kart-script retention, or filesystem groom —
  instead of hunting for repo_fleet_sweep, hook_wiring_audit, fleet_hardening_scan, etc.
---

# Fleet hygiene sweep

**One command. All hygiene audits. No scavenger hunt.**

Read-only by default — destructive phases (`kart` delete, `groom` archive) require explicit flags.

## Run it

```bash
cd ~/github/willow-2.0
WILLOW_AGENT_NAME=willow python3 scripts/fleet_hygiene_sweep.py
```

Via Kart (preferred in agent sessions):

```
agent_task_submit(
  app_id="willow",
  task="cd ~/github/willow-2.0 && WILLOW_AGENT_NAME=willow python3 scripts/fleet_hygiene_sweep.py",
)
kart_task_run(app_id="willow")
```

Dry-run / inventory:

```bash
python3 scripts/fleet_hygiene_sweep.py --list-phases
python3 scripts/fleet_hygiene_sweep.py --dry-run
```

Subset:

```bash
python3 scripts/fleet_hygiene_sweep.py --only repos,hooks,hardening
python3 scripts/fleet_hygiene_sweep.py --skip groom,kart
```

Raise SOIL flags (repos + hooks):

```bash
python3 scripts/fleet_hygiene_sweep.py --emit-flags
```

Destructive (operator-only):

```bash
python3 scripts/fleet_hygiene_sweep.py --apply-kart
python3 scripts/fleet_hygiene_sweep.py --apply-groom-t1
python3 scripts/fleet_hygiene_sweep.py --apply-groom-t2
```

## What it runs (8 default phases)

| Phase | Script | Output |
|-------|--------|--------|
| `repos` | `scripts/repo_fleet_sweep.py` | diverged repos, branch litter, untracked deliverables |
| `hooks` | `scripts/hook_wiring_audit.py` | `~/.claude/settings.json` hook events + loop registry |
| `hardening` | `scripts/fleet_hardening_scan.py` | merge conflicts, broken doc links, CI failures |
| `audit` | `scripts/audit_verify.py` | Kart sandbox S1–S18 gated closure |
| `mcp` | `scripts/mcp_inventory.py` | wired MCP servers for willow-2.0 |
| `paths` | `scripts/audit_safe_paths.py` | SAFE_ROOT / agents_root alignment |
| `kart` | `scripts/kart_scripts_sweep.py` | `.kart-scripts/` retention (dry-run default) |
| `groom` | `scripts/filesystem_groom_pass.py` | handoff/intake/backup TTL report (dry-run default) |

Report: `$WILLOW_HOME/reports/fleet_hygiene_sweep_report.json`

## Systemd timers (already installed)

| Timer | Phase | Schedule |
|-------|-------|----------|
| `repo-fleet-sweep.timer` | `repos` | Mon 04:00 |
| `hook-wiring-audit.timer` | `hooks` | daily 04:30 |

This sweep is the **manual superset** — run before release, after big merges, or when flags pile up.

## Optional (not in default)

| Item | When |
|------|------|
| `--only pii` | Pre-PR PII gate on `git diff` |
| `--mcp-fleet` | Slow `~/github` MCP inventory |
| `--stash-parity` | Stash ↔ KB atom parity (needs Postgres) |
| `scripts/health_report.py` | Operator comfort check |
| `scripts/check_mcp_registry.py` | Registry drift |

Listed in `--list-phases` under `optional_related`.

## Exit code

- `0` — all phases passed (no blocking findings)
- `1` — one or more phases reported issues (`hardening`, `audit`, `paths`, `pii` intentionally fail closed)

## Agent rules

1. **Never** run ad-hoc `git -C ~/github ...` loops for fleet hygiene — use this sweep.
2. Default run is **read-only** — do not pass `--apply-kart` or `--apply-groom-*` without operator consent.
3. Use `--emit-flags` when findings should surface at boot (repos/hooks only).
4. `audit` phase fails on **gated regressions** — treat as ship blocker, not noise.
5. For session memory / benchmarks, use `fleet-session-sweep` — not this skill.
