---
name: jj-divergent
description: Use when jj log shows divergent() entries, multiple commits share a change_id, "Added working copy commit as ... (divergent)" warnings appear, or the repo has accumulated divergent changes. Also use for any question about why jj shows duplicate commits, how change IDs relate to commit IDs, or systematic cleanup of divergence from remote rebases.
---

# Resolving Divergent Commits in jj

A **divergent** change has multiple visible commits sharing the same `change_id`. They appear in `jj log` with an offset label like `/0`, `/1` and are flagged as "divergent".

**Common causes:**
- A hidden commit becomes visible again: `jj new REV`, `jj edit REV`, fetching from a remote, or adding a bookmark to an old commit
- A remote rebases or amends a commit → jj imports the new `commit_id` but the old one remains visible
- Multiple workspaces or concurrent processes modify the same change simultaneously

**When divergence exists, change IDs are ambiguous.** Use commit IDs or the offset form `CHANGEID/0`, `CHANGEID/1` to refer to specific versions unambiguously.

## Step 1: Assess the Damage

```bash
# Count unique divergent change_ids
jj log -r 'divergent()' --no-graph -T 'change_id.short(8) ++ "\n"' | sort -u | wc -l

# Find ROOT divergences — fixing these cascades to all descendants
# A root divergent commit has no divergent ancestors
jj log -r 'divergent() & ~descendants(divergent() & ~roots(divergent()))' --no-graph
```

Focus only on root divergences — their descendants diverge in lockstep.

## Step 2: Classify Each Root Divergence

For each root, find both versions:

```bash
jj log -r 'all() & change_id(CHANGEID)' --no-graph \
  -T 'separate(" ", commit_id.short(8), if(immutable,"I","M"), bookmarks, description.first_line()) ++ "\n"'
```

| Situation | Fix |
|-----------|-----|
| One version is in `ancestors(main)` (already merged) | Abandon the non-main version |
| One version is an orphan (no bookmark, mutable) | Abandon the orphan |
| Both versions have local bookmarks | Pick one, move the bookmark, abandon the other |
| Old version kept alive by a remote bookmark you own | Rebase the branch onto the new base, force push |
| Old version kept alive by a remote bookmark you don't own | Coordinate with owner, or `jj bookmark forget --include-remotes` |

## Step 3: Safety Check Before Every Abandon

Use `jj interdiff` to verify the two versions introduce identical changes. It compares patches (what each commit *does*), not file trees — so it works correctly even when the divergent commits have different parents after a rebase.

```bash
jj interdiff --from OLD_COMMIT --to NEW_COMMIT
# Expect: no output (identical patches)
```

If there is output, the commits are not equivalent — investigate before abandoning.

`jj interdiff` is preferable to `diff <(jj diff -r A --git) <(jj diff -r B --git)` because it handles differing parent histories natively rather than relying on shell process substitution.

## Step 4: Fix Orphaned or Merged Divergences

Three resolution options depending on the situation:

**Abandon the unwanted version** (one is clearly obsolete):
```bash
jj abandon COMMIT_ID

# Abandon an entire orphaned chain at once
jj abandon 'divergent() & mutable() & ~bookmarks()'
```

**Assign a new change ID** (both versions are legitimate separate changes):
```bash
jj metaedit --update-change-id COMMIT_ID
```
This gives one version a fresh change ID, resolving the divergence without losing either commit.

**Squash both together** (both have useful content to merge):
```bash
jj squash --from SOURCE_COMMIT_ID --into TARGET_COMMIT_ID
```

**Accept divergence** (when immutable history prevents cleanup and there's no immediate problem): leave it. The only cost is that change ID references are ambiguous — use `CHANGEID/0` and `CHANGEID/1` offsets to refer to specific versions.

## Step 5: Rebase Branches Built on an Old Base

When a branch is built on the old version of a rebased commit:

```bash
# Find what's keeping the old parent alive
OLD_PARENT_CHID=$(jj log -r 'OLD_PARENT' --no-graph -T 'change_id')
jj log -r "all() & change_id($OLD_PARENT_CHID)" --no-graph \
  -T 'separate(" ", commit_id.short(8), bookmarks) ++ "\n"'

# Check for potential conflicts (overlapping files = conflict risk)
jj diff -r BRANCH_TIP --stat
jj diff -r OLD_PARENT..NEW_PARENT --stat

# Rebase the first unique commit of the branch onto the new counterpart
jj rebase -s FIRST_UNIQUE_COMMIT -d NEW_COUNTERPART --ignore-immutable

# Verify patches are unchanged after rebase
jj interdiff --from OLD_COMMIT --to NEW_COMMIT

# Push if you own the branch
jj git push --remote REMOTE --bookmark BRANCH_NAME
```

## Step 6: Handle Remote Tracking Bookmarks Keeping Old Commits Alive

When old commits can't be abandoned because remote bookmarks make them immutable:

```bash
# Find which remote bookmarks are keeping old commits alive
jj log -r 'remote_bookmarks(remote=REMOTE) & descendants(OLD_ROOT_COMMIT)' \
  --no-graph -T 'separate(" ", commit_id.short(8), bookmarks) ++ "\n"'

# Forget the bookmark (reversible — comes back on next jj git fetch)
jj bookmark forget BOOKMARK_NAME --include-remotes

# Now re-check mutability and abandon orphaned old commits
jj abandon '(ancestors(OLD_ROOT) | OLD_ROOT) & divergent() & mutable()'
```

## Step 7: Prevent Re-Importing Forgotten Bookmarks

```bash
# Fetch only the branches you care about (note: jj git fetch uses --branch, not --bookmark)
jj git fetch --remote REMOTE --branch 'wip/yourname/*' --branch 'main'
```

## Step 8: Verify

```bash
jj log -r 'divergent()' --no-graph -T 'change_id.short(8) ++ "\n"' | sort -u | wc -l
# Expect: 0 (or only unavoidable ones from branches you've chosen not to track)
```

## Recovery

Every jj operation is undoable:

```bash
jj op log          # see operation history
jj op undo         # undo last operation
jj op restore ID   # restore to any prior state
```

## Related Skills

- **`/jj`** — Daily operations and working copy management
- **`/jj-troubleshoot`** — General error messages and conflict resolution
