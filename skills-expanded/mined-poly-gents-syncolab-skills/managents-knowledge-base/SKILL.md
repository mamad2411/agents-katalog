---
name: managents-knowledge-base
description: "Project Knowledge Base concept tree — decisions, risks, notes, and custom taxonomy inside Managents (no extra OAuth)"
---

# Managents Knowledge Base

## Purpose

Project Knowledge Base concept tree — decisions, risks, notes, and custom taxonomy inside Managents (no extra OAuth)

This skill provides operational guidance for the Managents Knowledge Base, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with the Managents Knowledge Base.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to the Managents Knowledge Base or covered by a more specific skill (e.g. Notion/Google Docs curation via `curate-docs`).
- When required integrations or credentials are unavailable.

## Expected Outcome

- Correct use of domain tools with verified results (not fabricated).
- Clear summary of actions taken, data returned, and recommended next steps.
- Errors and missing permissions reported explicitly.

## Inputs to Gather

- User goal, constraints, and any identifiers (project id, concept id, type id).
- Available tool sets and connection status.
- Relevant context from related systems before destructive writes.

## Workflow

1. Confirm the request maps to the Managents Knowledge Base and required tools are available.
2. Gather identifiers and scope (project, concept, type/status).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

## When to use platform tools

The Knowledge Base is a per-project tree of **concepts** (decisions, risks, notes, and other custom types) organized under a **taxonomy** of types and statuses — distinct from Planning (sprints/roadmaps) and Timelines (dated milestones).

- Call **kb_get_taxonomy** (or **kb_list_concept_types**) first in a new project to learn valid `type_id` / `status` values before creating or filtering concepts — never guess them.
- Use **kb_list_concepts** (optionally filtered by `parent_concept_id`, `type_id`, `status`, `include_archived`) to browse the tree before creating duplicates; use **kb_get_concept** for a single node's full detail.
- Use **kb_create_concept** for new nodes and **kb_update_concept** for edits — only send the fields that changed. Set `archived_at` on **kb_update_concept** to archive a node and its descendants instead of deleting it when history should be preserved.
- Use **kb_create_concept_type** / **kb_update_concept_type** and **kb_create_concept_status** / **kb_update_concept_status** to extend the taxonomy itself (new node kinds or workflow states) — do this before creating concepts of a kind that doesn't exist yet.
- Use **kb_list_hierarchy_seeds** to discover ready-made concept trees, then **kb_import_hierarchy_from_refs** (by seed id) or **kb_import_hierarchy** (custom JSON tree of title/type_id/children) to bulk-populate a taxonomy.
- **project_id** is required in chat surfaces; in workspace tasks it is usually injected via `appContext` — you may omit it when the run already carries `projectId` / `project_id`.

## Safe order of operations

1. **Read first:** `kb_get_taxonomy`, `kb_list_concepts`, `kb_list_hierarchy_seeds`.
2. **Structure:** confirm/extend taxonomy (types, statuses) before creating concepts of a new kind.
3. **Destructive / approval tools:** `kb_delete_concept` (deletes descendants too), `kb_import_hierarchy`, and `kb_import_hierarchy_from_refs` (bulk-append new roots) require explicit human approval when enabled. Summarize blast radius (how many concepts, which subtree) before calling.

## Coordination with other agents

Knowledge Base concepts (decisions, risks) often relate to **Timelines** entries (milestones) and **Planning** goals/scopes. When a milestone or task is driven by a documented decision or risk, cite the `concept_id` so a Project Manager or SCRUM Master agent can link it on a timeline entry or task.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `managents-knowledge-base`



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
- Confirm destructive operations (delete, archive-cascade, bulk import) when appropriate.

## Escalation / Dispatch Rules

- If the task spans multiple domains, use or suggest related skills via `relationships.skills`.
- If write access is required but unavailable, dispatch or ask the user to enable tools.

## References

- `skills/skill.instruction.md`, `skills/meta.instructions.md`
