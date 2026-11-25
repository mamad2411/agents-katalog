---
name: "mindforge-do"
description: "Route freeform text to the right MindForge command automatically"
---

<objective>
Analyze freeform natural language input and dispatch to the most appropriate MindForge command.

Acts as a smart dispatcher — never does the work itself. Matches intent to the best MindForge command using routing rules, confirms the match, then hands off.

Use when you know what you want but don't know which `/mindforge-*` command to run.
</objective>

<execution_context>
@.agent/workflows/mindforge-do.md
@docs/References/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the do workflow from @.agent/workflows/mindforge-do.md end-to-end.
Route user intent to the best MindForge command and invoke it.
</process>
