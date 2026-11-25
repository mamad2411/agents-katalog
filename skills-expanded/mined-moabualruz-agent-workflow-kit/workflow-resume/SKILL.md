---
name: workflow-resume
description: Resume an Agent Workflow Kit run record in Antigravity.
---

# Workflow Resume

Re-run a workflow, replaying the unchanged agent prefix from its journal:

```sh
agent-workflow-kit workflow-resume <run-id> --json
```

Resume re-runs the workflow with the original run's args and serves the longest unchanged prefix of `agent()` calls from the prior journal (recorded as `agent:cached` events); the first changed call and everything after it runs live. Read `workflow-events` on the original run to verify its `run:resumed` marker.
