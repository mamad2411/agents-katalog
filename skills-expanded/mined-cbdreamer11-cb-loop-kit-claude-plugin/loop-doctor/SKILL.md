---
name: loop-doctor
description: Checks that the loop is actually installed and working in this project - files present, role profiles valid, connections alive, effort level real. Use after setup, after an upgrade, or when something behaves as if the method is not loaded.
---

# Doctor

Verify the installation the same way the method verifies everything else: by
observing, not by assuming it took.

## 1 · The files

`ls -la .loop/ .loop/roles/ .claude/agents/ 2>&1` and confirm: `STATE.md`,
`VERIFY.md`, `DECISIONS.md`, `GOTCHAS.md`, the four role profiles, the `loop`
wrapper (and that it is executable), and the role agents in the project's
`.claude/agents/`.

Report anything missing, and whether `.loop/ACCESS.local.md` is gitignored — if it
is tracked, stop and say so loudly: it is the file most likely to hold a credential.

## 2 · The contract is still true

`.loop/VERIFY.md` rots faster than anything else. **Run each declared command** and
report which ones still work. A verification contract with a stale build command is
worse than none, because it produces confident green nonsense.

## 3 · The connections

Re-run the connection table from session 0: build, browser, database, payments test
mode, git remote. PASS / FAIL / ABSENT. Every ABSENT should already be a declared
GAP in `.loop/VERIFY.md`; if it is not, add it.

## 4 · The effort this session is really running at

This session's effort level: **${CLAUDE_EFFORT}**

If that shows a level, that is the real one — including any silent downgrade. If it
printed the placeholder literally, this version does not interpolate it; run
`echo "$CLAUDE_EFFORT"` in a shell instead. There is deliberately no equivalent for
the model: **no session can read which model it is running on**, so do not print a
guess. If the role matters, relaunch with `./loop <role>` and trust the profile.

## 5 · Verdict

One table: what is healthy, what is broken with the exact command to fix it, and
what is absent by design. If anything in section 1 or 2 is broken, say plainly that
the method is **not** in force in this project yet.
