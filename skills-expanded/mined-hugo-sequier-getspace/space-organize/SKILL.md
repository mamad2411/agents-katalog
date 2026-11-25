---
name: space-organize
description: Create and apply the categories, sections and project links that give a Space its structure, including classifying stored memory. Use for "create a category", "organise this memory", "put these notes under a section", or "why is this claim unassigned?".
---

# Structure and labels

Space structure comes from four kinds of workspace item: a **project** groups tasks and documents, a **section** groups projects, and a **category** groups memory claims. This skill creates that structure and applies it. It does not decide what the user should care about, and it does not rename the user's vocabulary.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource, and resolve the Space with `workspace_info`.
- Send the returned `agent_id` on every content call.
- Use the live tool schema for field names and bounds.

## Read the existing structure first

List what already exists before creating anything: `list_workspace_items` with `kind="category"`, `"section"` or `"project"`, following `next_cursor`. Archived items appear only with `deleted=true`.

Reuse the user's own labels. A near-duplicate category is worse than none, because it splits recall and makes the user's own browsing inconsistent. When a label the user asked for already exists under different wording, use the existing one and say so instead of creating a second.

Never invent a label ID. Every ID you pass must come from a read.

## Create a category or a section

Both are label items with a name and a description, and both use the same save call as a project. Generate the item ID yourself, because `item_id` is a caller-supplied UUID and the server does not invent one, and send `expected_revision=0`.

A label's `name` is what the user sees and what the classifier matches against. Keep it short and in the user's words; put the explanation in `description`. A label's kind cannot change after creation, so a category is never converted into a section.

Create a label when the user asks for one, or when they ask for something to be organised and no suitable label exists. Creating structure is a visible change to the user's Space, so do not do it to tidy up a single claim.

## Apply structure to memory

Memory claims carry assignments: a `scope`, and lists of category, project and section IDs.

- `scope="project"` with one or more `project_ids` scopes the claim to those projects.
- `scope="global"` marks a claim that applies everywhere, and it must carry no `project_ids`.
- `scope="unassigned"` is the default, and it must also carry no `project_ids`.

Every ID must name a live item of the right kind, the lists must be unique, and each list holds at most 32 IDs. Apply assignments with `classify_memory_claim`, passing the memory resource ID, the current revision and the claim's `entry_id`.

Classifying a project also adds that project's parent section to `section_ids`, when the section is still active. The 32-section limit is applied after that addition, so a request can fail on a count the caller did not send. Count the parent sections of the projects you select before sending.

The two failures are different and worth reporting apart: an ID that names nothing returns not-found, while an ID of the wrong kind, or an archived one, is refused as an inactive selection. A section count over the limit is refused separately.

A manual classification survives later edits and rebuilds, which is why it is worth setting deliberately. A `classify_memory_claim` call with no `classification` hands the claim back to the configured classifier, which replaces the assignments; when no classifier is configured the write is rejected, and when the classifier cannot answer, the existing assignments are kept and the write fails as temporarily unavailable.

Read the claim first with `list_memories`, so you classify the claim that exists rather than the one you remember. Correct a wrong claim before organising it, and never reclassify a user's correction without their request.

## Apply structure to work

A project takes a `section_id` and must name an active section in the same Space. A folder may take a `section_id` and a `project_id`, and a database a `project_id` or `section_id`; a project wins over a section in the map. A folder's project places the folder only: the documents inside keep their own `project` and `folder`. A task or document takes a `project` field and must name a project in the same Space. All of these are references, so all are resolved from a read, and all are rejected when the target does not exist.

When you create or merge containers, or the user says what belongs where, save that placement rule with `remember` and `routes_to` naming the containers, or move an existing rule with `route_memory_claim`. Check the result in `get_space_map`.

Attaching a record to a project or a section does not change who can read it. Every record in a Space inherits that Space's access.

## Report the result

Name what you created, what you applied, and what you deliberately left alone. Report a claim you could not classify, and say why: no matching label, a classifier that could not answer, or an assignment the server rejected. Never report an unassigned claim as organised.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

`save_workspace_item(space_id, change)` with `kind="category"` or `kind="section"`:

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | New per change, reused unchanged on retry |
| `item_id` | UUID | Required on creation too; generate it yourself |
| `expected_revision` | int >= 0 | `0` on creation, otherwise the revision just read |
| `kind` | `category` or `section` | Cannot change after creation |
| `data` | object | `name` (string, 1-200) and `description` (string, up to 1000) |

`classify_memory_claim(space_id, change)`:

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | New per change, reused unchanged on retry |
| `resource_id` | UUID | The memory resource holding the claim |
| `expected_revision` | int >= 1 | The revision just read |
| `entry_id` | UUID | The claim to classify |
| `classification` | object | `scope`, `category_ids`, `project_ids`, `section_ids`; omit it to let the classifier decide |

`classification.scope` is `global`, `project` or `unassigned`. Each ID list holds at most 32 unique IDs. Project scope requires at least one `project_ids` entry; `global` and `unassigned` must have none.

`route_memory_claim(space_id, change)`: `command_id`, `resource_id`, `expected_revision` (>= 1), `entry_id`, and `routes_to`, up to 8 container IDs from `get_space_map`. It replaces the rule's current containers; an empty list clears them and keeps automatic routing from setting them again.

`list_workspace_items(space_id, kind, after, deleted)` lists the structure, at most 25 items per page, ordered by item ID. `set_workspace_item_deleted` archives or restores a label, which removes it from the classifier's active catalog.

## Boundaries

- Do not create a label to organise one claim, or a near-duplicate of an existing label.
- Do not invent a category, section or project ID.
- Do not reclassify a user's correction, or replace manual assignments, without their request.
- Do not use `scope="global"` for a claim that is specific to one project.
- Do not present a label as an access control.
- Do not archive a label that records still reference without saying so.

## Failures and retries

Reuse the same `command_id` and payload after an uncertain write; a changed payload needs a fresh command ID. On a revision conflict, reread the claim or item and reconcile. When the classifier reports that it is unavailable, the existing assignments were kept: report that, and retry only if the user still wants the change. Automatic classification stops when the Space holds more than 32 active categories, projects and sections together, and the affected claims stay unassigned; the fix is to archive labels, not to add more.
