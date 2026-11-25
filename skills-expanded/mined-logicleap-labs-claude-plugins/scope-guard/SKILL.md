---
name: scope-guard
description: Use at the START of any focused task — a bug fix, one feature, a single file's refactor — and ALWAYS when more than one agent shares a working tree. Declare which files the task is allowed to touch so edits outside that set are blocked. Triggers on "only change X", "just fix the bug in", "don't touch anything else", "stay in your lane", "scoped change", "while you're in there" (the thing to prevent), shared-tree / multi-agent work, and any task where creep is the risk.
---

# Scope Guard

**The most expensive edits are the ones nobody asked for.** A "while I'm here"
rename, a reformatted file two directories away, an import you "tidied" — each
one widens the diff, risks another agent's work on a shared tree, and turns a
reviewable change into a guessing game.

Scope Guard makes you commit to a blast radius up front, then a PreToolUse hook
holds you to it: any `Edit`/`Write`/`MultiEdit` outside the declared files is
**blocked before it happens**.

## The rule

> **Declare the files, then only touch the files.** Widening scope is a
> decision you state out loud — never a side effect.

## Step 1 — Declare scope at the start of the task

Pick the **narrowest** set of paths that can satisfy the request. Three ways to
declare, highest priority first:

1. **`.scope-guard` file** in the project root (best for a whole session / a
   repo someone else also works in) — one glob per line:

   ```
   # the only files this task may touch
   src/checkout/**
   src/lib/money.ts
   !src/checkout/legacy/**     # never these, even though src/checkout/** allows them
   ```

2. **`SCOPE_GUARD_PATHS` env var** — `export SCOPE_GUARD_PATHS="src/**, !src/legacy/**"`

3. **An in-band sentinel** on its own line in your reply (best for a single
   task, no file to clean up):

   ```
   SCOPE-GUARD: src/checkout/**, src/lib/money.ts
   ```

Glob rules: `**` spans directories, `*` stays within one segment, a bare token
with no `/` (e.g. `*.ts`) also matches that basename anywhere, a directory
(`src` or `src/`) means `src/**`, and a leading `!` excludes.

## Step 2 — Work normally

Edits inside scope go through untouched. The first time you reach for a file
outside it, the hook blocks the edit and tells you which file and which scope.

## Step 3 — When you hit the wall, make a decision (don't just widen)

A block is a signal, not a nuisance. Ask **why** the file is out of scope:

- **It genuinely belongs to this task** (you under-scoped) → re-declare with a
  new `SCOPE-GUARD:` line that includes it, and say *why* in your reply. Now
  it's a recorded decision, not a drive-by.
- **It's a real but separate change** → leave it. Note it as follow-up.
- **It's another agent's file on a shared tree** → leave it. Not yours.

Never widen scope silently to make a block go away.

## What this catches

- "While I'm here" refactors and reformats outside the task
- Edits to files another agent is mid-task on (shared working tree)
- Touching generated/vendored/lock files you didn't mean to
- Scope creep that turns a 1-file fix into a 20-file diff

## Kill switch

False positive, or a deliberately broad task: `touch .scope-guard-off` in the
project root (or `~/.claude/.scope-guard-off` globally), or
`export SCOPE_GUARD_GATE=off`. With no scope declared at all, the hook is a
silent no-op — it only ever acts once you've opted in.

## Pairs with

- **`verify-before-done`** — scope says *which* files; verify says *prove the
  change works*. Narrow diff + real evidence = a reviewable change.
- **`visual-quality`** — when the in-scope files render UI.
