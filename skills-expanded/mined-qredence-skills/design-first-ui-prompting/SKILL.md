---
name: design-first-ui-prompting
description: Turn a vague product, page, screen, component, or prototype request into a Figma-ready prompt with clear goal, audience, layout, typography, color, content, states, constraints, and non-goals. Use before asking Figma Agent or Figma Make to generate, revise, or refine UI when the user needs a stronger prompt rather than direct design execution.
---

# Design-First UI Prompting

Use this skill to convert an unclear UI request into a precise prompt for Figma Agent or Figma Make.

The output is a prompt or prompt brief. Do not generate UI unless the user explicitly asks you to apply the prompt after writing it.

## Output Mode

Choose the output mode from the user's request:

- If the user asks for a `prompt`, `brief`, or `instruction`, return only the Figma-ready prompt.
- If the user asks to `improve my prompt`, rewrite their prompt and briefly state what changed.
- If the user asks to `use this prompt`, first return the prompt and ask for confirmation unless the requested change is small and unambiguous.
- If the user asks for direct design work, use this skill only to structure the instruction before acting.

## Core Rule

Prompt like a design system, not like a wish.

Specify the product job, hierarchy, structure, content, visual system, and constraints before asking Figma to generate or revise the UI.

## Inputs

Use the user's request, selected Figma frame or Make context, and any explicitly attached references.

If the user gave a usable brief, do not ask questions. Convert it directly.

Ask at most three questions only when the answer would materially change the design:

- What is the single primary thing this screen, component, flow, or prototype must help the user understand or do?
- Who is the target user, and what situation are they in?
- What must be preserved: brand, layout, copy, components, variables, styles, or interaction model?

## Prompt Structure

Return one complete prompt using this structure:

```markdown
GOAL
- Build or revise:
- Target user:
- Primary outcome:
- Success criteria:

FIGMA CONTEXT
- Target: Figma Design / Figma Make / both
- Work area:
- Preserve:
- Use connected library, styles, components, or variables when available:
- Do not invent a new design system unless explicitly asked:

LAYOUT
- Scope:
- Primary reading or task path:
- Main regions:
- Hierarchy:
- Responsive or variant expectations:

TYPE
- Role-based type hierarchy:
- Intended tone:
- Copy density:
- Wrapping or long-content rules:

COLOR + MATERIAL
- Background:
- Text and surface contrast:
- Accent role:
- Effects, shadows, or materials:
- Accessibility constraints:

CONTENT
- Exact copy:
- Realistic replacement content when exact copy is missing:
- Required data ranges or edge cases:

STATES
- Required states:
- Empty:
- Loading:
- Error:
- Success:
- Disabled:
- Long-content:

INTERACTION
- Figma Design: describe visual feedback, states, and motion intent only when relevant.
- Figma Make: describe behavior, navigation, validation, and state changes.

CONSTRAINTS
- Must keep:
- Must avoid:
- Open decisions the agent should ask about before changing:

NEGATIVE PROMPT
- No generic filler.
- No decorative elements that do not support the task.
- No extra text beyond supplied copy unless realistic content is requested.
- No changes to unrelated frames or flows.
```

## Decision Rules

- If the user asks for Figma Design work, focus on frames, hierarchy, components, styles, variables, copy, states, and visual feedback.
- If the user asks for Figma Make work, include app behavior, state transitions, inputs, validation, and publishable prototype expectations.
- If a design system, connected library, selected frame, or brand direction exists, preserve it unless the user explicitly requests a new direction.
- Convert style requests into concrete choices: density, contrast, type roles, spacing rhythm, surface treatment, and imagery rules.
- Mark exact copy as exact copy. Do not ask the agent to rewrite it unless requested.
- Ask for one major design move per revision unless the user requested a replacement.
- Do not ask Figma Agent or Figma Make to use external files, scripts, or hidden context that was not provided.

## Quality Check

Before returning:

- The prompt has one clear goal.
- The primary hierarchy is explicit.
- The prompt names what to preserve and what not to touch.
- Figma Design expectations and Figma Make behavior are separated.
- The prompt does not depend on unsupported file access, helper scripts, or external assets.
