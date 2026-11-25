---
name: kindergarten-detach
description: Pull the current conversation OUT of the AgentKindergarten classroom and continue it in a plain local terminal. Use when the user says "detach", "take this out of the kindergarten/classroom", "back to a normal terminal", or wants this conversation to stop being streamed to the relay. The inverse of /kindergarten-mirror and /kindergarten-join.
---

# Pull this conversation out of the classroom

Goal: this conversation stops being a classroom student (nothing about it is streamed
to the relay anymore) and the user continues it in a plain local `claude` — same
history, no daemon in the loop. Closing the student **kills the running claude
process** (very possibly the one executing this skill), so the resume instructions
must be printed BEFORE the close, and the close must be the last action.

## Steps

1. **Find this conversation's session id** (needed for the resume command).
   Claude Code stores the transcript at `~/.claude/projects/<munged-cwd>/<session-id>.jsonl`,
   where `<munged-cwd>` is the absolute project path with every character that is not
   a letter or digit replaced by `-`. The current conversation is the **most recently
   modified** `.jsonl` in that folder.

   PowerShell:
   ```powershell
   $proj = (Get-Location).Path -replace '[^A-Za-z0-9]', '-'
   Get-ChildItem "$env:USERPROFILE\.claude\projects\$proj\*.jsonl" |
     Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty BaseName
   ```
   bash:
   ```bash
   proj=$(pwd | sed 's/[^A-Za-z0-9]/-/g')
   ls -t ~/.claude/projects/$proj/*.jsonl | head -1 | xargs -n1 basename | sed 's/\.jsonl$//'
   ```

2. **Identify the classroom student hosting this conversation:** run `agk ls`
   (rows are `sessionId  status  name  cmd`). In order of confidence: a running
   student whose `name` is this project's folder name, else a running student whose
   `cmd` starts with `claude`. If it is ambiguous, show the rows and ask the user —
   closing the wrong student kills someone else's session.

   If `agk ls` shows no matching student, this conversation is not in the classroom;
   say so and stop.

3. **Print the resume instructions FIRST** — they must be on screen before anything
   is killed. Tell the user, literally:

   > This conversation is leaving the classroom. To continue it locally, open any
   > terminal and run:
   >
   > `cd <project-dir>`
   > `claude --resume <session-id>`
   >
   > (`claude -c` also works if this was the folder's most recent conversation.)
   > The classroom tile will disappear in a moment — that is expected.

4. **Close the student — the final action:**
   ```
   agk close <sessionId-or-name>
   ```
   If this conversation itself was running inside that student, the process dies
   right here and no further output appears — that is the intended behavior. The
   transcript is already safe on disk and resumable.

## Notes

- `agk close` removes the tile from the classroom; the conversation history lives in
  `~/.claude` and is untouched.
- If the user only wants to stop *watching* remotely but keep the student alive,
  that is not a detach — just close the browser tab instead.
