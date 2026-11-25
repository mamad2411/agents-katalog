---
name: context-management
description: Keeps long agent sessions on track with a running notes file, checkpoints and tightly scoped reads, so quality does not fade as the context fills.
---

# Context management

Put facts on disk, read narrowly, and checkpoint often.

## Steps

1. At the start, create `.agent/notes.md` (add it to `.git/info/exclude` so it is not committed). Write four headings: Goal, Decisions, Done, Next. Fill Goal in the user's words plus the done check.
2. Read narrowly. Search for the symbol or string first, then read only that function or the lines around it. Open a whole file only when you are about to edit most of it. Use `wc -l` before opening anything unfamiliar.
3. Summarize large outputs. For test runs, build logs and diffs, keep the failing lines and counts, not the whole text. Redirect long output to a file and grep it.
4. Record decisions the moment they are made, with the reason: "use the existing retry helper in src/net.ts, because it handles 429". Record failed approaches with the cause, so they are not tried again.
5. Checkpoint after each completed step: update Done and Next, run the relevant tests, and commit when the user wants commits. A checkpoint is safe to resume from.
6. Delegate noisy side work, such as scanning many files, to a subagent and take back only its conclusion.
7. Watch for drift: if you are about to repeat a command, reread the notes first. If the same problem fails twice, stop, write what you know, and propose a different approach.
8. When the session ends or grows heavy, write a handoff block in the notes: current state, exact next command, open questions, and files in flight.

## Rules

- Never paste secrets into the notes.
- Keep the notes under 80 lines. Prune what is no longer true.
- The notes file records facts, not plans you have not decided on.

## Report

At each checkpoint, one line on what is done and what is next.
