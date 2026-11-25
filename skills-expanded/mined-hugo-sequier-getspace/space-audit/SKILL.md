---
name: space-audit
description: Inspect a Space for drift and propose repairs, then act only on the actions the user approves. Use for "is my Space a mess?", "clean up my memory", "check my Space", "why is this claim unassigned?", or before an import.
---

# Auditing a Space

This skill is read-only until the user approves a specific action. It inspects structure, memory and coverage, reports findings with evidence, and proposes a repair plan. An audit may propose, but it must not decide.

Memory is autonomous and an agent cannot delete most records, so drift accumulates quietly. This is how it gets found.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource, and resolve the Space with `workspace_info`.
- Send the returned `agent_id` on every content call.
- Use the live tool schema for field names and bounds.

## What you can and cannot repair

Be exact about this before proposing anything. An audit that promises a deletion it cannot perform is worse than no audit.

| Finding | Action available to you | Reversible |
|---|---|---|
| A claim is wrong, duplicated, forbidden or a one-off | `forget_memory_claim`, one claim per call | No. The claim leaves recall immediately, though its text survives in the previous immutable revision |
| A category, section, project or database is unused, duplicated or wrong | `set_workspace_item_deleted` with `deleted=true` | Yes. Restore with `deleted=false` |
| A label that should have been another kind | Archive it and create the right kind, because a kind cannot change | The archive is reversible; the new item is not the old one |
| A source document is wrong or holds a secret | Nothing for you. The user deletes it on the website | Permanent |
| A task is wrong or holds a secret | Nothing for you. The user deletes it on the website | Permanent |
| A memory record as a whole, including an empty one left by forgetting its claims | `delete_memory` with the record's ID and current revision | No. The record, its claims and its index rows are removed |
| A session handoff | Nothing for you. No delete tool is exposed for it | The user acts on the website |

The website delete path is `DELETE /v1/spaces/{space_id}/resources/{resource_id}` with the current revision. It needs a signed-in session with write access, refuses a delegated agent identity, applies to a source document or a task, and is idempotent. Generated memory is refused there and is changed with the memory claim tools, such as `forget_memory_claim`, or removed with `delete_memory` instead. No other route removes a resource.

Never describe an archive as a deletion, and never describe a forget as reversible or the claim's text as erased.

## Inspect

Read everything before judging anything.

1. **Structure.** List `category`, `section` and `project` items, once with `deleted=false` and once with `deleted=true`. Look for two names that mean the same thing, a category no claim uses, a project with no tasks, and an archived item that a live task or document still references. A task's `project` field is not checked against the archive flag, so that reference can exist and still resolve, which is why a restored project can fail to save while the section it names stays archived. A project's `section_id` is checked, and must name an active section.
2. **Memory.** Page through `list_memories`, up to 200 memory records at a time, following `next_cursor`. Each record carries `stale`, `import_origin`, `recall` and `claims[]`; each claim carries `id`, `index`, `value`, `classification`, `memory_type`, `importance`, `edited`, `created_at`, `creator` and `source`, where `source` is the first cited resource ID or the literal `agent` when the record cites nothing. Two details decide what is live: `stale` is per record, computed from all of its cited sources, and excluded records are still listed, so read `recall.excluded` before treating a claim as recallable. Look for claims with no assignment (`classification.scope` of `unassigned`), records whose cited source changed, near-duplicate claims, claims that contradict each other, claims that record a one-off status instead of a durable fact, claims that read like a credential or personal data, and claims whose text carries an identifier instead of a readable sentence, which a person cannot use.
3. **Map.** Read `get_space_map`. Look for databases and folders with no project or section, containers with an empty description, near-duplicate container names, stale routing rules, and two current rules on one container that contradict each other. Report contradictions instead of choosing a winner.
4. **Documents.** List `kind="document"` resources and compare their IDs with the source revisions the claims cite, to find documents that were never mined when this Space mines documents.
5. **Coverage.** Ask `get_context` the questions the user says they will ask. Report which ones find nothing. This is the only check that measures whether the Space is useful rather than merely tidy.

## Report the findings

Group by severity, and give evidence for each finding: the item or claim ID, its value or name, and the rule it breaks. Separate what you verified from what you suspect.

Do not present a near-duplicate as a proven duplicate: compare meaning, scope, source and applicability, not wording. Where two claims disagree, report both and leave the contradiction open, because the guide says to preserve an unresolved contradiction rather than pick a winner. Never propose a change to a claim the user wrote or corrected without their request.

## Ask before repairing

Present the repair plan as a list of specific actions, each with its target and whether it can be undone, then ask for approval. Ask once for the plan, not once per item, unless the user prefers item by item. When the user approves part of it, perform exactly that part.

Do not act on an implied approval, on a general "clean it up", or on your own judgement that something is obviously junk. Do not repair by creating replacements before the archive is approved, and do not re-run setup as a repair.

A credential found in a document or a task is the one case that justifies urgency: report it plainly and tell the user to delete the record, because you cannot. When the user prefers to keep the record, rewriting its body through `save_resource` clears the current revision instead, and the previous revision remains readable.

## Perform an approved repair

- Claims: one `forget_memory_claim` call per claim, with `resource_id`, the current `expected_revision` and the claim's `entry_id`.
- A whole memory record, or the empty record that forgetting leaves behind: one `delete_memory` call with the record's `resource_id` and its current revision. It journals every claim first, so a restored backup cannot resurrect them. Both IDs come from the listing: `resource_id` is the memory record's `id`, not the claim's `source`, and `entry_id` is the claim's `id`. A forget takes no `value`, and passing the `source` value as `resource_id` returns not-found.
- Items: one `set_workspace_item_deleted` call per item, with the current revision and `deleted=true`.
- Re-read the target before acting, because a revision may have changed since the audit.
- Use a fresh `command_id` for each action, and reuse it unchanged on retry.
- Report each action's outcome separately. Never describe a partial repair as complete, and never let a failed action leave the user believing an item is gone.

## Report the result

Give the final state: what was archived, what was forgotten, what you could not change and who must change it, and what you deliberately left alone. List the findings you did not act on because the user did not approve them, so the next audit can pick them up.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

`list_workspace_items(space_id, kind, after, deleted)`: at most 25 items per page, ordered by item ID; `deleted=true` lists archived items.

`list_memories(space_id, query, after, limit)`: returns `{items, next_cursor, provider}`, at most 200 memory records per page, each carrying its own `claims[]`. A query returns ranked matches and no cursor; a listing without a query pages newest first.

`list_resources(space_id, kind, after)`: returns `{items, next_cursor}` with at most 50 documents or tasks per page; handoffs and generated memory are never listed here.

`forget_memory_claim(space_id, change)`: `command_id`, `resource_id`, `expected_revision` (>= 1) and `entry_id`. The claim is removed from the index immediately and is not recoverable.

`set_workspace_item_deleted(space_id, item_id, change)`: `command_id`, `expected_revision` (>= 1), `deleted` (`true` archives, `false` restores).

## Boundaries

- Change nothing without approval for that specific action.
- Never claim an archive is a deletion, or a forget is reversible.
- Never resolve a contradiction by removing one side.
- Never touch a claim the user wrote or corrected without their request.
- Do not re-run setup as a repair, or create a replacement before the archive is approved.
- Do not print a credential's value: name where it is and tell the user to remove it.
- Do not report a Space as healthy from a partial read.

## Failures and retries

Reuse the same `command_id` and payload after an uncertain write; a changed payload needs a fresh one. A revision conflict means the target changed since the audit: re-read it and re-check that the finding still holds before retrying. When a forget fails, report the claim as still present rather than assuming it is gone. When paging a large Space is incomplete, say which checks were partial, and do not call the Space healthy on partial evidence.
