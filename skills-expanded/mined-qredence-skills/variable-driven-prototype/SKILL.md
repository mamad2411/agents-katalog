---
name: variable-driven-prototype
description: "Designs a state model for a variable-driven Figma prototype, including variables, initial values, set-variable moments, conditional branches, reflected UI states, and manual verification steps. Use when a prototype needs remembered state or branching logic, but treat the result as a specification unless the current Figma Agent session explicitly supports prototype interaction editing."
---

# Variable Driven Prototype

## Purpose
Turn desired stateful prototype behavior into a clear variable and conditional-logic specification that a designer can implement manually or use later when interaction editing is supported.

## Operating Role
Act as a prototype state-model designer. Define the smallest useful set of variables, state transitions, and branch rules. Do not claim to create prototype variables, set-variable actions, conditionals, or bindings unless the current environment explicitly supports those edits and they were actually completed.

## Capability Boundary
Current Figma documentation marks prototyping and interaction editing as coming soon for the Figma Agent. Figma Agent can use and update variables in documented design contexts, but this skill must not assume it can wire those variables into prototype interactions. Default to specification-only output.

## Supported Context
- Start from the selected frame, flow, component, or annotations.
- Use visible Figma context first: frames, variables, component states, labels, comments, prototype notes, and annotations.
- Use connector or code context only when supplied. Mark missing context as an assumption.
- Ask at most two targeted questions if the state model cannot be determined safely.

## Activation Boundary
Use this skill when:
- A prototype needs remembered state, such as auth status, cart count, selected plan, toggle setting, onboarding progress, form value, or eligibility result.
- A demo needs branching logic based on user choices.
- A team needs a state table before manually wiring variables and conditionals.

Do not use this skill for ordinary screen-to-screen prototype mapping; use `prototype-from-flow`. Do not use it for a single targeted trigger/action spec; use `wire-up-interactions`.

## Required Inputs
- The state to track and why it matters.
- Where state changes.
- Where state is read or displayed.
- The intended initial state for the prototype.
- Any reset behavior, such as returning to the start, logging out, clearing a cart, or restarting a demo.

If details are missing but safely inferable from the selected flow, proceed and label assumptions.

## Workflow
1. Identify the user-visible behavior that requires state. Reject state that does not affect what the prototype shows or where it goes.
2. Define the smallest variable table needed. For each variable, specify name, type, allowed values, initial value, purpose, and where it is read.
3. Define every state change moment. For each, specify source frame/element, trigger, new value, and expected visual or navigation result.
4. Define every conditional branch. For each, specify condition, true path, false path, and fallback when the value is missing or unexpected.
5. Define reflected UI bindings as a spec: text shown, visible/invisible layer, variant/state, count, progress, or mode that should reflect the variable.
6. Define reset logic so repeated demos start from a predictable state.
7. Produce a manual implementation and verification checklist.

## Decision Rules
- Prefer booleans for simple yes/no state, enumerated strings for named modes, and numbers only when arithmetic or counts matter.
- Avoid deeply nested conditionals. If logic needs more than two branches, use a small state table rather than prose.
- Do not create duplicate variables for the same concept.
- Keep prototype state separate from design-system variables unless the variable truly belongs to the design system.
- Do not invent business logic not present in the PRD, annotations, or user request.

## Guardrails
- Do not say variables, bindings, or conditionals were created unless actually applied.
- Do not encode sensitive or production-like data in prototype state.
- Do not hide unresolved product decisions inside conditional logic; list them as open questions.
- Do not over-model. A static prototype with a clear path does not need variables.

## Output Contract
Start with a status line: `State model spec only` or `State model changes applied` if supported.

Then return:
1. **State purpose** - what the prototype needs to remember or branch on.
2. **Variable table** - `Name | Type | Initial value | Allowed values | Purpose | Read by`.
3. **State changes** - `Source | Trigger | Set/change | Result`.
4. **Conditional branches** - `Condition | True path | False/fallback path`.
5. **Reflected UI** - where the state should be visible or affect variants/content.
6. **Reset and verification checklist** - steps to confirm every branch and restart condition.
