---
name: working
description: Enter worker mode — agent polls for tasks every 10 seconds and executes them automatically. Other agents or Dashboard can assign tasks to you. Type anything to exit worker mode.
disable-model-invocation: true
allowed-tools: Bash(bash:*), Read, Write, Edit
---

# Worker Mode

## Your Identity
!`bash -c 'cat .cortex/agent-identity.json 2>/dev/null | head -5 || echo "no identity"'`

## Enter Worker Loop

You are now in **worker mode**. Poll for tasks every 10 seconds:

Use the `/loop` command to poll:
```
/loop 10s cortex_task_pickup
```

When a task is found in the response:
1. Call `cortex_task_accept(taskId)` immediately
2. Execute the task described in the title/description
3. Call `cortex_task_update(taskId, status: "completed", result: {...})` when done
4. Continue polling for next task

If no tasks found, just wait for next poll cycle.

**To exit worker mode:** type any message or press Ctrl+C.

## Important
- Stay in this project directory while working
- Use cortex_code_search and cortex_knowledge_search before editing files
- Report progress via cortex_task_update(status: "in_progress", message: "...")
- Store findings via cortex_knowledge_store when you learn something new
