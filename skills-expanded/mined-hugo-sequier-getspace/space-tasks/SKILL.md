---
name: space-tasks
description: Capture, find and update actionable tasks in Space while preserving the original idea, reason and completion criteria. Use for "save this as a task", "what is left to do?", "why did we create this task?", or an explicit task-status update.
---

# Tasks that retain their context

Make a task understandable when its title is all the user remembers. A lookup or prioritization request is read-only. Create or update records when the user asks, or when an established instruction covers keeping the relevant task current. A suggestion in a recap is not automatically a new commitment.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource, and resolve the authorized Space with `workspace_info`.
- Send the returned `agent_id` on every content call.
- Use the live tool schema for field names and bounds; support differs across deployed versions.

Tasks live in the Space's existing canonical Tasks collection, reached through `save_resource` with `kind="task"`. No separate board or collection is created.

A project can also keep its work as rows of a task database, a database with a `tasks` setting that the `space-base` skill describes. For "what is on today?" or "plan this for tomorrow", read the task databases listed in `get_space_map` as well as native tasks: a row is on a day's plan when its planned field holds that day or an earlier one and its status is not a done option. Do not copy a row into a native task to plan it; set the row's planned field.

## Find the right task

Prefer a known resource ID. Otherwise search with `get_context(mode="search")` using distinctive words from the task and the project, then read candidates with `get_resource`. For an inventory, or to check beyond ranked matches, use `list_resources(kind="task")` and follow `next_cursor` as `after`. It returns up to 50 records per page and orders by resource ID, not by time, so an old-looking record is not a reason to stop paging.

Open a matching task before changing it. If several tasks plausibly match, resolve the target from context or ask. Before creating, check whether an existing task already covers the same outcome; a ranked search miss does not prove that none exists. State incomplete coverage rather than promising uniqueness, and keep separate tasks that have different scopes even when their titles are similar.

## Capture the idea and outcome

Choose a title that describes the action. Keep the body proportionate to the task, retaining these details when they are known:

- Original request: the user's wording or a faithful paraphrase.
- Purpose: the problem it addresses and why it matters.
- Intended outcome and scope, including explicit exclusions.
- Completion criteria: an observable result, not "work on it".
- Decisions, constraints and links to supporting records.
- Open questions and the next action; mark a proposed approach as a proposal.

When the surrounding conversation establishes the intent, "Implementation of sessions" can become "Add agent session skills" with the purpose "Let users resume work and save progress through their connected agent." The task's meaning survives even if the conversation is forgotten; the title alone would not establish that interpretation.

Do not manufacture a missing rationale, owner, deadline or acceptance decision. For "save this idea for later", preserve the idea now with the unknowns stated, and ask only when the intended record or scope cannot be determined. Saving an idea as a task does not schedule it or start implementation.

## Map the supported fields

| Task state | Representation |
|---|---|
| Captured or not started | `status="todo"` |
| Work has started | `status="in_progress"` |
| Completion is established | `status="done"` |
| Waiting on the user's decision, approval or merge | `status="needs_you"`, with the question or the thing to approve stated first in the body. The task stays on the user's home page until they change its status, so do not also write a separate "blocked" document |
| Deferred, or blocked on something other than the user | Keep the closest supported status and explain the condition in the body |

| Fact | Where it goes |
|---|---|
| Project | `project`, a UUID for an existing project workspace item in the same Space |
| Priority | `priority`, one of `High`, `Medium`, `Low` |
| Owner, deadline, estimate, external ticket | The body, because there is no field for them |
| Topics and existing Space citations | `recall.topics` and `recall.sources` |

To attach a task to a project, resolve the project's workspace item first with `list_workspace_items(kind="project")` or `search_workspace`, and never invent an ID. The server rejects a project that does not exist in the same Space. Creating a project is a separate, user-authorized action through `save_workspace_item(kind="project")`, and this skill does not take it on its own.

Do not pass invented fields, and do not imply that body text creates reminders, assignments or enforceable permissions.

## Update without losing work

For creation, omit `resource_id` and set `expected_revision=0`. For an update, use the resource ID and the revision just read. Send the full intended title, body and status: the operation replaces content, so a status-only change must preserve the existing title and body. Preserve recall metadata, including any exclusion setting and existing references. A resource cannot change kind: a document stays a document.

Move work to done when the user's explicit report or a relevant observed result supports it. Attribute the evidence and record what remains unverified. If sources disagree, explain the conflict and resolve it before changing status, and do not run unrelated checks just to close a task.

Delete a task only when the user asks for it to be gone. `delete_task(space_id, resource_id, expected_revision)` needs a write grant and the revision just read, and it permanently removes every revision; separately saved memories remain. Do not delete a task to close finished work: move it to done with `set_task_status` instead. When the user names several tasks, resolve each one before deleting and report which were deleted. Agents cannot delete documents; a signed-in user does that on the website.

## Report the result

Return the saved task's resource ID, revision and resulting status. A save response carries no URL, so give a link only when the Space's website origin is known. When only some requested updates succeed, name the saved and unsaved tasks separately and do not describe the batch as complete. Task capture does not also write a journal, create long-term memory or modify an external board unless the user's workflow calls for it.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

`save_resource(space_id, change)`, schema defaults at this revision:

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | New per change, reused unchanged on retry |
| `resource_id` | UUID, optional | Omit on creation |
| `expected_revision` | int >= 0 | `0` on creation, otherwise the revision just read |
| `kind` | `document` or `task` | `task` here |
| `title` | string, 1-300 | Must not be blank |
| `body` | string, up to 700000 | Defaults to empty |
| `status` | `todo`, `in_progress`, `needs_you` or `done`, or a configured column | Defaults to `todo` |
| `recall` | object, optional | `category`, `topics` (up to 12), `sources` (up to 20), `excluded` |
| `project` | UUID, optional | An existing project workspace item in this Space |
| `priority` | `High`, `Medium` or `Low`, optional | The user's recorded priority |

`recall.category` accepts `source`, `handoff` or `memory`, but only `source` is usable for an ordinary task: `handoff` is rejected for a task, and `memory` is reserved for a generated memory record, so an ordinary write that sets it is rejected and an existing memory resource cannot be edited this way. A new `recall.sources` entry must resolve to a real `{resource_id, revision}` in the same Space; an existing citation survives deletion of its source. The whole request must stay within 1 MiB.

`list_workspace_items(space_id, kind, after, deleted)` lists `project`, `database`, `category` or `section` items; follow `next_cursor` for all of them.

## Boundaries

- Do not create a task the user did not ask for, or one that a recap merely suggested.
- Do not manufacture owners, deadlines or acceptance criteria.
- Do not change status to match a handoff, or to close an argument between sources.
- Do not invent a project ID or a field the schema does not have.
- Do not write memory, a journal or an external board as a side effect.

## Failures and retries

Use a new `command_id` per change and reuse it with the same payload when retrying, including after an uncertain result. On a revision conflict, read the latest version and merge compatible changes, then use a new ID for the changed payload. Ask when reconciling would mean choosing between conflicting user intentions.
