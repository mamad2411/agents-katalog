---
name: orc-memory
description: Use when saving or recalling short project facts in ORC (ports, conventions, gotchas, decisions, pointers), on "remember this" or "what did we decide", or when deciding whether something is a memory or a skill.
allowed-tools: mcp__orc__memory_list mcp__orc__memory_read mcp__orc__memory_create mcp__orc__memory_update mcp__orc__memory_delete mcp__orc__memory_history mcp__orc__memory_revert mcp__orc__context
---

# ORC Memory

A memory is a short project fact worth knowing next session. Memories belong to one
project and are identified by name, like skills.

Good memories:

- **Ports and endpoints** - "API listens on 7700; e2e uses 7799"
- **Conventions** - "IDs are ULIDs; never use `any`"
- **Gotchas** - "On Windows, kill the bun server with `taskkill /F /T` or children survive"
- **Decisions** - "Hono over Express: runs natively in Bun" (include the _why_)
- **Pointers** - "Release procedure lives in the orc-release skill"

## Memory vs skill

| Memory                                  | Skill                                     |
| --------------------------------------- | ----------------------------------------- |
| One fact, rule or decision              | A procedure or long guidance              |
| At most 800 characters                  | Steps, checklists, examples               |
| `memory_create` / `memory_update`       | `skill_create` / `skill_update`           |

If it does not fit in 800 characters, it is a skill. Write the skill, and keep at most
a short memory that points to it ("Release steps: see skill orc-release"). Content over
the cap is rejected with that advice.

Do not store what the code, git history, CLAUDE.md/AGENTS.md or project docs already
say, or in-progress task details (use tasks and session events).

## Fields

- **name** - lowercase-hyphenated, at most 64 characters, unique in the project. Name
  the subject, not the event: `api-port`, `ulid-ids`, `windows-bun-kill`.
- **description** - at most 300 characters, saying **when it matters**:
  "Check before starting or killing the API server on Windows." It is all an agent sees
  in `context` and `memory_list`, so it decides whether the memory gets read.
- **content** - the fact itself, with the reason or evidence when it is not obvious.
- **priority** - 0-100, or unset. How important and broadly relevant the memory is:
  - 80-100: must-know for almost any work in the project (core conventions, hard rules)
  - 40-79: matters for a common area of work
  - 0-39: narrow or situational
  - unset: not scored yet; ranks below scored memories

`context` lists the top 30 memories by priority as `name [pN] - description`. Agents
read the ones that look relevant with `memory_read`. Score honestly; inflating
priority pushes useful memories out of that list.

## Workflow

1. **Recall** - call `context` first. Read relevant listed memories with
   `memory_read(name)`. For anything not listed, `memory_list({ q })` searches names and
   descriptions; `sort` is `reads` (default), `recent` or `priority`.
2. **Before creating** - `memory_list({ q })` for the subject. If a memory already
   covers it, `memory_update` that one instead of creating a near-duplicate.
3. **Create** - `memory_create({ name, description, content, priority })`.
4. **Correct** - `memory_update(name, { description?, content?, priority?, reason })`.
   Only the passed fields change; `priority: null` clears the score. Give a reason.
5. **Remove** - `memory_delete(name, reason)` when a memory is wrong or obsolete.

Pass `project` (readable name) when the session is not already scoped to the project.

## History and revert

Every create, update, delete and revert is recorded with the state before and after.

- `memory_history(name)` lists changes newest first.
- `memory_revert(name, change_id, expected_change_id, reason)` restores the state from
  before `change_id`; reverting a creation deletes the memory. `expected_change_id` must
  be the latest change from `memory_history`; if someone changed it since, reread first.
- A deleted memory can be restored by reverting its delete.

## Common mistakes

| Mistake                                 | Fix                                                  |
| --------------------------------------- | ---------------------------------------------------- |
| Pasting a procedure into a memory       | Make it a skill; keep a short pointer memory         |
| Description restates the name           | Say when the memory matters                          |
| Creating a second memory on one subject | `memory_list({ q })` first, then `memory_update`     |
| Every memory at priority 90+            | Reserve high priority for broadly relevant facts     |
| Deleting a decision to change it        | `memory_update` with a reason; history keeps the old |

## Related

- **orc-memory-review** - review this work unit's memory changes before delivery
- **orc-session** - session start, events and logging
- **orc-knowledge** - knowledge bases: search with citations, documents, comments and digests
