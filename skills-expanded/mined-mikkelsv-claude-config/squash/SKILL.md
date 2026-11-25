---
name: squash
description: Squash commits on the current branch since divergence (default main, or a custom base) down to 1-3 commits, using /commit's bracket tag format and synthesized messages
---

# Squash Branch Commits

**Execute mechanically.** Follow the steps; no need to weigh alternatives or deliberate.

Collapse every commit ahead of a base ref down to **1-3 commits**. One is the common case and the default. Reach for 2-3 only when the branch did genuinely separable pieces of work and the history reads better split. Format and tag selection mirror `/commit`.

Scripts: `$HOME/.claude/skills/squash/scripts`

## What the commits are for

History here is **communication, not bisection**. Intermediate commits need not build, compile, or pass tests individually — a group is a chapter heading, not a checkpoint. Don't reshuffle a grouping to make each commit independently green, and don't reject a split because one half wouldn't compile alone.

This is safe because the branch merges to `main` as one unit: `git bisect` stays reliable at the `main` level, and only the intra-branch commits are non-bisectable. If you ever need a bisectable branch, don't squash it.

## Modes

- **Interactive (default)**: invoked by user; runs steps 1-7. Base = `main`.
- **Automated**: invoked by another skill (e.g., `/implement` for per-phase squash). `$ARGUMENTS` carries `base=<sha>` and `message=<text>`. A supplied `message=` means one commit — skip grouping, skip confirmation.

Argument format when called by another skill:

```text
base=<commit-sha-or-ref>
message=<single-line subject; for multi-line, use \n separator>
push=true
```

## Steps

1. **Parse arguments**. If `$ARGUMENTS` contains `base=...` and `message=...`, enter automated mode → single commit, skip to step 7a. Otherwise interactive.
2. **Inventory** — `pwsh -NoProfile -File "$HOME/.claude/skills/squash/scripts/git-squash-inventory.ps1" -Base <base-or-main>`. Handle `status`:
   - `on-main` / `detached` / `dirty` / `none` / `single` / `error` → report the reason and stop. (`single` → suggest `/commit` amend.)
   - `ok` → continue with `commitCount`, `subjects`, `log`, `stat`.
3. **Decide the commit count** from the inventory's `subjects` and `stat`. Default to **1**. Split into 2-3 only when *all* of these hold:
   - Two or three **separable concerns** are present — not just many files. Ask whether a reader scanning `git log` would want them listed apart.
   - The split falls on **file boundaries**, with no file needed by two groups. The grouped script enforces this and aborts if violated.
   - Each group has a subject worth reading on its own. If two subjects would paraphrase each other, it's one commit.

   Signals for splitting: a refactor that enabled the feature, plus the feature. A product change plus unrelated tooling or config swept up on the way. Two features that shared a branch for convenience.

   Signals against: one coherent change touching many files (very common — still 1). A feature plus its own tests (that's one thing). A change plus fixups to itself.
4. **Pick tags** — apply `/commit`'s tag-selection rules verbatim: custom feature tag preferred, fallback `[Feat]`/`[Fix]`/`[Refac]`/`[Docs]`. Each group gets its own tag; they may differ (e.g. `[Harness]` then `[Refac]`).
5. **Draft messages** — per group, one imperative subject describing the *result*, not a concatenation of the originals. Body optional: `Squashed from N commits:` plus a bullet list, only where worth preserving.
6. **Confirm** (interactive only) via `AskUserQuestion`:
   - **Landing on 1 commit** → don't ask about grouping. Confirm only push: **Squash & push** (Recommended) / **Squash, don't push** / **Cancel**.
   - **Landing on 2-3** → show the proposed grouping (subject + file count per group) and confirm: **Squash as proposed** (Recommended) / **Collapse to one instead** / **Cancel**. Then confirm push as above.

   In automated mode, push follows the `push=true|false` arg (default true).
7. **Execute** — record `git rev-parse HEAD` first as the pre-squash sha. Write the groups with the `Write` tool to `$HOME/.claude/local/tmp/squash-groups.json` (a file, not inline, because multi-line bodies do not survive shell quoting), shaped `[ { "message": "...", "paths": [...] }, ... ]` in commit order:
   - **a. One commit** — a single group with `"paths": ["."]` (claims every changed file).
   - **b. Two or three** — one group per commit, each listing its paths.

   Then `pwsh -NoProfile -File "$HOME/.claude/skills/squash/scripts/git-squash-execute-grouped.ps1" -Base <base> -GroupsFile "$HOME/.claude/local/tmp/squash-groups.json"` (add `-Push`). It verifies every changed file is claimed by exactly one group **before** committing anything, so a bad grouping fails clean.

   Report each `commits[].hash` and `pushed` from the JSON result.

## Rules

- Never run on `main` when squashing onto `main` (inventory enforces this; non-main bases are fine).
- Never use `git rebase -i` — interactive editor not supported.
- Always `--force-with-lease`, never `--force`.
- **Never exceed 3 commits.** If the branch seems to need more, it wanted to be more than one branch; say so and squash to 3 or ask.
- Verify the result: `git log --oneline <base>..HEAD` for the count, and `git diff <pre-squash-sha> HEAD` must be **empty** — squashing changes history, never content.
