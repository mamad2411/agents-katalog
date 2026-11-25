---
name: samepage
description: One command that puts this pane on the same page as every other agent pane on this repository: it pings them for a one-line status, gathers the shared memory, and prints a short digest. Use when the user says samepage, /samepage, get on the same page, I am opening another terminal, or before starting work in a new pane.
---

# samepage

Run `samepage` (add `--task "<what you are about to do>"` when you know it). One command; it needs nothing else from you.

What it does in a few seconds: creates the shared brain if this repository has none, pings every other live agent pane on this repository for a one-line status (only the ones whose note is stale; never the same pane twice in ten minutes), waits briefly for their answers, and prints a digest of at most forty lines: who is open and what each is doing, the live memory rows, the last lessons, and OVERLAP if your task touches what another pane is working on.

Then:
- Read the digest. If OVERLAP names a pane, tell the user which files it touches and ask before editing them.
- Write your own note early: `samepage wip "<one line>"`. A crash saves nothing.
- A durable lesson: `samepage remember "<one line>"`. Search: `samepage recall <word>`.
- Do not re-ask the user for anything the digest already says.

If a one-line message arrives in this pane asking you to run `samepage wip`, that is another pane's sonar: run that one command with a one-line status and carry on. Do not run `samepage prime` or `samepage init` by hand; `samepage` does what is needed.
