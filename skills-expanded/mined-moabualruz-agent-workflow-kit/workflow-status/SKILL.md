---
name: workflow-status
description: Read an Agent Workflow Kit run status in Antigravity.
---

# Workflow Status

Read persisted run status through the shared CLI:

```sh
agent-workflow-kit workflow-status <run-id> --json
agent-workflow-kit workflow-status <run-id> --tree
agent-workflow-kit workflows --watch
```

Use the returned artifact paths instead of transcript scraping.
