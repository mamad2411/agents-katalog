---
name: elementor-pro-designer-skill
description: "Use this skill whenever helping someone build, design, or troubleshoot layouts in Elementor Pro V4 using the visual editor. Triggers on ANY mention of Elementor, page builder, Flexbox widget, Div block, section layout, widget configuration, responsive breakpoints, dark mode, scroll animations, Interactions tab, Variables Manager, Class Manager, Custom Code snippets, or any visual design work inside the Elementor panel. Also trigger when someone asks how to position elements, set spacing, apply typography, configure dark mode, prevent FOUC, or build scroll-triggered effects in Elementor. ALWAYS use this skill before suggesting any Elementor V4 implementation — it contains critical V4-specific panel structure, common AI mistakes to avoid, and production-tested patterns."
version: "1.0.0"
elementor_pro: "4.x"
tested_with: "Claude Sonnet, Claude Opus"
---

# Elementor Pro V4 — Visual Builder Skill

## How to Use This Skill

This file covers the V4 panel structure and decision rules. Detailed references are in:

- **references/panel.md** — Full tab/widget/field reference, Variables Manager, Class Manager
- **references/classes.md** — Class system, variable naming, how many to create, state variants
- **references/patterns.md** — Reusable layout patterns with panel instructions
- **references/troubleshooting.md** — Common problems and fixes

Read the relevant reference before giving panel instructions.

---

## V4 vs V3: What Changed

V4 is a breaking change from V3 in several areas. Never suggest V3 patterns.

| Area | V3 | V4 |
|---|---|---|
| Primary layout widget | Container | **Flexbox** (atomic) |
| Secondary layout widget | Inner Container | **Div block** (atomic) |
| Panel tabs | Content / Style / Advanced | **General / Style / Interactions** — no Advanced tab |
| Class system | Limited | **Class Manager** — global reusable classes with 4 states |
| Design tokens | Not native | **Variables Manager** — CSS custom properties |
| Interactions | Basic | Native per-element, stackable, scroll-triggered |
| Typography | Text Editor widget | **Paragraph** (atomic) replaces Text Editor |

**Critical**: If you catch yourself writing "Advanced tab" or "Container widget" — stop. Those are V3. In V4: Style tab, Flexbox widget, and Interactions tab.

---

## First Questions to Ask

Before giving panel instructions, clarify two things if not already known:

**1. Are you using a dark/light mode theme switcher?**
If yes → all colors must use CSS variables. Hardcoded panel values won't respond to the theme toggle.
If no → colors can be set directly in the panel. Variables are still recommended for global consistency but not required.

**2. Do you have an existing class and variable system, or are we building one?**
If existing → ask for their variable names and class conventions before creating new ones.
If building from scratch → create a logical system together. See references/classes.md for recommended starting sets and naming conventions.

---

## Decision Hierarchy

Before suggesting ANY implementation, work through this order:

1. Can existing classes handle it? Stack them. (`t-h2 + is-accent`)
2. Can panel Style tab settings handle it? Use them as a LOCAL value.
3. Can a CSS variable handle it? Reference it via the variable picker (ƒ icon).
4. Does it need a new global class? Create in Class Manager, set properties via panel.
5. Does it need a new variable? Create in Variables Manager.
6. Does it absolutely need Custom Code? Stop and rethink — there is almost always a panel-first solution.
7. If Custom Code is truly unavoidable: create a **separate named snippet**. Never add to the Design Tokens snippet.

**Global class vs local**: If a property will be reused on multiple elements → global class. If it's one-off → local.

---

## Common AI Mistakes in Elementor V4

**❌ Referencing the Advanced tab**
V4 has no Advanced tab. Properties live across General, Style, and Interactions tabs only. The Custom CSS field is at the bottom of the Style tab but should always be left empty.

**❌ Suggesting inline CSS or custom CSS per widget**
Classes first, panel settings second. Custom CSS on individual widgets bypasses the class system and creates unmaintainable one-offs.

**❌ Confusing Flexbox with Container**
`Container` is the V3 widget. In V4, use `Flexbox` (in Atomic Elements). Different widgets, different behavior.

**❌ Hardcoding hex colors when using a theme switcher**
If the project uses a dark/light mode toggle, all colors must use CSS variables. Hardcoded hex values won't respond to theme changes. If there is no theme switcher, colors can be set directly in the panel — ask first.

**❌ Using fixed heights for layout**
Use `Flex child > Flex Size: custom (grow: 1)` to fill available space. Fixed heights break responsive behavior.

**❌ Using margins on children for even spacing**
Set gaps on the parent Flexbox. Use margins on specific children only for irregular spacing.

**❌ Suggesting position: absolute for layout problems**
Most layout problems can be solved with Flex child settings. Absolute is a last resort.

**❌ Assuming Laptop is a default breakpoint**
V4 ships with 3 breakpoints: Desktop, Tablet (1024px), Phone (767px). Laptop (1366px) is a custom breakpoint — useful to add, but not present by default.

**❌ Assuming all items start without padding**
Some V4 widgets have a default padding of 10px. Always explicitly set padding to 0 if not needed, rather than assuming it starts at zero.

---

## Instruction Format

Always give instructions in tab order: General → Style → Interactions. Never describe CSS — describe panel field names and values.

```
WIDGET: Flexbox
NAME: "Hero Content"
  (This is what to type in the Structure panel label field)

GENERAL TAB:
  HTML Tag: Section
  ID: hero-content  [only if needed for JS or anchor links]

STYLE TAB:
  Classes: l-stack  ← GLOBAL CLASS

  Layout:
    Display: Flex  ← from class l-stack
    Direction: Column  ← from class l-stack
    Justify: Center  ← LOCAL
    Align: Center  ← LOCAL
    Gap, Row: var(--spacing_md)  ← LOCAL, use variable picker (ƒ)
  Spacing:
    Padding, Top: var(--spacing_xl)  ← LOCAL
    Padding, Bottom: var(--spacing_xl)  ← LOCAL
  Size:
    Height: 90vh  ← LOCAL

INTERACTIONS TAB:
  1: Page load / Fade In / 750ms / delay 0ms
```

**Labels:**
- `← GLOBAL CLASS` — property is set by the class, don't override locally
- `← LOCAL` — set directly in the panel for this element only
- `← NEW CLASS [name]` — create in Class Manager first, then apply
- `use variable picker` — click the ƒ icon in the field, never type hex

**Panel language, not CSS:**

| ❌ CSS | ✅ Panel |
|---|---|
| "Set margin-top to auto" | Spacing > Margin > Top: auto ← LOCAL |
| "Add border-radius: 50%" | Border > Radius: 50px (link all corners) ← LOCAL |
| "Use position: absolute" | Position > Position: Absolute ← LOCAL |
| "Set display: flex" | Layout > Display: Flex ← from class or LOCAL |

---

## Layer Architecture

```
Page
└── Flexbox "Section Wrap"            ← outermost, always Flexbox
    ├── Flexbox "Section Content"     ← primary layout container
    │   ├── Flexbox "Group A"         ← element grouping
    │   │   ├── Heading "..."
    │   │   └── Paragraph "..."
    │   └── Flexbox "Group B"
    │       └── Image "..."
    └── Div block "Transition"        ← decorative, non-structural
```

**Structure panel naming:**
Every layer should be renamed in the Structure panel (right sidebar). Use descriptive names — not the widget default ("Flexbox 3"). The NAME field in instruction format above is what to type in the Structure panel rename field. Good examples: "Hero Wrap", "Nav Row", "Card Group", "Fold Crease". Clear layer names are essential for team collaboration and debugging.

Rules:
- Outermost section = always Flexbox (never Div block)
- Nesting limit: 4 levels maximum
- Space distribution: Flex child > Flex Size (grow), not fixed heights
- Even spacing: gaps on parent Flexbox
- Irregular spacing: margin on specific child only

---

## Responsive System

**Default V4 breakpoints:** Desktop (base), Tablet (1024px), Phone (767px).

Laptop (1366px) is a recommended custom breakpoint — add via Elementor > Site Settings > Layout. Not present by default.

Desktop is always the base. Set all properties at desktop first, then switch the breakpoint selector in the panel header to override at smaller sizes. Overrides cascade down — a Tablet override applies to Phone unless Phone has its own explicit override.

**CSS variables do not change per breakpoint.** For responsive sizing without breakpoint overrides, use `clamp()` in Variables Manager. Example:

```css
/* In Variables Manager — scales fluidly between 16px at 320px viewport and 24px at 1440px */
--spacing_section: clamp(1rem, 3vw, 1.5rem);

/* For font sizes */
--font_h1: clamp(2rem, 5vw, 4rem);
```

Use clamp for: font sizes, section padding, gap values. This reduces the number of breakpoint overrides needed.

Standard Phone overrides (when not using clamp):
- Heading font sizes: −20% from desktop value
- Padding: reduce to smaller spacing variable
- Flex direction: Row → Column for stacking
- Gaps: reduce from large to small spacing variable

---

## Dark Mode

Only implement if the project uses a light/dark theme switcher. If not, skip this section.

The V4 approach uses a `[data-theme="dark"]` attribute on `<html>`, toggled by JavaScript, with CSS variable overrides in the Design Tokens snippet.

1. Define light values on `:root`
2. Define dark overrides under `[data-theme="dark"]`
3. All panel colors set via variables — they swap automatically on toggle
4. Toggle button uses a `data-theme-toggle` custom attribute (General tab → Attributes)

See references/snippets.md for the full implementation.

---

## Interactions

The Interactions tab is Tab 3 on every V4 widget. Multiple animations can be stacked per element.

| Field | Options |
|---|---|
| Trigger | Page load / Scroll into view |
| Effect | Fade / Slide / Scale |
| Type | In / Out |
| Direction | Up / Down / Left / Right |
| Duration | 0 / 100 / 200 / 300 / 400 / 500 / 750 / 1000 / 1250 / 1500 ms |
| Delay | 0 / 100 / 200 / 300 / 400 / 500 / 750 / 1000 / 1250 / 1500 ms |

Above-the-fold elements (visible on page load without scrolling): use **Page load** trigger.
Below-the-fold elements: use **Scroll into view** trigger.

---

## Quality Checklist

Before marking any section done:

- [ ] Structure panel layer names are descriptive (not "Flexbox 3")
- [ ] No custom CSS in any widget's Custom CSS field
- [ ] Decision hierarchy followed (class → panel → variable → code)
- [ ] No more than 4 nesting levels
- [ ] If using theme switcher: all colors use variables, no hardcoded hex
- [ ] Responsive checked at Desktop, Tablet, Phone (+ Laptop if added)
- [ ] Interactions: Page load for above-fold, Scroll into view for below-fold
- [ ] Spacing uses gaps on parents, not margins on children
- [ ] Elements with unexpected spacing: check for default 10px padding
