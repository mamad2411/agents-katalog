---
name: agent-zero
description: "Create and manage Agent Zero autonomous tasks. Run goals, check status, cancel tasks, list history, and use pre-built templates."
metadata: {"thinkfleetbot":{"emoji":"🧠","requires":{},"always":true}}
---

# Agent Zero Skill

Agent Zero is an autonomous task execution engine running inside the ThinkFleetBot container. It can execute multi-step goals using tools like shell commands, Python scripts, filesystem operations, and web access.

## Run a Task

Create and start an Agent Zero task with a goal description:

```
/az run Research the latest trends in AI agent frameworks and summarize the top 5
```

The task runs asynchronously. You'll receive progress updates and a final summary with artifacts.

## Check Task Status

Get the current status and progress of a running or completed task:

```
/az status <taskId>
```

## Cancel a Task

Cancel a running task:

```
/az cancel <taskId>
```

## List Tasks

List recent Agent Zero tasks for this agent:

```
/az list
```

## Templates

List available pre-built task templates:

```
/az templates
```

Run a template by name:

```
/az template "Research Competitor" --company "Acme Corp" --market "SaaS"
```

## Task History

View completed task history with summaries:

```
/az history
```

## Constraints

Tasks run with configurable constraints:
- **Time budget**: Max execution time (default 300s, max 3600s)
- **Tool call limit**: Max number of tool invocations (default 20, max 200)
- **Allowed tools**: `web`, `filesystem`, `shell`, `python`

Override defaults when running:

```
/az run --time 600 --tools web,python Analyze this dataset and generate charts
```

## Health Check

Check if Agent Zero is running and healthy:

```
/az health
```

## Gateway Methods

These RPC methods are available through the ThinkFleetBot gateway:

| Method | Description |
|--------|-------------|
| `agentzero.health` | Check Agent Zero health status |
| `agentzero.task.create` | Create and start a new task |
| `agentzero.task.get` | Get task status by ID |
| `agentzero.task.cancel` | Cancel a running task |
| `agentzero.task.list` | List all tasks |
