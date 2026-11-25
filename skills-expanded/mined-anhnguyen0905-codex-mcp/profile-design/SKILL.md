---
name: profile-design
description: Design document profile standards for game goals, systems, economy, risks, and measurable outcomes.
---

# Profile design

Serves: design — R2.2, R2.6, R2.7

## Core method

- State the goal, target player, player fantasy, and the ordered core loop with time per loop. Source: ~/.claude/skills/game-director/SKILL.md
- Inventory every system with inputs, outputs, unlocks, dependencies, flows, and telemetry; remove orphan systems. Source: ~/.claude/skills/game-designer-systems/SKILL.md
- Put each currency/resource's sources, sinks, rates, pacing target, risks, and KPI definitions in tables. Source: ~/.claude/skills/game-designer-balance/SKILL.md

## Definition of done

The design states goal and fantasy, core loop, systems and dependencies, economy/balance numbers, risks, and KPIs. Each KPI has a definition, baseline, target, and measurement event. Repeated numbers agree.

## Rubric

- `goal-and-fantasy` — pass when goal, target player, and player fantasy are stated; evidence: goal and audience lines.
- `core-loop` — pass when the loop is ordered and gives time per loop; evidence: loop table.
- `systems-and-dependencies` — pass when every system has inputs, outputs, unlocks/dependencies, and no orphan remains; evidence: system/dependency matrix.
- `economy-balance` — pass when every currency/resource has named sources and sinks, numeric rates, and a pacing target; evidence: economy table and parameters file.
- `risks` — pass when at least three risks have impact and mitigation or kill criterion; evidence: risk register.
- `kpis` — pass when KPIs have definition, baseline/target, and an event used to measure them; evidence: KPI table and event names.
- `numbers-consistent` — pass when a number reused across sections has one value; evidence: cross-section comparison.

## Default skills

Load `game-designer-systems`, `game-designer-balance`, and `game-director` with the Skill tool when installed. If missing, resolve the facet through `codex-flow:skill-selection` (LOAD/VET/AUTHOR); never proceed without a verdict. Embed only distilled blocks into the executor prompt.

## Evidence

When evidenceMode is not `off`, every number follows evidence v2 as in codex-flow:profile-pilot: use anchors and a manifest, and have claims cite figures. Measured numbers come from their data source. Designed rates, targets, prices, and capacities live in a parameters file next to the deliverable, such as `params.csv`; figure/table commands READ that file. A command that echoes its own constant is forbidden. With evidence `off`, apply the `exec-deliverable` Verification block.

## Sampling

When evidence is not off, sample 3 figure-backed claims with `--sample 3 --seed <task number>` for the owner in one AskUserQuestion, as codex-flow:profile-pilot describes. A claim marked wrong is a finding.

## Failure modes

- Do not accept a system without an input/output and dependency record; it cannot be reviewed or implemented. Source: ~/.claude/skills/game-designer-systems/SKILL.md
- Do not accept vague balance adjectives, unmatched faucets/sinks, or unmeasured pacing; require tunable values. Source: ~/.claude/skills/game-designer-balance/SKILL.md

## Reviewer checklist

- Confirm fantasy, loop timing, unlock order, and system interactions are coherent. Source: ~/.claude/skills/game-director/SKILL.md
- Recalculate source/sink rates and compare every repeated number. Source: ~/.claude/skills/game-designer-balance/SKILL.md
- Check each rubric item pass/fail with evidence in reviews.md. derived, unverified

## Provenance

- Default game-system, balance, and director methods: Source: ~/.claude/skills/game-designer-systems/SKILL.md; Source: ~/.claude/skills/game-designer-balance/SKILL.md; Source: ~/.claude/skills/game-director/SKILL.md
- Evidence and rubric integration: Source: skills/profile-pilot/SKILL.md
