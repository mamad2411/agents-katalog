---
name: dummyindex-remember
description: "Save a session handoff into dummyindex's `.context/session-memory/` store. Use at session end, before context loss, or when the user says save the session, remember this, `/dummyindex-remember`, or `$dummyindex-remember`. Appends a first-person summary to `now.md`, rolls `now` to `recent` to `archive`, and promotes durable facts to `core-memories.md`."
---

# /dummyindex-remember / $dummyindex-remember — save the session into `.context/session-memory/`

> Installed from dummyindex `__VERSION__`.

Write a handoff so the next session continues cleanly. You were here — write in the first person ("I").

## Steps

1. **Locate the store** at `<repo>/.context/session-memory/`. If it's missing, create it:
   ```bash
   dummyindex context memory init
   ```

2. **Read `now.md`** (`<repo>/.context/session-memory/now.md`). A 1-line read is
   enough to preserve the existing handoff before editing it.

3. **Prepend one entry** to the TOP of `now.md` (newest first), dated so the roller can bucket it:
   ```
   ## YYYY-MM-DD HH:MM | <branch>
   <2–4 lines: what I did, what I decided, what's next. Specific: files, PRs, branches.>
   ```

4. **Roll the tiers** (deterministic + idempotent — relocates dated entries now→recent→archive):
   ```bash
   dummyindex context memory roll
   ```

5. **Compress the rolled prose.** Read the roller's report. For each date it moved into `recent.md`,
   tighten that `## YYYY-MM-DD` section to one compact paragraph. Heavily compress anything pushed
   into `archive.md`.

6. **Promote durable facts.** Move any cross-session fact or key moment worth keeping verbatim into
   `core-memories.md` as a bullet (prefix a standout moment with `IDENTITY CANDIDATE:`).

7. Say **"Saved."** — nothing else.

## Rules

- Under ~20 lines of actual writing. Forward-looking — the next session doesn't care about the journey.
- Specific: file paths, PR numbers, branch names.
- If there's nothing meaningful to hand off, append `No active work.` to `now.md` and stop.
- Never delete prior entries; the roller relocates, it doesn't erase.
