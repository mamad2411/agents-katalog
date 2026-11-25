---
name: workflow-stop
description: Stop an Agent Workflow Kit run record in Antigravity.
---

# Workflow Stop

Stop a workflow record while keeping artifacts available:

```sh
agent-workflow-kit workflow-stop <run-id> --json
```

Follow with `workflow-status` or `workflow-events` to verify persisted state.
