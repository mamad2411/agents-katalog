---
name: new-form
description: Generate a Camunda Form (.form JSON) for user tasks. Use when creating forms for human task interaction.
argument-hint: "[form description]"
---

Generate a Camunda Form (.form JSON). Look up the current schemaVersion via Docs MCP. The form `id` must match the `formId` in the BPMN user task's `<zeebe:formDefinition>`.

$ARGUMENTS

Save to resources/.
