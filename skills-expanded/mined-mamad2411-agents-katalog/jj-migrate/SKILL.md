---
name: jj-migrate
description: Help users migrate from Git to Jujutsu (jj). Use when user mentions Git migration, transitioning from Git, Git commands in jj context, or wants to understand jj from a Git perspective. Includes comprehensive Git-to-jj command translations and mental model differences.
---

# Migrating from Git to Jujutsu (jj)

Comprehensive guide for Git users transitioning to jj. Covers mental model differences, command translations, and migration strategies.

## Quick Mental Model Shift

**Git:** Working directory → Staging area (index) → Repository
**jj:** Working directory = working-copy commit (no staging!)

**Git:** Always on a branch (or detached HEAD)
**jj:** Working copy is just a commit; bookmarks are optional pointers

**Git:** Manual rebase of dependent branches
**jj:** Children automatically rebase when parents change

**Git:** Conflicts block operations
**jj:** Conflicts are first-class, don't block work

## Essential Git-to-jj Command Translations

| Git Command | jj Equivalent | Key Difference |
|-------------|---------------|----------------|
| `git add; git commit` | `jj describe` or `jj new` | No staging needed |
| `git commit --amend` | `jj describe` or `jj squash` | Change ID stays same |
| `git checkout -b branch` | `jj new` + `jj bookmark create` | Bookmarks optional |
| `git rebase -i` | `jj rebase`/`squash`/`split` | Multiple focused commands |
| `git reflog` | `jj op log` + `jj undo` | Operation log is better |
| `git stash` | `jj new` | Just create a commit |
| `git cherry-pick` | `jj rebase -r <rev> -d @` | Rebase specific commit |

For complete translation table, see [GIT-COMPARISON.md](GIT-COMPARISON.md).

## Common Git User Misconceptions

### "Detached HEAD is dangerous"
**In Git:** Easy to lose commits
**In jj:** No "attached" mode. Every commit stands on its own. Bookmarks are optional.

### "I need to create a branch before working"
**In Git:** Best practice
**In jj:** Work without bookmarks. Create them later when you need to push.

### "I'll lose work without branches"
**In Git:** Unreferenced commits get garbage collected
**In jj:** Operation log tracks everything. `jj undo` works even after GC.

### "I need to stage changes carefully"
**In Git:** Staging area is key
**In jj:** No staging. Use `jj split` for selective commits after making changes.

### "Conflicts must be resolved immediately"
**In Git:** Conflicts block operations
**In jj:** Conflicts are just markers. Work on other things, resolve when convenient.

## Migration Workflow

### Starting Fresh
```bash
# New jj repository
jj git init

# Or colocated (shares directory with Git)
jj git init --colocate
```

### Migrating Existing Git Repository
```bash
# Clone with jj
jj git clone <url>

# Or colocated for gradual transition
jj git clone --colocate <url>
```

### Colocated Repositories
**Benefits:**
- Can use Git tools that read `.git` directly
- Gradual transition from Git to jj
- Git commands work (but avoid mixing!)

**Cautions:**
- Don't interleave git and jj commands
- Run `jj git import` if you use git commands
- Stick to one tool per session

## Common Workflow Patterns

### Feature Branch (Git)
```bash
git checkout -b feature
# make changes
git add .
git commit -m "Add feature"
git push -u origin feature
```

### Feature Branch (jj)
```bash
# make changes
jj describe -m "Add feature"
jj bookmark create feature
jj git push --bookmark feature
```

**Key differences:** No explicit branch creation, no staging, fewer commands.

### Interactive Rebase (Git)
```bash
git rebase -i HEAD~3
# pick, squash, edit in editor
```

### Interactive Rebase (jj)
```bash
# Squash specific commit
jj squash -r <change-id>

# Split specific commit
jj split -r <change-id>

# Move commit to new parent
jj rebase -r <change-id> -d <new-parent>
```

**Key difference:** Focused commands for specific operations instead of interactive editor.

## Full Documentation

For comprehensive Git-to-jj coverage:
- **[GIT-COMPARISON.md](GIT-COMPARISON.md)** - Complete command translation table, mental models, and misconceptions

## When to Use Other Skills

- **`/jj`** - For daily jj operations after you're comfortable
- **`/jj-troubleshoot`** - If you encounter issues during migration

## Migration Tips

1. **Start with colocated repo** - Use `--colocate` to keep Git repo alongside jj
2. **Keep using Git commands initially** - Run `jj git import` to sync to jj
3. **Gradually shift to jj commands** - Move one workflow at a time
4. **Learn revsets** - More powerful than Git revision syntax
5. **Embrace working copy as commit** - Stop thinking about staging
6. **Use operation log** - Your safety net for mistakes
7. **Create bookmarks sparingly** - Only when needed for remotes
