---
name: trim-agent-setup
description: "Finds the memory files, instruction files, rules and skills that recorded agent sessions never read, and what the files they load cost in tokens, then helps remove or shorten them safely. Use when the user asks to trim or audit their agent setup, shorten AGENTS.md or CLAUDE.md, cut context or token cost, or find unused skills and memory files."
license: MIT
---

# Trim the agent setup

Uses the coding.sh MCP server's `harness_audit` tool. It reads sessions recorded on this machine
and the instruction files on disk, and changes nothing.

## Steps

1. Call `harness_audit`. Pass `since` when the user names a window, such as `90d`. The default is
   30 days.
2. Read `files`. Each has its size in `tokens`, how many sessions `loaded`, `read` and `wrote` it,
   and `flags`. List the flagged files first:
   - `never-read`: no session loaded it or read it.
   - `write-only`: sessions wrote it and none read it back.
   - `loaded-not-read`: a skill that was listed in context and never used.
   - `deleted`: sessions wrote it and none read it back, and it is gone from disk. There is nothing
     to remove; say so instead of proposing to delete it.
3. Then give what loading costs: `loadTokensPerSession` for the whole setup, and the files with the
   largest `loadTokens`, which is what loading that file cost over the whole window. These are
   files to shorten, not to delete.
4. Propose what to delete or shorten. Change nothing until the user says yes.
5. After the edits, call `harness_audit` with `check: true`. It compares the uncommitted edits with
   the last commit. `check.rejections` lists each protected safety line that was deleted, reworded
   or relaxed. Show each one and put it back unless the user asked for that removal. This result's
   `next` is the command that allows the removal: give it only when the user wants that.
6. The result of step 1 can have `next`: a `coding.sh refine run` command that tests a shorter file
   on an eval suite. Give it to the user to run, because it takes minutes. When that result also
   has `note`, there is no suite to test on yet: tell the user that instead.

## Rules

- A file the sessions never read can still be loaded on purpose. Ask before removing a rule that
  forbids something, such as a line about force pushes or secrets.
- A short window hides files that are used rarely. Before deleting a skill, run the audit again
  with a longer `since`.
- Delete nothing yourself that the user did not agree to in this conversation.
