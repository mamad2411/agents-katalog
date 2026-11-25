---
name: building-components
description: Guide for building modern, accessible, and composable UI components. Use when building new components, implementing accessibility, creating composable APIs, setting up design tokens, publishing to npm/registry, or writing component documentation.
---

# Building Components

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/definitions.mdx` — artifact taxonomy: primitives, components, blocks, templates and when to use each · read when choosing the right abstraction level for a new component.
- `references/principles.mdx` — core component design principles: single responsibility, composition over configuration, minimal API surface · read when designing a new component's API.
- `references/accessibility.mdx` — ARIA roles/attributes, keyboard navigation, focus management, WCAG compliance patterns · read when implementing interactive or custom-widget components.
- `references/composition.mdx` — slot patterns, render props, controlled/uncontrolled state, compound components · read when designing composable component APIs.
- `references/as-child.mdx` — the Radix-style `asChild` pattern for element polymorphism without wrapper divs · read when implementing `asChild` or polymorphic roots.
- `references/polymorphism.mdx` — `as` prop, generic polymorphic components, TypeScript inference for polymorphic types · read when a component must render as different HTML elements.
- `references/types.mdx` — TypeScript typing patterns: discriminated unions, generic props, `ComponentPropsWithoutRef`, `forwardRef` · read when typing component props or forwarding refs.
- `references/state.mdx` — controlled vs uncontrolled state, `useControllableState`, default value patterns · read when deciding how a component should own or delegate its state.
- `references/data-attributes.mdx` — using `data-*` attributes for CSS state, testing hooks, and styling variants · read when styling component states or wiring tests.
- `references/design-tokens.mdx` — CSS custom property token systems, theming, dark mode, token naming conventions · read when setting up or extending a design token layer.
- `references/styling.mdx` — CSS Modules, Tailwind, CSS-in-JS, class variance authority (CVA), style encapsulation · read when choosing or implementing a component styling approach.
- `references/registry.mdx` — shadcn/ui-style registry distribution, `components.json`, CLI-installable components · read when publishing via a component registry.
- `references/npm.mdx` — npm package publishing: entry points, bundling, peer deps, package.json fields · read when shipping a component library to npm.
- `references/marketplaces.mdx` — component marketplace distribution (Shadcn registry, v0, etc.) · read when distributing components via a marketplace.
- `references/docs.mdx` — writing component documentation: prop tables, usage examples, Storybook stories · read when documenting a component for end users.
