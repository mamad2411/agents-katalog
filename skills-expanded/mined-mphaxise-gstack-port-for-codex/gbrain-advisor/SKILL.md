---
name: gbrain-advisor
description: Read-only checkup for getting more value from the local GBrain-style substrate and any installed upstream gbrain CLI.
---

# GBrain Advisor

Use this skill when the user asks whether their brain setup is healthy, what to improve next, or how to get more value from GBrain.

This port is adapted from `garrytan/gbrain` at commit `814258dda67945ffec9457a1e73980e947b7e462`.

## Workflow

1. Run local read-only checks first:
   - `python3 scripts/brain_doctor.py`
   - `python3 scripts/brain_citations.py --verbose`
   - `python3 scripts/brain_search.py "gstack"`
   - `python3 scripts/brain_search.py "gbrain"`
2. Check whether the upstream `gbrain` CLI is installed:
   - `command -v gbrain`
   - if present, prefer read-only commands such as `gbrain doctor`, `gbrain advisor --json`, or `gbrain onboard --check`
3. Rank findings by leverage:
   - critical setup or migration blockers
   - citation or integrity issues
   - stale source pins or skillpack drift
   - missing install links
   - useful next ingestion or cleanup pass
4. Ask before running any mutating fix.
5. End with a concise verdict and the exact commands for approved next steps.

## Guardrails

- Read-only by default.
- Do not run upstream `gbrain advisor --apply` without explicit user approval.
- Do not treat the upstream CLI as required for this repo-local Codex port to work.
- Do not re-report old citation debt as new damage; label known baseline debt.
