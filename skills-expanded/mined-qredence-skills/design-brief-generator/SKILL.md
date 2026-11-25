---
name: design-brief-generator
description: Plan a Figma Design screen, component, flow, or Figma Make prototype through a short discovery interview, then produce a confirmed design brief without generating UI. Use when the user has a vague request, early product idea, unclear scope, competing constraints, or needs alignment before design generation.
---

# Design Brief Generator

Use this skill to decide what should be made before asking Figma Agent or Figma Make to make it.

The output is a confirmed design brief. Do not generate frames, components, prototypes, visual directions, or code while shaping.

## Output Mode

Choose the output mode from the user's request:

- If the request is vague, ask a short discovery round and then write a brief.
- If the request is mostly clear, write the brief directly and mark assumptions.
- If the request bundles unrelated jobs, recommend a split before briefing.
- If the user asks to proceed after the brief, stop using this skill and switch to the appropriate design, prompt, critique, layout, polish, or component workflow.

## Discovery Discipline

Ask only questions that change the result.

Default to one short question round. Ask at most three questions. Add a second round only when the first answers expose a material blocker.

Do not dump a questionnaire. State your likely read of the request and ask for correction when helpful.

## Question Bank

Choose from:

- What exact product surface, screen, flow, component, or prototype are we shaping?
- Who reaches it, in what situation, and what are they trying to do?
- What is the primary action or understanding the design must support?
- What real content, data, examples, or assets must the design carry?
- What states matter: first-run, empty, loading, error, success, disabled, permissions, long content, or overflow?
- What existing Figma frame, library, variables, styles, components, copy, or interaction model must remain authoritative?
- What must not change, even if a redesign would look cleaner?
- Is this for Figma Design, Figma Make, or both?
- What fidelity is needed: sketch, wireframe, high-fidelity screen, component spec, single flow, or interactive prototype?

Never ask for raw CSS values. Ask about product intent, constraints, and decision boundaries.

## Scope Gate

Before writing the brief, decide whether the request is one coherent job.

Recommend splitting when the request combines:

- product strategy and polished UI
- a whole app and a component system
- critique and replacement design
- Figma Design system authoring and Figma Make implementation
- multiple unrelated audiences, flows, or surfaces

When splitting is needed, recommend the smallest next brief to write first.

## Brief Structure

Use the smallest useful brief. For simple requests, write three to five bullets. For ambiguous or high-stakes work, use the full structure:

```markdown
## Confirmed Design Brief

### Job and Audience
- Surface:
- User:
- Context:
- Primary need:

### Outcome and Proof
- Primary action or understanding:
- Success criteria:
- Product-specific truth or evidence:

### Scope
- Figma target:
- Fidelity:
- Breadth:
- In scope:
- Out of scope:

### Design Direction
- Structural thesis:
- Visual authority:
- Interaction thesis:
- Key focal moment:

### Content and States
- Required content:
- Minimum, typical, and maximum content ranges:
- Required states:

### System Constraints
- Preserve:
- Use when available:
- Avoid:
- Open decisions:

### Next Prompt
- Recommended next Figma Agent or Figma Make instruction:
```

## Confirmation Rule

After returning the brief, ask for explicit confirmation or one correction round.

Stop after the brief. Do not continue into design generation unless the user confirms and asks to proceed.

## Quality Check

Before finalizing:

- The brief names one primary job.
- The user and situation are clear enough to guide design.
- Assumptions are labeled.
- Figma Design and Figma Make expectations are separated.
- The brief names what must remain untouched.
- Open decisions are explicit.
