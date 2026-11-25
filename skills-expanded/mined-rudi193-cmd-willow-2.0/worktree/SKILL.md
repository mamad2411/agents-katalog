---
name: worktree
description: Every code change goes through a worktree branch + PR. No direct master commits — ever. Covers git worktree setup, Willow fork tracking, and PR flow.
---

# Worktree — Required Development Pattern

**This is a hard constraint, not a guideline.** Every change to the codebase goes through a worktree branch and a PR. Direct commits to master are banned.

## Start work

```bash
# 1. Create branch (simple) or isolated worktree directory (multi-session)
git checkout -b feat/<slug>
# — or —
git worktree add worktrees/<slug> -b feat/<slug>
```

```
# 2. Register a Willow fork (SOIL tracking)
fork_create(app_id="hanuman", title="<title>", created_by="hanuman", topic="<slug>")
# Save the returned fork_id

# 3. Log the branch
fork_log(fork_id=<fork_id>, component="git", type="branch", ref="feat/<slug>", app_id="hanuman")
```

Check `$WILLOW_HOME/session_anchor_${WILLOW_AGENT_NAME}.json` for an active `fork_id` before creating a new one.
Check open forks before starting: `fork_list(status="open", app_id="hanuman")`

## During work

- All commits go to the feature branch only
- Log KB writes: `fork_log(fork_id, "kb", "atom", atom_id, app_id="hanuman")`
- Branch naming: `fix/<slug>` · `feat/<slug>` · `chore/<slug>`

## Open PR

```bash
git push -u origin feat/<slug>
gh pr create --title "..." --body "..."
```

CI must pass. USER approves. Then merge.

## Teardown after merge

```bash
git worktree remove worktrees/<slug>   # only if worktree directory was used
git branch -d feat/<slug>
```

### Husk removal runs on the host (S18 exception)

A worktree directory is bind-mounted into **every** Kart sandbox, so `git worktree remove` / `rmdir` / `rm -rf` against it returns **EBUSY** inside bwrap — the cleanup must run host-side. This is the **one** sanctioned exception to the MCP-first / no-agent-Bash rule: agent `Bash` is permitted for a *single, unchained* `rm`/`rmdir`/`git worktree remove|prune` whose targets all live under a `/worktrees/` directory. Anything with chaining or substitution (`;`, `&&`, `|`, `` ` ``, `$(`) falls through to the normal guards. Enforced in `willow/fylgja/events/pre_tool.py` (`_is_worktree_cleanup`).

```bash
rm -rf ~/github/<repo>/worktrees/<slug>   # full dir → rm -rf (rmdir only removes an empty one)
git -C ~/github/<repo> worktree prune
```

```
fork_merge(fork_id=<fork_id>, outcome_note="merged to master", app_id="hanuman")
```

## Fork operations reference

| Operation | Call |
|-----------|------|
| Open fork | `fork_create(title, created_by, topic, app_id)` |
| Join existing | `fork_join(fork_id, component, app_id)` |
| Log branch/atom/task | `fork_log(fork_id, component, type, ref, app_id)` — type: branch/atom/task/thread |
| Check status | `fork_status(fork_id, app_id)` |
| List open | `fork_list(status="open", app_id)` |
| Merge (USER only) | `fork_merge(fork_id, outcome_note, app_id)` |
| Delete (USER only) | `fork_delete(fork_id, reason, app_id)` |

## Tips

- Worktrees share the git object store — add `worktrees/` to `.gitignore`
- Create the worktree at the **start** of scope, not midway through
- The Willow MCP server runs from the main repo — worktrees share it automatically
