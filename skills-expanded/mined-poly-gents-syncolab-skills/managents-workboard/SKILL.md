---
name: managents-workboard
description: "Roadmaps, scopes, sprints, and execution work boards inside Managents (no extra OAuth)"
---

# Managents Planning and Work Boards

## Purpose

Roadmaps, scopes, sprints, and execution work boards inside Managents (no extra OAuth)

This skill provides operational guidance for Managents Planning and Work Boards, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Managents Planning and Work Boards.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to Managents Planning and Work Boards or covered by a more specific skill.
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

1. Confirm the request maps to Managents Planning and Work Boards and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

## When to use platform tools

Use **workboard_*** and **planning_*** tools for **in-product** delivery state: backlog, scopes, sprints, milestones, and physical work boards tied to a **project_id** and **room_name**.

- **project_id** is required in chat surfaces; in **workspace tasks** it is usually injected via `appContext` — you may omit it when the run already carries `projectId` / `project_id`.
- In **Managents persona** chats (`managents:persona_direct`, `managents:project_room`, room group), the runtime stamps `projectId` and `roomName` onto `appContext` from `scopeKind` / `scopeRef` so tools match workspace behaviour.
- **room_name** defaults from workspace `appContext` when absent from arguments (bulk assign, work board ops, sprint filters, etc.).
- Resolve a specific board with **workboard_get** (needs `work_board_id` + project) after **workboard_list** when working across multiple boards.

## Safe order of operations

1. **Read first:** `planning_overview`, `planning_list_tasks`, `workboard_list`, `planning_sprint_list`.
2. **Structure:** roadmaps → goals → milestones / scopes before large task moves.
3. **Destructive / approval tools:** `workboard_clear`, `planning_tasks_bulk_move`, `planning_tasks_bulk_detach_scope`, `planning_scope_detach_task`, sprint **complete**/**delete**, entity **delete** routes, and **planning_import_roadmap** require explicit human approval when enabled. Summarize impact before calling.

## Jira alignment

Prefer **Jira** tools for vendor issue keys and remote workflow; use **planning_*** for Managents workspace tasks and planning graph. If both exist, keep titles/status directionally aligned and cite which system is authoritative for the step you are taking.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `managents-planning`



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

- Legacy content migrated from `skills/old_skills.json` (`managents-workboard`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
