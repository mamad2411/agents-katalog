---
name: workflow
description: Create, persist, and run an Agent Workflow Kit workflow in Antigravity.
---

# Workflow

Create, persist, and run a generated workflow through the shared CLI:

```sh
agent-workflow-kit workflow "<task>" --json
```

Use `--project-root "${AGENT_WORKFLOW_KIT_PROJECT_ROOT:-$PWD}"` when the active Antigravity workspace root is ambiguous.
<!-- AGENT_WORKFLOW_KIT_ULTRACODE_START -->
## Ultracode & multi-phase orchestration

Authoring and running a workflow spins up many subagents and spends real tokens. Author a workflow only when the user typed "workflow"/"workflows", asked for multi-agent orchestration, when the **ultracode** standing opt-in or keyword trigger applies, when a skill or command instructed it, or when the user named a saved workflow. Otherwise act directly or offer a workflow and let the user opt in.

**Ultracode** has three separate meanings in this kit. The standing opt-in is the persisted project behavior (`agent-workflow-kit ultracode on|off|status`, stored in `.agent-workflow-kit/config.json`) that author-runs a workflow for substantive tasks by default. The keyword trigger is recorded separately as `ultracodeKeywordTriggerEnabled` and is disabled when workflows are disabled. Model effort is host-owned: this standalone CLI reports model effort as unsupported and records `ultracodeEffortMode: "orchestration-only"` when orchestration is enabled. Turn ultracode on only when the user asks; when off, revert to the opt-in gate.

For larger work, decompose into a **sequence** of workflows (understand -> design -> implement -> review), inspecting each run with `workflow-run --stream`, `workflow-events --follow`, or `workflow-status --tree` between phases rather than one giant run.
<!-- AGENT_WORKFLOW_KIT_ULTRACODE_END -->
