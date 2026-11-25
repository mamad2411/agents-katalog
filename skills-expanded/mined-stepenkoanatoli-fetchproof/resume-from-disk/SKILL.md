---
name: resume-from-disk
description: Resumes a Fetchproof project after an interruption - a reset sandbox, a cut turn, a new agent - by reading where it stands from disk (doctor, handoff, preflight, git status, the last commit report, docs/ARCHITECTURE.md) instead of starting over and paying for collected pages twice. Use at the start of any session that continues earlier work, when the user says "continue", "pick up where you left off" or "resume", or when the state is unclear.
---

# Resume from disk

The repository survives; the session does not. The gate is a pure function of
repository state, so the state can be read rather than remembered.

## Read, in this order

1. `node "$HOME/.agents/fetchproof/bin/doctor.mjs"` - which machine (collector or
   builder), whether the project is gated, what blocks.
2. `node "$HOME/.agents/fetchproof/bin/handoff.mjs"` - whether the corpus is whole here.
3. `node "$HOME/.agents/fetchproof/bin/preflight.mjs"` - which unknowns are proven.
4. `node "$HOME/.agents/fetchproof/bin/research.mjs" --status` - what is collected and
   what the budget is (spends nothing).
5. `git status` and `git log -3` - uncommitted changes are the interrupted task itself,
   possibly partial and unverified: read them as work in progress, never as state to
   trust. The last commit report names the task and how it was verified.
6. `docs/ARCHITECTURE.md` - what the code is, and which seams the task touched.

## Then

- Continue the interrupted task from where the disk says it is. Collected pages are not
  collected again; credits already spent are not spent twice.
- Re-verify anything the uncommitted work claims before building on it.
- Use `skill-router` to pick the next skill from the state just read.
- If the task cannot be finished, say plainly which state it was left in.
