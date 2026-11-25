---
name: managents-timelines
description: "Stakeholder-facing project timelines and milestones inside Managents (no extra OAuth)"
---

# Managents Timelines

## Purpose

Stakeholder-facing project timelines and milestones inside Managents (no extra OAuth)

This skill provides operational guidance for Managents Timelines, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Managents Timelines.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is about sprint execution or backlog detail — use `managents-workboard` / `planning_*` instead.
- When required integrations or credentials are unavailable.

## Expected Outcome

- Correct use of domain tools with verified results (not fabricated).
- Clear summary of actions taken, data returned, and recommended next steps.
- Errors and missing permissions reported explicitly.

## Inputs to Gather

- User goal, constraints, and any identifiers (project id, timeline id, entry id).
- Available tool sets and connection status.
- Relevant context from related systems before destructive writes.

## Workflow

1. Confirm the request maps to Managents Timelines and required tools are available.
2. Gather identifiers and scope (project, timeline, entry).
3. Follow the domain guidance below; prefer list/get before create/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

## When to use platform tools

Timelines are per-project, ordered lists of **entries** (milestones, phases, dates) for narrative, stakeholder-facing schedules (launch plans, program timelines) — distinct from Planning's sprints/roadmaps and from the Knowledge Base's concept tree.

- Use **timelines_list** to see existing timelines for the project before creating a new one; use **timelines_get** for one timeline's full entry list.
- Use **timelines_create** to start a new timeline (`type`, title) and **timelines_update** to edit it.
- Use **timelines_create_entry** to add milestones, passing `parent_entry_id` to nest a sub-phase and `relative_span` for duration; use **timelines_update_entry** to adjust dates/titles and **timelines_reorder_entries** to resequence without recreating entries.
- Optionally attach a **concept_id** (or `related_concept_ids`) from the Knowledge Base on an entry so a milestone links back to the decision/risk that drives it — coordinate with the Knowledge Base skill/agent when a project has one.
- **project_id** is required in chat surfaces; in workspace tasks it is usually injected via `appContext` — you may omit it when the run already carries `projectId` / `project_id`.

## Safe order of operations

1. **Read first:** `timelines_list`, `timelines_get`.
2. **Structure:** create the timeline, then add top-level entries before nesting sub-phases with `parent_entry_id`.
3. **Destructive / approval tools:** `timelines_delete` and `timelines_delete_entry` require explicit human approval when enabled. Confirm which timeline/entry and summarize impact before calling.

## Coordination with other agents

When a timeline milestone is driven by a documented decision or risk, cite the Knowledge Base `concept_id`. When a milestone maps to delivery work, cross-reference the relevant Planning goal/scope/sprint so the SCRUM Master or Project Manager agent can keep both views aligned.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `managents-timelines`



## Review / Decision / Execution Criteria

- Prefer smallest safe change; confirm destructive actions with the user.
- Use evidence from tool responses; cite ids and links when present.
- Match integration-specific conventions (JQL, RFC3339, A1 notation, etc.) where applicable.

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
- Confirm destructive operations (delete timeline, delete entry) when appropriate.

## Escalation / Dispatch Rules

- If the task spans multiple domains, use or suggest related skills via `relationships.skills`.
- If write access is required but unavailable, dispatch or ask the user to enable tools.

## References

- `skills/skill.instruction.md`, `skills/meta.instructions.md`
