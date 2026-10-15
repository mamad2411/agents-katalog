---
name: martix-fluent-ui
description: Fluent UI React v9 engineering for packages, providers, themes, tokens, Griffel, public component and slot composition, accessibility and focus, Next.js SSR, icons, motion, charts, legacy Fabric/v8/v0 migration, and rare Vue integration through @fluentui/web-components. Use when a task names Fluent UI, Fabric UI, an @fluentui package, FluentProvider, Griffel, Fluent tokens or components, or a React codebase already using them. Do not use for generic React/CSS or visual design without a Fluent package implementation.
---

# MartiX Fluent UI

Use this skill to make Fluent UI decisions that remain accessible, theme-aware,
upgradeable, and consistent with the installed package generation.

## Operating workflow

1. Inventory the target: framework, renderer, package manager, installed
   `@fluentui/*` and React versions, SSR mode, providers, styling, and tests. Reuse
   repository conventions and verify facts that can drift. **Done when every
   version or host assumption that affects the solution is known or explicit.**
2. Select one branch and open only its routed rule: React v9 by default, migration
   for Fabric/v8/v0 or mixed generations, and Web Components for Vue. **Done when
   one package family owns the implementation and cross-skill handoffs are named.**
3. Implement from the interaction inward: choose the highest-level public
   component, then public props, slots, or compound components. Keep static
   application styling CSS-first, using the repository's stylesheet convention or
   CSS Modules by default, and consume Fluent semantic tokens there. Use Griffel
   only for a concrete capability that stylesheet classes cannot safely provide.
   Preserve semantics, focus, directionality, user preferences, and consumer
   overrides. Use `_unstable` recomposition only behind a verified, tested adapter
   when public surfaces cannot meet a concrete requirement. **Done when the public
   contract, style ownership, and accessibility behavior are explicit in code.**
4. Verify the changed behavior with the target repository's test, typecheck, and
   build commands. Exercise relevant keyboard, focus, theme, forced-colors,
   reduced-motion, and hydration paths. **Done when every affected behavior passes
   or is recorded as a specific unresolved constraint.**

## Route by concern

| Concern | Open |
| --- | --- |
| Packages, provider, themes, nested scopes | [Foundation, packages, and themes](./rules/foundation-packages-provider-theme.md) |
| CSS-first styling, tokens, Griffel exceptions, RTL, forced colors | [CSS-first tokens and Griffel boundaries](./rules/styling-tokens-griffel.md) |
| Component choice, slots, compound components, custom composition | [Component composition](./rules/component-composition-slots.md) |
| Semantics, keyboard, focus, overlays, forms | [Accessibility and focus](./rules/accessibility-focus.md) |
| Server rendering, hydration, Next.js | [SSR and Next.js](./rules/ssr-nextjs.md) |
| Icons, animation, data visualization | [Icons, motion, and charts](./rules/icons-motion-charts.md) |
| v8, v0, Fabric, mixed-generation code | [Migration and coexistence](./rules/migration-v8-v0.md) |
| Vue request or non-React host | [Vue Web Components exception](./rules/vue-web-components.md) |
| Tests and final review | [Testing and quality gates](./rules/testing-quality-gates.md) |

For component selection, open
[the component map](./references/component-selection-map.md). For drifting facts,
use [the version map](./references/version-support-map.md) and
[source index](./references/source-index.md).

## TypeScript ownership

Fluent UI examples and composed components use TypeScript and TSX. This skill owns
Fluent component props, slots, tokens, styling, and accessibility behavior. Open
`martix-typescript` when the work becomes primarily about:

- reusable generic API or discriminated-union design;
- `tsconfig`, JSX mode, module resolution, or monorepo references;
- declaration emit, package exports, or consumer fixtures;
- type-level tests unrelated to a Fluent component contract.

Do not weaken types to make an example compile. Resolve the actual package,
module-resolution, or public-contract issue.

## Output contract

For implementation work, return:

1. the smallest repository-conforming code change;
2. concise rationale for component and styling choices;
3. relevant accessibility and compatibility notes;
4. targeted validation commands or results.

For reviews, separate blocking behavior or accessibility defects from migration
risks and optional refinements. Cite files, installed versions, or official sources
for claims that can drift.
