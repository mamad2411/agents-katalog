---
name: note-first
description: |
  Saves the last assistant message as a note attached to the current task.
  Auto-numbered (note-01, note-02...), bidirectional link with task.md.
  Invoked manually by the user.

  Use when: "/note-first", "save a note", "remember this",
  "save the last message"
---

# Note-First Protocol

Saves the last Claude message as a note attached to the current task.

## Input

The user's request to save the agent's most recent chat message; the current task context.

## Output

`note-{NN}.md` with two-way links (task.md ↔ note file), auto-numbered.

## Hands off to

— (terminal).

---

## Step 0 — Task context

Ensure `{log_dir}` and `{slug}` are known. Otherwise resolve from the latest task log folder.

Cannot skip — without `{log_dir}` the note has nowhere to go.

---

## Step 1 — Capture the last message

Take the assistant message that comes **immediately before** the `/note-first` command.

Rules:
- Copy verbatim — no abbreviations, no rephrasing
- If no previous assistant message exists → tell the user, finish

---

## Step 2 — Determine note number

```bash
ls {log_dir}/note-*.md 2>/dev/null | sort | tail -1
```

- No files → `note-01.md`
- `note-02.md` exists → write `note-03.md`

---

## Step 3 — Write file + update task.md

### Write the note

```markdown
> 🔗 Task: tasks/log/{slug}/task.md

# Note NN

**Date:** {date}

{verbatim last assistant message}
```

### Update task.md

Add a header line after the last `> 📋` or `> 📝` line:

```
> 📝 Note N: tasks/log/{slug}/note-NN.md
```

If none exist — add as the first line of the file.

---

## Step 4 — Confirm

Report in one line:

```
📝 Saved: {log_dir}/note-NN.md
```

Nothing more — the note is already visible in the chat.

---

## Anti-patterns

### ❌ Rephrasing before saving
Copy the message verbatim. The user is saving what was actually said.

### ❌ Writing the file but not updating task.md
Both actions in Step 3 are mandatory. Otherwise the note is orphaned.

### ❌ Saving the user's own message
The `/note-first` command is not the content. Save the previous assistant reply.

### ❌ Imitating the skill inline
Always via `$note-first`. Never copy the protocol from memory — outdated versions drift silently.

---

## Related skills

- **decision-first** — saves an architectural decision (structured, not free-form)
- **plan-first** — plans execution steps (before code, not after)
