---
name: design-review-pro
description: Professional UI/UX design review for web apps, desktop apps, dashboards, landing pages, and product screens. Inspired by gstack design-review/design-consultation workflows and adapted for Codex v4.3. Use when reviewing screenshots, implemented UI, Figma designs, visual regressions, or proposed layouts.
---

# Design Review Pro

## Workflow

1. Identify product type, target user, and screen goal.
2. Review hierarchy, layout, density, navigation, and primary workflow.
3. Review visual system: typography, color, spacing, surfaces, icons, states, and motion.
4. Review usability: discoverability, feedback, error recovery, keyboard, and responsive behavior.
5. Prioritize findings by user impact and implementation cost.

## Finding Categories

- `P1`: Blocks task completion, major confusion, inaccessible critical path.
- `P2`: Noticeable friction, weak hierarchy, inconsistent state, poor responsive behavior.
- `P3`: Polish issue, minor inconsistency, small copy or spacing problem.

## Review Checklist

- Main task and primary action are clear.
- Layout supports scanning and repeated use.
- Controls match expected patterns.
- Text fits containers on desktop and mobile.
- Visual treatment matches product category.
- Empty/error/loading states are complete.
- Accessibility basics are respected.
- UI avoids generic AI visual tropes.

## Output

Use findings first:

```markdown
发现：
- [P1] ...

建议：
- ...

验证：
- ...
```

Avoid broad redesign unless the user asks for a redesign.
