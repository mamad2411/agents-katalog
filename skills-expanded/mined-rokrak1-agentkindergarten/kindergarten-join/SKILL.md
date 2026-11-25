---
name: kindergarten-join
description: Hand the current Claude Code conversation off to the AgentKindergarten classroom (phone/web only, no local terminal). Use when the user says "join the classroom", "send this to my phone", "I'm leaving, put this in the kindergarten", or wants to walk away from this PC and keep the conversation going remotely. Optional argument, a student name.
---

# Hand this conversation off to the classroom

Goal: this exact conversation continues as a classroom **student** — a daemon-owned
PTY running `claude --resume <this-conversation>` — watchable and drivable from the
web UI and phone. Unlike `/kindergarten-mirror`, no local terminal is opened: this is
the "I'm walking away from the PC" move. The copy you are executing in right now goes
stale the moment the student is born, so say goodbye first, enroll last.

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
   *before* the enroll is part of the history the student resumes, everything after is
   not. Tell the user:
   - the conversation is moving to the classroom as `<name>` — open the relay URL in
     any browser or the phone PWA and it is under 🧒 Students;
   - **this** terminal's copy is now frozen history — do not type here anymore;
   - to pull it back into a local terminal later: `agk attach "<name>"`, or
     `/kindergarten-detach` from the classroom side.

5. **Enroll — the final tool call of this conversation:**
   ```
   agk run "claude --resume <session-id>" --name "<name>"
   ```

## Notes

- `agk run` talks to the daemon's local loopback API, so this works even on daemons
  hardened with `--lock-commands` (that policy only gates commands arriving from the
  relay).
- If a student with that name already exists, pick a different name or suggest
  `agk close <name>` first.
