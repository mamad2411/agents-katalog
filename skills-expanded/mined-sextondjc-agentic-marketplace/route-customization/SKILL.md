---
name: route-customization
description: Use when deciding whether a behavior should be implemented as a custom agent, an instruction file, or a reusable skill.
---

# Customization Routing Decision

## Specialization

Determine the correct customization artifact before implementation:

- Agent file (`*.agent.md`)
- Instruction file (`*.instructions.md`)
- Skill (`SKILL.md`)

This skill prevents overlap, duplicate guidance, and poor discovery.

## Decision Flow

Use this order. Stop at the first `Yes`.

1. Is the need to define or change a specialized operating mode with a distinct role, boundaries, and tool behavior?
   - Yes: create or update an agent (`*.agent.md`).
2. Is the need to enforce always-on policy or coding standards for matching files (via `applyTo`) regardless of user request wording?
   - Yes: create or update an instruction file (`*.instructions.md`).
3. Is the need a reusable workflow, method, or decision guide that should be discovered and loaded only when relevant?
   - Yes: create or update a skill (`SKILL.md`).
4. If none apply:
   - Do not create a new artifact yet. Clarify the requirement and reassess scope.

## Artifact Selection Matrix

| Signal | Agent (`*.agent.md`) | Instruction (`*.instructions.md`) | Skill (`SKILL.md`) |
|---|---|---|---|
| Primary goal | Define a specialized agent mode | Apply persistent repo rules | Teach reusable workflow/pattern |
| Activation model | Explicit mode or subagent invocation | Automatically applied by path pattern | Loaded when trigger conditions match |
| Scope | Role-level behavior and delegation boundaries | File-type or path-scoped policy | Task-level guidance |
| Best for | Multi-phase orchestration or specialist lane | Security, style, architecture, CI guardrails | Repeatable implementation/checklist workflows |
| Avoid when | Rule is static and path-scoped | Need dynamic decision tree | Need always-on enforcement |

## Boundary Rules

- MUST choose an instruction when the requirement is mandatory and path-scoped.
- MUST choose a skill when guidance is situational and should not run in every task.
- MUST choose an agent only when a dedicated persona/work mode is needed.
- SHOULD update an existing artifact before creating a new one.
- SHOULD avoid duplicating the same rule in both instructions and skills.

## Anti-Patterns

- Creating a new agent just to store static coding standards.
- Putting global policy only in a skill (skills are not always loaded).
- Putting task workflows in instructions that trigger on every file.
- Creating overlapping artifacts with contradictory guidance.

## Required Output

When this skill is used, return a routing decision using this structure:

```markdown
Decision: <Agent | Instruction | Skill | No New Artifact>
Why: <one to three concrete reasons>
Target Path: <exact file path to create or update>
Alternative Rejected: <what was considered and why not selected>
```

## Naming Guidance

- Agent names: role-focused and lane-specific (for example, `security-researcher.agent.md`).
- Instruction names: policy domain and scope (for example, `testing-strategy.instructions.md`).
- Skill names: action-oriented and discoverable (for example, `customization-routing-decision`).

## Done Criteria

A routing decision is complete only when:

- Exactly one primary artifact type is selected.
- The decision includes rationale and a concrete target path.
- Overlap with existing agents, instructions, and skills was checked.
- The chosen artifact aligns with activation model and scope.

## Trigger Conditions

Invoke this skill when any of the following is true:

- The user needs to decide between an agent, instruction, or skill.
- A behavior request crosses customization boundaries and needs routing.
- A new customization idea must be classified before authoring.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute the skill-specific steps and produce the required artifacts or decisions.
3. Validate outputs for completeness and consistency with active workspace instructions.

