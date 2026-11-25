---
name: team-orchestration
description: Use when evaluating whether to spawn agent teammates for a task, when managing an active team during the EXECUTE phase, or when file ownership conflicts or teammate coordination issues arise.
user-invocable: false
---

# Team Orchestration Skill

Reference material for Agent Teams mode in `/cs-loop` EXECUTE phase.

## Team Eligibility Check

Evaluate three signals after task creation in PLAN phase:

| Signal | Check | Threshold |
|--------|-------|-----------|
| Scope | Count tasks with no `blockedBy` dependencies | >= 3 independent tasks |
| Independence | Compare directory paths of independent tasks | No overlapping file scopes |
| Complexity | Estimate total work across all tasks | > simple feature or bug fix |

All three must be true AND `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be enabled. If env var not set, skip silently and use standard mode.

## Agent Matching

1. Read `.claude/agents/*.md` agent definition files
2. Match each work stream to the best-fit agent based on `expertise` arrays
3. Use the agent's `spawn_prompt`, `rules_to_load`, and `file_scope_hints`
4. Fall back to generic role prompts if no matching agent exists

## Teammate Spawning

**Default strategy: worktree-per-teammate** (eliminates file ownership conflicts).

1. Partition tasks into independent work streams (no overlapping files)
2. For each stream, create an isolated worktree:
   - Branch: `team/{agent-name}-{stream-id}`
   - Path: `.worktrees/team-{agent-name}`
3. Spawn teammate agent in the worktree directory
4. Agent receives: task list, quality gates, file scope, rules
5. On completion: run gates in worktree, merge if passing

**Fallback**: If tasks share files or worktrees unavailable, fall back to shared workspace with file ownership tracking (original behavior).

See `references/worktree-strategy.md` for full details, conflict resolution, and merge order.

**Performance note**: Do NOT use `--bare` for teammate agents - they need full MCP and settings context for quality gates. `--bare` is only appropriate for quick lookup subagents spawned during EXECUTE.

Require plan approval before teammates make changes (see [Plan Approval Protocol](#plan-approval-protocol) below).

## Plan Approval Protocol

Before a teammate makes any changes, they must submit a plan for lead approval. This prevents scope creep, architectural misalignment, and wasted work.

### When to Require Approval

Require approval when the teammate's planned work involves:
- Modifying > 3 files
- Architectural changes (new abstractions, interface changes, schema modifications)
- Ambiguous task descriptions where multiple valid approaches exist
- Changes that touch files outside the teammate's declared scope

### Message Format

**Teammate → Lead (request):**
```json
{
  "type": "plan_approval_request",
  "request_id": "approve-{task-id}-{timestamp}",
  "task_id": "{task-id}",
  "plan_summary": "Brief description of approach",
  "files_to_modify": ["path/to/file1", "path/to/file2"],
  "approach": "Detailed explanation of the implementation strategy",
  "alternatives_considered": "Other approaches and why this was chosen"
}
```

**Lead → Teammate (approval):**
```json
{
  "type": "plan_approval_response",
  "request_id": "{same request_id}",
  "decision": "approved",
  "feedback": "Optional guidance or constraints"
}
```

**Lead → Teammate (rejection):**
```json
{
  "type": "plan_approval_response",
  "request_id": "{same request_id}",
  "decision": "rejected",
  "reason": "Why the plan was rejected",
  "suggested_approach": "What to do instead"
}
```

### Lead Behavior

When reviewing a `plan_approval_request`:
1. Check that `files_to_modify` are within the teammate's declared scope
2. Verify the approach aligns with existing patterns (check DECISIONS.md if relevant)
3. Approve with optional feedback, or reject with a specific reason and suggested approach
4. Respond using the exact `request_id` from the request for correlation

### Teammate Behavior

- On **approval**: proceed with implementation as planned, incorporating any feedback
- On **rejection**: revise the plan based on `suggested_approach`, then resubmit a new request with a new `request_id`
- Do not begin any file modifications until `decision: "approved"` is received
- If no response after reasonable wait, send a follow-up ping referencing the original `request_id`

## Progress Monitoring

After spawning, switch to coordination-only mode:

1. Track progress via shared task list
2. Redirect teammates that drift from scope
3. Unblock teammates that report issues
4. Synthesize results as tasks complete

## Result Collection

When all teammate tasks complete:

1. Send shutdown requests to all teammates
2. Wait for shutdown confirmations
3. Review combined changes across all streams
4. Report: `[EXECUTE] Team complete: {completed}/{total} tasks`
5. Proceed to VERIFY with all changes

## Gotchas

- **File ownership conflicts**: Carefully partition file ownership — two teammates editing the same file causes "File modified since read" errors. If a teammate modifies a file you need, re-read before editing. The `task-completed.cjs` hook tracks file ownership and rejects tasks that create conflicts.
- **Teammate shutdown protocol**: Always send `shutdown_request` and wait for `shutdown_approved` before calling TeamDelete. TeamDelete fails if any members are still active — this is a hard requirement, not a suggestion.
- **MAX_TEAMMATES cap**: `teammate-idle.cjs` caps tracked teammates at 50, pruning oldest entries. If you see unexpected teammate state loss, this cap may have been hit.
- **team-state.json default shape**: Both `teammate-idle.cjs` and `task-completed.cjs` must use identical defaults (`teammates`, `completed_tasks`, `file_ownership`). Mismatched defaults cause crashes when the wrong hook creates the file first.
- **CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS**: Team mode silently degrades to solo mode if this env var is not set. Don't report "team not eligible" when the real issue is the missing env var.
- **completed_tasks cap**: Capped at 100 entries in team-state.json. Long-running team sessions may lose early task history.
- Worktree cleanup: Always `git worktree remove` after merge, even on failure - leaked worktrees consume disk
- Merge order matters: Merge agents that touch foundational files (types, interfaces) first
