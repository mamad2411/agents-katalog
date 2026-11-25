---
name: heroui-design-principles
description: >
  Apply HeroUI v3's 10 core design principles (semantic intent, accessibility,
  composition, progressive disclosure, predictable APIs, type safety, styles/logic
  split, DX, full customization, open extensibility). Use when building or reviewing
  HeroUI React UI, choosing Button/Chip variants, composing Accordion/Tabs/Alert,
  theming with CSS variables or BEM, wrapping Next.js Link with buttonVariants, or
  avoiding v2 visual variants (solid/flat/bordered). Keywords: HeroUI design principles,
  semantic variants primary secondary tertiary, compound components, React Aria, @heroui/styles.
  Use when the user runs /heroui-design-principles.
---

# HeroUI Design Principles (v3)

Core principles that guide HeroUI v3 design and development. Prioritize clarity, accessibility, customization, and developer experience.

**Source:** https://heroui.com/en/docs/react/getting-started/design-principles

## Apply the Skill

- Read `references/principles.md` before implementing or reviewing HeroUI UI structure, variants, composition, theming, or wrappers.
- Treat these principles as the default when working with `@heroui/react` and `@heroui/styles`.
- For install, per-component anatomy, props, and theming setup, also use the `heroui-react` skill or fetch component docs. This skill is the **policy layer** (what and why); `heroui-react` is the **implementation layer** (how for each component).
- For v2 → v3 migrations, use `heroui-migration` and still enforce these principles on the target code.

## Non-Negotiables

| Do | Don't |
|----|--------|
| Semantic variants: `primary`, `secondary`, `tertiary`, `danger`, `ghost` | Visual variants: `solid`, `flat`, `bordered` (v2) |
| **One** primary action per context | Multiple competing primaries |
| Compound components (named exports and/or dot notation) | Flat mega-props that hide structure |
| Progressive APIs: start minimal, add props only when needed | Require every prop up front |
| Shared patterns: `size` `sm` \| `md` \| `lg`, `className`, data attrs | One-off APIs per component |
| Full TypeScript types; extend with `Omit<…Props, …>` | Untyped wrappers or stringly variants |
| Styles in `@heroui/styles` / CSS vars / BEM; logic in `@heroui/react` | Coupling styling-only needs to React components |
| Rely on React Aria (ARIA, keyboard, screen readers) | Reimplement a11y from scratch on HeroUI hosts |
| `onPress` where HeroUI/React Aria expects it | `onClick` as the default interactive handler |
| No `HeroUIProvider` in v3 | Reintroducing v2 provider / framer-motion stacks |

## Work in This Order

1. **Intent hierarchy** — Map actions to primary / secondary / tertiary / danger before picking visuals.
2. **Compose structure** — Prefer compound parts (heading, trigger, panel, body) over a single overloaded component.
3. **Progressive surface** — Ship the minimal API first; layer icons, loading, disabled only when required.
4. **Predictable API** — Match existing size/variant/`className` conventions across the surface.
5. **Theme slots** — Prefer CSS variables and BEM/`@layer components` before one-off Tailwind soup.
6. **Extend only if needed** — Custom wrappers, `*Variants` on foreign hosts (e.g. Next.js `Link`), or `tv({ extend })` last.

## Decision Rules

### Semantic variants (emphasis)

| Variant | Purpose | Usage |
|---------|---------|-------|
| **Primary** | Main action to move forward | 1 per context |
| **Secondary** | Alternative actions | Multiple allowed |
| **Tertiary** | Dismissive (cancel, skip) | Sparingly |
| **Danger** | Destructive actions | When needed |

```tsx
// ✅ Semantic hierarchy
<Button variant="primary">Save</Button>
<Button variant="secondary">Edit</Button>
<Button variant="tertiary">Cancel</Button>
```

### Composition

- Rearrange, omit, or restyle compound parts freely.
- Named exports and dot notation are both valid (`AlertIcon` vs `Alert.Icon`).

### Progressive disclosure

```tsx
// Level 1: minimal
<Button>Click me</Button>

// Level 2: enhanced
<Button variant="primary" size="lg">Submit</Button>

// Level 3: advanced (loading, disabled, composed children)
<Button variant="primary" isDisabled={isLoading}>…</Button>
```

### Styles vs logic

- Plain HTML / any framework: BEM classes (e.g. `button button--primary`).
- Style a non-HeroUI host: `buttonVariants` / `linkVariants` from `@heroui/styles`.
- Behavior + a11y: components from `@heroui/react`.

### Extensibility

- Prefer thin wrappers that map domain intents → HeroUI semantic variants.
- Prefer `tv({ extend: buttonVariants, … })` over forking component source.
- Apply BEM classes directly when the host is framework-specific (Next.js `Link`, etc.).

## Anti-Patterns

- v2 visual variant names or `HeroUIProvider` + framer-motion as default animation stack
- Many primary buttons in one dialog/toolbar
- Flattening Accordion/Tabs/Card into single-file prop bags when compound parts exist
- Hardcoding brand colors instead of `--accent` / theme variables
- Building custom keyboard/ARIA behavior on top of React Aria components
- Copying v2 `classNames` multi-slot props when v3 uses `className` + BEM/CSS

## Quick v2 vs v3

| Aspect | v2 | v3 (this skill) |
|--------|----|-----------------|
| Variants | Visual (solid, bordered, flat) | Semantic (primary, secondary, tertiary) |
| Pattern | Single components, many props | Compound components |
| Styling | Tailwind v3-era / theme package | Tailwind v4 + `@heroui/styles` |
| Animations | Framer Motion | CSS + GPU-friendly |
| Bundle | Larger | Tree-shakeable, smaller |

## Reference Map

- Full principles, code samples, and customization recipes: `references/principles.md`
- Official docs: https://heroui.com/en/docs/react/getting-started/design-principles
- Raw MDX: https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(overview)/design-principles.mdx
- Component install/docs skill: `heroui-react`
- Migration skill: `heroui-migration`
