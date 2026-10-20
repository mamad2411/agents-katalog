---
name: temporal-orchestrate
description: "Orchestrate durable workflows with automatic retries using Temporal at {{TEMPORAL_HOST}}:{{TEMPORAL_PORT}}."
metadata:
  openclaw:
    emoji: "⏱️"
---

# Temporal Workflow Orchestration

Temporal is available at `{{TEMPORAL_HOST}}:{{TEMPORAL_PORT}}` within the Docker network.

## List Workflows

```bash
tctl --address {{TEMPORAL_HOST}}:{{TEMPORAL_PORT}} workflow list
```

## Start a Workflow

```bash
tctl --address {{TEMPORAL_HOST}}:{{TEMPORAL_PORT}} workflow start \
  --taskqueue my-queue \
  --workflow_type MyWorkflow \
  --input '{"key": "value"}'
```

## Tips for AI Agents

- Temporal guarantees workflow completion even through failures.
- Use activities for side-effect operations and workflows for orchestration.
- The Web UI at port 8080 provides workflow visualization.
