---
name: ui-ux-pro-max
description: General-purpose UI/UX design and implementation across 10 web/mobile stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, plain HTML/CSS). Make sure to use this skill whenever the user says design or build a UI/component/page/screen, refactor a UI, review UI code, choose a color palette/font, design a chart, improve UX, fix a layout, design for accessibility, or describes any general front-end design or implementation work. For cybersecurity-product-specific UI work, prefer ckmui-styling (which has security-product trust patterns and shadcn/Tailwind specialization). For brand identity/logo, use ckmdesign. For presentations, use ckmslides. For banner/ad creative, use ckmbanner-design. This skill is the catchall for UI work that doesn't fit one of the specialized skills.
---

# UI/UX Pro Max

General-purpose UI/UX design across 10 stacks: React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, plain HTML/CSS.

## When to use vs. specialized design skills

| Use this skill when... | Use a different skill when... |
|---|---|
| General UI/UX work across any stack | Building security/cybersec product UI specifically → `ckmui-styling` |
| Cross-stack design system or component | Brand identity, logo, brand palette → `ckmdesign` |
| Mobile (SwiftUI / React Native / Flutter) | Presentation slides → `ckmslides` |
| Charts, data viz | Banner ads or social creative → `ckmbanner-design` |
| Accessibility review on existing UI | Conversion landing page (no security context) → `create-landing-page` |

## Stack selection

Before building anything, identify the stack:

1. Check the user's existing repo / files for stack signals (package.json, .swift files, etc.)
2. Check workspace memory (CLAUDE.md, project docs)
3. If still ambiguous, ASK before assuming. Cross-stack defaults waste time.

Then read the relevant reference file:

| Stack | Reference file |
|---|---|
| React (general, no shadcn) | `references/react.md` |
| Next.js | `references/nextjs.md` |
| Vue | `references/vue.md` |
| Svelte | `references/svelte.md` |
| Tailwind utilities | `references/tailwind.md` |
| shadcn/ui components | `references/shadcn.md` |
| SwiftUI (iOS) | `references/swiftui.md` |
| React Native | `references/react-native.md` |
| Flutter | `references/flutter.md` |
| Plain HTML/CSS | `references/html-css.md` |

## Universal UI principles (apply regardless of stack)

These travel with every UI decision. The reference files cover stack-specific implementation; this section is the philosophy.

### 1. Hierarchy first
Every screen has ONE primary thing. Identify it, make it dominant. Everything else supports.

If you can't identify the primary, the design isn't done.

### 2. Reduce cognitive load
- Group related items
- Limit choices (Hick's law: more choices = slower decisions)
- Use established patterns (don't reinvent navigation)
- Progressive disclosure (don't show everything at once)

### 3. Consistency over cleverness
A surprising UI is a hostile UI. The 5th screen the user sees should feel like the 4th. Same patterns, same vocabulary, same component locations.

### 4. Feedback for every action
Every user action must have a response within 100ms (visual at minimum). Async operations need:
- Loading state (skeleton or spinner, after 200ms not before)
- Success state (subtle, not modal)
- Error state (specific, recoverable, with what to do next)

### 5. Accessibility is not optional
- Keyboard navigation everywhere
- Focus rings visible
- Color is never the only signal
- Contrast WCAG AA minimum
- Screen reader semantics correct
- Alt text on every image
- Form labels associated correctly

### 6. Mobile-aware even on desktop UI
60%+ of B2B traffic is mobile. Test mobile viewport at 380px wide, every page.

### 7. Performance is design
- Page weight matters (every 100ms of load drops conversion 1-2%)
- Animation is design tax (use sparingly)
- Image optimization (WebP, lazy load, srcset)
- Code splitting (only ship what the route needs)

## Design token foundation (all stacks)

Three-layer token architecture:

**Primitive tokens** — raw values
```
color-blue-500: #3b82f6
spacing-4: 16px
font-size-base: 14px
```

**Semantic tokens** — purpose-mapped
```
color-action-primary: var(--color-blue-500)
color-text-body: var(--color-gray-900)
spacing-card-padding: var(--spacing-4)
```

**Component tokens** — component-specific
```
button-primary-bg: var(--color-action-primary)
card-padding: var(--spacing-card-padding)
```

Refactoring color schemes touches semantic tokens, not primitive or component. Component restyling touches component tokens. The layering pays off the second you change anything.

## Chart selection (data viz)

Pick chart based on data shape, not style:

| Data type | Best chart |
|---|---|
| Trend over time | Line chart |
| Comparison across categories | Bar chart |
| Part-to-whole (≤5 parts) | Pie or donut |
| Part-to-whole (>5 parts) | Stacked bar |
| Distribution | Histogram or violin |
| Correlation | Scatter |
| Geographic | Choropleth or symbol map |
| Hierarchy | Treemap or sunburst |
| Flow / process | Sankey or flow diagram |
| Single KPI | Big-number with trend indicator |

Library defaults by stack:
- React: Recharts (simple) or Visx (custom)
- Vue: Apache ECharts
- Svelte: LayerCake
- iOS: Swift Charts
- Universal: D3 (when nothing else fits)

## Color palette guidance (all stacks)

For most product UIs, you need:
- 1 brand primary (and 2-3 shades around it)
- 1 brand secondary (optional, for accents)
- Neutral scale (gray, 9-11 stops from white to near-black)
- Semantic colors (success/warning/error/info, in 1-2 shades each)
- Surface colors (background, card, border, in light + dark mode)

Total: ~25-35 unique colors in a complete system.

DON'T:
- Mix more than 2 hues for accents
- Use pure black (#000) — too harsh, use #0a0a0a or #18181b
- Use pure white in dark mode — use rgba with low opacity instead
- Use color as the only signal (always pair with icon or text)

## Font pairing (all stacks)

Two-font max for most UIs:
- Sans-serif body font (Inter, IBM Plex Sans, Roboto, system default)
- Optional display font for headings (only if it serves a brand purpose)
- Monospace for code, IDs, hashes (JetBrains Mono, SF Mono, Menlo)

Avoid 3+ fonts unless designing editorial. Each font is a download tax.

## Common patterns by component

For implementation specifics, see the stack-specific reference file. High-level rules:

- **Buttons:** primary / secondary / ghost / destructive variants minimum. Loading state. Disabled state with reason.
- **Forms:** label above field, helper text below, error inline, submit at bottom-left or right per locale convention.
- **Modals:** for destructive confirmation or focused workflows. NOT for marketing CTAs. Always escapable.
- **Tables:** sortable, filterable, paginated past 50 rows, virtual-scroll past 1000.
- **Cards:** consistent padding, clear actionable region, optional hover state.
- **Navigation:** ≤7 top-level items. Sidebar collapses on mobile.
- **Empty states:** never just blank. Show what will appear, what to do to populate.
- **Loading:** skeleton > spinner. Match the eventual layout.
- **Error states:** specific. Recoverable. With next action.

## Output

Depending on the request:
- **Component implementation:** code in the chosen stack with accessible markup, responsive, dark-mode if applicable
- **Design review:** annotated feedback per principle
- **Token system:** three-layer token spec for the chosen stack
- **Wireframe:** Markdown structure if no implementation yet
- **Always:** state coverage (loading/empty/error/success), accessibility notes, mobile considerations
