---
name: jj-troubleshoot
description: Troubleshoot Jujutsu (jj) problems including error messages, conflicts, divergent changes, stale working copy, and recovery scenarios. Use when user encounters jj errors, unexpected behavior, needs to recover from mistakes, or mentions problems with jj operations.
disable-model-invocation: true
---

# Jujutsu Troubleshooting

Solutions to common jj problems, error messages, and recovery scenarios. Invoke manually with `/jj-troubleshoot` or reference when encountering issues.

## Quick Diagnostics

Run these commands to gather information:
```bash
jj status              # Current state
jj log -n 10           # Recent history
jj op log -n 5         # Recent operations
jj bookmark list       # Bookmark status
```

## Common Error Messages

### "Bookmark is conflicted"
**Error:** `Refused to push a conflicted bookmark`

**Solution:**
```bash
# 1. List bookmarks to see conflict
jj bookmark list       # Look for ?? marker

# 2. View commits involved
jj log

# 3. Move bookmark to correct commit
jj bookmark move main --to <correct-commit-id>

# 4. Push
jj git push --bookmark main
```

### "Divergent changes"
**Warning:** `Added working copy commit as ... (divergent)`

**Explanation:** Two visible commits share the same change ID. Often from remote rebases importing a new `commit_id` while the old one stays visible.

For a single stray divergent commit, abandon the unwanted version:
```bash
jj abandon <unwanted-id>
```

For widespread divergence across many commits, use **`/jj-divergent`** — it provides a systematic 8-step cleanup procedure including root-cause identification, safety checks, and remote bookmark handling.

### "Stale working copy"
**Error:** `Working copy is stale`

**Solution:**
```bash
jj workspace update-stale
# or
jj status  # Triggers snapshot
```

### "Non-fast-forward push rejected"
**Error:** `Remote has moved forward`

**Solution:**
```bash
# 1. Fetch updates
jj git fetch

# 2. Rebase your changes
jj rebase -s <your-first-commit> -d main@origin

# 3. Push again
jj git push --bookmark main
```

## Common Problems

### Accidentally Undid After Push
**Problem:** Ran `jj undo` after `jj git push`

**Solution:**
```bash
# Option 1: Redo (if just did undo)
jj redo

# Option 2: Re-push
jj git push --bookmark <name> --force

# Option 3: Fetch and reconcile
jj git fetch
jj bookmark move <name> --to <name>@origin
```

**Prevention:** Don't undo after push operations.

### Mixed Git and jj Commands
**Problem:** Used both tools, now state is weird

**Solution:**
```bash
# Import Git state to jj
jj git import

# Check for conflicts
jj bookmark list
jj log

# Resolve any conflicts
```

**Prevention:** Stick to one tool at a time.

### Can't Find Recent Changes
**Likely causes:**

1. **Not snapshotted:**
   ```bash
   jj status  # Triggers snapshot
   jj diff    # Now shows changes
   ```

2. **Looking at wrong commit:**
   ```bash
   jj log     # Find working copy (marked @)
   ```

3. **Changes were committed:**
   ```bash
   jj show @-  # Check parent
   ```

### Bookmark Not Moving
**Problem:** Making commits but bookmark stays on old commit

**Explanation:** This is expected! Bookmarks don't auto-advance in jj.

**Solution:**
```bash
# Move bookmark manually
jj bookmark move <name> --to @
```

**Better pattern:** Create bookmarks only when ready to push.

### Too Many Commits in Log
**Problem:** `jj log` shows overwhelming history

**Solutions:**
```bash
# Show only ancestors of working copy
jj log -r ::@

# Show last 10 commits
jj log -n 10

# Show commits between main and @
jj log -r main::@

# Configure default
jj config set --user revsets.log '::@ | @::'
```

### Lost Commits
**Problem:** Commits seem to have disappeared

**Solution using operation log:**
```bash
# 1. View operation history
jj op log

# 2. Find operation before commits disappeared
# 3. View repo at that operation
jj --at-op=<operation-id> log

# 4. Restore if commits are there
jj op restore <operation-id>

# 5. Or undo recent operations
jj undo
```

### File Deletion Not Tracked
**Problem:** Deleted files outside jj, not showing in diff

**Solution:**
```bash
jj status  # Triggers snapshot
jj diff    # Now shows deletion
```

**Prevention:** Run `jj status` after manual file operations.

## Conflict Resolution

### Identifying Conflicts
```bash
jj log     # Look for × marker
jj status  # May show "conflict" markers
```

### Understanding Conflict Markers
```
<<<<<<< Conflict 1 of 1
+++++++ Contents of side #1
changes from first parent
------- Contents of base
original content
+++++++ Contents of side #2
changes from second parent
>>>>>>> Conflict 1 of 1 ends
```

### Step-by-Step Resolution
```bash
# 1. Create working copy on conflict
jj new <conflicted-change-id>

# 2. Edit files to resolve (remove markers, keep desired content)

# 3. Review resolution
jj diff

# 4. Squash resolution into conflicted commit
jj squash

# 5. Verify conflict resolved
jj log  # × marker should be gone
```

### Alternative: Abandon and Redo
If conflict is too complex:
```bash
jj abandon <conflicted-change-id>
# Redo operation more carefully
```

## Recovery Scenarios

### Completely Lost - Start Over
```bash
# 1. Save current state
jj op log > ~/jj-op-log-backup.txt

# 2. Find good state
jj op log

# 3. Restore to known good operation
jj op restore <good-operation-id>
```

### Accidentally Force Pushed Wrong Thing
**If you have local operation log:**
```bash
# 1. Find operation before bad push
jj op log

# 2. Restore
jj op restore <operation-id>

# 3. Re-push correctly
jj git push --bookmark <name> --force
```

## Full Documentation

For comprehensive troubleshooting:
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Complete guide with all error messages and solutions

## When to Use Other Skills

- **`/jj`** - Return to normal operations after resolving issues
- **`/jj-migrate`** - If issues stem from Git mental model confusion
- **`/jj-divergent`** - Systematic cleanup of widespread divergent commits

## Diagnostic Commands

When reporting issues, provide:
```bash
jj --version
jj status
jj log -n 10
jj op log -n 5
jj bookmark list
```
