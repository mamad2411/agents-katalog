---
name: space-projects
description: Create, read, update and archive projects in Space, and attach tasks and documents to them. Use for "create a project", "what projects do we have?", "archive the old project", or "put this task under the launch project".
---

# Projects

A project is a named workspace item that groups related tasks and documents. It has a name, a description, a status and an optional section, and it is versioned like any other record. This skill manages the project record and the references to it. It does not plan the work, write documents or change memory.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource, and resolve the Space with `workspace_info`.
- Send the returned `agent_id` on every content call.
- Use the live tool schema for field names and bounds; support differs across deployed versions.

## Find a project before you make one

List the Space's projects with `list_workspace_items(kind="project")` and follow `next_cursor` for all of them. It returns at most 25 items per page, ordered by item ID, and hides archived items unless you pass `deleted=true`.

Use `search_workspace` with a name or topic when you do not know the project's name. Read a candidate with `get_workspace_item` to confirm its description and status before changing it.

Create a project only when the user asks for one, or when an established instruction covers it. A project name that appears in a conversation is not by itself a request to create a project.

## Create or update a project

For a new project, generate the item ID yourself: `item_id` is a caller-supplied UUID and the server does not invent one. Send `expected_revision=0`.

For an update, read the project first and pass its current `revision` as `expected_revision`. The server compares it and rejects the write when it does not match, so an update must never be sent from a stale read. A project's kind cannot change.

Send the full intended snapshot every time: `name`, `description`, `status` and any `section_id`. The server does not reject a partial snapshot, which makes omission the dangerous case: an omitted `description` is stored as empty, an omitted `status` becomes `todo`, and an omitted `section_id` clears the project's section. An update that only changes the status must therefore carry the current name, description and section.

Saving also clears the archived flag. An ordinary save on an archived project restores it, so use archive and restore deliberately rather than as a side effect of an edit.

## Sections

A section groups projects. Reference one through `section_id`, and resolve its ID with `list_workspace_items(kind="section")` first. The server rejects a section that does not exist or is archived in this Space, so never invent a section ID.

## Archive and restore

Archiving hides a project from ordinary listings while preserving its history. It is not a deletion, and the revisions remain readable by ID.

Archive or restore with `set_workspace_item_deleted`, passing the current revision and `deleted` true or false. Archiving is not a way to settle an argument about which project is correct, and it does not touch the tasks or documents that reference the project. The active-section check runs on an ordinary save only, so archiving does not re-validate a section that was archived after the project was saved.

## Attach work to a project

A task or a document references a project through the `project` field of `save_resource`, which takes the project's item ID. The server rejects an ID that is not a project in the same Space, so resolve it first and report the rejection rather than retrying blindly.

Detaching work from a project means editing its `project` field, not removing the record. An agent with a write grant can delete a task the user asked to remove with `delete_task`, but not a document; a signed-in user with write access can delete either one on the website. Deletion removes every revision.

## Report the result

Return the project's item ID, its new revision and the resulting name and status. State whether the write created or updated the project. Report an archive or restore as such, and never describe an archived project as deleted or a failed save as complete.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

`list_workspace_items(space_id, kind, after, deleted)`:

| Field | Type | Notes |
|---|---|---|
| `kind` | `project`, `database`, `category` or `section` | Required |
| `after` | UUID, optional | The `next_cursor` from the previous page |
| `deleted` | bool, default false | `true` lists archived items |

Returns `{items, next_cursor}` with at most 25 items per page, ordered by item ID.

`get_workspace_item(space_id, item_id, revision)`: reads one item, optionally at a historical revision. The result carries the item's data plus `id`, `kind`, `revision`, `deleted`, `updated_at` and `author_agent`.

`save_workspace_item(space_id, change)`:

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | New per change, reused unchanged on retry |
| `item_id` | UUID | Required on creation too; generate it yourself |
| `expected_revision` | int >= 0 | `0` on creation, otherwise the revision just read |
| `kind` | `project`, `database`, `category` or `section` | `project` here, and it cannot change |
| `data` | object | Validated per kind, see below |

`data` for a project:

| Field | Type | Notes |
|---|---|---|
| `name` | string, 1-200 | Must not be blank |
| `description` | string, up to 10000 | Defaults to empty |
| `status` | `todo`, `in_progress` or `done` | Defaults to `todo` |
| `section_id` | UUID, optional | Must be an active section in this Space |

`set_workspace_item_deleted(space_id, item_id, change)`:

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | New per change, reused unchanged on retry |
| `expected_revision` | int >= 1 | The revision just read |
| `deleted` | bool | `true` archives, `false` restores |

The whole item snapshot must stay within 900 KiB.

## Boundaries

- Do not create a project the user did not ask for.
- Do not invent an item ID for an existing project, a section ID or a project reference.
- Do not update from a stale revision, or send a partial snapshot.
- Do not archive a project to resolve a naming or ownership disagreement.
- Do not claim that archiving deletes the project or its history.
- Do not detach or edit tasks and documents as a side effect of a project change.

## Failures and retries

Reuse the same `command_id` and payload after an uncertain write. The same command ID with a different payload is rejected as reused, so a changed payload needs a fresh one. On a revision conflict, read the current item and reconcile. A rejected section ID means the section is missing or archived, not that the write is impossible: report it and let the user choose.
