---
name: create-memory
description: The user wants something kept across tasks, such as who they are, a lasting preference, a fact about their setup or a mistake not to repeat, or a saved memory changed or forgotten. Not for this task only, procedures, secrets or project memory files.
---

You help the user save something the agent should remember across tasks, or correct or forget a
memory that is already saved.

A memory has these parts. Work them out from the conversation, asking only for what is missing:

1. **body** — the memory itself: one stable fact, preference or correction, written so it still
   makes sense in a future task with no context. Keep the user's meaning; do not add details they
   did not give.
2. **description** — one line saying what the memory holds and when it applies. The agent sees
   descriptions in its memory index and reads a body only when the description matches the task,
   and the index shows only the first 250 characters, so make it specific and keep it within
   them; the tools refuse more than 300.
3. **type** — what kind of memory it is:
   - `user` — who the user is: role, language, background, how they like answers.
   - `memory` — a lasting preference, convention, or fact about their tools and environment.
   - `failure` — a correction: something the agent got wrong and what to do instead. It may also
     take a **category**: `failure`, `correction`, `insight`, `preference`, `convention` or
     `tool-quirk`.
4. **name** — optional: lowercase words joined by hyphens, such as `prefers-pnpm`. Without one, a
   name is derived from the description.
5. **activation** — optional. Leave it out unless the user wants the memory applied to every task;
   then ask for `core`. Only the user decides what every task includes: the memory is saved to the
   index, and a suggestion to include it in every task waits for them in Settings → Memory, so tell
   them it is there. Taking a memory out of every task is likewise theirs to do in Settings. `search`
   keeps a memory out of the index, so only a search finds it.

Before writing, call `memory_search` with the key terms to find a memory that already covers the
same subject, and read a candidate with `memory_read` when its description is not enough to tell.

- If one does, change it with `memory_replace`, naming it and passing only the fields that change
  (`description`, `body` or `activation`). Do not add a second memory about the same thing.
- If the user asks to forget something, find it the same way and call `memory_remove` with its
  name.
- Otherwise call `memory_add` with the parts above.

The memory tools save at once, without asking the user. When the user gave the wording, or asked
plainly to forget a memory, write without asking. Otherwise ask once with the `ask_user` tool: the
question shows the name, type, description and body you will save, briefly, and the `options` are
short answers such as saving it as written, changing the wording, or not saving it, the first one
recommended. Save on the first, ask what to change on the second, and write nothing on the third
or when the user skips the question. After a write, report in one line what was saved, changed or
forgotten, with the memory's name.

Only save what the user wants kept long term. Decline one-off task instructions, file contents,
and secrets such as passwords, tokens, or keys; suggest where they belong instead. A multi-step
procedure, such as how a project is released, belongs in a skill rather than in memory: offer to
create one with the create-skill skill. When it is genuinely unclear whether the user means a
statement to last beyond this task, or whether it is a procedure that belongs in a skill, settle
that in the same `ask_user` question, with options such as remembering it for later tasks,
using it only in this task, or saving it as a skill; otherwise do not ask whether to save.

Use only the memory tools; never edit memory files on disk. If a write is refused because
automatic learning is paused, say so and ask the user to resume learning in Settings → Memory, or
to edit their memories there directly.
