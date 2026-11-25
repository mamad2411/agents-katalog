---
name: aa-resume
description: Use when the user says resume, continue, or pick up where we left off, starts a new session on an existing Agent-Agile project, or is recovering after a crash or context reset, for example "/aa-resume", "let's continue", "where were we".
license: MIT
metadata:
  system: agent-agile
---

# aa-resume

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/execution.md`'s "Resume protocol" section from that root, and follow it exactly:

1. If `.planning/STATE.md` does not exist, no project has been started here yet. Say so plainly, and point the user at the three front doors instead of guessing at a state that isn't there: a vague spark → `/aa-grill`, a clear idea → `/aa-new-project`, an existing plan or spec → `/aa-import`.
2. Otherwise, read `.planning/STATE.md` first and only. Don't re-derive status by re-reading the whole epic history — `STATE.md` is the baton, kept small on purpose so this step stays cheap every time.
3. Follow its pointers — at most three files — and read exactly those, nothing wider.
4. Continue the work from exactly where `STATE.md` says the run is: the phase it names (grill, intake, panel, prereqs, an epic's wave, review, or done), the "Now" sentence, and the "Next" sentence.
5. If `STATE.md` names a blocker, resolve or surface that blocker before doing anything else — never work around it silently.

Close the session, without exception, with one `STATE.md` update: what's in progress, what's next, the pointers the next session needs, and any blocker. A session that stops without this update leaves the next session to reconstruct state from scratch — the entire point of the baton is that this never has to happen.
