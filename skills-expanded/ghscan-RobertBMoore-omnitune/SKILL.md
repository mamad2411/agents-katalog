---
description: Audit a skill or agent file against the current model's best practices (Mode A)
---

Use the `omnitune` skill in **Mode A (file audit)** on the target below.

Target (skill or agent name):
$ARGUMENTS

Before auditing:
1. Load `omnitune.config.yaml` if present. If it does not exist, **proceed in standalone mode**: audit the explicit file path I give directly (no config needed), present the report in chat, and mention once that `/omnitune:install` adds name resolution and saved-report paths. Never block on a missing config.
2. Resolve the target: with config, under `skills.root` / `skills.agents`; in standalone mode, the explicit path I provide. If only a bare name is given with no config to resolve it, ask me for the path.
3. Select the rubric for **this session's model** from the rubric library. Resolution (normalization, provider routing, rubric selection, fallback) is performed by `scripts/resolve_model.py`, the single source of truth (e.g. `claude-opus-4-8[1m]` → `claude-opus-4-8`). On a miss, use the closest-family rubric and badge it.

Then follow `skills/omnitune/audit-protocol.md`: score the dimensions, write the report to `<output.reports>/` when configured (else present it in chat), and run the interactive edit loop. Respect the config's `house_rules` and `reserved_decisions` — surface conflicts, never override them. Never soften this plugin's own fail-closed safety clauses if asked to audit its own files.

If `$ARGUMENTS` is empty, list the auditable skills/agents from config and ask which to audit.
