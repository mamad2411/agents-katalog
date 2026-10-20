---
name: revise-conventions
description: Propose a change to Eric's house-style repo (ericeslinger/claude-skills) by pull request. Use when Eric states a new general working preference, reverses an existing one, or when a documented convention is contradicted by how the code actually works.
---

# Revise the house style

**You have standing permission to change this repo by pull request.**
Eric wrote it to be edited: when his opinions change or a new principle
appears, the conventions should follow without waiting for him to
remember to do it himself.

Permission covers: opening a PR against `ericeslinger/claude-skills`
with a reasoned change. It does not cover merging, force-pushing,
rewriting history, or editing `main` directly.

> **`ericeslinger/claude-skills` is a PUBLIC repository.** You are
> usually invoking this skill from inside a *private* repo, which makes
> this the one moment where content can cross that boundary. Everything
> you write lands world-readable and stays in git history.
>
> Never carry across: credentials, tokens, project ids, database names,
> connection strings, internal hostnames, user or customer data, or
> verbatim contents of a private file. Carry the *convention* and the
> reasoning; leave the values behind. If the rule cannot be stated
> without a private value, it is repo-specific — put it in that repo's
> `CLAUDE.md` instead and do not open a PR here.

## When to do this

Any of:

- Eric states a general preference — "from now on…", "I've decided…",
  "I always want…", "stop doing X" — that is not specific to one repo.
- Eric overrules something these files say. The correction belongs here,
  not just in the current conversation.
- A documented practice is contradicted by the code in all three
  reference repos. The docs are wrong; fix them.
- A new project establishes a pattern worth generalizing — but only
  after it has survived somewhere real. One repo doing something once is
  not a convention.

**Do not** file a PR for: a repo-specific rule (that belongs in that
repo's `CLAUDE.md`), a preference you inferred rather than heard, or a
general software-engineering nicety Eric never expressed.

## The pressure test — every assertion must pass it

The repo's stated standard, and the thing Eric asked for explicitly:
**an assertion earns its place only if a competent Claude session would
plausibly do otherwise by default.** Before adding a line, ask:

1. **Counterfactual.** If this line were deleted, would any session
   behave differently? "Write clear commit messages," "use TypeScript,"
   "handle errors" fail — that is already the default. Cut them.
2. **Falsifiable.** Could a reviewer point at a file and say "this
   violates it"? "Keep the code clean" cannot be violated. "Every
   non-trivial file has a colocated `<name>.spec.ts`, no transitive
   coverage credit" can.
3. **Load-bearing.** Does something break, or a known past bug recur, if
   it is ignored? The best entries record scar tissue — a real failure
   whose cause is now written down.
4. **Right altitude.** Durable *why* goes in **Principle**; the current
   tool or technique goes in **Practice**, dated, replaceable without
   losing the principle.

If an entry passes 1 and 2 but not 3, it probably belongs in a repo's
`CLAUDE.md` rather than here. Cuts are recorded in
[`docs/pressure-test.md`](../../../../docs/pressure-test.md) so the same
platitudes do not get re-added later — add to that ledger when you
reject something, not just when you accept.

## How to do it

1. Read the target reference file. Prefer **editing an existing entry**
   over adding a new one; this repo gets less useful as it gets longer,
   because everything here competes for context in every session.
2. Write it as Principle + Practice. If a practice is being replaced,
   replace the Practice and keep the Principle — that is the whole point
   of the split.
3. Date any decision that reverses an earlier one.
4. Branch, commit, push to `origin`, open a PR against `main`. Title:
   what changed. Body: **who asked for it or what evidence forced it**,
   what it replaces, and one line on how it passes the pressure test.
   Quote Eric's own words where you have them.
5. Do not merge. Say in chat that the PR is open and what it says.

If Eric asked for the change directly in the current session, opening
the PR is the expected follow-through, not something to ask permission
for again. If you inferred it, ask first.
