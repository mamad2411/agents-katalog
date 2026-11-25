---
name: workflows
description: List Agent Workflow Kit runs in Antigravity.
---

# Workflows

List persisted workflow runs without transcript spam:

```sh
agent-workflow-kit workflows --json
agent-workflow-kit workflows --watch
agent-workflow-kit workflow-status <run-id> --tree
```

Use the returned run IDs with `workflow-status`, `workflow-events`, `workflow-resume`, or `workflow-stop`.
