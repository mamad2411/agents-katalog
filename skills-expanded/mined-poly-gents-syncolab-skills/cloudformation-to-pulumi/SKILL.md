---
name: cloudformation-to-pulumi
description: "Migrate AWS CloudFormation stacks/templates to Pulumi."
---

# CloudFormation to Pulumi

## Purpose

Migrate AWS CloudFormation stacks/templates to Pulumi.

This skill provides operational guidance for CloudFormation to Pulumi, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with CloudFormation to Pulumi.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to CloudFormation to Pulumi or covered by a more specific skill.
- When required integrations or credentials are unavailable.

## Expected Outcome

- Correct use of domain tools with verified results (not fabricated).
- Clear summary of actions taken, data returned, and recommended next steps.
- Errors and missing permissions reported explicitly.

## Inputs to Gather

- User goal, constraints, and any identifiers (URLs, IDs, project keys).
- Available tool sets and connection status.
- Relevant context from related systems before destructive writes.

## Workflow

1. Confirm the request maps to CloudFormation to Pulumi and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

# CloudFormation to Pulumi

Use this Pulumi Agent Skill from `pulumi/agent-skills` when the task matches this workflow.

## What it is for

- Migrate AWS CloudFormation stacks/templates to Pulumi.
- Follow the skill's migration/authoring sequence and safety checks before applying changes.
- Prefer preview/plan-first behavior and explicitly confirm destructive steps.

## Source

- GitHub: https://github.com/pulumi/agent-skills

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `kubernetes`
- `docker`
- `pulumi`



## Review / Decision / Execution Criteria

- Prefer smallest safe change; confirm destructive actions with the user.
- Use evidence from tool responses; cite IDs and links when present.
- Match integration-specific conventions (JQL, RFC3339, A1 notation, etc.).

## Output Format

Report:

1. What was requested and what was done.
2. Key results (tables or bullets).
3. Errors, blockers, or missing permissions.
4. Suggested next steps.

## Quality Bar

- Specific, actionable, and grounded in tool output.
- Concise unless the user asked for detail.
- Respect rate limits, pagination, and API semantics.

## Safety and Boundaries

- Do not commit secrets, tokens, or PII into skills or user-visible logs.
- Do not fabricate validation, send, or write confirmations.
- Confirm destructive operations (delete, destroy, mass update) when appropriate.

## Escalation / Dispatch Rules

- If the task spans multiple domains, use or suggest related skills via `relationships.skills`.
- If write access is required but unavailable, dispatch or ask the user to enable tools.

## References

- Legacy content migrated from `skills/old_skills.json` (`cloudformation-to-pulumi`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
