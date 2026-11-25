---
name: ckmdesign-system
description: Designs and maintains design token architecture — primitive → semantic → component three-layer tokens, CSS variables, spacing/typography scales, component specifications, and brand-compliant token systems. Make sure to use this skill whenever the user says design tokens, build a design system, set up design variables, refactor our color system, define spacing scale, build a component library spec, design system tokens, or describes wanting a structured token architecture rather than ad-hoc styling. Pairs with ckmui-styling (which uses these tokens to build the actual UI). Do NOT use for: implementing UI components themselves (use ckmui-styling), brand identity / logo / palette decisions (use ckmdesign — though that skill produces the inputs to this one), presentations (use ckmslides), or banner ads (use ckmbanner-design). Defining characteristic: "structured token architecture and component spec, NOT the implementation of components themselves."
---

# Design System (Token Architecture)

Three-layer token architecture and component specifications for design systems.

## When to use vs. adjacent design skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Designing the token architecture | Building actual UI components → `ckmui-styling` |
| Defining color/spacing/typography scales | Brand identity, logo, color choice → `ckmdesign` |
| Component specifications | Building presentations → `ckmslides` |
| Refactoring CSS variable structure | Banner/ad design → `ckmbanner-design` |

## Three-layer token architecture

### Layer 1 — Primitive tokens (raw values)
The atomic values. No semantic meaning yet.

```css
/* Color primitives */
--color-blue-50:  #eff6ff;
--color-blue-100: #dbeafe;
--color-blue-500: #3b82f6;
--color-blue-600: #2563eb;
--color-blue-900: #1e3a8a;

--color-gray-50:  #f9fafb;
--color-gray-100: #f3f4f6;
--color-gray-500: #6b7280;
--color-gray-900: #111827;

/* Spacing primitives */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
--space-12: 48px;

/* Typography primitives */
--font-size-xs:  12px;
--font-size-sm:  14px;
--font-size-base: 16px;
--font-size-lg:  18px;
--font-size-xl:  20px;
--font-size-2xl: 24px;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Layer 2 — Semantic tokens (purpose-mapped)
Names describe purpose. Built from primitives.

```css
/* Color semantic */
--color-action-primary:  var(--color-blue-600);
--color-action-hover:    var(--color-blue-700);
--color-text-body:       var(--color-gray-900);
--color-text-muted:      var(--color-gray-500);
--color-surface-page:    var(--color-gray-50);
--color-surface-card:    #ffffff;
--color-border-default:  var(--color-gray-200);
--color-status-success:  var(--color-green-600);
--color-status-warning:  var(--color-yellow-600);
--color-status-error:    var(--color-red-600);

/* Spacing semantic */
--space-card-padding:    var(--space-6);
--space-section-gap:     var(--space-12);
--space-stack-tight:     var(--space-2);
--space-stack-loose:     var(--space-6);

/* Typography semantic */
--text-body:             var(--font-size-base);
--text-heading-1:        var(--font-size-2xl);
--text-heading-2:        var(--font-size-xl);
--text-caption:          var(--font-size-xs);
```

### Layer 3 — Component tokens (component-specific)
Component-specific values. Built from semantic.

```css
/* Button */
--button-bg-primary:     var(--color-action-primary);
--button-bg-primary-hover: var(--color-action-hover);
--button-text-primary:   #ffffff;
--button-padding-x:      var(--space-4);
--button-padding-y:      var(--space-2);
--button-radius:         8px;
--button-font:           var(--text-body);

/* Card */
--card-bg:               var(--color-surface-card);
--card-padding:          var(--space-card-padding);
--card-radius:           12px;
--card-border:           1px solid var(--color-border-default);
--card-shadow:           0 1px 3px rgba(0,0,0,0.1);

/* Input */
--input-bg:              var(--color-surface-card);
--input-border:          1px solid var(--color-border-default);
--input-padding:         var(--space-3);
--input-radius:          6px;
```

## Why three layers (not one or two)

**One layer (just primitives everywhere):** changing brand color requires touching every component file. Painful.

**Two layers (primitives + components):** changing semantic concepts (e.g., "muted text") requires component-by-component update. Less painful but still messy.

**Three layers:** brand color change → update primitive only. Concept change ("muted text becomes less muted") → update semantic only. Component restyle → update component token only. Each layer absorbs one type of change.

## Spacing scale design

Geometric scales feel more harmonious than linear:

**4px-based scale (most common):**
0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128

**8px-based scale (looser):**
0, 8, 16, 24, 32, 48, 64, 96, 128

**Modular scale (golden-ratio based, for editorial):**
4, 7, 11, 18, 29, 47, 76, 123

Pick one and STAY IN IT. Mixing scales creates visual chaos.

## Typography scale design

Typographic scales should also be geometric:

**1.250 (Major Third) — calm, content-friendly:**
12, 15, 19, 24, 30, 38, 48, 60

**1.333 (Perfect Fourth) — moderate hierarchy:**
12, 16, 21, 28, 37, 50, 67, 89

**1.500 (Perfect Fifth) — strong hierarchy, brand-bold:**
12, 18, 27, 41, 61, 92

For most product UI: 1.250 ratio. For marketing landing pages: 1.333 or 1.500.

## Component specification structure

Every component gets a spec:

```markdown
# Component: [Name]

## Purpose
[One sentence — what this component does]

## States
- [ ] Default
- [ ] Hover
- [ ] Active (pressed)
- [ ] Focused (keyboard)
- [ ] Disabled (with reason)
- [ ] Loading
- [ ] Error

## Variants
- Primary
- Secondary
- Tertiary / Ghost
- Destructive

## Sizes
- Small
- Medium (default)
- Large

## Tokens used
- Background: [token]
- Text: [token]
- Padding: [token]
- Border: [token]
- Radius: [token]

## Accessibility requirements
- Keyboard navigation: [tab + enter behavior]
- ARIA: [role, attributes]
- Screen reader: [announcements]
- Focus visible: [yes, with what indicator]
- Contrast ratio: [ratio]

## Behavior
[Click handlers, async behavior, edge cases]

## Don'ts
[Misuse to avoid]
```

## Common token mistakes

- **Skipping semantic layer** — primitive directly in components defeats the architecture
- **Naming primitives semantically** — `--color-button-blue` is a primitive named like a semantic; rename to `--color-blue-500`
- **Inconsistent spacing scale** — mixing 4px-based and 5px-based values
- **Too many primitives** — 200 colors when you need 30
- **Component tokens that don't use semantic** — bypassing the architecture
- **Magic numbers in CSS** — `padding: 13px` (not in any scale) breaks rhythm
- **No dark mode plan from the start** — bolted-on dark mode never quite works

## Dark mode pattern

Best approach: token aliasing per theme.

```css
/* Light theme */
:root {
  --color-surface-page: var(--color-gray-50);
  --color-surface-card: #ffffff;
  --color-text-body:    var(--color-gray-900);
}

/* Dark theme */
[data-theme="dark"] {
  --color-surface-page: #0a0a0a;
  --color-surface-card: var(--color-gray-900);
  --color-text-body:    var(--color-gray-50);
}
```

Component tokens reference semantic tokens, which automatically swap with theme. Components never know which theme is active.

## Cybersecurity product design system overlay

For security/cybersec product design systems, additional considerations:

- **Severity color tokens** explicit and consistent across the app:
  ```css
  --color-severity-critical: var(--color-red-600);
  --color-severity-high:     var(--color-orange-600);
  --color-severity-medium:   var(--color-yellow-600);
  --color-severity-low:      var(--color-cyan-600);
  --color-severity-info:     var(--color-slate-600);
  ```
- **Status indicator tokens** distinct from severity (one is "is the system healthy", other is "how bad is this finding"):
  ```css
  --color-status-operational: var(--color-green-600);
  --color-status-degraded:    var(--color-yellow-600);
  --color-status-down:        var(--color-red-600);
  ```
- **Monospace tokens** for IDs, hashes, IPs (security UIs use a lot):
  ```css
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
  --text-mono-sm: 13px;
  ```
- **Trust-element tokens** for badges (SOC 2, ISO, etc.):
  ```css
  --badge-trust-bg: var(--color-blue-50);
  --badge-trust-text: var(--color-blue-900);
  --badge-trust-border: var(--color-blue-200);
  ```

## Output

Produces:
1. The full three-layer token architecture in CSS variables (or Tailwind config / Style Dictionary / etc. as requested)
2. Spacing scale recommendation
3. Typography scale recommendation
4. Component specifications for the components requested
5. Dark mode aliasing plan
6. Migration plan if refactoring an existing system
7. Suggested chain to `ckmui-styling` for component implementation
