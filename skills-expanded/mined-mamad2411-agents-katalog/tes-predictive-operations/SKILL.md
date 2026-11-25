---
name: tes-predictive-operations
description: "Local-only self-consumed guidance for choosing the next reasoning mode during active project work: prospect, mine, alternate, or package. Use when balancing planning pressure, evidence mining, and packaging timing across project reasoning. Prefer tes-high-agency-pattern for designing or reviewing one local development-layer skill/workflow operating pattern. Do not present as user-invoked."
license: MIT
---

# TES Predictive Operations

Operational contract: `tes.predictive_operations@0.1.0`.

Local development surface only. Do not package, publish, materialize, or treat
as distributable TES.

Self-consume only while already balancing planning pressure, evidence mining,
or local skill packaging. Do not ask the user to invoke this skill.
`tes-prospect` and `tes-mine` are reference skills; do not edit them.

Prefer `tes-high-agency-pattern` when the active decision is how to design or
review the operating pattern of one local development-layer skill.

## Contract

Use the smallest reasoning mode:

- `prospect`: risk is in the plan, boundary, dependency, or next decision.
- `mine`: risk is in language, code evidence, contradiction, or durable memory.
- `alternate`: pressure exposes risk, mining checks evidence, pressure returns
  with a sharper decision.
- `package`: behavior is clear, but the local skill surface needs tightening.

Load references only when needed:

- `references/predictive-operations.md` for mode details.
- `references/temperament-mode-selection.md` when deciding whether the next skill
  should behave like a sniper, miner, prospector, builder, gate, or curator.
- `references/skill-packaging.md` for packaging checks.

## Brake

On `pause`, `pausa`, `freia`, `segura`, `para`, `hold`, `step back`,
`volta um nivel`, or `resuma onde estamos`, stop pressure, summarize state, and
wait for explicit resume.

## Output

- `Mode`
- `Reason`
- `Next question/check`
- `Recommended answer`
- `Write policy`
- `Packaging check` when relevant

## Validation

When this skill changes, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/tes-predictive-operations
```

## Done

`tes-predictive-operations` is done when the next reasoning mode is selected,
the next question or repository check is singular, and no durable write is
performed outside the active workflow's write policy.

## Locks

- Do not modify `src/adapters/**`.
- Do not edit `tes-mine` or `tes-prospect`.
- Do not expose this as a user command or ask the user to invoke it.
- Do not create a third commercial skill or execution engine.
- Do not ask multiple questions at once.
- Do not package an unclear workflow.
