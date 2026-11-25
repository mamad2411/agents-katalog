---
name: capturing-meeting-actions
description: Extracts action items from meeting notes, transcripts, or a brain dump and creates them as owned, dated tasks in Astravue. Use when the user pastes meeting notes or a transcript, asks to turn notes or standup discussion into tasks, capture action items, or "make tasks out of this".
---

# Capturing Meeting Actions

Converts unstructured discussion into structured, traceable tasks. Every action item should end up with an owner, a due date, and a link back to where it came from — that traceability is what makes the output trustworthy.

## Workflow

1. **Read the source and extract candidate actions**

   Pull every commitment, decision-with-follow-up, and "someone should…" out of the notes. For each, capture:
   - A clear task title (imperative: "Send the revised quote to Acme")
   - The owner named or implied in the text
   - A due date if stated or inferable ("by Friday", "before launch")
   - The source line, so the task traces back to the discussion

   Ignore pure status updates and discussion that produced no commitment.

2. **Resolve owners to workspace members**

   For each named owner, resolve to a real member with `astravue_get_member_by_email` (if an email is given) or `astravue_get_workspace_members` (to match by name). Flag any owner you can't resolve rather than guessing.

3. **Pick the target project**

   Confirm which project the tasks belong to. Use `astravue_list_projects` if unclear.

4. **Present the action list and confirm**

   Show a table: title | owner | due date | source. Mark rows missing an owner or due date so the user can fill them. Ask for approval before creating anything.

5. **Create after approval**

   - `astravue_bulk_create_tasks` — create the confirmed action items in one call
   - `astravue_add_task_comment` — optionally attach the source line as a comment for context

   Report which tasks were created, and re-list any items that were skipped because they lacked an owner or due date.

## Important

- Every action item needs an owner and a due date — flag the ones that don't rather than creating orphan tasks.
- Resolve owners against real members; never assign to an unverified name.
- Don't invent due dates the notes don't support — leave them empty and flag instead.
- Capture commitments, not status chatter.
