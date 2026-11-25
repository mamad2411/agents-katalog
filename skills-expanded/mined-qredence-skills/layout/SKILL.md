---
name: layout
description: Diagnose or improve layout in selected Figma frames, screens, components, or Figma Make prototypes by clarifying reading order, grouping, hierarchy, spacing rhythm, density, adaptation, and content extremes. Use when UI feels crowded, flat, misaligned, hard to scan, structurally unclear, or unstable across sizes.
---

# Layout

Use this skill to improve structure without replacing the design's identity.

Layout changes reading order, grouping, hierarchy, spatial rhythm, density, and adaptation. It does not invent a new brand, art direction, product concept, or component system.

## Output Mode

Choose the output mode from the user's request:

- If the user asks to `review`, `diagnose`, or `explain`, return a layout report only.
- If the user asks to `fix`, `improve`, `adjust`, or `apply`, make layout changes and summarize them.
- If the target is too broad, narrow to one selected frame, flow, component set, or Make area.
- If layout cannot solve the main problem, say whether the issue is content, product scope, interaction design, or visual direction.

## First Classify The Surface

Identify the main visitor mode:

- `Persuade`: landing pages, onboarding, marketing, conversion moments
- `Operate`: dashboards, tools, forms, admin panels, repeated workflows
- `Read`: documents, reports, articles, changelogs, documentation
- `Native`: mobile app surfaces following platform expectations

Let the mode control density and structure.

Persuade surfaces may use stronger asymmetry and focal moments. Operate and Read surfaces need predictable scan paths, stable density, and clear grouping.

## Layout Assessment

Inspect the selected target and answer:

- Reading order: With details blurred, what is primary, secondary, and tertiary?
- Grouping: Which elements belong together? Which groups need more separation?
- Hierarchy: Does visual weight match product priority?
- Rhythm: Are spacing intervals deliberate, or monotonous?
- Density: Does information density match use frequency and decision complexity?
- Structure: Are repeated cards, columns, sections, or controls genuinely equivalent?
- Adaptation: What happens at smaller, wider, zoomed, and long-content conditions?
- Extremes: What breaks with long labels, missing content, empty states, overlays, or small touch targets?

## Spatial Thesis

Before changing the design, state the intended structure:

```markdown
## Spatial Thesis
- Primary reading/task path:
- Main groups:
- Lead element:
- Supporting elements:
- Density:
- Spacing rhythm:
- Responsive or variant behavior:
```

## Apply Changes

Use these rules:

- Group by meaning before adding containers.
- Use proximity first; use borders, cards, and backgrounds only when proximity is insufficient.
- Make the primary path easier to see before polishing secondary details.
- Create rhythm with contrast between tight related spacing and generous section spacing.
- Use existing spacing styles, variables, components, and grids when available.
- Keep repeated structures consistent unless product priority differs.
- Make responsive behavior structural: stack, collapse, reorder, reveal, or simplify based on task priority.
- Preserve logical order for keyboard and assistive technology expectations.
- Keep touch targets usable when the design is intended for touch.
- Use depth only to clarify hierarchy, elevation, selection, or overlay state.

## Verification

After changes, verify:

- The squint test reveals the intended primary and secondary path.
- Related content reads as grouped.
- Unrelated content no longer blends together.
- Density fits the visitor mode.
- Long content and empty states remain usable.
- The structure still works at relevant frame sizes or Make breakpoints.
- The design still feels like the same product.

## Output Contract

When reporting work, use:

```markdown
## Layout Changes
- Target:
- Visitor mode:
- Spatial thesis:
- Changes made or recommended:
- Remaining risks:
```

## Quality Check

Before finishing:

- Do not disguise a redesign as layout polish.
- Do not add cards around everything.
- Do not flatten hierarchy by making spacing perfectly uniform.
- Do not optimize only the visible viewport when other content ranges matter.
- Do not change unrelated screens, flows, copy, or component behavior.
