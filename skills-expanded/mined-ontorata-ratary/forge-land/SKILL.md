---
name: forge-land
description: >-
  Close a forge branch: verify tests, choose merge/PR/keep/discard, clean up
  worktree. Use when blueprint tasks are complete.
---
# Forge Land

**Activates:** all blueprint tasks checked off.

## Verify

```bash
npm test
npm run typecheck   # if available in package.json scripts
```

Record final test count vs isolate baseline.

## Present options

Ask owner (or infer from prior instruction):

| Option | When |
|--------|------|
| **Merge local** | Small, reviewed, owner wants direct merge to main |
| **Open PR** | Default for shared repo — use `gh pr create` |
| **Keep branch** | Experimental — document in handoff |
| **Discard** | Wrong approach — revert branch/worktree |

## Cleanup

```bash
git worktree remove ../ratary-{slug}   # if used
git branch -d forge/{slug}               # after merge
```

## Docs

- Promote design draft to phase folder if gate PASS
- Update CHECKLIST / TASK_PROMPT when phase work completes

Then run `forge-remember`.
