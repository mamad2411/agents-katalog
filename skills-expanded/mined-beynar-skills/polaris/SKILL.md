---
name: polaris
description: "Shopify Polaris design system — the complete reference for building Shopify admin apps. Use this skill ANY TIME the user mentions Polaris, Shopify admin UI, Shopify app development, @shopify/polaris, Polaris components, Polaris tokens, or is building any interface that targets the Shopify ecosystem. Also trigger when the user asks about Shopify design patterns, admin layout, resource pages, settings pages, or any Polaris component by name (Button, Card, Page, TextField, IndexTable, Banner, etc.)."
---

# Shopify Polaris Design System — Master Reference

This is the orchestrator skill for the complete Polaris design system. It contains **96 individual skills** organized across 7 categories. Read the relevant sub-skill for detailed guidance.

## Skill Map

### Foundations (5 skills)
Core principles that underpin every Polaris interface.

| Skill | Path | When to read |
|-------|------|-------------|
| Accessibility | `foundations/accessibility/` | Building any UI — a11y is non-negotiable |
| Formatting Currency | `foundations/formatting-currency/` | Displaying prices, money, multi-currency |
| Internationalization | `foundations/internationalization/` | i18n, translations, locale-aware UI |
| Information Architecture | `foundations/information-architecture/` | Structuring navigation, page hierarchy |
| Experience Values | `foundations/experience-values/` | Understanding Shopify's design philosophy |

### Design Guidelines (11 skills)
Visual design specifications and principles.

| Skill | Path | When to read |
|-------|------|-------------|
| Pro Design Language | `design/pro-design-language/` | Overall design philosophy and density |
| Color | `design/color/` | Color usage, semantics, accessibility |
| Depth | `design/depth/` | Shadows, elevation, visual hierarchy |
| Icons | `design/icons/` | Icon usage, sizing, meaning |
| Layout | `design/layout/` | Page structure, grid, spacing |
| Motion | `design/motion/` | Animation, transitions, timing |
| Typography | `design/typography/` | Font scales, hierarchy, text styles |
| Data Visualizations | `design/data-visualizations/` | Charts, graphs, data display |
| Illustrations | `design/illustrations/` | When and how to use illustrations |
| Interaction States | `design/interaction-states/` | Hover, focus, active, disabled states |
| Sounds | `design/sounds/` | Audio feedback patterns |

### Content Guidelines (6 skills)
Writing for the Shopify admin.

| Skill | Path | When to read |
|-------|------|-------------|
| Fundamentals | `content/fundamentals/` | Core content principles |
| Grammar | `content/grammar/` | Capitalization, punctuation, numbers |
| Error Messages | `content/error-messages/` | Writing clear error states |
| Naming | `content/naming/` | Product and feature naming |
| Alternative Text | `content/alternative-text/` | Alt text for images and icons |
| Inclusive Language | `content/inclusive-language/` | Writing inclusively |

### Patterns (7 skills)
Proven compositions of components for common use cases.

| Skill | Path | When to read |
|-------|------|-------------|
| App Settings Layout | `patterns/app-settings-layout/` | Building settings pages |
| Card Layout | `patterns/card-layout/` | Card structure and anatomy |
| Common Actions | `patterns/common-actions/` | Add, Edit, Delete, Copy patterns |
| Date Picking | `patterns/date-picking/` | Date and date-range selection |
| New Features | `patterns/new-features/` | Highlighting new functionality |
| Resource Details Layout | `patterns/resource-details-layout/` | Individual resource pages |
| Resource Index Layout | `patterns/resource-index-layout/` | Resource list/table pages |

### Tokens (1 skill + 10 reference files)
Design tokens (CSS custom properties) for consistent styling.

| Reference | Path | Contents |
|-----------|------|----------|
| Master | `tokens/SKILL.md` | Overview + quick lookup |
| Color | `tokens/references/color.md` | All `--p-color-*` tokens |
| Font | `tokens/references/font.md` | `--p-font-*` tokens |
| Space | `tokens/references/space.md` | `--p-space-*` tokens |
| Motion | `tokens/references/motion.md` | `--p-motion-*` tokens |
| Border | `tokens/references/border.md` | `--p-border-*` tokens |
| Breakpoints | `tokens/references/breakpoints.md` | `--p-breakpoints-*` |
| Shadow | `tokens/references/shadow.md` | `--p-shadow-*` tokens |
| Z-Index | `tokens/references/z-index.md` | `--p-z-index-*` tokens |
| Height | `tokens/references/height.md` | `--p-height-*` tokens |
| Width | `tokens/references/width.md` | `--p-width-*` tokens |

### Components (66 skills)
Individual React component references organized by category.

#### Actions (3)
`components/actions/` — account-connection, button, button-group

#### Layout & Structure (14)
`components/layout/` — bleed, block-stack, box, callout-card, card, divider, empty-state, form-layout, grid, inline-grid, inline-stack, layout, media-card, page

#### Selection & Input (15)
`components/selection-input/` — autocomplete, checkbox, choice-list, color-picker, combobox, date-picker, drop-zone, filters, form, inline-error, radio-button, range-slider, select, tag, text-field

#### Images & Icons (5)
`components/images-icons/` — avatar, icon, keyboard-key, thumbnail, video-thumbnail

#### Feedback Indicators (10)
`components/feedback/` — badge, banner, exception-list, progress-bar, skeleton-body-text, skeleton-display-text, skeleton-page, skeleton-tabs, skeleton-thumbnail, spinner

#### Typography (1)
`components/typography/` — text

#### Tables (2)
`components/tables/` — data-table, index-table

#### Lists (7)
`components/lists/` — action-list, description-list, list, listbox, option-list, resource-item, resource-list

#### Navigation (4)
`components/navigation/` — footer-help, link, pagination, tabs

#### Overlays (2)
`components/overlays/` — popover, tooltip

#### Utilities (3)
`components/utilities/` — app-provider, collapsible, scrollable

## How to use this skill system

1. **Building a specific component?** → Read the component skill directly
2. **Designing a page layout?** → Start with the relevant pattern skill, then component skills
3. **Styling with CSS?** → Read `tokens/SKILL.md` then the specific token reference
4. **Writing UI copy?** → Read the relevant content guideline skill
5. **Need design principles?** → Read the design guideline skill for that topic

All paths are relative to this skill's directory.
