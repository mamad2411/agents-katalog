---
name: ux-to-prompts
description: "Turn a UX spec into build-order prompts for UI tools like v0 or Bolt."
disable-model-invocation: true
---

# Skill: UX Spec to Build-Order Prompts

> Adapted from UX-spec-to-prompts skill

## Overview

Transform a UX specification into a sequence of self-contained prompts optimized for UI generation tools (v0, Bolt, Claude, Stitch, etc.). Each prompt builds one discrete feature/view with full context included.

## When to Use

- After `/ux-spec`, when you want to feed specs into external UI generation tools
- When a UX spec is too large for a single prompt
- When you need build-order sequencing (foundations → features → polish)

**Not for:** Quick component requests, features that fit in one prompt, or projects where you're building with code directly (use `/execute` instead).

## Build Order

Generate prompts in this sequence:

| Phase | What to Include | Why First |
|-------|-----------------|-----------|
| **Foundation** | Design tokens, shared types, base styles | Everything depends on these |
| **Layout Shell** | Page structure, navigation, panels | Container for all features |
| **Core Components** | Primary UI elements (nodes, cards, inputs) | Building blocks for features |
| **Interactions** | Drag-drop, connections, pickers | Depend on components existing |
| **States & Feedback** | Empty, loading, error, success states | Refinement of existing elements |
| **Polish** | Animations, responsive, edge cases | Final layer |

## Extraction Process

### Step 1: Identify Atomic Units

Read the UX spec and list discrete buildable features:
- Each screen/view
- Each reusable component
- Each interaction pattern
- Each state variation

### Step 2: Map Dependencies

For each unit, note what it requires:
- "Node card requires design tokens"
- "Connection lines require nodes to exist"
- "Lens picker requires prompt field"

### Step 3: Sequence by Dependency Graph

Order units so dependencies come first. Group tightly coupled items into single prompts.

### Step 4: Write Self-Contained Prompts

For each prompt:
1. Re-state relevant context — don't assume reader saw previous prompts
2. Include specific measurements from the spec
3. Include all states from state design (Pass 5)
4. Include interaction details from affordances (Pass 3)
5. Set boundaries — what this prompt does NOT include

## Prompt Structure

Each generated prompt follows this template:

```markdown
## [Feature Name]

### Context
[What this feature is and where it fits in the app]

### Requirements
- [Specific behavior/appearance requirement]
- [Include relevant specs: dimensions, colors, states]

### States
- Default: [description]
- [Other states from spec]

### Interactions
- [How user interacts]
- [Keyboard support if applicable]

### Constraints
- [Technical or design constraints]
- [What NOT to include]
```

## Self-Containment Rules

Each prompt MUST include:
- Enough context to understand the feature in isolation
- All visual specs (colors, spacing, dimensions) relevant to that feature
- All states that feature can be in
- All interactions for that feature

Each prompt MUST NOT:
- Reference "see previous prompt" or "as described earlier"
- Assume knowledge from other prompts
- Leave specs vague ("appropriate styling")

## Output

Write to `docs/plans/Build-Order-Prompts-{topic}.md` with this structure:

```markdown
# Build-Order Prompts: [Project Name]

## Overview
[1-2 sentence summary]

## Build Sequence
1. [Prompt name] - [brief description]
2. [Prompt name] - [brief description]
...

---

## Prompt 1: [Feature Name]
[Full self-contained prompt]

---

## Prompt 2: [Feature Name]
[Full self-contained prompt]
```

## Quality Checklist

Before finalizing:
- Every measurement from spec is captured in a prompt
- Every state from spec is captured in a prompt
- Every interaction from spec is captured in a prompt
- No prompt references another prompt
- Build order respects dependencies
- Each prompt could be given to someone with no context

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Prompts too large (whole spec in one) | Break into atomic features |
| Prompts reference each other | Re-state needed context inline |
| Missing states | Cross-reference UX spec's state design (Pass 5) |
| Vague measurements ("good spacing") | Use exact values from spec |
| Wrong build order | Check dependency graph |
| Duplicated component definitions | Each component defined once, in first prompt that needs it |
