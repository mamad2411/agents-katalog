---
name: reference-driven-design
description: Build an evidence-backed visual reference brief before UI concept or polish work. Use when a product needs a modern visual direction, category-aware references, comparative design analysis, or protection from generic AI-generated styling without copying a specific brand.
---

# Reference-Driven Design Skill

## Role

Translate current product and platform references into an abstract, traceable visual direction.

## Mission

Improve visual judgment without turning taste, trends, or one admired product into unsupported design rules.

## When To Use

- A user asks for a more modern, polished, premium, expressive, or product-specific interface.
- A new surface needs a visual direction before implementation.
- Existing UI feels generic but the workflow and object model are already clear.
- A prompt needs reference categories and explicit anti-copy constraints.

## When Not To Use

- Product direction, user goal, or object model is unresolved.
- The task is a narrow visual bug with an existing token and component answer.
- No source, screenshot, product behavior, or graph context is available; record a research gap first.

## Inputs

- Product goal, primary action, audience, and platform.
- Current UI or implementation.
- Existing components, tokens, and product design direction.
- Focused graph context from `npm run context`.
- Supplied references or traceable current product and platform evidence.

## Process

1. Resolve graph context for the target task.
2. Classify the surface by product type, workflow density, platform, and emotional tone.
3. Select two or three relevant reference families, not a single brand to imitate.
4. For each source, separate observed behavior from interpretation.
5. Extract reusable abstractions:
   - content and functional layers;
   - hierarchy and density;
   - typography and shape roles;
   - material and color meaning;
   - state and motion behavior;
   - responsive and input adaptation.
6. Map recommendations to existing research, rules, patterns, and tokens.
7. Mark unsupported ideas as observations or research needs instead of instructions.
8. Define what must not be copied: branding, proprietary assets, distinctive composition, or platform-inappropriate effects.
9. Hand the brief to `visual-designer`, `motion-designer`, or `prompt-architect`.

## Output Format

```md
## Reference Brief
- Product category:
- User goal:
- Platform and density:
- Evidence date:

## Reference Matrix
| Source | Observed behavior | Reusable abstraction | Limit |
| --- | --- | --- | --- |

## Visual Direction
- Content layer:
- Functional layer:
- Focal emphasis:
- Typography and shape:
- State and motion:
- Responsive adaptation:

## Graph Traceability
- Research:
- Rules:
- Patterns:
- Missing evidence:

## Anti-Copy Boundary
- Do not copy:
- Platform constraints:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Recommendations come from observable source behavior.
- At least two reference families are compared when the task is exploratory.
- Product purpose determines expression level and density.
- Content and primary action remain dominant.
- Platform-specific materials have fallbacks.
- The brief names unsupported ideas as gaps.
- No specific brand composition or proprietary asset is copied.

## Related Research

- `RESEARCH-00009` Expressive System UI In 2026
- `RESEARCH-00010` Motion As State Continuity
- `RESEARCH-00011` Contextual And Observable Agentic Interfaces

## Related Rules

- `RULE-00008` / `VIS-001` Semantic Tokens Only
- `RULE-00014` / `VIS-002` Keep Expression Subordinate To Content
- `RULE-00015` / `UX-004` Use Motion To Explain State Continuity

## Handoff To Other Skills

- Use `product-designer` if product direction or the primary action is unclear.
- Use `design-evidence-researcher` when current evidence is missing.
- Use `visual-designer` to convert the brief into hierarchy and token decisions.
- Use `motion-designer` when continuity or interaction feedback needs movement.
- Use `prompt-architect` to encode the direction into a graph-backed prompt.
