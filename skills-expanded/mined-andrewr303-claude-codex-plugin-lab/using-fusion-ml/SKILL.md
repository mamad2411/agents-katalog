---
name: using-fusion-ml
description: >-
  Bootstrap skill for Fusion-ML. Use when starting a Fusion-ML task or when
  adapting copied SPML/Superpowers/Claude-oriented instructions to Codex.
---

# Using Fusion-ML

Use this skill as the compatibility shim for the bundled Fusion, ML workflow,
and Loop-God skills.

## Host Mapping

When copied source material names Claude Code tools, map them in Codex:

- `TodoWrite`, `TaskCreate`, `TaskUpdate` → `update_plan`
- `Bash tool` → `shell_command`
- `Agent tool` / subagent → real external Fusion CLI dispatch when advisory, or
  Codex-owned implementation with Fusion panel review when repository mutation
  is required
- `CronCreate` reminders → if not available, use explicit sleep/check loops only
  when the active task is a true monitoring loop
- `spml:*` references are retargeted to `fusion-ml:*`

## Pairing Rule

Use the narrow domain skill for the ML behavior and Loop-God for convergence:

- ML design → `ml-brainstorming`
- Implementation plan → `experiment-planning`
- Plan execution → `fusion-ml-subagent-dev`
- Static/runtime validation → `validation-pyramid`, `ml-static-checks`,
  `ml-runtime-validator`
- Long run → `training-handoff` then `watchdog`
- N-round compound iteration → `ml-iteration`
- Single-metric autonomous search → `autoresearch-create`, `autoresearch-handoff`,
  `autoresearch-run`, `autoresearch`
- Final claims → `verification`

Always start user-facing Fusion-ML tasks with the five-option menu from
`fusion-ml` unless the user already chose a specific path.

