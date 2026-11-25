---
name: commit
description: Stage all changes with a bracket-tagged message (a custom feature tag by default, or fallback [Feat]/[Fix]/[Refac]/[Docs]), optionally amend, and push
---

# Commit

**Execute mechanically.** Follow the steps; no need to weigh alternatives or deliberate.

Stage, commit, and push. Satisfies `wf-use-commit-skill` when invoked.

## Message format

`[TAG] Imperative message.` with optional body for multi-file changes.

**Custom feature tags are the default.** Name the feature area the change belongs to, PascalCase: `[GridCreation]`, `[WebXr]`, `[AuthFlow]`, `[Harness]`. A tag that names the area tells a reader where to look; `Feat` tells them nothing they couldn't get from the diff.

**Fallback tags,** when no coherent feature area exists: `Fix` (fixes/minor improvements), `Refac` (renaming, moving, cleanup), `Docs` (docs/Claude setup), `Feat` (last resort — a new feature you genuinely can't name an area for). Title case, never all-caps.

One tag per commit — either custom or fallback.

## Tag selection

Parse `$ARGUMENTS`:

- Starts with `[...]` → respect as-is; rest = message hint.
- Single PascalCase word (no spaces, e.g. `GridCreation`) → treat as custom tag; Claude drafts the message from the diff.
- Longer text → treat as message hint; Claude picks the tag per below.

When Claude picks the tag, try custom first — reach for a fallback only when the attempt fails:

- **Can you name the feature area?** Ask what a reader six months out would want the tag to say. The branch name, the directory the diff clusters in, and the plan being implemented are all good sources. If a name is obvious → use it, no confirmation. This is the common path.
- **Area plausible but ambiguous** (two defensible names, or you'd be guessing at the boundary) → propose via `AskUserQuestion`:
  - **Use `[<Proposed>]`** (Recommended)
  - **Use `[<Alternative>]`**
  - **Edit** (free-text override)

  Wait for the answer before committing.
- **Genuinely no coherent area** — a scattered sweep, a routine one-liner, a docs touch → best-fit fallback tag, no confirmation.

A confirmation prompt on every commit would defeat the preference, so don't ask when the area is clear. Ask only when you'd otherwise be inventing a boundary.

## Steps

1. Run `pwsh -NoProfile -File "$HOME/.claude/scripts/git-preflight.ps1"`. Stop if no changes.
2. Read the diff (`git diff` + `git diff --cached`) to pick tag and write the message.
3. **Branch check** — read `.claude/rules/git-workflow.md` if it exists.
   - **Feature branches** + on `main`: stop and ask the user to switch or confirm.
   - **Direct to main**: proceed silently regardless of branch.
   - No rule file: feature-branch default (warn if on main).
4. If changes are very small (≤5 lines, ≤2 files), ask via `AskUserQuestion`: **Amend last commit** vs **New commit**. Skip for larger changes.
5. **Stage, commit, push** directly:
   - `git add .`
   - `git commit -m "[TAG] msg"` (HEREDOC for multi-line). Add `--amend` if amending.
   - `git push` (or `git push --force-with-lease` if amending).
6. Report the commit hash. If push failed, tell the user.

## Rules

- No Co-Authored-By — use the user's git auth only.
- Do not confirm a clear custom tag or a fallback tag — commit and push immediately.
- Confirm only an **ambiguous** custom tag, via `AskUserQuestion`. User-supplied tags (in `$ARGUMENTS`) never confirm.
- Always push. Amend uses `--force-with-lease`, never `--force`.
- Imperative mood: "Add user auth" not "Added user auth".
- **No plan references in commit messages.** Never include task IDs, phase labels, or plan names (e.g. `A1 —`, `Task 3:`). Bad: `[AuthFlow] A1 — Add user auth`. Good: `[AuthFlow] Add user auth`.
