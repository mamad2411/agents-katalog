---
name: wp-divi-5-template-customization
description: Implements and reviews Divi 5 template customizations. Use when choosing Theme Builder or hooks instead of a copied template, or when a necessary child-theme override must be versioned and maintained.
---

# Divi 5 Template Customization

## Decision Order

1. Theme Builder for global visual templates and dynamic content.
2. WordPress or documented Divi hook/filter for a small markup or behavior change.
3. Minimal child-theme template override only when the first two cannot satisfy the requirement.
4. Standalone plugin when the behavior is portable or owns data.

## Hook Review

- Verify the hook exists and fires in the installed Divi version.
- Confirm parameters, timing, output context, priority, and whether multiple callbacks can coexist.
- Escape callback output for the final context.
- Avoid replacing large HTML fragments through fragile string filters when a better extension point exists.
- Test Theme Builder overrides and third-party extensions that may bypass or alter classic template paths.

## Override Requirements

- Copy from the exact installed parent version in a controlled environment.
- Preserve required WordPress and Divi hooks.
- Make the smallest change possible and mark project-specific sections.
- Add the file to [template-override-register.md](resources/template-override-register.md).
- Test representative content, logged-in/out states, archives, search, 404, pagination, comments, forms, responsive views, and accessibility as applicable.
- Compare against every later Divi parent version before rollout.

## Workflow

Use [implement-divi-template-customization-workflow.md](workflows/implement-divi-template-customization-workflow.md).

## Prohibitions

- No direct parent edits.
- No copied parent `functions.php`.
- No proprietary Divi parent templates committed as examples in this Antigravity plugin.
- No undocumented assumption that a Divi 4 template or hook is unchanged in Divi 5.
