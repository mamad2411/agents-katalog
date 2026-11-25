---
name: git-workflow
description: "Git flow for changes: isolated branch/worktree, incremental commits, pull request and post-merge cleanup."
license: MIT
---

# Git workflow

## Default branch

The examples use `main`. If the project uses another name (`master`, `develop`, `trunk`…), that name is
the default branch. Detect it once instead of assuming:

```bash
BASE=$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's#^origin/##')
echo "$BASE"   # -> main
```

Every rule that mentions the **default branch** refers to `$BASE`.

## Start

```bash
git checkout "$BASE"
git pull origin "$BASE"
```

Branches and worktrees are created from an up-to-date default branch.

## Change cycle

### 1. Isolate

```bash
git worktree add .worktrees/<change> -b feature/<change>
cd .worktrees/<change>
```

All work for the change (artifacts, code, reports) happens inside that worktree.

### 2. Commit

One logical change = one commit (see `conventional-commits`). An agent commits after each approved
step; it never accumulates work.

### 3. Close

1. Verify design → code consistency.
2. Update documentation if business rules changed.
3. Open the pull request:

```bash
gh pr create --base "$BASE" --head feature/<change> --title "<type>: <change>"
```

> `gh` (GitHub CLI) es **opcional**: si no está instalado, abre el PR desde la web con los mismos
> datos (base, head, título y cuerpo). No bloquea el flujo.

4. The user reviews and approves `archive`; commit it in the same PR, then the user merges.

### 4. Post-merge

```bash
git branch -d feature/<change>
git worktree remove .worktrees/<change>
```

## Simple branch exception

A feature branch in the main checkout replaces the worktree only when **all** of these hold:

- the human asks for it explicitly;
- the working tree is clean;
- the change branch is the same in the project and its submodules (no mixed branch state);
- the exception is recorded in the change;
- the branch is never the base branch.

Otherwise use a worktree. The pre-commit guard still blocks any commit on the base branch.

## Integration branches

When the default branch must stay stable, use an integration branch:

```
<default branch>
  └── feat/<stage>
        ├── feat/<stage>-part-1
        └── feat/<stage>-part-2
```

Partial PRs target the integration branch; the merge to the default branch happens once at the end.

## Bootstrap exception

The initial setup (`.atlas/BOOTSTRAP.md`) is the **only** task that does not use a change worktree. It runs on
its own `chore/bootstrap` branch, with one commit per phase and no push unless the user asks. The user
reviews and merges that branch.

## Rules

- The default branch is always clean and up to date.
- Never commit secrets.
- Do not rewrite history of shared branches. `--force-with-lease` only on your own, unmerged branches.
- Role byline on agent commits: `By <role>.`
- A worktree per change; no two changes in the same worktree.
