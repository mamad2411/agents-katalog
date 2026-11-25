---
name: polish
description: Run a final Figma Design or Figma Make quality pass that refines spacing, alignment, typography, color consistency, component state coverage, copy consistency, accessibility basics, and visual coherence without changing the underlying concept. Use when a UI is close and needs launch-ready finish rather than redesign. Not for Figma Sites publish readiness (site-launch-checklist) or Dev Mode handoff preparation (dev-handoff-prep).
---

# Polish

Use this skill for refinement, not redesign.

Preserve the incumbent visual world, content intent, product behavior, and scope. If the concept, information architecture, or flow is wrong, say so and recommend a critique or shape pass instead of quietly replacing the design.

Use `site-launch-checklist` for Figma Sites publish readiness and `dev-handoff-prep` for Dev Mode handoff preparation.

## Output Mode

Choose the output mode from the user's request:

- If the user asks for a `polish pass`, `cleanup`, `final pass`, or `make this feel finished`, apply narrow refinements and summarize them.
- If the user asks for a `review` or `check`, return a polish report only.
- If the work is not ready for polish, name the blocking critique, layout, content, or scope issue first.
- If a requested change would alter the concept, ask before making it.

## Establish The System

Before polishing, identify:

- selected frame, flow, component, or Make prototype area
- connected libraries, local components, variables, styles, or tokens
- neighboring screens or variants that define the pattern
- known constraints, unfinished areas, or intentional exceptions

If no formal system is visible, infer only from repeated local patterns in the selected work.

## Triage Order

Fix or recommend issues in this order:

1. Broken or blocked primary task.
2. Missing essential states: loading, empty, error, success, disabled, permissions, long content.
3. Hierarchy, layout, responsiveness, and system drift.
4. Typography, color, icon, image, and motion inconsistencies.
5. Small alignment and cleanup details.

Do not perfect one corner while leaving the rest below the same quality bar.

## Polish Pass

### Flow and Hierarchy

- Make the current state, primary action, and next step obvious.
- Keep secondary actions visible but clearly secondary.
- Align terminology and interaction patterns with neighboring surfaces.

### Layout and Type

- Align to the visible grid, spacing scale, and component rhythm.
- Fix optical alignment, not only mathematical alignment.
- Keep same-role typography consistent.
- Check wrapping, truncation, localization expansion, and zoom-sensitive text.

### Color, Effects, and Imagery

- Use semantic color roles consistently.
- Keep text, controls, and focus indicators visually legible.
- Keep icon family, stroke, size, and alignment coherent.
- Preserve image aspect ratios and avoid layout shift in Make outputs.
- Use effects only when they clarify hierarchy, surface, state, or emphasis.

### Interaction and States

- Check default, hover, focus, active, disabled, loading, error, and success states when applicable.
- Keep visible focus and logical tab order in Make prototypes.
- Use motion sparingly; it should clarify feedback or transition.
- Respect reduced-motion expectations when specifying Make behavior.

### Content

- Keep capitalization, punctuation, button labels, helper text, and status language consistent.
- Do not rewrite factual claims unless the user asked for copy changes.
- Replace placeholder text only when realistic product content is clearly inferable or requested.

## Output Contract

Return:

```markdown
## Polish Summary
- Target:
- Quality bar:
- Changes made or recommended:
- System elements preserved:
- States checked:
- Remaining risks or intentional exceptions:
```

## Quality Check

Before finishing:

- The work still has the same concept and scope.
- The primary task is clearer.
- Repeated elements are consistent.
- Important states are covered or called out.
- No new visual system was introduced without permission.
- No unsupported automation, export, or hidden file access is assumed.
