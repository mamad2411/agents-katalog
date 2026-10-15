---
name: consistency-design-systems
description: This skill should be used when the user is building a design system, defining design tokens, creating component libraries, implementing CSS custom properties, ensuring visual consistency across pages, choosing between design systems (Material, Ant, Carbon), or auditing a codebase for design consistency. Covers design tokens (primitive → semantic → component layers), atomic design methodology, token governance, and systematic consistency.
version: 1.0.0
---

# Identical Components Must Be Identical -- Consistency Is the Fastest Path to Perceived Quality

Consistency is the most central aesthetic factor. The VisAWI (Visual Aesthetics of Websites Inventory) instrument identifies Craftsmanship as a primary dimension -- and the fastest way to score high on Craftsmanship is rigid consistency. Every time a user encounters the same component rendered two slightly different ways, trust erodes. The CRAP design framework (Contrast, Repetition, Alignment, Proximity) names Repetition as a core principle for exactly this reason.

## Design Token Layers

Design tokens are the atomic values that encode visual decisions. Organize them in three layers, referencing downward only.

| Layer | Naming Pattern | Example | Changes When |
|-------|---------------|---------|--------------|
| **Primitive** | `--{category}-{scale}` | `--blue-500`, `--space-4`, `--radius-md` | Brand overhaul |
| **Semantic** | `--color-{purpose}` | `--color-primary`, `--color-bg-surface` | Theme switch (light/dark) |
| **Component** | `--{component}-{property}` | `--button-bg`, `--card-radius` | Component redesign |

**Rule:** Components reference semantic tokens. Semantic tokens reference primitives. Never skip a layer.

## Token Categories

Define tokens for every visual property. Constrain each category to a finite set.

| Category | Max Unique Values | Example Tokens |
|----------|-------------------|----------------|
| Color | <= 15 | `--color-primary`, `--color-bg-surface`, `--color-status-error` |
| Spacing | <= 10 | See `whitespace-density` skill for the full spacing scale |
| Typography | <= 6 sizes | `--font-xs`, `--font-sm`, `--font-base`, `--font-lg`, `--font-xl`, `--font-2xl` |
| Elevation | <= 5 levels | `--shadow-0` through `--shadow-4` (see `craftsmanship-polish` skill for definitions) |
| Border radius | <= 4 values | See `craftsmanship-polish` skill for reference values |
| Motion | <= 3 durations | `--duration-fast` (100ms), `--duration-normal` (200ms), `--duration-slow` (300ms) |

## The "10 Unique Values" Audit

Extract all unique values for any single property in the codebase. If there are more than 10 unique values for spacing, or more than 15 for color, the system has drifted. Run this audit periodically.

**How to audit:**
1. Search the codebase for all padding, margin, and gap declarations
2. List every unique value
3. Flag any value not in the token scale
4. Replace rogue values with the nearest token

## Atomic Design Methodology

Build from the smallest constrained unit upward.

| Level | Definition | Example |
|-------|-----------|---------|
| **Atoms** | Single elements, unsplittable | Button, input, label, icon |
| **Molecules** | Small groups of atoms with one function | Search bar (input + button), form field (label + input + error) |
| **Organisms** | Complex groups forming a section | Navigation bar, pricing card, data table |
| **Templates** | Page-level layout with placeholder content | Dashboard layout, settings page layout |
| **Pages** | Templates filled with real content | The actual rendered screen |

Every atom uses tokens. Molecules compose atoms without overriding their tokens. If a molecule needs a different button color, create a semantic token variant -- never hard-code a value.

## Cross-Screen Consistency Rule

**The same component at the same level must share exact styles across every screen.** A "Save" button on the settings page must be pixel-identical to a "Save" button on the profile page. If it is not, the user perceives lower quality even without consciously noticing the difference.

Audit by taking screenshots of the same component across different pages and overlaying them. Any variation is a bug.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Magic numbers (`padding: 13px`) | Breaks the spacing scale, impossible to maintain | Use nearest token (`--space-3: 12px`) |
| One-off styles | Inconsistency across pages, maintenance burden | Create a reusable token or component |
| Token sprawl (50+ colors) | Effectively no system at all | Constrain to <= 15 colors, audit and merge |
| Inconsistent naming (`--btn-bg` vs `--button-background`) | Developer confusion, duplication | Adopt one naming convention and enforce it |
| Skipping token layers (component referencing primitive) | Theme switching breaks | Always reference through semantic layer |

## Cross-Media Notes

- **Presentations**: Master slides and layouts are tokens -- consistent heading position, font sizes, and color palette across all slides
- **CVs/Resumes**: One font, one heading style, one bullet style, one date format -- any variation looks unprofessional
- **Brand systems**: The design system is the brand -- every touchpoint must reference the same token set

## Examples

Working implementations in `examples/`:
- **`examples/design-tokens-system.md`** -- Complete token system in CSS custom properties with primitive/semantic/component layers, Tailwind config, and React theme provider

## Review Checklist

When reviewing or building a design system:

- [ ] Three token layers implemented: primitive, semantic, component
- [ ] Components reference semantic tokens, never primitives directly
- [ ] <= 15 unique color tokens in the semantic layer
- [ ] <= 10 unique spacing values in the scale
- [ ] <= 4 border-radius values defined
- [ ] <= 5 elevation/shadow levels defined (see `craftsmanship-polish` for reference values)
- [ ] No magic numbers -- every value traces to a token
- [ ] The same component renders identically across all pages
- [ ] Token naming follows a consistent pattern (category-purpose)
- [ ] The "10 unique values" audit passes for spacing and color
- [ ] Atomic design levels are respected (atoms -> molecules -> organisms)
- [ ] Token changes propagate automatically (CSS custom properties or theme provider)
