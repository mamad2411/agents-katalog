---
name: profile-plan
description: Project plan profile standards for dated milestones, dependencies, capacity, owners, and risks.
---

# Profile plan

Serves: plan — R2.3, R2.6, R2.7

## Core method

- Work backward from the milestone and state a measurable objective with success criteria. Source: ~/.claude/skills/project-manager/SKILL.md
- Date milestones, map predecessors, name the critical path, and give every workstream an owner. Source: ~/.claude/skills/project-manager/SKILL.md
- Show demand versus capacity per person, reserve uncertainty, and maintain a risk register with trigger and mitigation. Source: ~/.claude/skills/project-manager/SKILL.md

## Definition of done

The plan has a measurable objective, dated milestones with predecessors and named critical path, owned workstreams, demand-versus-capacity by person with no unflagged over-allocation, and risks with owners, triggers, and mitigations.

## Rubric

- `objective` — pass when the objective is measurable and has success criteria; evidence: objective and acceptance lines.
- `milestones-and-dependencies` — pass when milestones are dated, predecessors are shown, and the critical path is named; evidence: schedule and dependency graph.
- `owners-and-capacity` — pass when every workstream has an owner and demand versus capacity per person has no unflagged over-allocation; evidence: capacity table.
- `risks` — pass when each risk has an owner, trigger, and mitigation; evidence: risk register.

## Default skills

Load `project-manager` with the Skill tool when installed. If it is missing, resolve the facet through `codex-flow:skill-selection` (LOAD/VET/AUTHOR); never proceed without a verdict. Embed only distilled blocks into the executor prompt.

## Evidence

When evidenceMode is not `off`, every number follows evidence v2 as in codex-flow:profile-pilot: use anchors and a manifest, and have claims cite figures. Measured numbers come from their data source. Designed rates, targets, prices, and capacities live in a parameters file next to the deliverable, such as `params.csv`; figure/table commands READ that file. A command that echoes its own constant is forbidden. With evidence `off`, apply the `exec-deliverable` Verification block.

## Sampling

When evidence is not off, sample 3 figure-backed claims with `--sample 3 --seed <task number>` for the owner in one AskUserQuestion, as codex-flow:profile-pilot describes. A claim marked wrong is a finding.

## Failure modes

- Do not hide overload, omit predecessors, or assign work without a named owner. Source: ~/.claude/skills/project-manager/SKILL.md
- Do not call a vague activity a milestone; require a verifiable exit and date. Source: ~/.claude/skills/project-manager/SKILL.md

## Reviewer checklist

- Recompute dates, buffers, predecessor chains, and critical path. Source: ~/.claude/skills/project-manager/SKILL.md
- Compare each person's demand with capacity and flag load above 1.0. Source: ~/.claude/skills/project-manager/SKILL.md
- Check each rubric item pass/fail with evidence in reviews.md. derived, unverified

## Provenance

- Planning, dependency, capacity, and risk rules: Source: ~/.claude/skills/project-manager/SKILL.md
- Evidence and rubric integration: Source: skills/profile-pilot/SKILL.md
