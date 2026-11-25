---
name: pause
description: Keep this session's place before leaving it open or closing the computer - its name, where it stopped, the next step - so the next session start, in any repo, lists it with the command that resumes it. Use when the user says they stop, pause, come back later, or asks which session to resume.
argument-hint: "[what this session is about]"
---

Talk to the user in their language; a few seconds, nothing else touched.

1. In a few words, what this session works on (`$ARGUMENTS` if given): the task, the ticket if
   there is one (`<repo>#T-170: ion repo fix proves each commit`). Then the next step, one concrete
   sentence someone resuming cold can act on (`merge feat/fix-proof once the tests pass`).
2. Uncommitted work stays where it is: say which worktree holds it, never commit or stash it on
   your own to pause.
3. `ion repo pause "<name>" --next "<next step>"`, from the repo of the work (its worktree).
4. Tell the user it is kept, with what the command printed: the next session start lists it
   above the first prompt (name, age, next step, `claude --resume <id>`); `/rename <name>` also
   shows it under that name in Claude Code's `/resume` picker. Once resumed, or its branch merged
   and deleted, it leaves the list.
