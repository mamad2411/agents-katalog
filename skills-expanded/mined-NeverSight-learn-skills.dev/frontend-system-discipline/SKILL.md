---
name: frontend-system-discipline
description: Prevent frontend work from inventing local design tokens, theme constants, helper layers, or style-file sprawl. Use when building or reviewing UI, components, pages, theme tokens, styled files, composition, or helper placement in frontend code.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
---

# Frontend System Discipline

Use this skill when frontend code risks drifting away from the design system or when a change tempts the agent to invent local tokens, helper layers, or style buckets that do not carry real ownership.

This is a reuse and structure skill. It keeps UI work tied to the system that already exists instead of creating page-local versions of the same idea.

## When to use

Invoke this skill for:

- component or page implementation that touches styling, tokens, layout, or composition
- theme updates, design-token updates, or semantic styling changes
- refactors that introduce local helpers, constants, or wrapper components
- styled-component, CSS module, or style-file organization work
- code review focused on frontend reuse, token discipline, or component structure

## Non-negotiable rules

- Do not invent new visual tokens when the existing design system already expresses the need.
- Do not create page-local duplicates of theme values, palette values, spacing scales, typography values, or motion values.
- Do not extract trivial helpers, constants, or style fragments when the inline version is clearer.
- Do not create `helpers.ts`, `constants.ts`, or `styles.ts` buckets for a single use.
- Do not wrap a primitive component just to rename it or forward props unchanged.
- Do not split styles into another file unless the split creates a real ownership or reuse boundary.
- Do not duplicate composition patterns across sibling components when a shared primitive already exists.

## Required order of thought

Before adding frontend structure, evaluate in this order:

1. existing design-system component or primitive
2. existing semantic theme token
3. existing shared composition pattern
4. local inline implementation
5. new shared primitive only with explicit reuse or policy value

Skipping this order is non-compliant.

## Design-system and theme rules

- Reuse semantic tokens first.
- Keep tokens semantic, not page-specific.
- Promote a value into the theme only when it is stable, meaningful, and reused or expected to be reused.
- Keep product-specific or screen-specific values local until reuse proves otherwise.
- Do not create a token just because a literal appears twice in one file.
- Do not map a token to a one-off visual tweak when the inline literal is clearer.
- Prefer theme ownership for palette, typography, spacing, border radius, elevation, and motion primitives that need to stay consistent.

## Composition and helper placement

- Keep one-off transformations inline.
- Extract a helper only when it is reused, domain-bearing, or materially clarifies a complex render path.
- Prefer prop-driven composition before introducing wrappers or adapters.
- Move shared UI behavior into the appropriate shared primitive, not into a page-local convenience layer.
- Avoid helper names that only restate implementation details.
- Keep constant names meaningful only when the name adds more value than the literal itself.

## Styled file organization

- Keep local styled declarations beside the component when the style is truly local.
- Name style files after the owning component or shared primitive.
- Use shared style files only when multiple consumers actually benefit from them.
- Avoid generic style buckets that exist only to flatten the tree.
- Keep overrides close to the component unless they have become a real design-system concern.
- Split style files only when the split makes ownership, reuse, or maintenance clearer.

## Definition of done

- No trivial helper or wrapper layers were introduced.
- No one-off constant was extracted without shared meaning.
- No local token duplication remains where a theme token already exists.
- Styled files reflect ownership and reuse instead of convenience.
- The final structure is simpler or equally simple than the starting point.

## Final output contract

When this skill is used, report:

- which existing design-system or theme primitive was reused
- which tokens or constants were kept local and why
- which helpers or wrappers were rejected
- how styled files were organized and why that ownership is correct
- any new shared primitive added and the reuse or policy reason for it

## References

- `references/design-system-theme.md`
- `references/composition-and-styles.md`
- `evals/evals.json`
