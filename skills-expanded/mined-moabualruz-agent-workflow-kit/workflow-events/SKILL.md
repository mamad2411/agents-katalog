---
name: workflow-events
description: Read Agent Workflow Kit event streams in Antigravity.
---

# Workflow Events

Read progress events through the shared CLI:

```sh
agent-workflow-kit workflow-events <run-id> --json
agent-workflow-kit workflow-events <run-id> --follow
```

Use `--follow` for event-driven updates until terminal status; with `--json`, it prints JSONL.

Use events to inspect phases, child workflow markers, model requests, and terminal run state.
