---
name: kindergarten-mirror
description: Mirror the current Claude Code conversation into the AgentKindergarten classroom AND open a local attached terminal — phone, web, and this PC all become views of the same session. Use when the user says "mirror this", "put this conversation in the classroom/kindergarten", or wants to continue this exact conversation on their phone without losing the local terminal. Optional argument, a student name.
---

# Mirror this conversation into the classroom

Goal: this exact conversation is reborn as a classroom **student** — a daemon-owned
PTY running `claude --resume <this-conversation>` — and a fresh local terminal is
attached to it. Web, phone, and the new terminal are then three views of ONE session.
The copy you are executing in right now goes stale the moment the mirror is born, so
the order of steps below matters: say goodbye first, enroll last.

## Steps

1. **Preflight — the daemon must be up.** Run `agk ls`. If it fails with
   "daemon is not running", stop and tell the user to run `agk start`
   (or `agk init --relay <url> --token <pairing-token>` first if they have never
   configured it). Do not continue.

2. **Find this conversation's session id.** Claude Code stores the transcript at
   `~/.claude/projects/<munged-cwd>/<session-id>.jsonl`, where `<munged-cwd>` is the
   absolute project path with every character that is not a letter or digit replaced
   by `-` (e.g. `C:\dev\my-app` → `C--dev-my-app`). The current conversation is the
   **most recently modified** `.jsonl` in that folder.

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
   The basename (a UUID) is the session id. Sanity-check that the file's last lines
   mention work from this conversation before trusting it.

3. **Pick the student name.** Use the skill argument if the user gave one, otherwise
   the project folder name. Quote it if it contains spaces.

4. **Say goodbye BEFORE enrolling.** Print the handoff message now — everything said
   *before* the enroll is part of the history the mirror resumes, everything after is
   not. Tell the user:
   - the mirror is about to appear in the classroom as `<name>` and in a new local
     terminal window;
   - **this** terminal's copy is now frozen history — do not type here anymore;
   - on the phone/web, the session is under 🧒 Students.

5. **Enroll and attach — the final tool calls of this conversation:**
   ```
   agk run "claude --resume <session-id>" --name "<name>"
   ```
   then open a local terminal attached to it:
   - Windows: `start "" cmd /k agk attach "<name>"` (use `wt` new-tab syntax if the user prefers Windows Terminal)
   - macOS: `osascript -e 'tell application "Terminal" to do script "agk attach \"<name>\""'`
   - Linux: `x-terminal-emulator -e agk attach "<name>"` (or the user's terminal of choice)

## Notes

- `agk run` talks to the daemon's local loopback API, so this works even on daemons
  hardened with `--lock-commands` (that policy only gates commands arriving from the
  relay).
- The resumed student and its browser/phone/terminal viewers are all the SAME PTY —
  typing in any of them is safe. Only the pre-mirror terminal (this one) is a stale fork.
- If a student with that name already exists, pick a different name or suggest
  `agk close <name>` first.
