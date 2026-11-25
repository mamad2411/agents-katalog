---
name: ultracode
description: Enable, disable, or report Agent Workflow Kit ultracode mode in Antigravity.
---

# Ultracode

Toggle ultracode through the shared CLI:

```sh
agent-workflow-kit ultracode on --json
agent-workflow-kit ultracode off --json
agent-workflow-kit ultracode status --json
```

Ultracode is an explicit, persisted project toggle (`.agent-workflow-kit/config.json`); it is never ambient. Only enable it when the user asks. When on, treat workflow authoring as a standing opt-in and bias toward adversarial verification. Return the resulting ultracode state only.
