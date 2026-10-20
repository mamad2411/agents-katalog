---
name: shadow-design-engineer
description: "Bridge visual intent and implementation — component states, tokens, and handoff quality."
---

# Shadow Design Engineer

## Purpose

Bridge visual intent and implementation — component states, tokens, and handoff quality.

This skill provides operational guidance for Shadow Design Engineer, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Shadow Design Engineer.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to Shadow Design Engineer or covered by a more specific skill.
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

1. Confirm the request maps to Shadow Design Engineer and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

# Shadow Design Engineer

- Map design to component/state matrix
- Flag gaps: missing breakpoints, focus states, motion specs
- Prefer tokens and existing primitives over one-offs
- Call out implementation risks (SSR, perf, bundle size)

Output: handoff checklist for eng.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `figma`
- `storybook`
- `react`



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

- Legacy content migrated from `skills/old_skills.json` (`shadow-design-engineer`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
