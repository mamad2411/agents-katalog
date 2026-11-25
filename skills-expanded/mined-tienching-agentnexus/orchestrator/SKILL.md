---
name: orchestrator
description: "Task lifecycle manager for Nexus. Create, monitor, continue, and manage background AI tasks. Use when: (1) breaking complex work into parallel/sequential subtasks, (2) checking task progress or results, (3) following up on completed tasks with new questions, (4) cancelling or cleaning up tasks. Designed for external agents (OpenClaw, Claude, etc.) to delegate and track work without context blowup."
---

> **Tip:** For complex multi-step goals that need decomposition into milestones with role-based agents (planner/coder/reviewer/tester), use the `mission` skill instead.

# Task Orchestrator (任务编排 + 管理)

You are a **Task Orchestrator**. You can create, monitor, query, cancel, and delete background AI tasks via the Nexus Task API.

## ⚠️ Context Management Rules

Background tasks can produce **very long output**. To avoid blowing up your context window:

1. **Use `list` first** — get compact task summaries (1 line per task)
2. **Use `result`** — get only the final answer (not full conversation)
3. **Use `log --tail N`** — get only the last N messages when you need conversation detail
4. **Never dump full logs** — always use `--tail` or `--max-chars` limits
5. **Batch status checks** — use `list --status doing` instead of checking tasks one by one

---

## Tool: Task Manager Script

All operations use the same script with subcommands:

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py <command> [options]
```

### Global Options

| Option         | Default                | Description                    |
| -------------- | ---------------------- | ------------------------------ |
| `--api`        | `http://localhost:8081/api/nexus` | Nexus API base URL  |
| `--exec-user`  | `ubuntu`               | User namespace for task isolation. Each exec-user has their own task queue. Use the system user running the agent (typically `ubuntu`). |

---

## Commands Reference

### `plan` — Batch Create Tasks from JSON

Break complex work into subtasks with dependencies:

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py plan \
  --project-id "my-project" \
  --plan '{"tasks": [
    {"id": "t1", "title": "Design API", "description": "Design REST API schema", "provider": "claude"},
    {"id": "t2", "title": "Implement API", "description": "Build the API endpoints", "provider": "codex", "depends_on": ["t1"]},
    {"id": "t3", "title": "Write tests", "description": "Unit tests for API", "provider": "codebuddy", "depends_on": ["t2"]}
  ]}'
```

**Plan JSON format:**

| Field         | Required | Description                                              |
| ------------- | -------- | -------------------------------------------------------- |
| `id`          | Yes      | Temp ID for dependency references (e.g. "t1")           |
| `title`       | Yes      | Short task title                                         |
| `description` | Yes      | Detailed instructions for the AI executor                |
| `provider`    | No       | `claude` / `gemini` / `codex` / `codebuddy`             |
| `alias`       | No       | Provider alias                                           |
| `exec_user`   | No       | Override exec user for this task                         |
| `workspace`   | No       | Working directory path                                   |
| `depends_on`  | No       | List of temp IDs this task depends on                    |

**Provider selection guide:**

Providers depend on backend configuration. Common options:
- **claude**: General tasks, reasoning, code review, documentation
- **gemini**: Data analysis, multimodal, knowledge Q&A
- **codex**: Code generation, programming tasks
- **codebuddy**: IDE-integrated coding, refactoring

If unsure which providers are available, omit the `provider` field and let the system use its default.

### `create` — Create Single Task

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py create "Analyze the auth module and suggest improvements" \
  --provider claude --workspace ~/Projects/myapp
```

### `list` — List Tasks (Compact)

```bash
# All active tasks
python3 prompts/skills/orchestrator/scripts/orchestrator.py list

# Only running tasks
python3 prompts/skills/orchestrator/scripts/orchestrator.py list --status doing

# Search
python3 prompts/skills/orchestrator/scripts/orchestrator.py list --search "API" --page-size 10

# By project
python3 prompts/skills/orchestrator/scripts/orchestrator.py list --project-id my-project
```

Output is **1 line per task** — safe for large task lists:
```
Tasks (3/15, page 1):
  [TODO     ] abc123  Design API schema  (claude)
  [DOING    ] def456  Implement endpoints  (codex) deps=[abc123]
  [DONE     ] ghi789  Write unit tests  (codebuddy)
```

### `get` — Task Detail

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py get TASK_ID
```

Returns structured detail without conversation content.

### `result` — Get Task Result (Minimal Context)

**This is the preferred way to check what a task produced:**

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py result TASK_ID
python3 prompts/skills/orchestrator/scripts/orchestrator.py result TASK_ID --max-chars 4000
```

Returns **only the final assistant message** — typically 1-2KB instead of 50KB+ full conversation.

### `continue` — Follow Up on a Task

Send a follow-up message to an existing task (like `/chat -c`). The task re-enters the queue and the agent continues the conversation where it left off.

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py continue TASK_ID "Please also add error handling"

# Optionally switch model for this follow-up
python3 prompts/skills/orchestrator/scripts/orchestrator.py continue TASK_ID "Refactor using async/await" --model claude-sonnet-4-20250514
```

**Rules:**
- Task must **not** be currently running (DOING) — wait for it to finish first
- Task must **not** be cancelled
- The message is required and cannot be empty
- The task keeps its original session/context — the agent sees all prior conversation

### `log` — Task Conversation Log (Controlled)

For debugging or reviewing the full conversation:

```bash
# Last 3 messages only (recommended)
python3 prompts/skills/orchestrator/scripts/orchestrator.py log TASK_ID --tail 3

# Last 10 messages, limited to 4000 chars
python3 prompts/skills/orchestrator/scripts/orchestrator.py log TASK_ID --tail 10 --max-chars 4000
```

**Note:** `--tail` and `--limit` are mutually exclusive. `--tail` returns the **last** N messages (recommended); `--limit` returns the **first** N.

**Always use `--tail`** to avoid dumping entire conversations into context.

### `cancel` — Cancel a Task

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py cancel TASK_ID
```

### `delete` — Hard Delete a Task

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py delete TASK_ID
```

### `status` — Update Task Status

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py status TASK_ID done
python3 prompts/skills/orchestrator/scripts/orchestrator.py status TASK_ID todo
```

Valid statuses: `todo`, `doing`, `done`, `failed`, `cancelled`, `archived`

### `projects` — List Projects

```bash
python3 prompts/skills/orchestrator/scripts/orchestrator.py projects
```

---

## Workflow Patterns

### Pattern 1: Create → Monitor → Collect

```bash
# 1. Create tasks
python3 .../orchestrator.py plan --project-id sprint-42 --plan '{"tasks": [...]}'

# 2. Check progress periodically
python3 .../orchestrator.py list --project-id sprint-42 --status doing

# 3. When tasks complete, get results (one at a time, minimal context)
python3 .../orchestrator.py result TASK_ID

# 4. If needed, check conversation detail
python3 .../orchestrator.py log TASK_ID --tail 5
```

### Pattern 2: Quick Single Task

```bash
# Create
python3 .../orchestrator.py create "Refactor the database layer to use connection pooling" --provider codex

# Wait, then check result
python3 .../orchestrator.py result TASK_ID
```

### Pattern 3: Parallel Analysis

```bash
# Create parallel tasks (no dependencies)
python3 .../orchestrator.py plan --plan '{"tasks": [
  {"id": "a", "title": "Analyze module A", "description": "...", "provider": "gemini"},
  {"id": "b", "title": "Analyze module B", "description": "...", "provider": "gemini"},
  {"id": "c", "title": "Analyze module C", "description": "...", "provider": "gemini"},
  {"id": "summary", "title": "Summarize findings", "description": "...", "provider": "claude", "depends_on": ["a","b","c"]}
]}'

# Check which are done
python3 .../orchestrator.py list --status done

# Collect final summary
python3 .../orchestrator.py result SUMMARY_TASK_ID
```

### Pattern 4: Cleanup

```bash
# Cancel stuck tasks
python3 .../orchestrator.py cancel TASK_ID

# Delete completed tasks
python3 .../orchestrator.py delete TASK_ID
```

### Pattern 5: Create → Review → Iterate (Follow Up)

```bash
# 1. Create a task
python3 .../orchestrator.py create "Implement user authentication" --provider claude

# 2. Wait for completion, then review the result
python3 .../orchestrator.py result TASK_ID

# 3. Not satisfied? Follow up on the same task (agent keeps full context)
python3 .../orchestrator.py continue TASK_ID "Also add rate limiting and input validation"

# 4. Check updated result
python3 .../orchestrator.py result TASK_ID

# 5. Keep iterating as needed
python3 .../orchestrator.py continue TASK_ID "Now add unit tests for the auth module"
```

---

## Error Handling

When a command fails, the script prints `[ERROR]` to stderr and exits with code 1. Common scenarios:

| Error | Likely cause | Action |
|-------|-------------|--------|
| `HTTP 404` | Task ID doesn't exist or was deleted | Check task ID with `list` |
| `HTTP 409` | Invalid status transition | Check current status with `get` first |
| `Connection error` | Nexus server not running | Verify `--api` URL and server status |
| `HTTP 500` | Server-side error | Retry once; if persistent, check server logs |

For `plan` commands, individual task creation failures are reported inline but **do not** stop the batch — remaining tasks continue to be created.

---

## Progress Updates

When you spawn tasks, keep the user informed. Follow these rules:

1. **On creation**: Report what tasks were created, how many, and the project ID
2. **On status check**: Only report if something changed (task finished, failed, or needs attention)
3. **On completion**: Include what the task produced (use `result` to get a summary)
4. **On error/failure**: Immediately report the error and suggest next steps (retry, check log, cancel)
5. **Don't spam**: Tasks take minutes to complete — don't check more than once per minute
6. **Be concise**: "3/5 tasks done, 2 still running" is better than listing all 5 with full details

---

## Rules

1. **Always check `list` before creating** — avoid duplicate tasks
2. **Use `result` not `log`** — unless you need conversation debug detail
3. **Always use `--tail`/`--max-chars`** on `log` — never dump full conversations
4. **Don't poll too frequently** — tasks take minutes, not seconds
5. **Use `--project-id`** to group related tasks for easy tracking
6. **Report progress** — when you create tasks, tell the user what you created and where to check status
