---
name: photonic-copilot-workflow
description: Authoritatively orchestrate the end-to-end AI Photonic Design Copilot workflow by selecting the paper-reproduction or free-design runbook, routing each stage to the appropriate project Skill, and enforcing G1-G4 quality gates. Use when coordinating paper reproduction, free-form photonic design, solver selection, simulation, validation, case publication, legacy-case curation, or Skill updates in this repository.
---

# Photonic Copilot Workflow

Treat this Skill and the selected mode runbook as the authoritative source for workflow order, project-Skill routing, and mandatory pause points. Treat the [project README](../../README.md) as the human-facing explanation and invocation guide. If its workflow examples differ from this Skill, follow this Skill.

Use each source for its own boundary:

- Use this Skill and the selected runbook for orchestration.
- Use each child Skill for stage-specific implementation.
- Use [QUALITY_GATES.md](../../QUALITY_GATES.md) for approval criteria.
- Use [contracts.schema.json](../../schemas/v1/contracts.schema.json) for contract validation.

## Select one authoritative mode runbook

Determine the task mode before executing its workflow:

- For paper reproduction, read [the complete paper-reproduction runbook](references/paper-reproduction-workflow.md).
- For free-form design, read [the complete free-design runbook](references/free-design-workflow.md).

Read the selected runbook completely before starting its first stage. Do not preload the other runbook. If the task changes modes, finish or explicitly suspend the current mode, then read the other runbook completely before continuing. Treat fenced prompts in a runbook as reusable invocation or approval examples; apply their requirements directly instead of asking the user to paste them back stage by stage.

## Invoke project Skills formally

For every stage that requires a project Skill:

1. Identify the Skill required for the current stage.
2. Read that Skill's complete `SKILL.md` before acting on its instructions.
3. Announce the invocation exactly in this form:

   `Active project Skill: @skills/<skill>/SKILL.md`

4. Follow the loaded Skill for that stage.

A mention, link, or summary is not a formal invocation. Load only the Skill or Skills needed for the current stage; do not preload every project Skill.

## Route each stage

- Convert a paper PDF or images with [UniParser-Paper-Markdown](../UniParser-Paper-Markdown/SKILL.md).
- Extract paper evidence and build reproduction contracts with [reproduce-instructor](../reproduce-instructor/SKILL.md).
- Turn free-form design requirements into a contract with [free-design-intake](../free-design-intake/SKILL.md).
- For Meep FDTD, invoke [fdtd-core](../fdtd-core/SKILL.md) first, then [meep-fdtd-workflow](../meep-fdtd-workflow/SKILL.md).
- For Lumerical FDTD, invoke [fdtd-core](../fdtd-core/SKILL.md) first, then [lumerical-fdtd-workflow](../lumerical-fdtd-workflow/SKILL.md).
- Run PWE, GME, or Hopfield tasks with [legume-gme-workflow](../legume-gme-workflow/SKILL.md).
- Run RCWA tasks with [s4-rcwa-workflow](../s4-rcwa-workflow/SKILL.md).
- Curate legacy or nonstandard cases with [curate-photonic-example-case](../curate-photonic-example-case/SKILL.md).

## Select a solver before loading its Skill

After a `SimulationContract` exists, use the Tool Registry to match the requested method, capabilities, and solver. Load a solver Skill only after this selection. If the preferred solver is unavailable, report the reason and proposed alternative, pause for confirmation, and then formally invoke the confirmed replacement Skill. Never silently switch solvers.

Treat the Tool Registry, SolverAdapter, Example Library, Schema validation, and G1-G4 gates as platform components or approval gates, not as Skills.

If no project Skill matches the required stage, pause and report the missing capability. Do not invent a Skill path or bypass the project workflow.

## Enforce approval gates

- Do not generate a model before G1 contract approval.
- Do not start a real solver run before G2 execution approval.
- Do not publish an example before G3 result approval.
- Do not modify a project Skill before G4 Skill-update approval.

Keep approvals explicit and preserve the artifacts and hashes required by the child workflow and the project quality model.

For a project-Skill update, record the experience first, obtain G4 approval for the proposed diff, run the required regression tests, and wait for human merge approval. Do not turn a one-off correction directly into a Skill rule.
