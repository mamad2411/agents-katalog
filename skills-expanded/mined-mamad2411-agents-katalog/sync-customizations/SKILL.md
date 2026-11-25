---
name: sync-customizations
description: Use when maintaining .instructions.md and .agent.md files over time and evaluating whether their content remains aligned with current workspace standards and external guidance.
---

# Keeping Customizations Current

## Specialization

Maintain quality of `.instructions.md` and `.agent.md` files over time by continuously validating that their guidance is aligned with current workspace conventions, upstream standards, and actual agent behavior.

## Self-Containment Requirement

- REQUIRED: Keep execution self-contained within this skill. Do not delegate execution to sibling skills.
- REQUIRED: Keep execution self-contained within this skill. Do not delegate execution to sibling skills.

## Trigger Conditions

Invoke this skill when any of the following is true:

- Instructions or agents need maintenance against current workspace standards.
- Customization content may be stale, conflicting, or misaligned.
- A maintenance pass is needed before or after governance review.

## Inputs

Required:
- Target artifact set or explicit list of files to maintain.
- Evaluation date in ISO format (YYYY-MM-DD).
- Source catalog file path (default: `./references/source-catalog.md`).

Optional:
- Scope filter (instructions only, agents only, or both).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- Keep the source catalog in Markdown grid format.
- Every source row MUST include:
  - Source
  - What It Provides
  - Why It Is Valuable
  - In Use (Yes or No)
  - Last Evaluated (YYYY-MM-DD)
  - Current Status (Current, Needs Review, Deprecated)
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when no longer maintained or no longer relevant.
- Do not remove historical sources without adding a short deprecation note in the Notes column.

## Maintenance Workflow

1. Open [source-catalog.md](./references/source-catalog.md).
2. Re-evaluate each active source against current workspace behavior and spec guidance.
3. Update In Use, Last Evaluated, and Current Status for each source.
4. Record concrete deltas that affect workspace instruction or agent files.
5. For each affected artifact, assess against the evaluation criteria below.
6. Produce implementation-ready content changes for each affected artifact based on artifact type.
7. Run post-update validation checks within this workflow and record outcomes.
8. Publish a short maintenance summary in `.docs/changes/customization-maintenance/` with the date and impacted artifacts.

## Evaluation Criteria

Apply all checks for each instruction or agent file:

- **Relevance:** Does the content still reflect how the workspace operates?
- **Accuracy:** Are referenced tools, skill names, instruction file paths, and agent names still correct?
- **Completeness:** Are significant new workspace standards or conventions missing from the artifact?
- **Lean:** Is the file free of redundancy with other instructions or agent files?
- **Brevity:** Is wording economical for context efficiency without reducing clarity or boundary precision?
- **Behavior Alignment:** Does the artifact produce the intended behavior when loaded or invoked?

### Instructions-Specific Checks

- `applyTo` pattern still matches the intended file scope.
- No task workflow content has drifted in over time.
- No rules are now duplicated by a newer instruction file.

### Agent-Specific Checks

- All referenced collaborators and related assets are current and correctly named.
- All referenced instruction file names are current.
- Role boundary still matches what the orchestrator routes to this agent.

## Outputs

- Updated [source-catalog.md](./references/source-catalog.md).
- Optional source evaluation artifact using [source-evaluation-template.md](./references/source-evaluation-template.md).
- A concrete change list for impacted instructions and agents.
- A post-update validation summary when updates were made.

## Done Criteria

This skill is complete for a run only when:

- Every in-use source has an updated Last Evaluated date.
- Any stale source is marked Needs Review or Deprecated.
- All affected artifacts include explicit update instructions with rationale.
- Brevity expectations were evaluated for affected artifacts and included in any routed change list.
- Post-update validation results are recorded in the maintenance summary.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute the skill-specific steps and produce the required artifacts or decisions.
3. Validate outputs for completeness and consistency with active workspace instructions.



