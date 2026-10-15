---
name: commit-session
description: Use when the user wants to commit, stage, wrap up, or "ship" the work done in the current session — covers `/commit-session`, "let's commit this", "give me the commit message", end-of-session staging requests.
---

# commit-session

Help the user commit the work *you* did in this session. Output is **commands the user runs themselves**. You never invoke `git add`, `git commit`, `git push`, or any other git write command.

## When to use

- User says `/commit-session`, "wrap up", "let's commit this", "give me the commit", or similar.
- End of a coding session where you've edited files via Edit/Write/NotebookEdit.

## When NOT to use

- User explicitly asked you to commit yourself — fall back to the normal commit flow (still respect their preferences).
- Nothing was edited in this session — say so and stop.
- The user is mid-task and just asked a status question. Don't preempt them.

## What to do

### 1. Recall the session edits

Build the file list from **your own Edit/Write/NotebookEdit tool calls in this conversation**, not from `git status`. Files that were dirty before the session started are out of scope. If a file was created and later deleted in the same session, drop it.

If you genuinely can't recall the list (compacted context, etc.), say so and ask the user whether to fall back to `git status`.

Also check for a subagent-driven-development ledger: `cat "$(git rev-parse --show-toplevel)/.superpowers/sdd/progress.md" 2>/dev/null`. If one exists and has entries from this session, it's ground truth for both the task boundaries and the one-line summaries in step 4 — prefer it over reconstructing from memory.

### 2. Decide: one commit, or one per task?

Default is **one commit**. Switch to **one commit per task** when the session's edits decompose into independently-meaningful units — any of:

- A written plan was executed (subagent-driven-development, `docs/**/plans/*.md` with numbered tasks) — one commit per task.
- A code-review or `/simplify` pass fixed a numbered list of distinct findings, each touching its own file set.
- The user names 2+ separate concerns for this session that a future `git log` reader would want to see as separate commits (e.g. "fixed the race condition and also extracted the shared helper").

Stay single-commit when the edits are one cohesive change with no natural sub-boundary, the session is small (a handful of files, one concern), or the user asks for "the commit" (singular) with no further signal of separable work.

When splitting, group files by task/finding, not by file type or directory. A file touched by two tasks appears in both groups — `git add -p` lets the user stage each task's hunks separately even from the same file; call this out explicitly in the summary line for that file (e.g. "shared with Task 6 — use -p to pick just these hunks"). Don't force an artificial split of a genuinely single change just to produce more commits, and don't silently merge two independent fixes into one commit just because they happen to touch the same file.

If splitting, repeat steps 3-6 once per task/group, in task order. If not, do them once for the whole session as before.

### 3. Classify each file

Run `git status --porcelain -- <file>` (read-only) once per file, or `git status --porcelain` once and parse. Classify:

- **New / untracked** → first column is `??` or `A `
- **Modified tracked** → first column is ` M`, `M `, `MM`, etc.
- **Deleted** → ` D` or `D ` — call it out separately; `git add -p` won't help.

### 4. Summarise each file in one line

For each file, one sentence: what changed and why. Pull from the SDD ledger if step 1 found one, otherwise from your memory of the edits — not from `git diff`. This is the user's pre-staging cheatsheet — keep it under ~100 chars per line.

### 5. Emit the staging plan

For each file (or, when splitting, each file within the current task group), emit the command the user should run. Order: new files first (so `-N` lands before `-p`), then modified, then deleted.

```
# New files (intent-to-add so `git add -p` can see them)
git add -N path/to/new-file.ts

# Then walk hunks across everything
git add -p path/to/new-file.ts
git add -p path/to/modified-file.ts

# Deletions (stage explicitly)
git rm path/to/removed-file.ts
```

If there's only one file, skip the section headers — just the commands. When splitting into multiple tasks, put the `git commit` for that task's message directly after that task's staging commands, before moving to the next task's `git add` block — so the whole output is a sequential script the user can run top to bottom.

### 6. Propose a conventional commit message

One commit covering the whole change (or, when splitting, one commit per task — see step 2). Format:

```
<type>(<scope>): <subject>

<body — optional, only if subject doesn't carry it>
```

- **type**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`, `style`, `revert`. Pick the dominant one.
- **scope**: optional, lowercase, the area touched (`api`, `web`, `etl`, package name, feature). Drop it if it'd be noise.
- **subject**: imperative mood, lowercase, no trailing period, ≤72 chars.
- **body**: only if the *why* isn't obvious from the subject + diff. No bullet list of file names — the diff shows that.

**Quote characters are forbidden in the generated commit message.** The user copies this into `git commit -m "…"` or a HEREDOC, and an unescaped `'` or `"` in the payload breaks the shell command. Apply across subject AND body:

- No `"` (double quote). When referencing a literal value like `shared` or `feat`, drop the surrounding quotes — context already makes it a literal.
- No `'` (apostrophe / single quote). Rewrite contractions in full: `do not` not `don't`, `it is` not `it's`, `cannot` not `can't`.
- Backticks are fine; em-dashes, colons, and parentheses are fine.
- Worst case (unavoidable literal `'` or `"` in the payload): escape with backslash to match the surrounding shell quoting. Prefer rewording.

If the project's recent commits show a different convention (check `git log --oneline -20`), match that instead. Conventional Commits is the default fallback, not a mandate.

If step 2 chose single-commit but the work still spans multiple unrelated concerns you decided not to split (small session, no clean boundary), say so and recommend splitting — but still propose the single message the user asked for.

Wrap each message in its own fenced block so the user can copy it cleanly:

```
feat(scope): short subject in imperative mood

Optional body paragraph explaining the why.
```

### 7. Output shape

Single commit:

```
## Files edited this session

- `path/a.ts` — short summary
- `path/b.tsx` — short summary
- `path/c.md` (new) — short summary

## Stage

git add -N path/c.md
git add -p path/c.md
git add -p path/a.ts
git add -p path/b.tsx

## Commit message

```text
feat(scope): subject

Optional body.
```
```

One commit per task (step 2 chose to split) — one `## Task N: <name>` block per task, each with its own file list, staging commands, and commit inline, so the whole thing is a single top-to-bottom script:

```
## Task 1: <name>

- `path/a.ts` — short summary
- `path/b.ts` (new) — short summary

git add -N path/b.ts
git add -p path/b.ts
git add -p path/a.ts
git commit -m "fix(scope): task 1 subject"

## Task 2: <name>

- `path/c.ts` — short summary
- `path/a.ts` — shared with Task 1 — use -p to pick just these hunks

git add -p path/c.ts
git add -p path/a.ts
git commit -m "fix(scope): task 2 subject"
```

Keep prose minimal — the user is here for the commands, not a recap.

## Hard rules

- **Never run** `git add`, `git commit`, `git rm`, `git push`, `git stash`, or any other write command. Print them.
- **Never run** `git add .` or `git add -A` even as a suggestion — always per-file.
- **Never** suggest `--no-verify`, `--amend`, or `-c commit.gpgsign=false` unless the user already asked for them.
- Read-only git is fine: `git status`, `git diff`, `git log`, `git ls-files`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Listing files from `git status` instead of session edits | Source of truth is *your* tool-call history; only check `git status` to classify new vs modified |
| Subject longer than 72 chars or in past tense | Imperative mood, ≤72 chars: "add X", not "added X" |
| Multi-line summary per file | One line. The diff has details. |
| Suggesting `git add <file>` for new files | Use `git add -N <file>` first so `git add -p` can stage hunks of a new file |
| Bundling unrelated changes silently in single-commit mode | Flag the mix, recommend splitting into task commits (step 2) |
| Echoing the whole diff | The user can run `git diff` themselves |
| `'` or `"` in the commit message | Drop quotes around literals; rewrite contractions (`do not`, not `don't`). `git commit -m "…"` and HEREDOCs both break on unescaped quotes inside the payload. |
| Splitting a single cohesive change into artificial multi-commits | Only split on real task/finding boundaries (step 2) — one diff, one commit |
| Merging two independent tasks into one commit because they share a file | Keep them as separate task commits; use `git add -p` per task to split the shared file's hunks |
| Ignoring an existing SDD ledger and re-deriving task boundaries from scratch | Check `.superpowers/sdd/progress.md` first (step 1) — it's ground truth |
