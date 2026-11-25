---
name: design-system
description: >
  Create, audit, or extend a design system — tokens, components, patterns, and documentation.
  TRIGGER when: user says "design system", "component library", "design tokens",
  "style guide", "create a component", or works on systematic design infrastructure.
argument-hint: "[create|audit|extend|document] [component or token name]"
user-invocable: true
---

# Design System

Manage design systems — the shared vocabulary of tokens, components, and patterns that ensure consistency across a product.

## Operations

### Create — Build a new design system or component

#### Foundation Tokens

Define the atomic values everything else builds on:

```
## Design Tokens

### Color
| Token | Value | Usage |
|---|---|---|
| --color-gray-50 | #FAFAFA | Background, subtle fills |
| --color-gray-100 | #F5F5F5 | Hover backgrounds |
| --color-gray-200 | #E5E5E5 | Borders, dividers |
| --color-gray-500 | #737373 | Secondary text, placeholders |
| --color-gray-900 | #171717 | Primary text, headings |
| --color-brand-500 | #2563EB | Primary actions, links |
| --color-brand-600 | #1D4ED8 | Hover states |
| --color-brand-700 | #1E40AF | Active states |
| --color-error-500 | #DC2626 | Error text, borders |
| --color-success-500 | #16A34A | Success indicators |
| --color-warning-500 | #F59E0B | Warning indicators |

### Spacing Scale (4px base)
| Token | Value |
|---|---|
| --space-1 | 4px |
| --space-2 | 8px |
| --space-3 | 12px |
| --space-4 | 16px |
| --space-6 | 24px |
| --space-8 | 32px |
| --space-12 | 48px |
| --space-16 | 64px |

### Typography Scale
| Token | Size | Line Height | Weight |
|---|---|---|---|
| --text-xs | 12px / 0.75rem | 1.5 | 400 |
| --text-sm | 14px / 0.875rem | 1.5 | 400 |
| --text-base | 16px / 1rem | 1.5 | 400 |
| --text-lg | 18px / 1.125rem | 1.4 | 500 |
| --text-xl | 20px / 1.25rem | 1.3 | 600 |
| --text-2xl | 24px / 1.5rem | 1.3 | 600 |
| --text-3xl | 32px / 2rem | 1.2 | 700 |
| --text-4xl | 48px / 3rem | 1.1 | 700 |

### Border Radius
| Token | Value | Usage |
|---|---|---|
| --radius-sm | 4px | Small chips, tags |
| --radius-md | 8px | Cards, inputs |
| --radius-lg | 12px | Modals, popovers |
| --radius-full | 9999px | Avatars, pills |

### Shadow
| Token | Value | Usage |
|---|---|---|
| --shadow-sm | 0 1px 2px rgba(0,0,0,0.05) | Subtle elevation |
| --shadow-md | 0 4px 6px rgba(0,0,0,0.07) | Cards, dropdowns |
| --shadow-lg | 0 10px 15px rgba(0,0,0,0.1) | Modals, popovers |
```

#### Component Specification

For each component, document:

```
## Component: Button

### Variants
| Variant | Usage |
|---|---|
| Primary | Main CTA, one per screen |
| Secondary | Supporting actions |
| Ghost | Tertiary actions, toolbars |
| Destructive | Delete, remove, irreversible actions |

### Sizes
| Size | Height | Padding | Font Size | Icon Size |
|---|---|---|---|---|
| sm | 32px | 12px 16px | 14px | 16px |
| md | 40px | 12px 20px | 16px | 20px |
| lg | 48px | 16px 24px | 18px | 24px |

### States
| State | Visual Treatment |
|---|---|
| Default | Base variant color |
| Hover | Darken 10%, slight shadow lift |
| Active/Pressed | Darken 15%, shadow inset |
| Focus | 2px ring offset, brand color |
| Disabled | 40% opacity, cursor not-allowed |
| Loading | Spinner replaces label, maintains width |

### Anatomy
- Leading icon (optional)
- Label (required)
- Trailing icon (optional)
- Loading spinner (conditional)

### Props / API
| Prop | Type | Default | Description |
|---|---|---|---|
| variant | 'primary' \| 'secondary' \| 'ghost' \| 'destructive' | 'primary' | Visual variant |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Button size |
| disabled | boolean | false | Disables interaction |
| loading | boolean | false | Shows loading state |
| icon | ReactNode | — | Leading icon |
| fullWidth | boolean | false | Stretches to container width |

### Accessibility
- Use `<button>` element, never `<div>` or `<a>` for actions
- Include `aria-label` when using icon-only buttons
- `aria-disabled="true"` preferred over `disabled` attribute for screen reader announcements
- Loading state: add `aria-busy="true"` and announce via live region

### Do / Don't
| Do | Don't |
|---|---|
| Use one primary button per section | Multiple primary buttons competing |
| Start label with a verb: "Save changes" | Vague labels: "OK", "Submit" |
| Use destructive variant for irreversible actions | Red-styled primary button |
| Maintain minimum touch target of 44px | Buttons smaller than 32px height |
```

### Audit — Review an existing design system for gaps

1. **Token coverage**: Are all hardcoded values covered by tokens?
2. **Component completeness**: Does each component document all states, sizes, variants?
3. **Consistency**: Are spacing, typography, and color applied consistently?
4. **Accessibility**: Do all components meet WCAG AA?
5. **Naming conventions**: Are token and component names systematic and predictable?
6. **Missing patterns**: Are there common UI patterns used in the product that aren't in the system?

Output an audit report:

```
## Design System Audit

### Coverage Score: {N}/10

### Gaps Found
| Category | Issue | Severity | Recommendation |
|---|---|---|---|
| Tokens | No semantic color tokens | High | Map primitives to semantic names |
| Components | Button missing loading state | Medium | Add loading variant |
| Patterns | No empty state pattern | Medium | Create empty state template |
| Docs | Component props not documented | High | Add prop tables |
```

### Extend — Add a new component or token to an existing system

1. Read the existing design system files to understand conventions.
2. Follow established naming patterns, token usage, and documentation structure.
3. Generate the new component/token spec matching the existing format.
4. Identify where the new addition connects to existing components.

### Document — Generate or update documentation

1. Read existing component code or design files.
2. Generate documentation in the established format.
3. Include: variants, sizes, states, anatomy, props, accessibility notes, and do/don't guidelines.

## Principles

- **Systematic over ad-hoc**: Every value should trace back to a token.
- **Composable**: Components should combine predictably.
- **Accessible by default**: Accessibility is built in, not bolted on.
- **Document decisions**: Record *why* a pattern exists, not just *what* it is.
- **Minimal viable system**: Start with what you need. Don't pre-build unused components.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
