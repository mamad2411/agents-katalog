---
name: kindergarten-set
description: Name (or rename) the current conversation's AgentKindergarten classroom student so `agk attach <name>` and phone switching are easy. Use when the user says "call this session X", "name this student", or "rename this in the classroom". Argument, the new name.
---

# Name this conversation's classroom student

Goal: the classroom student that hosts this conversation gets a memorable label, so
`agk attach <name>` works and it is easy to find on the phone. This only makes sense
when the conversation is already enrolled (it was started with `agk claude`, or via
`/kindergarten-mirror` / `/kindergarten-join`).

## Steps

1. **A new name is required.** If the user gave no argument, ask for one.

2. **List the class:** run `agk ls`. If it fails with "daemon is not running", stop
   and tell the user to run `agk start`. Each row is
   `sessionId  status  name  cmd`.

3. **Identify this conversation's student.** In order of confidence:
   - a **running** student whose `name` equals this project's folder name
     (`agk claude` names students after the folder they started in);
   - a **running** student whose `cmd` starts with `claude` (including
     `claude --resume …`).
   If exactly one candidate matches, use it. If several match (or none), show the
   `agk ls` rows to the user and ask which student is this conversation — do not guess.

4. **Rename it:**
   ```
   agk rename <sessionId-or-current-name> "<new-name>"
   ```

5. **Confirm:** tell the user the student is now `<new-name>` — from now on
   `agk attach "<new-name>"` reaches it from any terminal on this machine, and the
   classroom/phone shows the new label immediately.

## Notes

- Renaming never restarts or interrupts the session — it is a label change only.
- If two students already share the new name, `agk attach <name>` will refuse and
  list ids; prefer unique names.
