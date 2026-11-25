---
name: context-save
description: "Write a short session brief to the notes tree so the same work resumes after compaction, commit it, then point OptMem at it. Manual: /context-save at milestones or before manual compaction."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Context Save

**Goal**: leave enough on disk that the next window resumes this work without retrying dead ends.

**Success means**: the brief exists with the six sections below, is committed in the notes tree, and one OptMem pointer names it.

**Stop when**: the file is written and committed and the pointer is appended (or the session has no entity to scope it to).

## Write the save

Take the session id from the `SESSION SCOPE: @s/<id>` line of the SessionStart wake output. The brief lives in the notes tree, among the agent run notes: `$NOTES_ROOT/mycelium/<YYYY-MM-DD>-<agent>-<id>-brief.md`, where `<agent>` is `claude` or `codex` and the date is today's on the first save. If a file matching `*-<id>-brief.md` already exists there, rewrite that file; a session has one brief, and the compaction hooks find it by the id. (Briefs moved there from an older, now frozen state directory on 2026-11-10; older briefs stay readable where they were.) Write it with these sections and nothing else:

- **Goal** — what this session is for.
- **State** — done / in flight / blocked.
- **Decisions** — each with its reason.
- **Next moves**.
- **Read on resume** — paths, one phrase of cue each.
- **Gotchas learned this session**.

Keep it short: the compaction hook inlines only the first `COMPACTION_SAVE_CHARS` characters. Point at durable documents by path instead of copying them; OptMem, specs, and git survive compaction untouched. Keep secrets out. Merge over an existing brief for this session rather than starting fresh.

## Commit it

```bash
git -C "$NOTES_ROOT" add -- mycelium/<file> && git -C "$NOTES_ROOT" commit --only -m "Save session brief <id>" -- mycelium/<file>
```

`--only` commits that one file and leaves whatever else is staged or modified in the notes tree alone. The push rides with the tree's next push.

## Point OptMem at it

Append one pointer per entity the session worked (usually one), skipping it when the session has no entity:

```text
P @e/<entity> @s/<id> @k/context-save <absolute path> | <why this save matters>
```

Pass it as one shell-quoted argument to `$MEMO_CMD note '<line>'`. The whole line must fit 280 UTF-8 bytes; shorten the why, never the path. Configure these interfaces in [config.example](../config.example).

Report the save path in one line.
