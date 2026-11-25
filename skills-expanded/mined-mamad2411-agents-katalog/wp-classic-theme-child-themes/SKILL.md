---
name: wp-classic-theme-child-themes
description: Plans, implements, and reviews WordPress child themes, parent overrides, load order, asset inheritance, and parent-update compatibility. Use when customizing a parent theme without editing it directly.
license: MIT
compatibility: "General parent/child guidance; inspect the exact parent theme and version."
---

# WordPress Classic Child Themes

## Use this skill when

- Creating a child theme.
- Overriding parent templates or assets.
- Adding presentation-specific PHP that must survive parent updates.
- Reviewing whether a child theme has become too large.
- Preparing for a parent-theme update.

## Approach

1. Inspect the exact parent theme and version.
2. Decide whether child theme, plugin, configuration, or a fork is appropriate.
3. Create the minimum child structure.
4. Verify `Template` metadata and load order.
5. Add only required overrides.
6. Document every override's parent source version.
7. Test parent updates with explicit comparisons.

## Workflow

Use [child-theme-change-workflow.md](workflows/child-theme-change-workflow.md).

## Resources

- [child-theme-decision-tree.md](resources/child-theme-decision-tree.md)
- [parent-update-impact-checklist.md](resources/parent-update-impact-checklist.md)
- [child-theme-bootstrap-patterns.md](examples/child-theme-bootstrap-patterns.md)

## Guardrails

- Never edit the parent.
- Never copy the entire parent into the child.
- Do not copy parent `functions.php`.
- Do not propose a grandchild theme.
- Move portable or site-critical behavior into plugins.
