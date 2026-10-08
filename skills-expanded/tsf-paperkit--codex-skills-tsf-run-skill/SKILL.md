---
name: tsf-run
description: Use when the user wants to create, validate, run, or ablate tsf-paperkit experiment configs from natural-language intent.
---
# tsf-run

Goal: turn user intent into small reproducible TSF runs.

Workflow:
1. Inspect or create a YAML config under `configs/`.
2. Prefer toy/smoke settings unless the user explicitly requests larger runs.
3. Run `python -m tsf_paperkit.cli run --config <config>`.
4. For ablations, run `python -m tsf_paperkit.cli ablate --config <config>`.
5. Report output directory, resolved config, results CSV, and any actionable failure.

Rules:
- Do not silently change experiment settings; record resolved config.
- Do not claim toy/smoke results are benchmark results.
