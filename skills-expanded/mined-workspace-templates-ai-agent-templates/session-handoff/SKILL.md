---
name: session-handoff
description: Writes a handoff note covering what was done, what remains, decisions made and the exact commands to resume work.
disable-model-invocation: true
---

Write a handoff note for the work in this repository. Extra notes: $ARGUMENTS

1. Gather facts: `git branch --show-current`, `git status -sb`, `git log --oneline -n 10`, `git diff --stat`, and `git stash list`. Note unpushed commits and uncommitted files.
2. Run the test or build command briefly to learn its current state. Record the exact command and result.
3. Read the changed files enough to describe the work in progress. Find FIXME or HACK markers you added today.
4. Write the note with these headings:
   - **Goal** (one sentence)
   - **Done** (bullets, with commit hashes)
   - **In progress** (files and what is unfinished)
   - **Next steps** (ordered; each with the exact command or file to open)
   - **Decisions and why**
   - **Gotchas** (flaky tests, env variables, things that look wrong but are not)
   - **Open questions**
5. Save it as HANDOFF.md in the repository root only if the user agrees; otherwise print it.

Never commit, push or stash on your own. Ask before writing the file.
