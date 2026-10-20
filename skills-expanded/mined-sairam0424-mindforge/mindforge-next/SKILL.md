---
name: "mindforge-next"
description: "Automatically advance to the next logical step in the MindForge workflow"
---

<objective>
Detect the current project state and automatically invoke the next logical MindForge workflow step.
No arguments needed — reads STATE.md, ROADMAP.md, and phase directories to determine what comes next.

Designed for rapid multi-project workflows where remembering which phase/step you're on is overhead.
</objective>

<execution_context>
@.agent/workflows/mindforge-next.md
</execution_context>

<process>
Execute the next workflow from @.agent/workflows/mindforge-next.md end-to-end.
</process>
