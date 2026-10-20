---
description: Show every file the OS changed this session. Say "what did you change" or "show me this session's changes" (or run /founder-os:changes). Lists action, change size, and a one-command restore per file. Works with or without git - this is the visibility half of the session-changes tracker, and the whole undo surface on a ZIP install before "own my history".
---

# Changes - what did this session touch

Print the per-session change manifest: every file written this session, what happened to it, and how to put any of them back.

## Procedure

1. Run:

   ```
   python scripts/session_changes.py --print
   ```

   (Use `python3` where `python` is not found.)

2. Print the output verbatim. No commentary, no reformatting. The manifest is the artifact.

3. If it prints `No session changes recorded yet.`, print that and stop.

## How this works (context, not steps)

- A PreToolUse hook snapshots each file's pre-edit bytes on the FIRST touch per session, into `state/.snapshots/<session>/`, and logs every write to `state/.session-changes/<session>.jsonl`.
- A Stop hook renders `state/session-manifest.md` at session end. This command re-renders the most recent session's manifest on demand, so mid-session it reflects the session so far.
- Restore any modified file to its pre-session state:

  ```
  python scripts/session_changes.py --restore <path> --session <sid>
  ```

  The manifest prints the exact command per file. A file created this session has no snapshot - delete it to undo.
- None of this needs git. On a git-full install it runs as a second net under save/history/restore.

## Rules

- Read-only apart from the tracker's own runtime state under `state/`.
- No other skills.
- No em dashes or en dashes. Hyphens only.
