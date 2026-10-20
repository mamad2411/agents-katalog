---
name: "mindforge-ui-phase"
description: "Generate UI design contract (UI-SPEC.md) for frontend phases"
---

<objective>
Create a UI design contract (UI-SPEC.md) for a frontend phase.
Orchestrates mindforge-ui-researcher and mindforge-ui-checker.
Flow: Validate → Research UI → Verify UI-SPEC → Done
</objective>

<execution_context>
@.agent/workflows/mindforge-ui-phase.md
@docs/References/ui-brand.md
</execution_context>

<context>
Phase number: $ARGUMENTS — optional, auto-detects next unplanned phase if omitted.
</context>

<process>
Execute @.agent/workflows/mindforge-ui-phase.md end-to-end.
Preserve all workflow gates.
</process>
