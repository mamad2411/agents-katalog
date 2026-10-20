---
description: Report what changed since the last time this command ran. Say "what changed since last session", "what did I miss", "catch me up", or run /founder-os:since-last-session. Reads the marker at brain/.last-session and reports five things: hours elapsed, brain/log.md entries added, flags decayed, commitments now overdue, and files modified in context/. Updates the marker at the end. First run prints a one-line note and seeds the marker.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Founder OS since last session

Run the since-last-session skill at `skills/since-last-session/SKILL.md` end to end. No arguments.

## Procedure

1. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
2. If `skills/since-last-session/SKILL.md` is missing, reply `since-last-session skill not found at skills/since-last-session/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
3. If `brain/` does not exist, reply `brain/ folder missing. Say "set up Founder OS" to build it.` and stop.
4. Follow the since-last-session skill instructions exactly.
   - If `brain/.last-session` is missing: print the seed message, write the marker, stop. No delta on the first run.
   - If `brain/.last-session` is present: read it, compute elapsed time, render the 5-section report, then overwrite the marker with the current ISO-8601 timestamp.
5. Output the structured block defined in the skill. Nothing before, nothing after the fenced block, except the one-line `Marker advanced to ...` confirmation outside the fence.

## When to use

- Returning to the OS after a gap and you want the delta, not the full read.
- Before any planning work, so the report scopes to what shifted while you were away.
- After a parallel session ran on another machine and you want a quick "what is new on disk".

## When NOT to use

- Full state-of-the-OS orientation. Use `/founder-os:strategic-read` for the 5-section read across the brain.
- A single-topic question. Use `/founder-os:brain-pass "<question>"` or `/founder-os:query "<keyword>"`.

## Examples

- `/founder-os:since-last-session`
- "what changed since last session"
- "catch me up since I was last here"

## Rules

- The skill reads the file layer and writes only to `brain/.last-session`. No other file is modified.
- No external dependencies. No paid API. Git is used only to list filenames; the skill runs without git if the install is not a repo.
- No em dashes or en dashes. Hyphens only with spaces.
- No banned words per `rules/writing-style.md` or its template fallback.
- The five section headers are a contract. Keep them verbatim.
- First run seeds the marker only. Subsequent runs report the delta.
