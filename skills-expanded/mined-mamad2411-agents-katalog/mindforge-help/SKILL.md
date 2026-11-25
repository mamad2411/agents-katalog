---
name: "mindforge-help"
description: "Show available MindForge commands and usage guide"
---

<objective>
Display the complete MindForge command reference.

Output ONLY the reference content below. Do NOT add:
- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
</objective>

<execution_context>
@.agent/workflows/mindforge-help.md
</execution_context>

<process>
Output the complete MindForge command reference from @.agent/workflows/mindforge-help.md.
Display the reference content directly — no additions or modifications.
</process>
