---
name: karea
description: Use this skill for ALL Karea task-manager work, and load it BEFORE calling any `karea` / `mcp__karea__*` MCP tool. Triggers whenever the user wants to create, edit, close, view, or look up Karea tasks, projects, categories, notes, sticky notes, questions, meetings, reminders, or resources; set/read a task's AI Context or long-form markdown; get a recap; link an AI session to a task; or any request that sounds like task tracking ("add a task", "what's on my plate", "mark X done", "add a note", "ask a question", "pick up <task>", or references a task by its ID like KA123 / HA42 / C1 / T2). If you are about to use a `karea` / `mcp__karea__*` MCP tool and this skill is not loaded, load it first and follow its discipline (read Context before working, link the session automatically, keep Context current, notes vs context vs markdown). Prefer this skill over generic note-taking.
---

# Karea

Karea is an MCP-first task manager at [karea.app](https://karea.app). This skill lets the user drive Karea from inside Claude Code through the `karea` MCP server.

## When to use this skill

- The user asks to create, edit, close, delete, or view a task / project / category.
- The user asks "what do I have to do", "show my tasks", "what's blocked".
- The user wants a recap of recent activity.
- The user wants to read or write the markdown document attached to a task (common during debugging -- dump findings, root cause, fix).
- The user references a task by its per-project ID (e.g. `HA123`) or its category-visual ID (e.g. `C1`, `T2`).
- The user wants to add, edit, or read notes on a task.
- The user wants to ask or answer open questions.
- The user wants to manage resources (files, text snippets, links).
- The user wants to plan or prepare a meeting, set a reminder, or jot something on the sticky board.

## Tools available via the `karea` MCP

There are two ways the user may be connected, and they behave identically once
you are talking to Karea:

- **Local (npm)** - `karea-mcp` over stdio, with `KAREA_API_KEY` in their MCP
  config. This is the power-user path and supports `KAREA_MCP_LEGACY_TOOLS`.
- **Hosted (KA395)** - the connector at `https://karea.app/api/mcp`, added in
  Claude's connector settings and authorised in a browser with OAuth. Nothing
  is installed, so this is the only option on mobile.

Enable **only one** of the two in a given client. With both on, every tool is
listed twice (`mcp__karea__karea_read` and `mcp__claude_ai_Karea__karea_read`)
and the model has to choose between twins on every call.

<!-- SYNC:TOOL_CATALOGUE -->
The server advertises **9 tools** (one read-only tool, write tools by area, one delete tool, plus `karea_help`), covering
**70 actions**. Every tool takes `{ action, params }`.

**Calling convention: actions are not tools.** Call the tool that lists the
action, and pass the action name as `action`. In Claude Code the tool is
`mcp__karea__<tool>` (or `mcp__claude_ai_Karea__<tool>` for the hosted
connector), never `mcp__karea__<action>`.

- Correct: `karea_read` with `{ "action": "karea_list_notes", "params": { "task": "KA12" } }`
- Correct: `karea_tasks_write` with `{ "action": "karea_create_task", "params": { "name": "Fix the navbar", "priority": 1 } }`
- Wrong: a tool named `karea_list_notes` or `mcp__karea__karea_list_notes` (no such tool exists)
- Wrong: `karea_tasks_write` with `{ "action": "karea_list_notes" }` (the server refuses it and names `karea_read`)

The `karea_` prefix of an action may be dropped (`"list_notes"` works too).
Unsure which tool owns an action? `karea_help` with that action name says.

| Tool | What it covers | Its actions (pass one as `action`) |
|---|---|---|
| `karea_read` | Read anything in Karea without changing it: projects, tasks, subtasks, notes, sticky notes, task documents and AI context, open questions, resources, meetings, reminders, Jira links, AI sessions, and the activity recap. The main entry point - start here. | `karea_list_projects`, `karea_list_tasks`, `karea_view_task`, `karea_view_tasks`, `karea_task_changes`, `karea_list_subtasks`, `karea_list_notes`, `karea_list_sticky_notes`, `karea_get_markdown`, `karea_get_context`, `karea_list_questions`, `karea_list_resources`, `karea_get_resource`, `karea_list_meetings`, `karea_view_meeting`, `karea_check_reminders`, `karea_get_jira_link`, `karea_list_sessions`, `karea_recap` |
| `karea_tasks_write` | Create and change tasks: create, edit one or many, close one or many, log finished or in-progress work, plus subtasks and closing requisites (the checklist a task needs before it can close). | `karea_create_task`, `karea_quick_task`, `karea_doing`, `karea_edit_task`, `karea_edit_tasks`, `karea_close_task`, `karea_done`, `karea_create_subtask`, `karea_add_requisite`, `karea_toggle_requisite` |
| `karea_notes_write` | Write notes: add or edit task notes (human-readable updates) and sticky notes, and write a task's markdown document or an entry of its AI Context (private cross-session memory). Overwrites what an edit replaces. | `karea_add_note`, `karea_edit_note`, `karea_create_sticky_note`, `karea_edit_sticky_note`, `karea_set_markdown`, `karea_set_context` |
| `karea_projects_write` | Create a project or a category inside one, or share a project with someone by email. | `karea_create_project`, `karea_create_category`, `karea_share_project` |
| `karea_meetings_write` | Create and edit meetings and put tasks or questions on their agenda; create, answer and edit open questions; create, snooze, dismiss or complete reminders. | `karea_create_meeting`, `karea_edit_meeting`, `karea_link_task_to_meeting`, `karea_link_question_to_meeting`, `karea_create_question`, `karea_answer_question`, `karea_edit_question`, `karea_create_reminder`, `karea_snooze_reminder`, `karea_dismiss_reminder`, `karea_mark_reminder_done` |
| `karea_resources_write` | Create, upload and update resources in the file/document library and attach them to tasks; link a task to a Jira issue or to an AI coding session. | `karea_create_resource`, `karea_upload_resource`, `karea_update_resource`, `karea_link_resource_to_task`, `karea_link_jira`, `karea_link_session` |
| `karea_assistant` | Send a natural-language request to the Karea AI assistant, which may read or change your tasks to carry it out. | `karea_ask` |
| `karea_delete` | Delete or detach things. Permanent deletes (project, category, task, requisite, note, sticky note, question, resource, meeting) need confirm=true where stated; detaching a resource, task, question, Jira issue or AI session from what it is linked to. | `karea_delete_project`, `karea_delete_category`, `karea_delete_task`, `karea_delete_requisite`, `karea_delete_note`, `karea_delete_sticky_note`, `karea_delete_question`, `karea_delete_resource`, `karea_delete_meeting`, `karea_unlink_resource_from_task`, `karea_unlink_task_from_meeting`, `karea_unlink_question_from_meeting`, `karea_unlink_jira`, `karea_unlink_session` |
| `karea_help` | Full parameter list of any action, and the tool to call it through. | none: pass an action name as `action`, or nothing to list them all |

Call `karea_help` with an action name for its full parameter schema. Set
`KAREA_MCP_LEGACY_TOOLS=1` to go back to 70 individual tools.
<!-- /SYNC:TOOL_CATALOGUE -->

### Tasks

Reads go through `karea_read`; changes through `karea_tasks_write` (documents and AI Context through `karea_notes_write`); deletes through `karea_delete`.


| Action | Use for |
|---|---|
| `karea_list_tasks` | List tasks in a project. Needs at least one filter: `projectId`, `status` (open, in_progress, blocked, review, backlog, done, cancelled, all; comma-separated works), `closedSince`, `category`, `priority`, `assignee` or `search`. Without a `status` it returns the open ones (everything but done and cancelled), capped at 200; for closed work pass `status: "done"` plus `closedSince` (`7d`, `24h`). |
| `karea_view_task` | Full detail of one task (resolves UUID, `HA123`, `C1`, or exact title). Output also includes any linked resources with their IDs. Pass `includeContext: true` to inline the task's AI Context (avoids a follow-up `karea_get_context` round-trip); when omitted, the response hints that Context exists. |
| `karea_view_tasks` | Same as `karea_view_task` but batched: pass an array of task refs (visual IDs, names, or UUIDs) and get one consolidated response with a block per task. Max 50 per call. `includeContext: true` and `includeMarkdown: true` inline each task's AI Context and document. Prefer this over calling `karea_view_task` N times when inspecting a batch. |
| `karea_task_changes` | What changed on ONE task in the last `sinceMinutes` minutes (1 to 2880, i.e. up to 48 hours): status, fields, notes (short excerpt), Context entry titles, links, each with who, how (`user` = browser, `mcp` = API/AI, `jira`, `system`) and when, newest first. Use the smallest window you need (5 is typical; a poller passes the minutes since its last check). Cheaper than re-reading the whole task. |
| `karea_create_task` | New task. Flags: `name` (keep it under 50 characters: recommended, not enforced; hard limit 500), `category`, `priority`, `sla` (`2d`/`5h`/`tomorrow`), `description` (rendered as Markdown -- use `**bold**`, lists, `code`, links), `source`, `closingRequisites`, `tags`, `markdown`, `jiraIssueKey`, `parentId` (visual ID, name or UUID). For subtasks, prefer `karea_create_subtask`. |
| `karea_create_subtask` | Create a subtask under a parent. Takes `parent` (visual ID like `KPL77`, name, or UUID) plus the same flags as `karea_create_task`. Inherits the parent's category by default. |
| `karea_list_subtasks` | List subtasks of a parent task. Accepts `parent` as visual ID, name, or UUID. |
| `karea_edit_task` | Edit any field of a task: `name` (rename), `priority`, `status`, `reviewStage`, `sla`, `description` (Markdown), `markdown`, `category`, `tags` (with `clearTags` to replace), `closingRequisites` (with `clearClosingRequisites`), `jiraIssueKey` (set to `"unlink"` to remove), or `note` to append a note. |
| `karea_edit_tasks` | **The same change applied to many tasks, in ONE request**: `tasks` (array of refs) plus any of `status`, `priority`, `category`, `sla`, `assignee`, `note`. Returns a per-task result; an unresolvable ref is reported without costing the rest. Up to 5000 per call. Use this instead of looping `karea_edit_task` -- looping is N calls against a 60/min limiter to express one intention. |
| `karea_close_task` | Close a task; optional `resolution`. If closing requisites are still open it reports them instead of closing; tell the user, and only pass `confirm: true` if they want it closed anyway. If the task has open subtasks the close is refused and the subtasks are listed: ask the user, then call again with `closeSubtasks: true` (close them too) or `false` (only this task). |
| `karea_delete_task` | Delete; requires `confirm: true`. |
| `karea_doing` | Create a task already in `in_progress` status. |
| `karea_done` | **Close many tasks at once** (array of refs), in one request. Use this rather than calling `karea_close_task` N times; `karea_close_task` is for a single task where the closing-requisite check matters. |
| `karea_quick_task` | "I just did this" log entry (`/did`). |
| `karea_get_markdown` / `karea_set_markdown` | Read/write the long-form markdown doc on a task -- **use this to persist investigation notes**. |
| `karea_get_context` / `karea_set_context` | Read/write the task's **Context** -- titled entries of AI working memory that hold the **full history** of a task (what was tried, decided, discovered, abandoned) across sessions (e.g. `Plan`, `Findings`, `Decisions`, `Gotchas`, `Attempted`). `karea_set_context` upserts by `title` (default `General`); empty content deletes the entry. The title names the topic, never a date: a near-copy of an existing title (`Decisions 2026-10-21` beside `Decisions`) is refused unless you pass `allowSimilarTitle: true`; append to the existing entry instead. Read FIRST when picking a task up, then update **incrementally** -- never overwrite with just the current status. Distinct from notes (human-readable) and markdown (long-form docs). |
| `karea_add_requisite` | Add a closing requisite (checklist item before task can close). |
| `karea_toggle_requisite` | Mark a closing requisite as done or undone. |
| `karea_delete_requisite` | Delete a closing requisite. |

### Notes

Reads go through `karea_read`; changes through `karea_notes_write`; deletes through `karea_delete`.

When a note mentions a resource, write it as a Markdown link, never its name plus a bare UUID: `[spec.md](https://karea.app/dashboard/resources?open=<resource UUID>)`. Resource responses print this line ready to paste (`Markdown link:`). Tasks are `[[KA12]]`; see "Referencing other items" below.


| Action | Use for |
|---|---|
| `karea_add_note` | Add a note to a task. Pass `replyTo` (a note ID) to reply to that note; replies are threaded under it. |
| `karea_edit_note` | Edit an existing note's content. |
| `karea_delete_note` | Delete a note from a task. |
| `karea_list_notes` | List all notes on a task, with replies indented under the note they answer. |

### Questions

Reads go through `karea_read`; changes through `karea_meetings_write`; deletes through `karea_delete`.


| Action | Use for |
|---|---|
| `karea_create_question` | Create an open question on a project. Accepts an optional `markdown` body (long-form context) and `taskIds` to pre-link tasks (visual IDs or UUIDs). Pass `meeting` (a meeting UUID, or words of its title: `"daily"` means today's occurrence in the user's time zone; `meetingDate` / `meetingTime` narrow it) to put the question on that meeting in the same call: when the user already named the meeting, do not ask which one; when they did not, ask before creating it (the next few upcoming meetings from `karea_list_meetings` plus "No meeting"). If they did not say which project and it is not clear from the task at hand, ask that too instead of picking one. An ambiguous name creates nothing and lists the candidates. |
| `karea_edit_question` | Update a question. Editable: `question`, `answer`, `status` (`open` / `answered` / `cancelled`), `markdown`. Link tasks with `taskIdsAdd`, unlink with `taskIdsRemove` (visual IDs like `KA12` or UUIDs). |
| `karea_answer_question` | Answer a question (also flips status to `answered`). Accepts the question's short ID (e.g. `KAQ3`) or UUID. |
| `karea_edit_question` / `karea_delete_question` | Edit or delete a question by its short ID (e.g. `KAQ3`) or UUID. |
| `karea_list_questions` | List questions. Needs at least one filter: `projectId`, `status` (`open`, `answered`, `cancelled`, or `all`), `task` (a task's visual ID or UUID) or `search`; filters combine. Each question has a static short ID (`<prefix>Q<seq>`, e.g. `KAQ3`) you can reference from anywhere. |

### Resources

Reads go through `karea_read`; changes through `karea_resources_write`; deletes and unlinks through `karea_delete`.

Every resource response (`karea_create_resource`, `karea_upload_resource`, `karea_update_resource`, `karea_get_resource`, `karea_list_resources`) gives its deep link, `Link: https://karea.app/dashboard/resources?open=<id>`, and a ready `Markdown link: [name](...)`. Paste that Markdown link wherever you mention the resource (notes, descriptions, Context, markdown); a bare id is not clickable.


| Action | Use for |
|---|---|
| `karea_create_resource` | Create a text resource. Accepts `name`, `content`, optional `folder`. Put a file extension in the name (`notes.md`, `data.csv`): it is the resource's only format, so `.md` renders as Markdown and `.csv` as a table, and a name without one is plain text with no format. |
| `karea_upload_resource` | Upload a file as a resource. Pass exactly one of: `path` (local karea-mcp only: the file is read from disk, up to your plan's file size; use it for anything bigger than a few hundred KB), `data` (base64, small files only) or `link: true` (returns a 15-minute upload URL and the `curl` command to run; use it with the hosted connector, which cannot read your disk). Optional `name` (defaults to the file's own name with `path`), `mimeType`, `folder`, and `task` to link it to a task on upload. Give the name an extension (`spec.pdf`, `notes.md`): without `mimeType` the type is taken from it. With no extension (or an unknown one) the file is stored as `application/octet-stream`, with no format and no preview. |
| `karea_get_resource` | Get a resource's full metadata + content by UUID. Text comes back inline, images as an image you can look at, other files (PDF, docs) as base64 with their MIME type; above 8 MB you get metadata and a download URL instead. |
| `karea_update_resource` | Update a resource. Editable: `name`, `content` (text resources only), `folder`. `content` **replaces** the text, it does not append: read it first with `karea_get_resource` if you are adding to it. A rename should keep the extension, or the resource loses its format. |
| `karea_delete_resource` | Delete a resource (needs the resource UUID). |
| `karea_link_resource_to_task` / `karea_unlink_resource_from_task` | Link or unlink an existing resource to/from a task (one task per call). Unlinking keeps both. |
| `karea_list_resources` | List resources. Needs at least one filter (`projectId`, `query`, `folder`, `type`, `mime`, `minSize`, `maxSize`). With a `projectId` it returns every resource in that project -- assigned to it, linked to one of its tasks, or filed under a folder named after the project (e.g. knowledge-base docs). Without `projectId` the other filters search all your resources, including unfiled ones. Output includes size, MIME, folder, and linked tasks. |

### Reminders (KA422)

Reads go through `karea_read`; changes through `karea_meetings_write`.


Reminders on a task, a meeting or an open question. When a reminder fires, Karea shows a full-screen in-app modal to the user and (optionally) emails them. The MCP surfaces reminders in two ways:

1. **Auto-nudge:** every `karea` / `mcp__karea__*` tool response automatically appends a `⏰ Pending reminders:` block if the caller has any past-due or currently-firing reminders. No polling needed - the very next tool call surfaces them.
2. **Dedicated tools:**

| Action | Use for |
|---|---|
| `karea_check_reminders` | List the caller's pending reminders (no filter needed). Optional `taskId` filter; `includeDone` needs `taskId`. Useful before doing focused work so you know what will interrupt. |
| `karea_create_reminder` | Schedule a reminder on a task (`task`: visual ID like `KA12` or UUID) or an open question (`question`: short ID like `KAQ12` or UUID); pass exactly one. `fireAt` accepts ISO datetime or friendly forms like `2h`, `3d`, `tomorrow 9am`. Optional `title` (falls back to the task title or the question text), `repeat` (`daily` / `weekly` / `monthly`), `emailOptIn` (bool, default false - in-app modal is always on). |
| `karea_snooze_reminder` | Snooze by N minutes. |
| `karea_dismiss_reminder` | Cancel a reminder - it will not fire again. |
| `karea_mark_reminder_done` | Fulfill a reminder AND close the underlying task (status = done). A reminder on a meeting or a question is just closed. |

When you see the `⏰ Pending reminders:` footer, decide with the user before dismissing anything. Snoozing (`+15m`, `+1h`, `tomorrow`) is the safe default when the user is busy.

### Meetings

Reads go through `karea_read`; changes through `karea_meetings_write`; deletes and unlinks through `karea_delete`.

A meeting is a calendar event the user prepares for: it carries prep notes, an
agenda of linked tasks, open questions to raise, and afterwards a transcript.
Meetings belong to the **user**, not to a project, because a person's calendar
spans projects - `projectId` is an optional filing, not ownership.

| Action | Use for |
|---|---|
| `karea_list_meetings` | What is coming up, or what already happened. Needs at least one filter: `scope` (`upcoming` / `past`), `projectId`, or a `from` / `to` date range. |
| `karea_view_meeting` | One meeting in full: attendees, notes, linked tasks and questions, transcript. |
| `karea_create_meeting` | Schedule one. `startAt` / `endAt` are ISO datetimes. |
| `karea_edit_meeting` | Change the facts, or paste a transcript after the fact. |
| `karea_delete_meeting` | Destructive. Confirm first. |
| `karea_link_task_to_meeting` / `karea_unlink_task_from_meeting` | Put a task on the agenda, or take it off. Unlinking keeps both. |
| `karea_link_question_to_meeting` / `karea_unlink_question_from_meeting` | Same, for an open question the user wants to raise there (short ID like `KAQ3` or UUID). Linking a question also links its tasks to the meeting; linking a task never brings its questions. Unlinking does not cascade. |

Meeting times are printed in the user's time zone with its name (`2026-11-18 09:30 Europe/Madrid`): repeat them as they are, never convert them.

Two things worth knowing when you read a meeting back:

- **It may repeat (KA506).** A recurring meeting is a series master carrying the
  rule plus real occurrence rows pointing at it. Editing the schedule of a
  master affects future occurrences and is destructive, so it is a decision for
  the user, not for you.
- **It may have a join link (KA512).** Meet / Zoom / Teams URLs are stored apart
  from `location`, which stays free text for rooms.

### Sticky notes

Reads go through `karea_read`; changes through `karea_notes_write`, alongside the task notes; deletes through `karea_delete`.

The scratch layer: no status, no assignee, no deadline, nothing to close. A
command the user keeps re-typing, a URL they need for the next twenty minutes,
three bullets before a call. **If it has a lifecycle, it is a task** - reach for
`karea_create_task` instead. The board caps at 100.

| Action | Use for |
|---|---|
| `karea_list_sticky_notes` | Read the board. Needs `projectId` (that project's notes plus the global ones) or `scope` (`global` / `all`). |
| `karea_create_sticky_note` | Jot something down. `content` is the body; `title` is very short (60 chars). Optional `color` and `projectId`. |
| `karea_edit_sticky_note` | Change the text, colour, pin state, or which project it belongs to. |
| `karea_delete_sticky_note` | Destructive and irreversible - there is no trash. Confirm unless the user asked for that note to go. |

A note is **global** by default and follows the user everywhere; give it a
`projectId` and it only appears inside that project. Markdown works in the body,
and `@resource` mentions plus bare task IDs like `KA123` become links.

### AI Sessions

Reads go through `karea_read`; links through `karea_resources_write`; unlinks through `karea_delete`.


Link your current AI coding session (Claude Code, OpenCode, Codex, Cursor, Aider) to a task so the user can see the history and copy a resume command later.

| Action | Use for |
|---|---|
| `karea_link_session` | Link the current session: `task`, `provider` (`claude-code` / `opencode` / `codex` / `cursor` / `aider` / `other`), `sessionId`, optional `label`. Call this automatically as soon as the user names the task they're working on (see "Session linking" below). Re-linking the same session refreshes its last-active stamp. Inside a Karea Connect session (Claude Code started from Karea), the id is recognised and the Connect session itself is linked to the task, so it shows on the task and on the Connect page. |
| `karea_list_sessions` | List AI sessions linked to a task (provider, session id, last active, row id). |
| `karea_unlink_session` | Remove a linked session by its row id (from `karea_list_sessions`). |

### JIRA

Reads go through `karea_read`; links through `karea_resources_write`; unlinks through `karea_delete`.


| Action | Use for |
|---|---|
| `karea_get_jira_link` | Get the JIRA link for a task. |
| `karea_link_jira` | Link a task to a JIRA issue by key (e.g. PROJ-123). |
| `karea_unlink_jira` | Remove the JIRA link from a task. |

### Projects & Categories

Reads go through `karea_read`; changes through `karea_projects_write`; deletes through `karea_delete`.


| Action | Use for |
|---|---|
| `karea_list_projects` | List the user's projects with IDs and category summary. |
| `karea_create_project` / `karea_delete_project` | Project management. |
| `karea_share_project` | Share a project with another user by email. `role` is one of `owner`, `editor`, `viewer` (default: `editor`). |
| `karea_create_category` | Create a category in a project. |
| `karea_delete_category` | Delete a category **and every task in it** (cascade). Requires `confirm: true`. Move tasks out first if they should survive. |

### Other

`karea_recap` goes through `karea_read`; `karea_ask` through `karea_assistant`.


| Action | Use for |
|---|---|
| `karea_recap` | Recent activity summary over a time window (`hours`, default 24). Returns sections: DONE, QUICK TASKS, IN PROGRESS, BLOCKED, DUE TODAY, OPEN QUESTIONS. |
| `karea_ask` | Natural-language request routed through Karea's AI (the same engine the in-app chat uses). It can do most of what the actions above do, meetings, reminders and sticky notes included, and always asks before sharing a project. It counts against the user's monthly AI allowance, so prefer the direct actions when you know what to call. |

## Referencing other items in notes and descriptions

A note, a task description or a sticky note can point at another task, open
question, meeting or resource. Write the reference in this exact form and the
user sees a pill with a hover preview; a bare name is just text.

| Kind | Write | Where the id comes from |
|---|---|---|
| Task | `[[KA12]]` (any project) | the task's Short ID |
| Open question | `[KAQ3](https://karea.app/dashboard/questions?open=<question UUID>)` | `ID:` line of `karea_list_questions` / `karea_create_question` |
| Meeting | `[Weekly sync](https://karea.app/dashboard/meetings?open=<meeting UUID>)` | `id` from `karea_list_meetings` / `karea_view_meeting` |
| Resource | `[spec.md](https://karea.app/dashboard/resources?open=<resource UUID>)` | `ID:` line of `karea_list_resources` / `karea_create_resource` |

Questions, meetings and resources need the **UUID** in the link: their preview
is looked up by id. `[[KAQ3]]` is read as a task ID and links nowhere, and a
resource named with `@spec.md` or `[[resource:spec.md]]` shows a pill but no
preview. A bare `KA12` links only when it is in the same project as the task
it is written on; `[[KA12]]` works everywhere.

```
karea_notes_write { action: "karea_add_note", params: { task: "KA40", content: "Blocked on [[KA12]]; raised as [KAQ3](https://karea.app/dashboard/questions?open=3efdb184-...) at [Weekly sync](https://karea.app/dashboard/meetings?open=223c57bd-...). Spec: [spec.md](https://karea.app/dashboard/resources?open=41a3e537-...)." } }
```

## Output the tools return

Every mutation or single-record lookup ends with a small footer the user expects you to surface verbatim:

```
ID: <uuid>
Short ID: <visual id, e.g. KA231>          # only on tasks
Link: https://karea.app/dashboard/task/<uuid>
```

When you report back to the user, **include the Link** so they can click straight through. Don't replace it with the raw UUID and don't strip it.

## Conventions the user expects

- **Task IDs**: prefer per-project IDs like `HA123` when the project has a prefix, else the short visual ID like `C1` / `T2`. Never paste a UUID to the user unless they ask.
- **Status values**: `open`, `in_progress` ("Doing"), `blocked`, `review`, `backlog`, `done`, `cancelled`. When the user says "doing" they mean `in_progress`; when they say "review" they mean `review`.
- **Priority**: `1` = critical, `5` = minor. Default is `3`.
- **SLA shortcuts** (user's timezone): `2d`, `5h`, `30m`, `1w`, `today` (18:00), `tomorrow` / `monday` (09:00), a day with a time (`today 13:30`, `tomorrow 9:00`, `friday at 17:00`), a time alone (`13:30`), or a date (`2026-10-20 13:30`).
- **Projects** (`projectId`): a UUID, the exact name, the prefix (`KA`), one part of a `/` name (`Mobile` for `Acme/Mobile`), or a unique piece of the name. Several matches or none is an error that lists the candidates: pick one and retry, never guess.
- **Review stages**: a task in `review` also carries a **stage** saying who is holding it -- by default `Developer review`, `Peer review`, `Client review`, and each project can define its own. Set it with `reviewStage` on `karea_edit_task`; passing one moves the task into Review if it is not there already. Moving a task into `review` without naming a stage gives it the project's first stage, whichever way the change is made (edit, bulk edit, chat, app); moving it out clears the stage. Projects can turn the feature off, in which case `reviewStage` is rejected. `karea_view_task` shows it as `review: peer review`.

## Bulk first

When the same operation applies to more than one record, there is a bulk action for it. **Use it.**

| Instead of | Call |
|---|---|
| `karea_edit_task` N times | `karea_tasks_write { action: "karea_edit_tasks", params: { tasks: [...], status: "done" } }` |
| `karea_close_task` N times | `karea_tasks_write { action: "karea_done", params: { tasks: [...] } }` |
| `karea_view_task` N times | `karea_read { action: "karea_view_tasks", params: { tasks: [...] } }` -- max 50 |
| `karea_add_note` N times, same text | `karea_notes_write { action: "karea_add_note", params: { tasks: [...], content } }` |

Each of these is one HTTP request and one database transaction. The looped version is N requests against a **60 per minute** rate limiter, and it trips at about eight. The only reason to loop is when each record needs a *different* value.

## Session linking -- do this automatically

When the user says they are working on a specific Karea task ("working on KA123", "let's do HA42", "pick up the flares bug"), do BOTH of these immediately, without being asked:

1. **Link the session**: call `karea_resources_write` with action `karea_link_session` and the current session id (`provider: "claude-code"`, the id Claude Code reports for `claude --resume`) and a short label describing the work. Re-linking the same session later is safe -- it just refreshes the "last active" stamp. Alternatively, every task-referencing tool (`karea_create_task`, `karea_edit_task`, `karea_close_task`, `karea_quick_task`, `karea_doing`, `karea_set_markdown`, `karea_set_context`, `karea_add_note`, `karea_edit_note`, `karea_create_subtask`) also accepts the same session fields inline (`aiSessionId`, `toolType`, `sessionLabel`) so a plan/note/status-change can link the session in one call.
2. **Set it in progress** (if you are starting work now): `karea_tasks_write { action: "karea_edit_task", params: { task, status: "in_progress" } }`.
3. **Read the Context**: `karea_read { action: "karea_get_context", params: { task } }` before doing anything else, so you resume with full memory instead of re-deriving it.

## Context discipline -- keep it current, automatically

Context tracks the **full history** of a task -- what was tried, decided, discovered, and abandoned along the way -- NOT just its current state. Treat it as the DEFAULT place to persist what you learn, and update it **incrementally** so the journey is preserved:

- After making a **plan** -> `karea_notes_write { action: "karea_set_context", params: { task, title: "Plan", context: ... } }`.
- After a significant **finding, root cause, or discovery** -> read + append to the `Findings` entry.
- After a **decision** (approach chosen, trade-off accepted) -> read + append to the `Decisions` entry with the reasoning.
- Hit a **gotcha** worth remembering -> read + append to `Gotchas`.
- After trying and abandoning an approach -> read + append to `Attempted` so the next session doesn't retry it.
- **Titles name the topic, never a date.** Use `Plan`, `Findings`, `Decisions`, `Progress`, `Gotchas`, `Attempted`, `Loose ends`, `Scope`. Dates go inside the entry (a `### 2026-10-21` header or a dated bullet), not in the title. Before writing, look at the existing titles (`karea_get_context`) and append to the matching entry instead of creating a sibling like `Decisions 2026-10-21 follow-up`. Split only when an entry gets too big or mixes clearly different audiences, with topic sub-names (`Tech decisions`, `Business decisions`). Dated titles only when the user asks or the content is a true log (e.g. per release). `karea_set_context` warns when a new title looks like an existing one: merge into that entry.
- **Read first with `karea_get_context`, refine, write back.** Do NOT overwrite an entry with the current status -- that erases the reasoning that got you here. Same title = same entry, but its content grows as the task evolves.
- Notes, markdown, and description are still used when the user asks for them or the content is human-facing -- but Context gets updated **as well**, always.

## Tags -- use existing only

`tags` on `karea_create_task` / `karea_edit_task` / `karea_create_subtask` upserts by name, so a typo or a paraphrase creates a **duplicate** tag. Rule:

- Only pass tags that already exist in the project. Check `karea_view_task` (a similar task) or the project's tag list first.
- Do NOT invent a new tag unless the user explicitly asked for one.
- When unsure whether a tag exists, omit it and ask the user.

## How to work

1. **Read before writing.** Before editing anything non-trivial, call `karea_view_task` or `karea_list_tasks` so you see the current state.
2. **Confirm destructive actions.** `karea_delete_task`, `karea_delete_project`, `karea_delete_category` and `karea_delete_meeting` all require `confirm: true`. Ask the user for authorization before passing it, and say what will go with it: deleting a **project** takes its tasks, categories, notes and history; deleting a **category** takes **every task inside it** (the schema cascades `Task.category`), which is rarely what someone picturing "remove this label" expects -- move the tasks with `karea_edit_task` first if they should survive. Deleting a **meeting** is the exception: linked tasks and questions outlive it, only the links go.
3. **Markdown is your scratchpad.** When the user asks you to investigate a bug tied to a task, dump your findings with `karea_set_markdown`. Always read first with `karea_get_markdown` to avoid overwriting existing content.
4. **Don't invent tasks.** If the user asks about a task that doesn't resolve, say so -- don't guess at a best-match title.
5. **Notes vs Context vs Markdown -- three different things.** `karea_add_note` = a short, **human-readable** update the user reads (markdown supported). `karea_set_context` = titled entries of **AI working memory** that persist across sessions (Plan, Findings, Decisions, Gotchas) -- your default save target; keep it current proactively (see "Context discipline" above). `karea_set_markdown` = the long-form documentation/knowledge base. Human update -> note; your own cross-session memory -> context (always); long-form docs -> markdown.
6. **Questions for blockers, only with a yes.** Use `karea_create_question` when the user asks for an open question. If you think one is needed, quote its exact text in chat and ask first; create it only after they agree. Never create one on your own initiative. Before creating it, ask which meeting to put it on (unless they named one) and which project (unless it is clear); never guess either.

## Example flows

Every call below is `<tool> { action, params }`: the tool is what you call
(`mcp__karea__karea_tasks_write` in Claude Code), the action goes in `action`.

**"Add a bug: flares broken on external monitor. P2, due tomorrow at 13:30."**
```
karea_tasks_write { action: "karea_create_task", params: { name: "Flares broken on external monitor", category: "Bugs", priority: 2, sla: "tomorrow 13:30" } }
```

**"Mark HA42 as doing, note: started on the regex."**
```
karea_tasks_write { action: "karea_edit_task", params: { task: "HA42", status: "in_progress", note: "Started on the regex." } }
```

**"Tag HA42 as bug + urgent and link it to JIRA PROJ-101."**
```
karea_tasks_write { action: "karea_edit_task", params: { task: "HA42", tags: ["bug", "urgent"], jiraIssueKey: "PROJ-101" } }
```

**"Dump what we found about HA123 to its markdown."**
```
karea_read { action: "karea_get_markdown", params: { task: "HA123" } }
karea_notes_write { action: "karea_set_markdown", params: { task: "HA123", markdown: "# Root cause\n\n...\n\n# Fix\n\n..." } }
```

**"Weekly recap."**
```
karea_read { action: "karea_recap", params: { hours: 168 } }
```

**"Add a note to HA42: deployed the fix to staging."**
```
karea_notes_write { action: "karea_add_note", params: { task: "HA42", content: "Deployed the fix to staging." } }
```

**"What open questions do we have?"**
```
karea_read { action: "karea_list_questions", params: { status: "open" } }
```

**"Re-read HA42 before going on."** (one batch, all through `karea_read`)
```
karea_read { action: "karea_get_context", params: { task: "HA42" } }
karea_read { action: "karea_list_notes", params: { task: "HA42" } }
karea_read { action: "karea_list_questions", params: { projectId: "HA", status: "open" } }
```
