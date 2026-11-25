---
name: "merge"
description: "Merge the winning agent's branch into base, archive losers, and clean up worktrees. Use when the user runs /hub:merge or asks to land the winning AgentHub result and tidy the session."
command: /hub:merge
---

# /hub:merge — Merge Winner

Merge the best agent's branch into the base branch, archive losing branches via git tags, and clean up worktrees.

## Usage

```
/hub:merge                                       # Merge winner of latest session
/hub:merge 20260317-143022                       # Merge winner of specific session
/hub:merge 20260317-143022 --agent agent-2       # Explicitly choose winner
```

## What It Does

### 1. Identify Winner

If `--agent` specified, use that. Otherwise, use the #1 ranked agent from the most recent `/hub:eval`.

### 2. Merge Winner

```bash
git checkout {base_branch}
git merge --no-ff hub/{session-id}/{winner}/attempt-1 \
  -m "hub: merge {winner} from session {session-id}

Task: {task}
Winner: {winner}
Session: {session-id}"
```

### 3. Archive Losers

For each non-winning agent:

```bash
# Create archive tag (preserves commits forever)
git tag hub/archive/{session-id}/{agent-id} hub/{session-id}/{agent-id}/attempt-1

# Delete branch ref (commits preserved via tag)
git branch -D hub/{session-id}/{agent-id}/attempt-1
```

### 4. Clean Up Worktrees

```bash
python {skill_path}/scripts/session_manager.py --cleanup {session-id}
```

### 5. Post Merge Summary

Write `.agenthub/board/results/merge-summary.md`:

```markdown
---
author: coordinator
timestamp: {now}
channel: results
---

## Merge Summary

- **Session**: {session-id}
- **Winner**: {winner}
- **Merged into**: {base_branch}
- **Archived**: {loser-1}, {loser-2}, ...
- **Worktrees cleaned**: {count}
```

### 6. Update State

```bash
python {skill_path}/scripts/session_manager.py --update {session-id} --state merged
```

## Safety

- **Confirm with user** before merging — show the diff summary first
- **Never force-push** — merge is always `--no-ff` for clear history
- **Archive, don't delete** — losing agents' commits are preserved via tags
- **Clean worktrees** — don't leave orphan directories on disk

## After Merge

Tell the user:
- Winner merged into `{base_branch}`
- Losers archived with tags `hub/archive/{session-id}/agent-{N}`
- Worktrees cleaned up
- Session state: `merged`

## Purpose
Merge the winning AgentHub agent branch into the base branch, archive the losers as tags, and clean up worktrees.

## When to use
After `/hub:eval` has ranked agents, or the user asks to land the winning AgentHub result.

## When NOT to use
- No AgentHub session or no ranked winner yet -> run eval first.
- Ordinary git merges outside AgentHub.

## Inputs
Session id (default: latest), optional `--agent` to force a winner, clean base branch.

## Core workflow
1. Identify the winner (`--agent` or top-ranked agent).
2. Merge the winner into the base branch.
3. Tag each losing branch (archive tag) then delete the branch ref.
4. Remove worktrees.
5. Post a merge summary to the board.

## Edge cases and failure handling
- Merge conflicts -> resolve (see resolving-merge-conflicts) before archiving losers.
- Dirty base branch -> stop and ask the user to commit or stash.

## Validation
- Base contains the winner commits; every loser has an archive tag; worktrees are gone; build/tests pass on base.

## Output requirements
Merge summary: winner, tags created, worktrees removed.

## Example
```text
`/hub:merge 20260317-143022 --agent agent-2` -> merge agent-2, tag others, clean up.
```

## Related skills
hub-init, hub-status, board
