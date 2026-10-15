---
name: code-brainstorming
description: Turn coding ideas into approved designs and planning-ready implementation briefs before coding starts. Use for new features, meaningful behavior changes, ambiguous implementation requests, refactors that change system shape, or early architecture and design discussions. Do not use for tiny obvious edits, isolated typo fixes, trivial null checks, or other straightforward bug fixes that do not need design work.
---

# Brainstorming

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

## Hard Gate

- Do not write code.
- Do not scaffold files or projects.
- Do not take implementation action until the design brief has been presented and approved.

## Workflow

### 1. Explore context first

- Read relevant files, docs, types, configs, and recent changes before asking intent questions.
- Follow existing patterns instead of inventing unrelated ones.
- Assess scope early. If the request spans multiple independent subsystems, say so and help decompose it before refining one slice.

### 2. Clarify intent one question at a time

- Ask one question per message.
- Prefer concrete multiple-choice questions when they reduce ambiguity.
- Focus on purpose, constraints, success criteria, and boundaries the user cares about.
- Do not ask questions that the repository can answer.

### 3. Identify gray areas

- Convert the request into specific decisions that will change the design.
- Focus on behavior, interfaces, data flow, states, failure handling, and testing expectations as appropriate.
- Keep scope fixed. If the user suggests a new capability, mark it as deferred and return to the current change.

### 4. Compare approaches

- Present 2-3 viable approaches.
- Lead with the recommended option.
- Explain tradeoffs in terms of codebase fit, complexity, flexibility, and user goals.

### 5. Present the design in sections

- Present small sections sized to the complexity of the change.
- Cover the parts that matter: architecture, components, data flow, edge cases, error handling, and testing.
- Ask for confirmation after each section before moving on.
- Revise when the user pushes back or new constraints appear.

### 6. Synthesize the approved brief

- Produce a concise planning brief in chat after the design is approved.
- Make the brief concrete enough that a planner or engineer can use it without repeating discovery.

Use this structure:

```md
## Goal

## Scope / Non-Goals

## Key Decisions

## Recommended Approach

## Risks / Unknowns

## Open Follow-Ups
```

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design, get approval before moving on
- **Be flexible** - Go back and clarify when something doesn't make sense
- **Question** - Call out assumptions explicitly.