---
name: coordinator-handoff
description: Pause the Souls development coordinator and hand the running agenda to a fresh coordinator in any harness (Claude, Codex, other), or take one over. Use when Gene says to hand off, migrate, switch provider, or that usage is about to run out, or when a takeover prompt names this skill. Not for a first-time orientation; that is the fresh-session starter in docs/process/development-coordinator.md.
---

# Coordinator handoff

A handoff carries state, never rules: the rules live in `AGENTS.md`,
[development-coordinator.md](../../../docs/process/development-coordinator.md) and the agenda issue. Start no new
task from the moment the handoff begins.

1. **Tell each lane to push and comment.** Send every lane (and the steward): "Handoff. Finish the step you are on,
   start nothing new, push your branch (a WIP commit if needed, never `git stash`) and comment on your issue with
   what is done and the exact next step. Don't stop a declared run between arms: finish or abandon it and say
   which. Then stop." Never cancel CI, a gate or a merge-train run to make the switch
   tidy; it keeps running and the successor reads its result.
2. **Write the state file.** Update the private state file (owner, `paused: true`, bindings for anything still
   running, including a release in flight with its candidate head, receipts and next command, standing rules, `updated_at`) and run `node tools/coordinator/state.mjs check <file>`.
3. **Post the checkpoint on the coordination issue.** Paste the output of
   `node tools/coordinator/state.mjs checkpoint <file> --agenda <issue>`, with one line each for what is running and
   what waits on Gene.
4. **Stop.** Confirm no lane is still writing (one that has not stopped is recorded as cut off, with its branch),
   then give Gene the takeover prompt and end the session: "You are the Souls development coordinator, resuming
   agenda #N. Read AGENTS.md, docs/process/development-coordinator.md (Start or resume, takeover) and the latest
   checkpoint on #N, then re-dispatch."

**One writer per worktree.** The successor dispatches only after the previous coordinator and its lanes have
stopped. Two writers never share a worktree, a branch or the state file.
