---
name: team-mode
description: Team Mode - parallel multi-agent coordination for complex tasks
category: coordination
exposure: standard
---

# Team Mode

Team Mode enables parallel multi-agent coordination. OFF by default. Enable via `team_mode.enabled` in config.

## When to use

- Split a large job across several agents
- Keep a lead agent focused while member agents work in parallel
- Use worktree mode for isolated code changes

## Eligible agents

**Primary agents (can be team members):**
- `orchestrator` - Main coordinator, plans + delegates
- `atlas` - Plan executor, todo management
- `bio-orchestrator` - Biological science specialist

**Conditional:**
- `deep-worker` - Deep code modification (requires high-context model)

**Hard-reject (read-only, use delegate-task instead):**
- `prometheus` - Plan-mode-only
- All subagents: `explorer`, `librarian`, `oracle`, `designer`, `fixer`, `observer`, `council`, `councillor`, `metis`, `momus`, `multimodal-looker`, `reviewer`

## Member kinds

- `kind: "subagent_type"` - Direct agent (orchestrator, atlas, bio-orchestrator)
- `kind: "category"` - Routed through category system with specified model

## Lifecycle

1. **Create team**: `team_create({ teamName: "my-team" })` or `team_create({ inline_spec: {...} })`
2. **Assign work**: `team_send_message` or `team_task_create`
3. **Track progress**: `team_task_list`, `team_status`
4. **Shutdown**: `team_shutdown_request` → `team_approve_shutdown` / `team_reject_shutdown`
5. **Delete team**: `team_delete` when done

## Tools

| Tool | Purpose |
|------|---------|
| `team_create` | Create a new team |
| `team_delete` | Delete a team |
| `team_send_message` | Send message to member |
| `team_task_create` | Create task |
| `team_task_list` | List tasks |
| `team_task_update` | Update task status |
| `team_task_get` | Get task details |
| `team_status` | Get team status |
| `team_list` | List all teams |
| `team_shutdown_request` | Request member shutdown |
| `team_approve_shutdown` | Approve shutdown |
| `team_reject_shutdown` | Reject shutdown |

## Communication rules

- Use `team_send_message` to communicate (not plain text)
- Use `to: "lead"` for lead, `to: "<name>"` for specific member
- Members cannot call `delegate-task` (budget is zero)
- No nested teams (members cannot call `team_create`)

## Bounds

- Max 8 members
- Max 4 parallel workers
- Max 32KB per message
- Max 256KB unread inbox

---

## Two-Stage Review (Subagent-Driven Development)

When executing implementation plans with independent tasks, use this pattern:

### The Pattern

For each task:
1. **Implementer** — Executes the task, writes code, runs tests
2. **Spec Reviewer** — Verifies code matches the specification
3. **Quality Reviewer** — Checks code quality, style, best practices

### Stage 1: Spec Compliance Review

After implementer completes a task, dispatch a spec reviewer:

```
task(subagent_type="oracle", prompt="Review this implementation for spec compliance:
- Does it match the requirements?
- Are all acceptance criteria met?
- Are there any missing features?
Return: PASS/FAIL with specific issues.")
```

### Stage 2: Code Quality Review

If spec review passes, dispatch a quality reviewer:

```
task(subagent_type="oracle", prompt="Review this code for quality:
- Code style and readability
- Error handling
- Performance considerations
- Security concerns
Return: PASS/FAIL with specific issues.")
```

### Execution Flow

```
Task assigned to implementer
    ↓
Implementer completes task
    ↓
Spec reviewer dispatched
    ↓
PASS? → Quality reviewer dispatched
FAIL? → Implementer fixes issues, re-review
    ↓
PASS? → Task marked complete
FAIL? → Implementer fixes issues, re-review
```

### Benefits

- **Isolated context** — Each reviewer gets fresh context
- **Focused review** — Spec and quality reviewed separately
- **Fast iteration** — Issues caught early
- **High quality** — Two independent checks per task

### When to Use

| Scenario | Use Two-Stage Review? |
|----------|----------------------|
| Complex feature with multiple tasks | Yes |
| Simple single-task change | No (use auto-review) |
| High-risk changes (security, data) | Yes |
| Quick fixes | No |
| User explicitly asks for thorough review | Yes |

---

## Integration with Our Workflow

- **Plan execution:** Use `plan-protocol` for task breakdown
- **Task implementation:** Use `test-driven-development`
- **Spec review:** Use oracle agent
- **Quality review:** Use oracle agent
- **Final review:** Use `auto-review` (todo-continuation)
- **Debugging:** Use `systematic-debugging` if issues found
